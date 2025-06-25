from rest_framework import serializers
from .models import CoursePackage, CourseVariation, CourseSessionOption, FlexibleCourseOption
from .models import Instructor, Testimonial
from .models import ScheduledSession, EnrolledCourse

class CourseSessionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSessionOption
        fields = ('meetings', 'price')

class CourseVariationSerializer(serializers.ModelSerializer):
    sessions = CourseSessionOptionSerializer(many=True, read_only=True)
    class Meta:
        model = CourseVariation
        fields = ('transmission', 'sessions')

class CoursePackageSerializer(serializers.ModelSerializer):
    variations = CourseVariationSerializer(many=True, read_only=True)
    name = serializers.CharField(source='get_name_display') 
    class Meta:
        model = CoursePackage
        fields = ('id', 'name', 'description', 'variations')

class FlexibleCourseOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlexibleCourseOption
        fields = ('meetings', 'price_manual', 'price_matic', 'description')

class ScheduledSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledSession
        fields = ('session_number', 'date', 'time', 'completed') # Tambahkan instructor jika ada

class EnrolledCourseSerializer(serializers.ModelSerializer):
    schedule = ScheduledSessionSerializer(many=True, read_only=True)
    
    # Jika user adalah ForeignKey, Anda mungkin ingin nested serializer untuk user info
    # user = UserProfileSerializer(read_only=True) # Impor UserProfileSerializer dari users.serializers

    class Meta:
        model = EnrolledCourse
        fields = ('id', 'user', 'course_name', 'package_type_display', 'transmission_display', 
                  'total_meetings', 'price_paid', 'enrollment_date', 'schedule')
        # read_only_fields = ('user', 'enrollment_date')

class EnrollCourseSerializer(serializers.Serializer): # Bukan ModelSerializer
    # Frontend mengirim `packageInfo`, `transmission`, `session` (meetings, price)
    # Anda perlu menentukan field yang dikirim frontend untuk enrollment
    package_name = serializers.CharField()
    transmission_type = serializers.CharField()
    meetings = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    # course_package_id = serializers.IntegerField(required=False, allow_null=True) 
    # session_option_id = serializers.IntegerField(required=False, allow_null=True)
    # flexible_option_id = serializers.IntegerField(required=False, allow_null=True)

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('id', 'name', 'bio', 'photo')

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ('id', 'name', 'content', 'rating', 'created_at')

class EnrollmentTrendSerializer(serializers.ModelSerializer):
    month = serializers.DateField(format="%Y-%m")
    count = serializers.IntegerField()

    class Meta:
        model = EnrolledCourse
        fields = ['month', 'count']

class InstructorClassSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = ScheduledSession
        fields = ['id', 'title', 'participants']

    def get_participants(self, obj):
        return list(obj.enrolledcourse_set.values('user__username', 'user__email'))