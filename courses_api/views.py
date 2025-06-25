from rest_framework import generics, permissions
from .models import CoursePackage, FlexibleCourseOption
from .serializers import CoursePackageSerializer, FlexibleCourseOptionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .models import Instructor, Testimonial
from .serializers import InstructorSerializer, TestimonialSerializer
from .serializers import (
    CoursePackageSerializer, 
    FlexibleCourseOptionSerializer,
    EnrollCourseSerializer  # Tambahkan ini
)
from .serializers import EnrolledCourseSerializer  # Pastikan import ini ada
from .models import ScheduledSession  # Pastikan model ini diimpor
from .serializers import ScheduledSessionSerializer  # Pastikan serializer ini ada
from django.contrib.auth.models import User
from .models import ScheduledSession  # Add this import
from .models import EnrolledCourse  # Import dari models.py di app yang sama
from .models import ScheduledSession, EnrolledCourse
from .serializers import ScheduledSessionSerializer
from .permissions import IsInstructor, IsDirector
from django.db import models
from django.http import JsonResponse
from django.db.models import Count, Sum
from .models import ScheduledSession
from django.shortcuts import render, redirect
from .forms import ParticipantForm
from django.db.models.functions import TruncMonth
from .serializers import EnrollmentTrendSerializer, InstructorClassSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny 


class CourseListView(APIView):
    permission_classes = [permissions.AllowAny] # Siapa saja bisa melihat kursus

    def get(self, request, *args, **kwargs):
        packaged_courses = CoursePackage.objects.prefetch_related('variations__sessions').all()
        flexible_options = FlexibleCourseOption.objects.all()

        packaged_serializer = CoursePackageSerializer(packaged_courses, many=True)
        flexible_serializer = FlexibleCourseOptionSerializer(flexible_options, many=True)

        return Response({
            'packaged_courses': packaged_serializer.data,
            'flexible_options': flexible_serializer.data
        })
    
# Lanjutan di courses_api/views.py

class EnrollCourseView(generics.CreateAPIView):
    serializer_class = EnrollCourseSerializer # Serializer ini hanya untuk validasi input
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # TODO: Logika untuk mencari CoursePackage/FlexibleOption berdasarkan ID jika dikirim
        # Atau validasi data yang dikirim (package_name, transmission, dll)

        enrolled_course = EnrolledCourse.objects.create(
            user=request.user,
            course_name=f"{data['package_name']} - {data['transmission_type']}",
            package_type_display=data['package_name'],
            transmission_display=data['transmission_type'],
            total_meetings=data['meetings'],
            price_paid=data['price']
        )

        for i in range(1, data['meetings'] + 1):
            ScheduledSession.objects.create(
                enrolled_course=enrolled_course,
                session_number=i
            )
        
        # Serialize EnrolledCourse yang baru dibuat untuk respons
        output_serializer = EnrolledCourseSerializer(enrolled_course)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

class MyEnrolledCoursesListView(generics.ListAPIView):
    serializer_class = EnrolledCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ambil data schedule juga
        return EnrolledCourse.objects.filter(user=self.request.user).prefetch_related('schedule')

class UpdateScheduledSessionView(generics.UpdateAPIView):
    queryset = ScheduledSession.objects.all() # Akan difilter berdasarkan user di get_object
    serializer_class = ScheduledSessionSerializer # Hanya untuk date, time, completed
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk' # atau 'id' jika field Anda bernama id

    def get_queryset(self):
        # Pastikan user hanya bisa update sesi miliknya
        return ScheduledSession.objects.filter(enrolled_course__user=self.request.user)
    
    def get_object(self):
        # Filter berdasarkan user yang login
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You can only update your own sessions")
        return obj

    def update(self, request, *args, **kwargs):
        # Hanya izinkan update date dan time
        # Frontend mungkin mengirim lebih, tapi serializer hanya akan proses field yang ada
        instance = self.get_object()
        # Pastikan sesi belum completed
        if instance.completed:
            return Response({'detail': 'Cannot update a completed session.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_staff
        )

class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAdminOrReadOnly]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.order_by('-created_at')
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]

class UpdateScheduledSessionView(generics.UpdateAPIView):
    queryset = ScheduledSession.objects.all()
    # rest of your view code

class InstructorScheduleView(generics.ListAPIView):
    serializer_class = ScheduledSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def get_queryset(self):
        instructor = self.request.user.instructor_profile
        return ScheduledSession.objects.filter(instructor=instructor)

class MarkSessionCompletedView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def post(self, request, pk):
        try:
            session = ScheduledSession.objects.get(pk=pk, instructor=request.user.instructor_profile)
            session.status = "completed"
            session.save()
            return Response({"detail": "Marked as completed."})
        except ScheduledSession.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
    
class DirectorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def get(self, request):
        total_students = EnrolledCourse.objects.count()
        total_revenue = EnrolledCourse.objects.aggregate(total=models.Sum("price_paid"))["total"] or 0
        return Response({
            "total_students": total_students,
            "total_revenue": total_revenue
        })
    
class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'instructor'

class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'director'

def director_dashboard(request):
    data = {
        "message": "Ini adalah halaman dashboard untuk direktur"
    }
    return JsonResponse(data)

class InstructorScheduleList(generics.ListAPIView):
    serializer_class = ScheduledSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def get_queryset(self):
        return ScheduledSession.objects.filter(instructor__user=self.request.user)

class MarkSessionCompleted(generics.UpdateAPIView):
    queryset = ScheduledSession.objects.all()
    serializer_class = ScheduledSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def perform_update(self, serializer):
        serializer.save(is_completed=True)

class DirectorDashboardStats(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def get(self, request):
        total_sessions = ScheduledSession.objects.count()
        completed_sessions = ScheduledSession.objects.filter(is_completed=True).count()
        # Contoh agregasi lain (misalnya pendapatan)
        
        return Response({
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
        })
    
def enroll_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()  # Menyimpan data peserta ke database
            return redirect('success_url')  # Arahkan ke halaman sukses
    else:
        form = ParticipantForm()
    return render(request, 'enroll.html', {'form': form})

def some_view(request):
    # Impor model setelah fungsi dipanggil
    from .models import Instructor
    instructor = Instructor.objects.all()
    return render(request, 'template.html', {'instructors': instructor})

class DirectorDashboardAPI(APIView):
    def get(self, request):
        # Data untuk direktur
        enrollment_data = (EnrolledCourse.objects
                         .annotate(month=TruncMonth('created_at'))
                         .values('month')
                         .annotate(count=Count('id'))
                         .order_by('month'))
        
        revenue_data = (EnrolledCourse.objects
                      .values('course__title')
                      .annotate(total=Sum('payment_amount')))
        
        return Response({
            'enrollment_trend': EnrollmentTrendSerializer(enrollment_data, many=True).data,
            'revenue_by_course': revenue_data
        })

class InstructorDashboardAPI(APIView):
    def get(self, request):
        if not request.user.is_authenticated or not hasattr(request.user, 'instructor'):
            return Response({"error": "Akses ditolak"}, status=403)
            
        classes = ScheduledSession.objects.filter(instructor=request.user.instructor)
        serializer = InstructorClassSerializer(classes, many=True)
        return Response(serializer.data)

class RegisterAPI(APIView):
    def post(self, request):
        # Contoh sederhana penerimaan data POST
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Di sini biasanya Anda akan:
        # - Validasi data
        # - Simpan ke database
        # - Kirim response
        
        # Contoh response sederhana
        return Response({
            'message': 'Registrasi berhasil',
            'data': {
                'username': username,
                'email': email
            }
        }, status=status.HTTP_201_CREATED)
    
class RegisterAPI(APIView):
    permission_classes = [AllowAny]  # <-- Ini yang penting!

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Validasi data
        if not all([username, email, password]):
            return Response(
                {'error': 'Username, email, dan password wajib diisi'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cek apakah user sudah ada
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username sudah digunakan'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buat user baru
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({
            'message': 'Registrasi berhasil',
            'data': {
                'user_id': user.id,
                'username': user.username
            }
        }, status=status.HTTP_201_CREATED)