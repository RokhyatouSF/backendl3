from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CustomTokenView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    SendEmailOTPView,
    VerifyEmailOTPView,
    FinalizeRegistrationView,
    VerifyIdentityDocumentView,
    RoleViewSet,
    UserViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # JWT
    path("token/", CustomTokenView.as_view(), name="token"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # OTP email
    path('send-otp/', SendEmailOTPView.as_view()),
    path('verify-otp/', VerifyEmailOTPView.as_view()),

    # Finalisation inscription
    path('finalize-registration/', FinalizeRegistrationView.as_view()),

    # OCR identité
    path('verify-id/', VerifyIdentityDocumentView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
