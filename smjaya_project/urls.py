"""
URL configuration for smjaya_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Untuk menyajikan media files
from django.conf.urls.static import static # Untuk menyajikan media files
from django.http import JsonResponse
from courses_api.admin_director import director_site
from courses_api.views_director import director_dashboard  # Pastikan import view-nya
from courses_api.views_instructor import instructor_dashboard
from courses_api.views_instructor import InstructorLoginView
from django.views.generic import RedirectView
from courses_api import views


def home_view(request):
    return JsonResponse({"message": "API backend is running!"})
urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Tambahkan ini
    path('admin/', admin.site.urls),
    path('api/', include('courses_api.urls')),
    path('', home_view),  # <- ini akan tangani root URL
    path('api/', include('courses_api.urls')),
    path('director-admin/', director_site.urls),  # ← INI yang bikin URL-nya aktif
    path('api/', include('courses_api.urls')),    # URL app kamu
    path('director/dashboard/', director_dashboard, name='director-dashboard'),
    path('api/', include('courses_api.urls')),
    path('instructor/dashboard/', instructor_dashboard, name='instructor-dashboard'),
    path('instructor/login/', InstructorLoginView.as_view(), name='instructor-login'),
    path('instructor/dashboard/', instructor_dashboard, name='instructor-dashboard'),
    path('accounts/profile/', RedirectView.as_view(url='/instructor/dashboard/')),
    path('api/register/', views.RegisterAPI.as_view(), name='register')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
