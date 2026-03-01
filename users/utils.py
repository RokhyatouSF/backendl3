import pyotp
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from django.core.cache import cache
import time


class OTPService:

    @staticmethod
    def _otp_key(value):
        return f"otp_secret_{value}"

    @staticmethod
    def _otp_verified_key(value):
        return f"otp_verified_{value}"

    @staticmethod
    def _otp_attempts_key(value):
        return f"otp_attempts_{value}"

    @staticmethod
    def _otp_block_key(value):
        return f"otp_block_{value}"

    @staticmethod
    def generate_otp(value: str) -> str:
        """
        Génère OTP et stocke secret en cache (5 min).
        """
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=300)
        otp = totp.now()

        cache.set(OTPService._otp_key(value), secret, timeout=300)
        return otp

    @staticmethod
    def verify_otp(value: str, otp_received: str) -> bool:
        secret = cache.get(OTPService._otp_key(value))
        if not secret:
            return False

        totp = pyotp.TOTP(secret, interval=300)
        return totp.verify(otp_received)

    @staticmethod
    def can_send_otp(value: str) -> bool:
        """
        Limite :
        - 3 envois en 15 min
        - Si dépassé => blocage 24h
        """
        # blocage 24h
        if cache.get(OTPService._otp_block_key(value)):
            return False

        attempts = cache.get(OTPService._otp_attempts_key(value)) or []
        now = time.time()

        # enlever les anciennes tentatives > 15 min
        attempts = [t for t in attempts if now - t < 900]

        if len(attempts) >= 3:
            cache.set(OTPService._otp_block_key(value), True, timeout=86400)
            return False

        cache.set(OTPService._otp_attempts_key(value), attempts, timeout=900)
        return True

    @staticmethod
    def record_send(value: str):
        attempts = cache.get(OTPService._otp_attempts_key(value)) or []
        attempts.append(time.time())
        cache.set(OTPService._otp_attempts_key(value), attempts, timeout=900)

    @staticmethod
    def send_otp_email(email: str, otp: str) -> None:
        send_mail(
            subject="Code de vérification SUNU SANTÉ",
            message=f"Votre code est : {otp}. Valide 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

    @staticmethod
    def send_otp_sms(telephone: str, otp: str) -> None:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Votre code SUNU SANTÉ : {otp}. Valide 5 minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=telephone
        )
