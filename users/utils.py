import pyotp
import datetime
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

class OTPService:
    @staticmethod
    def generate_otp():
        totp = pyotp.TOTP(pyotp.random_base32())
        return totp.now()

    @staticmethod
    def send_otp_email(email, otp):
        send_mail(
            'Code de vérification SUNU SANTÉ',
            f'Votre code est : {otp}. Valide 5 minutes.',
            settings.EMAIL_HOST_USER,
            [email],
        )

    @staticmethod
    def send_otp_sms(telephone, otp):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Votre code SUNU SANTÉ : {otp}. Valide 5 minutes.',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=telephone
        )

    @staticmethod
    def verify_otp(otp_sent, otp_received):
        return otp_sent == otp_received  # Simple pour tests ; ajoute expiration en prod