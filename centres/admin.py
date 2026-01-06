from django.contrib import admin
from .models import TypeCentre, Specialite, CentreSante, MedecinCentre

@admin.register(TypeCentre)
class TypeCentreAdmin(admin.ModelAdmin):
    list_display = ('nom_type',)
    search_fields = ('nom_type',)

@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ('nom_specialite',)
    search_fields = ('nom_specialite',)

@admin.register(CentreSante)
class CentreSanteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'gerant', 'type_centre', 'telephone_contact', 'verified')
    list_filter = ('type_centre', 'verified', 'created_at')
    search_fields = ('nom', 'adresse', 'gerant__first_name', 'gerant__last_name', 'telephone_contact')
    raw_id_fields = ('gerant',)

@admin.register(MedecinCentre)
class MedecinCentreAdmin(admin.ModelAdmin):
    list_display = ('medecin', 'centre', 'specialite')
    list_filter = ('specialite', 'centre')
    search_fields = ('medecin__user__first_name', 'centre__nom', 'specialite__nom_specialite')
    raw_id_fields = ('medecin', 'centre')