from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {'fields': (
            'phone', 'phone_verification_status', 'email_verification_status')}),
    )
