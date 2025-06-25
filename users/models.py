from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    PARTICIPANT = 'participant', _('Participant')
    ADMIN = 'admin', _('Admin')
    INSTRUCTOR = 'instructor', _('Instructor')
    DIRECTOR = 'director', _('Director')

class user(AbstractUser):
    # username, password, email, first_name, last_name sudah ada di AbstractUser
    email = models.EmailField(_('email address'), unique=True) # Jadikan email sebagai username field
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PARTICIPANT,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    USERNAME_FIELD = 'email' # Gunakan email untuk login
    REQUIRED_FIELDS = ['username'] # username tetap required karena AbstractUser

    def __str__(self):
        return self.email
    
class CoursePackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class CourseVariation(models.Model):
    package = models.ForeignKey(CoursePackage, on_delete=models.CASCADE)
    transmission = models.CharField(max_length=50)

class CourseSessionOption(models.Model):
    variation = models.ForeignKey(CourseVariation, on_delete=models.CASCADE)
    meetings = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class FlexibleCourseOption(models.Model):
    package = models.ForeignKey(CoursePackage, on_delete=models.CASCADE)
    meetings = models.IntegerField()
    price_manual = models.DecimalField(max_digits=10, decimal_places=2)
    price_matic = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="instructor_profile")
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='instructors/')

    def __str__(self):
        return self.user.get_full_name()

class ScheduledSession(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='scheduled_sessions')
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.instructor.user.get_full_name()}"
