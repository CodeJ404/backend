from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user

class CustomUserAdmin(UserAdmin):
    model = user
    # Sesuaikan fieldsets jika perlu, tambahkan field kustom Anda
    # UserAdmin.fieldsets += (('Custom Fields', {'fields': ('role', 'phone_number', 'address', 'profile_picture')}),)
    # UserAdmin.add_fieldsets += (('Custom Fields', {'fields': ('role', 'phone_number', 'address', 'profile_picture')}),)
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'role']


admin.site.register(user, CustomUserAdmin)