from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import User # Pastikan import UserRole juga jika perlu
from .models import ScheduledSession
from .serializers import ScheduledSessionSerializer
from django.http import JsonResponse


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,) # Siapa saja bisa mendaftar

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Frontend mengirim 'name', backend butuh 'first_name' dan 'last_name'
        name = request.data.get('name', '')
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Tambahkan ke data serializer sebelum create
        # Ini cara lain jika tidak di handle di serializer `extra_kwargs`
        # serializer.validated_data['first_name'] = first_name
        # serializer.validated_data['last_name'] = last_name

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        user_data = serializer.data
        # Frontend mungkin mengharapkan semua field user setelah registrasi
        # Kita bisa membuat user object dan serialize lagi dengan UserProfileSerializer jika perlu
        
        return Response(user_data, status=status.HTTP_201_CREATED, headers=headers)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user # Mengembalikan profil user yang sedang login

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True) # Selalu partial update (PATCH)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    from django.http import JsonResponse

def director_dashboard(request):
    return JsonResponse({"message": "Ini adalah dashboard director"})
    
    
    
    