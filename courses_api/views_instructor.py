# courses_api/views_instructor.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ScheduledSession
from django.contrib.auth.views import LoginView

@login_required
def instructor_dashboard(request):
    # Cek role user
    if not request.user.role == 'instructor':
        messages.error(request, 'Akses hanya untuk instruktur')
        return redirect('admin:login')
    
    # Ambil jadwal mengajar
    sessions = ScheduledSession.objects.filter(
        instructor=request.user
    ).order_by('start_time')
    
    context = {
        'sessions': sessions,
        'total_sessions': sessions.count(),
        'completed_sessions': sessions.filter(is_completed=True).count()
    }
    return render(request, 'admin/instructor_dashboard.html', context)

class InstructorLoginView(LoginView):
    template_name = 'registration/instructor_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/instructor/dashboard/'