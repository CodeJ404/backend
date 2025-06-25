from django.contrib.admin import AdminSite
from courses_api.models import ScheduledSession
from django.contrib import admin

class DirectorAdminSite(AdminSite):
    site_header = "Dashboard Direktur"
    site_title = "Panel Direktur"
    index_title = "Selamat Datang Direktur"

    def has_permission(self, request):
        return request.user.is_active and request.user.role == 'director'

director_site = DirectorAdminSite(name='director_admin')  # ✅ BENAR


