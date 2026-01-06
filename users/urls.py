from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'utilisateurs', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]