# users/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserDetailSerializer, UserDetailSerializer, ChangePasswordSerializer
from rest_framework import generics, status
from rest_framework.response import Response

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

class ChangePasswordView(generics.UpdateAPIView):
    """
    Kullanıcının şifresini değiştirmesi için bir endpoint.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "Şifre başarıyla güncellendi."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """
    Tüm kullanıcıları listelemek için bir endpoint.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,) # Sadece giriş yapmışlar listeyi görsün

class UserDetailView(generics.RetrieveAPIView):
    """
    ID'ye göre tek bir kullanıcının detayını görmek için bir endpoint.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)