from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/utilisateurs/', include('users.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/medecins/', include('medecins.urls')),
    path('api/gerants/', include('gerants.urls')),
    path('api/centres/', include('centres.urls')),
    path('api/rendez-vous/', include('rendez_vous.urls')),
]
