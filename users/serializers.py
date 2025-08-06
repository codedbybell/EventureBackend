# users/serializers.py

from rest_framework import serializers
from .models import CustomUser

class UserRegisterSerializer(serializers.ModelSerializer):
    # Kullanıcıdan şifreyi iki kez girmesini istiyoruz, doğrulama için.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        # API aracılığıyla hangi alanların alınıp verileceğini belirtiyoruz.
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True} # Şifrenin API cevabında geri dönmemesini sağlar.
        }

    # Bu fonksiyon, password ve password2'nin aynı olup olmadığını kontrol eder.
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifreler uyuşmuyor."})
        return attrs

    # Bu fonksiyon, veriler doğrulandıktan sonra kullanıcıyı nasıl oluşturacağımızı belirler.
    def create(self, validated_data):
        # password2'yi veritabanına kaydetmeyeceğimiz için listeden çıkarıyoruz.
        validated_data.pop('password2')
        # create_user metodu şifreyi otomatik olarak hash'ler (güvenli hale getirir).
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    # Bu serializer, kullanıcının profil bilgilerini göstermek için kullanılacak.
    class Meta:
        model = CustomUser
        # Şifre gibi hassas bilgileri ASLA burada göstermeyiz.
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'university', 'department', 'grade']

class ChangePasswordSerializer(serializers.Serializer):
    """
    Giriş yapmış kullanıcının şifresini değiştirmesi için serializer.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski şifreniz doğru değil.")
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Yeni şifreler uyuşmuyor."})
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user