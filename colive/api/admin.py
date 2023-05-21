from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CancellationPolicy, Room, Hotel, Place


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {'fields': (
            'phone', 'phone_verification_status', 'email_verification_status')}),
    )


admin.site.register(CancellationPolicy)
admin.site.register(Room)
admin.site.register(Hotel)
admin.site.register(Place)
admin.site.register(CustomUser, CustomUserAdmin)
