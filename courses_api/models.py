from django.db import models
from django.conf import settings  # Referensi ke custom user model
from django.contrib.auth.models import AbstractUser
from django.apps import apps
from django.utils import timezone 

# Model Course
class CoursePackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CourseVariation(models.Model):
    package = models.ForeignKey(CoursePackage, on_delete=models.CASCADE)
    transmission = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.package.name} - {self.transmission}"

class CourseSessionOption(models.Model):
    variation = models.ForeignKey(CourseVariation, on_delete=models.CASCADE)
    meetings = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variation} - {self.meetings} meetings"

class FlexibleCourseOption(models.Model):
    package = models.ForeignKey(CoursePackage, on_delete=models.CASCADE)
    meetings = models.IntegerField()
    price_manual = models.DecimalField(max_digits=10, decimal_places=2)
    price_matic = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.package.name} - Flexible Option"

# Model EnrolledCourse
class EnrolledCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrolled_courses')
    course_name = models.CharField(max_length=255)
    package_type_display = models.CharField(max_length=50)
    transmission_display = models.CharField(max_length=10)
    total_meetings = models.PositiveIntegerField()
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course_name}"

# Model ScheduledSession
class ScheduledSession(models.Model):
    title = models.CharField(max_length=100, default="Untitled")
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE, default=1)
    start_time = models.DateTimeField(default=timezone.now)  # Menggunakan waktu saat ini sebagai default
    # Field lainnya
    is_completed = models.BooleanField(default=False)  # Pastikan ini ada
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title

# Model Instructor
class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Make user nullable temporarily
    bio = models.TextField()
    photo = models.ImageField(upload_to='instructors/')
    
    def __str__(self):
        return self.user.get_full_name() if self.user else "No User Assigned"

# Model Testimonial
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.name}"

# Model Participant (Hapus Duplikasi)
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.ForeignKey(CoursePackage, on_delete=models.CASCADE)  # Menambahkan relasi ke Course

    def __str__(self):
        return self.name

# Model User (Custom User)
class User(AbstractUser):
    role = models.CharField(max_length=20, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='courses_api_users',  # Tambahkan related_name untuk menghindari konflik
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='courses_api_users_permissions',  # Tambahkan related_name untuk menghindari konflik
        blank=True,
    )

    def __str__(self):
        return self.username
    
class Course(models.Model):
    title = models.CharField(max_length=200)
