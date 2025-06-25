from django.urls import path
from .views import CourseListView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseListView, InstructorViewSet, TestimonialViewSet
from .views import EnrollCourseView, MyEnrolledCoursesListView, UpdateScheduledSessionView
from .views import InstructorScheduleView, MarkSessionCompletedView, DirectorDashboardView
from .views import InstructorScheduleList, MarkSessionCompleted
from .views import DirectorDashboardStats
from .views_director import director_dashboard
from .views import DirectorDashboardAPI, InstructorDashboardAPI
from . import views

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('director/stats/', DirectorDashboardStats.as_view(), name='director-stats'),
    path('instructor/schedule/', InstructorScheduleView.as_view()),
    path('instructor/session/<int:pk>/complete/', MarkSessionCompletedView.as_view()),
    path('director/dashboard/', DirectorDashboardView.as_view(), name='director-dashboard'),
    path('director/dashboard/', director_dashboard, name='director-dashboard'),
    path('api/director/', DirectorDashboardAPI.as_view()),
    path('api/instructor/', InstructorDashboardAPI.as_view()),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
]

# Lanjutan di courses_api/urls.py
urlpatterns += [
    path('enroll/', EnrollCourseView.as_view(), name='enroll-course'),
    path('my-courses/', MyEnrolledCoursesListView.as_view(), name='my-enrolled-courses'),
    path('my-schedule/<int:pk>/', UpdateScheduledSessionView.as_view(), name='update-scheduled-session'),
    # <int:pk> adalah ID dari ScheduledSession
    path('instructor/schedule/', InstructorScheduleView.as_view()),
    path('instructor/session/<int:pk>/complete/', MarkSessionCompletedView.as_view()),
    path('director/dashboard/', DirectorDashboardView.as_view(), name='director-dashboard'),
    
]

router = DefaultRouter()
router.register(r'instructors', InstructorViewSet, basename='instructor')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('', include(router.urls)),
    path('instructor/schedule/', InstructorScheduleList.as_view(), name='instructor-schedule'),
    path('instructor/schedule/<int:pk>/complete/', MarkSessionCompleted.as_view(), name='mark-session-completed'),
]