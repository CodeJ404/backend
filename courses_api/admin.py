# admin.py
from django.contrib import admin
from .models import Instructor, EnrolledCourse, ScheduledSession, Testimonial, CoursePackage, Participant
from django.contrib.auth.admin import UserAdmin
from .models import User


# Mengkustomisasi admin untuk User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'phone')}),  # Menambahkan field role dan phone
    )

admin.site.register(User, CustomUserAdmin)

# Registrasi model Instructor dengan admin yang dikustomisasi
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio_short')

    def bio_short(self, obj):
        return f"{obj.bio[:50]}..." if len(obj.bio) > 50 else obj.bio

    bio_short.short_description = 'Bio'

admin.site.register(Instructor, InstructorAdmin)

# Fungsi untuk mendaftarkan model lainnya
def register_models():
    admin.site.register(EnrolledCourse)
    admin.site.register(Testimonial)
    admin.site.register(CoursePackage)
    admin.site.register(Participant)

# Memanggil fungsi untuk registrasi model lainnya
register_models()

# Registrasi model ScheduledSession hanya sekali
class ScheduledSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor_name', 'formatted_start_time', 'completed_status')

    def formatted_start_time(self, obj):
        return obj.start_time.strftime("%d %b %Y %H:%M")
    formatted_start_time.short_description = 'Waktu Mulai'

    def completed_status(self, obj):
        return "✅" if obj.is_completed else "❌"
    completed_status.short_description = 'Status'
    completed_status.admin_order_field = 'is_completed'  # Untuk sorting

    # Filter dan pencarian
    list_filter = ('is_completed', 'instructor')
    search_fields = ('title', 'instructor__username')

    # Method untuk custom display
    def instructor_name(self, obj):
        return obj.instructor.get_full_name()
    instructor_name.short_description = 'Instruktur'

# Pastikan model hanya didaftarkan sekali
admin.site.register(ScheduledSession, ScheduledSessionAdmin)
