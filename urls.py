from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Untuk media files
from django.conf.urls.static import static # Untuk media files
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.admin.views.decorators import staff_member_required
from courses_api import director_site
from courses_api.admin_director import director_site
import courses_api.admin_director as admin_director

urlpatterns = [
     path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/', include('courses_api.urls')),
    path('admin/instructor/', staff_member_required(admin.site.urls), {'extra_context': {'is_instructor': True}}),
    path('admin/director/', staff_member_required(admin.site.urls), {'extra_context': {'is_director': True}}),
    path('admin/', admin.site.urls),
    path('director-admin/', director_site.urls),  # ← Tambahkan ini
    path('api/', include('courses_api.urls')),
    path('director-admin/', admin_director.director_site.urls),
]

# Untuk menyajikan media files (gambar profil) saat development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)