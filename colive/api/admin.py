from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Room, Place, City, Tag, Amenity, Interest


class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    filter_horizontal = ('interests',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Verification Status', {
         'fields': ('phone_verification_status', 'email_verification_status')}),
        ('Additional Fields', {
         'fields': ('age', 'bio', 'gender', 'city', 'interests')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


class PlaceAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)


class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('amenities',)


admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(City)
admin.site.register(Tag)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Interest)
