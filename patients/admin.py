from django.contrib import admin
from .models import Patient, Maladie, StatutMaladie, TypeAnalyse, ResultatAnalyse, NotePatient, RappelPatient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'nfc_id', 'numero_carte')
    search_fields = ('user__first_name', 'user__last_name', 'user__telephone', 'nfc_id', 'numero_carte')
    raw_id_fields = ('user',)

@admin.register(Maladie)
class MaladieAdmin(admin.ModelAdmin):
    list_display = ('nom_maladie', 'patient', 'date_diagnostic', 'created_at')
    list_filter = ('date_diagnostic', 'created_at')
    search_fields = ('nom_maladie', 'patient__user__first_name', 'patient__user__last_name')
    raw_id_fields = ('patient', 'resultat_analyse')

@admin.register(StatutMaladie)
class StatutMaladieAdmin(admin.ModelAdmin):
    list_display = ('nom_statut',)
    search_fields = ('nom_statut',)

@admin.register(TypeAnalyse)
class TypeAnalyseAdmin(admin.ModelAdmin):
    list_display = ('nom_type',)
    search_fields = ('nom_type',)

@admin.register(ResultatAnalyse)
class ResultatAnalyseAdmin(admin.ModelAdmin):
    list_display = ('nom_analyse', 'patient', 'type_analyse', 'date_analyse')
    list_filter = ('type_analyse', 'date_analyse')
    search_fields = ('nom_analyse', 'patient__user__first_name', 'patient__user__last_name')
    raw_id_fields = ('patient',)

@admin.register(NotePatient)
class NotePatientAdmin(admin.ModelAdmin):
    list_display = ('titre', 'patient', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('titre', 'contenu', 'patient__user__first_name')
    raw_id_fields = ('patient',)

@admin.register(RappelPatient)
class RappelPatientAdmin(admin.ModelAdmin):
    list_display = ('titre', 'patient', 'date_heure')
    list_filter = ('date_heure',)
    search_fields = ('titre', 'description', 'patient__user__first_name')
    raw_id_fields = ('patient',)