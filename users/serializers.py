# users/serializers.py

from rest_framework import serializers
from .models import User, UserRole # Import model User dan UserRole Anda
from .models import CoursePackage, CourseVariation, CourseSessionOption, FlexibleCourseOption
from .models import EnrolledCourse

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Field password hanya untuk input (write_only), tidak akan ditampilkan saat mengambil data user.
    # 'style' digunakan untuk memberitahu DRF bagaimana merender field ini di browsable API-nya.
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    # Frontend mengirim 'name'. Model User Django memiliki 'first_name' dan 'last_name'.
    # Kita bisa tambahkan 'name' di sini dan memecahnya di metode 'create',
    # atau mengharapkan frontend mengirim 'first_name' dan 'last_name' secara terpisah.
    # AuthContext.tsx di frontend Anda mengirim 'name' saat signup.
    name = serializers.CharField(write_only=True, required=True) # Tambahkan ini

    class Meta:
        model = User
        # Field yang akan disertakan dalam serializer
        fields = ('id', 'username', 'email', 'password', 'name', 
                  'first_name', 'last_name', # Ini akan diisi dari 'name'
                  'phone_number', 'address', 'role')
        extra_kwargs = {
            # 'first_name' dan 'last_name' tidak wajib diisi langsung oleh user, akan di-generate
            'first_name': {'required': False},
            'last_name': {'required': False},
            # 'role' hanya bisa dibaca (read_only), tidak di-set oleh user saat registrasi.
            # Role akan di-set ke default ('participant') oleh model atau diubah oleh admin.
            'role': {'read_only': True},
            'username': {'required': True} # Pastikan username dikirim, frontend mengirimkannya
        }

    def validate_email(self, value):
        # Validasi kustom untuk memastikan email belum terdaftar
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Pengguna dengan email ini sudah ada.")
        return value

    def create(self, validated_data):
        # Metode 'create' ini dipanggil saat serializer menyimpan data baru.
        # Kita akan mengambil 'name' dari validated_data dan memecahnya.
        full_name = validated_data.pop('name')
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Gunakan metode create_user dari model User untuk membuat user baru.
        # create_user akan menangani hashing password secara otomatis.
        user = User.objects.create_user(
            username=validated_data['username'], # Frontend mengirimkan username (diisi dengan email)
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name,
            phone_number=validated_data.get('phone_number'), # .get() agar tidak error jika tidak ada
            address=validated_data.get('address'),
            # 'role' akan menggunakan nilai default dari model ('participant')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    # 'name' adalah properti read-only di model, kita bisa menampilkannya.
    name = serializers.CharField(source='name', read_only=True)
    # Role juga read-only untuk user biasa yang mengupdate profilnya sendiri
    role = serializers.ChoiceField(choices=UserRole.choices, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'first_name', 'last_name', 
                  'phone_number', 'address', 'profile_picture', 'role')
        # Field yang tidak boleh diubah oleh user saat update profil (misalnya email, username, role)
        read_only_fields = ('email', 'username', 'role') 
        extra_kwargs = {
            'profile_picture': {'required': False, 'allow_null': True}, # Foto profil opsional
            'first_name': {'required': False}, # first_name dan last_name opsional saat PATCH
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        # Metode 'update' ini dipanggil saat serializer mengupdate data yang sudah ada.
        # Frontend AuthContext.tsx mengirim FormData dengan 'first_name', 'last_name', 'phone_number', 'address', 'profile_picture'.

        # Tangani 'profile_picture':
        # Jika 'profile_picture' ada di validated_data dan nilainya null (dari frontend mengirim string kosong atau null),
        # berarti user ingin menghapus gambar.
        # Jika file baru dikirim, DRF akan menanganinya.
        profile_picture = validated_data.pop('profile_picture', None) # Ambil profile_picture dari data

        if profile_picture is None and 'profile_picture' in self.initial_data: 
            # Jika frontend mengirim 'profile_picture' sebagai null/kosong untuk menghapus.
            # self.initial_data berisi data mentah sebelum validasi.
            if instance.profile_picture:
                instance.profile_picture.delete(save=False) # Hapus file lama dari storage
            instance.profile_picture = None # Set field di model jadi null
        elif profile_picture is not None : # Jika ada file baru
            instance.profile_picture = profile_picture

        # Update field lainnya
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        
        instance.save()
        return instance
    
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

class EnrollCourseSerializer(serializers.ModelSerializer):
    # Untuk field relasi, bisa ditampilkan sebagai string atau nested object
    course_name = serializers.CharField(source='course.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = EnrolledCourse
        fields = ['id', 'user', 'user_email', 'course', 'course_name', 
                 'enrollment_date', 'completion_date', 'status']
        extra_kwargs = {
            'user': {'write_only': True},  # user hanya untuk write operation
            'course': {'required': True}
        }