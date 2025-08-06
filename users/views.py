# users/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserDetailSerializer

# /api/register/ endpoint'i için
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,) # Herkesin bu endpoint'e erişimine izin ver (kayıt olmak için)
    serializer_class = UserRegisterSerializer

# /api/profile/ endpoint'i için
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,) # Sadece giriş yapmış kullanıcılar erişebilir
    serializer_class = UserDetailSerializer

    def get_object(self):
        # Bu fonksiyon, isteği yapan (giriş yapmış) kullanıcının kendisini döndürür.
        # Böylece /api/profile/1 gibi bir ID'ye gerek kalmaz.
        return self.request.user