# users/serializers.py

from rest_framework import serializers
from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Yeni kullanıcı kaydı için kullanılan serializer.
    Sadece gerekli alanları (isim, e-posta, şifre) ister.
    """
    # Şifre doğrulaması için bu alan zorunludur.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label="Confirm Password")

    class Meta:
        model = CustomUser

        # --- DOĞRU FİELDS LİSTESİ BURADA ---
        # Kayıt olurken kullanıcıdan sadece bu bilgileri istiyoruz.
        fields = ['email', 'password', 'password2', 'first_name', 'last_name']

        extra_kwargs = {
            # 'password' alanının API cevaplarında asla geri dönmemesini sağlar.
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        # Şifrelerin eşleşip eşleşmediğini kontrol eder.
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifreler uyuşmuyor."})
        return attrs

    def create(self, validated_data):
        # 'password2' alanını modelde olmadığı için veriden çıkarıyoruz.
        validated_data.pop('password2')
        # Modelimizin kendi create_user metodu ile şifreyi hashleyerek kullanıcıyı oluşturuyoruz.
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Giriş yapmış kullanıcının profil bilgilerini göstermek ve güncellemek için kullanılır.
    Hassas olmayan tüm kullanıcı bilgilerini içerir.
    """

    class Meta:
        model = CustomUser
        # Kullanıcının profilinde görünecek ve güncellenebilecek tüm alanlar.
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'university',
            'department',
            'grade',
            'profile_picture',
            'bio'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Giriş yapmış kullanıcının kendi şifresini değiştirmesi için serializer.
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