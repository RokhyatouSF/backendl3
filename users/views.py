from rest_framework import viewsets, parsers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
import os
import cv2
import pytesseract
from fuzzywuzzy import fuzz
import random
import string
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from .services.ocr_service import extract_text
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer, RegisterSerializer
from .serializers import CustomTokenObtainPairSerializer  # <-- IMPORTANT

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


User = get_user_model()


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


from rest_framework import status

class CustomTokenView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class SendEmailOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email requis"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email déjà utilisé"}, status=400)

        otp = ''.join(random.choices(string.digits, k=6))
        cache.set(f'otp_email_{email}', otp, 600)
        print(f"[DEBUG] OTP pour {email} : {otp}")  # 👈 affichage dans le terminal

        try:
            send_mail(
                subject='DIAM YARAAM CODE- Email',
                message=f'Code : {otp}\nValide 10 min.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return Response({"message": "Code email envoyé"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class VerifyEmailOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"error": "Email et code requis"}, status=400)

        stored = cache.get(f'otp_email_{email}')
        if stored and stored == code:
            cache.set(f'email_verified_{email}', True, 3600)
            cache.delete(f'otp_email_{email}')
            return Response({"message": "Email vérifié"})
        return Response({"error": "Code email incorrect ou expiré"}, status=400)


class FinalizeRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"email": "Email requis"}, status=400)

        if not cache.get(f'email_verified_{email}'):
            return Response({"error": "Email non vérifié"}, status=400)

        if 'photo_profil' not in request.FILES:
            return Response(
                {"photo_profil": "Photo de profil obligatoire"},
                status=400
            )

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.email_verified = True
            user.save()

            cache.delete(f'email_verified_{email}')
            return Response({"message": "Compte créé"}, status=201)

        print("❌ ERREURS SERIALIZER :", serializer.errors)
        return Response(serializer.errors, status=400)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers, permissions
from django.core.files.storage import default_storage
import os

from .services.ocr_service import extract_text
from .services.identity_service import check_identity


class VerifyIdentityDocumentView(APIView):
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        file = request.FILES.get("document_piece_identite")
        numero = request.data.get("piece_identite_numero")

        if not file:
            return Response({"error": "Document requis"}, status=400)

        if not numero:
            return Response({"error": "Numéro pièce requis"}, status=400)

        path = default_storage.save(f"tmp/{file.name}", file)
        full_path = default_storage.path(path)

        try:
            text = extract_text(full_path)

            temp_user = type("TempUser", (object,), {})()
            temp_user.first_name = request.data.get("first_name", "")
            temp_user.last_name = request.data.get("last_name", "")
            temp_user.date_naissance = request.data.get("date_naissance", "")  # <- AJOUTÉ


            verified, status_verif, score = check_identity(
                temp_user,
                text,
                numero
            )

            return Response({
                "status": status_verif,
                "score": score,
                "verified": verified
            })

        finally:
            if os.path.exists(full_path):
                os.remove(full_path)
