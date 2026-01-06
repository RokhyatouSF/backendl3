from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nom_role',)
    search_fields = ('nom_role',)
    ordering = ('nom_role',)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'telephone', 'role', 'genre', 'email_verified', 'phone_verified', 'is_staff')
    list_filter = ('role', 'email_verified', 'phone_verified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telephone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations SUNU SANTÉ', {
            'fields': (
                'telephone',
                'role',
                'date_naissance',
                'piece_identite_numero',
                'piece_identite_document_url',
                'photo_profil',
                'email_verified',
                'phone_verified',
                'created_at',
                'updated_at',
            )
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': (
                'telephone',
                'email',
                'first_name',
                'last_name',
                'role',
                'date_naissance',
            )
        }),
    )