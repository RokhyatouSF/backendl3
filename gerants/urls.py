from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GerantViewSet

router = DefaultRouter()
router.register(r'gerants', GerantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]