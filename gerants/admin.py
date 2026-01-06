from django.contrib import admin
from .models import Gerant

@admin.register(Gerant)
class GerantAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'get_telephone')
    search_fields = ('user__first_name', 'user__last_name', 'user__telephone')
    raw_id_fields = ('user',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nom complet'

    def get_telephone(self, obj):
        return obj.user.telephone
    get_telephone.short_description = 'Téléphone'