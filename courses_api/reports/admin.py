from django.contrib import admin
from django.db.models import Count, Avg, F
from django.template.response import TemplateResponse
from django.urls import path

class DirectorAdmin(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('director/', self.admin_view(self.director_dashboard))
        ]
        return custom_urls + urls

    def director_dashboard(self, request):
        # Hitung statistik
        from apps.training.models import TrainingSession
        total_sessions = TrainingSession.objects.count()
        revenue = TrainingSession.objects.aggregate(
            total=Sum('fee')
        )['total'] or 0
        
        # Data instruktur
        instructors = Instructor.objects.annotate(
            session_count=Count('training_sessions'),
            completion_rate=Avg(
                Case(
                    When(training_sessions__status='completed', then=1),
                    default=0,
                    output_field=FloatField()
                )
            ) * 100,
            rating=Avg('training_sessions__rating')
        )

        context = {
            **self.each_context(request),
            'total_sessions': total_sessions,
            'revenue': revenue,
            'completion_rate': round(
                TrainingSession.objects.filter(status='completed').count() / 
                total_sessions * 100, 2
            ) if total_sessions > 0 else 0,
            'instructors': instructors
        }
        return TemplateResponse(request, "admin/director/index.html", context)

director_site = DirectorAdmin(name='directoradmin')