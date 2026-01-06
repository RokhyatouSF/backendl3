from django.contrib import admin
from .models import ModeConsultation, StatutRdv, RendezVous

@admin.register(ModeConsultation)
class ModeConsultationAdmin(admin.ModelAdmin):
    list_display = ('nom_mode',)
    search_fields = ('nom_mode',)

@admin.register(StatutRdv)
class StatutRdvAdmin(admin.ModelAdmin):
    list_display = ('nom_statut',)
    search_fields = ('nom_statut',)

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('date_heure', 'patient', 'medecin', 'centre', 'mode_consultation', 'statut_rdv')
    list_filter = ('date_heure', 'mode_consultation', 'statut_rdv', 'centre')
    search_fields = (
        'patient__user__first_name',
        'patient__user__last_name',
        'medecin__user__first_name',
        'centre__nom',
    )
    raw_id_fields = ('patient', 'medecin', 'centre')
    date_hierarchy = 'date_heure'