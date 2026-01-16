from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet,
    UserViewSet,
    RegisterView,
    FirebaseLoginView,
    SendEmailOTPView,
    VerifyEmailOTPView,
    VerifyIdentityDocumentView,
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),

    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('firebase-login/', FirebaseLoginView.as_view()),
    path('send-email-otp/', SendEmailOTPView.as_view()),
    path('verify-email-otp/', VerifyEmailOTPView.as_view()),
    path('verify-id/', VerifyIdentityDocumentView.as_view()),
]
