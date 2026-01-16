from rest_framework import viewsets, status, parsers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import default_storage
import random
import string
import os
import cv2
import pytesseract
from fuzzywuzzy import fuzz
from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model


from .models import User, Role
from .serializers import UserSerializer, RoleSerializer, RegisterSerializer

User = get_user_model()  # Bonne pratique pour récupérer le modèle User custom

# ──────────────────────────────────────────────────────────────────────────────
# 1. ViewSets classiques (CRUD rôles et utilisateurs)
# ──────────────────────────────────────────────────────────────────────────────

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]  # Seulement admin peut CRUD les rôles


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # À affiner plus tard par rôle


# ──────────────────────────────────────────────────────────────────────────────
# 2. Inscription classique + envoi OTP email automatique
# ──────────────────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    """
    Inscription d'un nouvel utilisateur
    Accepte : first_name, last_name, email, telephone, date_naissance, genre, password, password2, role (ID)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Optionnel : envoyer un OTP email immédiatement après création
            # from .utils import send_email_otp  # si tu as cette fonction
            # send_email_otp(user.email)

            return Response(
                {
                    "message": "Inscription réussie ! Vérifiez votre email pour activer le compte.",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        # Retourne les erreurs précises (ex: email déjà pris, role invalide, etc.)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ──────────────────────────────────────────────────────────────────────────────
# 3. OTP Email indépendant
# ──────────────────────────────────────────────────────────────────────────────

class SendEmailOTPView(APIView):
    permission_classes = [permissions.AllowAny]  # Ou IsAuthenticated si tu veux restreindre

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        # Code 6 chiffres unique
        otp = ''.join(random.choices(string.digits, k=6))
        cache.set(f'email_otp_{email}', otp, timeout=600)  # 10 minutes

        try:
            send_mail(
                subject='Code de vérification SUNU SANTÉ',
                message=f'Votre code : {otp}\nValide 10 minutes.\nNe le partagez jamais.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({
                "message": "Code OTP envoyé par email",
                "expires_in": "600 secondes"
            })
        except Exception as e:
            return Response({"error": f"Erreur envoi : {str(e)}"}, status=500)


class VerifyEmailOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"error": "Code requis"}, status=400)

        email = request.user.email
        cache_key = f'email_otp_{email}'
        stored_otp = cache.get(cache_key)

        if stored_otp and stored_otp == code:
            request.user.email_verified = True
            request.user.save()
            cache.delete(cache_key)
            return Response({"message": "Email vérifié avec succès"})
        return Response({"error": "Code incorrect ou expiré"}, status=400)


# ──────────────────────────────────────────────────────────────────────────────
# 4. Login via Firebase Phone Auth (token reçu depuis Flutter)
# ──────────────────────────────────────────────────────────────────────────────

class FirebaseLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        id_token = request.data.get('idToken')
        if not id_token:
            return Response({"error": "Token Firebase requis"}, status=400)

        try:
            decoded = firebase_auth.verify_id_token(id_token)
            phone_number = decoded.get('phone_number')

            if not phone_number:
                return Response({"error": "Numéro téléphone non trouvé dans le token"}, status=400)

            try:
                user = User.objects.get(telephone=phone_number)
                user.phone_verified = True
                user.save()
            except User.DoesNotExist:
                # Création automatique (à sécuriser en production)
                username = f"user_{phone_number[-8:]}"
                user = User.objects.create_user(
                    username=username,
                    telephone=phone_number,
                    # Champs obligatoires à compléter plus tard
                )
                user.phone_verified = True
                user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })

        except firebase_auth.InvalidIdTokenError:
            return Response({"error": "Token Firebase invalide"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# ──────────────────────────────────────────────────────────────────────────────
# 5. Vérification IA de la pièce d'identité (OCR + matching)
# ──────────────────────────────────────────────────────────────────────────────

class VerifyIdentityDocumentView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if 'document_piece_identite' not in request.FILES:
            return Response({"error": "Image de la pièce d'identité requise"}, status=400)

        image_file = request.FILES['document_piece_identite']

        # Sauvegarde temporaire
        temp_path = default_storage.save(f'tmp/{image_file.name}', content=image_file)
        full_temp_path = default_storage.path(temp_path)

        try:
            # Prétraitement OpenCV
            img = cv2.imread(full_temp_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # OCR Tesseract (français + anglais)
            custom_config = r'--oem 3 --psm 6 -l fra+eng'
            extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

            # Extraction simplifiée
            extracted_data = self.extract_key_fields(extracted_text.lower())

            # Données utilisateur
            user_data = {
                'prenom': user.first_name.lower().strip(),
                'nom': user.last_name.lower().strip(),
                'date_naissance': str(user.date_naissance) if user.date_naissance else ''
            }

            # Scores de similarité
            score_prenom = fuzz.ratio(user_data['prenom'], extracted_data.get('prenom', ''))
            score_nom = fuzz.ratio(user_data['nom'], extracted_data.get('nom', ''))
            score_date = fuzz.ratio(user_data['date_naissance'], extracted_data.get('date_naissance', ''))

            # Score pondéré
            global_score = (score_prenom * 0.4 + score_nom * 0.4 + score_date * 0.2)

            # Décision
            if global_score >= 85:
                status_val = 'approved'
                user.id_verified = True
            elif global_score >= 60:
                status_val = 'manual'
            else:
                status_val = 'rejected'

            user.id_verification_status = status_val
            user.document_piece_identite = temp_path  # Sauvegarde définitive
            user.save()

            # Nettoyage
            if os.path.exists(full_temp_path):
                os.remove(full_temp_path)

            return Response({
                "status": status_val,
                "score": round(global_score, 2),
                "extracted": extracted_data,
                "message": f"Vérification terminée (score : {round(global_score, 1)}%)"
            })

        except Exception as e:
            if os.path.exists(full_temp_path):
                os.remove(full_temp_path)
            return Response({"error": str(e)}, status=500)

    def extract_key_fields(self, text):
        lines = text.split('\n')
        data = {'nom': '', 'prenom': '', 'date_naissance': ''}

        for line in lines:
            line = line.strip()
            if 'nom' in line and len(line) > 10:
                data['nom'] = line.split('nom')[-1].strip()[:30]
            elif 'prénom' in line or 'prenom' in line:
                split_key = 'prénom' if 'prénom' in line else 'prenom'
                data['prenom'] = line.split(split_key)[-1].strip()[:30]
            elif any(kw in line for kw in ['naissance', 'birth', 'date']):
                import re
                date_match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', line)
                if date_match:
                    data['date_naissance'] = date_match.group(0)

        return data