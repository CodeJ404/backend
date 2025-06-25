# admin/director.py

from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import SomeModel  # ganti sesuai model kamu
from .models import ScheduledSession

class DirectorAdminSite(AdminSite):
    site_header = "Dashboard Direktur"
    site_title = "Direktur"
    index_title = "Selamat datang, Direktur"

director_site = DirectorAdminSite(name='director_admin')

@admin.register(SomeModel, site=director_site)
class SomeModelAdmin(admin.ModelAdmin):
    list_display = ['nama', 'tanggal']

class ScheduledSessionAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_instructor', 'get_start_time', 'get_is_completed')
    
    # Method untuk menampilkan field relationship
    def get_title(self, obj):
        return obj.title
    get_title.short_description = 'Judul Sesi'
    
    def get_instructor(self, obj):
        return obj.instructor.get_full_name()
    get_instructor.short_description = 'Instruktur'
    
    def get_start_time(self, obj):
        return obj.start_time.strftime("%d %b %Y %H:%M")
    get_start_time.short_description = 'Waktu Mulai'
    
    def get_is_completed(self, obj):
        return "✅" if obj.is_completed else "❌"
    get_is_completed.short_description = 'Selesai'
    
    # Jika ingin filter
    list_filter = ('is_completed', 'instructor')
    search_fields = ('title', 'instructor__username')
