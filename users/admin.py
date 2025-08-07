# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Bu sınıf, CustomUser modelinin admin panelinde nasıl görüneceğini yönetir.
    model = CustomUser

    # Admin panelindeki kullanıcı listesinde hangi alanların görüneceği.
    # 'username' yerine 'email' gösteriyoruz.
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined')

    # Kullanıcıları neye göre sıralayacağımız.
    # Artık 'username' olmadığı için 'email'e göre sıralıyoruz.
    ordering = ('email',)  # <-- ASIL DEĞİŞİKLİK BURADA!

    # Admin panelindeki kullanıcı düzenleme formunun yapısı.
    # fieldsets içindeki 'username' referanslarını da 'email' olarak değiştirmeliyiz.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Kendi eklediğimiz alanları da admin panelinde görmek istersek buraya ekleyebiliriz.
        ('Custom Fields', {'fields': ('university', 'department', 'grade')}),
    )

    # Admin panelindeki arama kutusunun hangi alanlarda arama yapacağı.
    search_fields = ('email', 'first_name', 'last_name')


# CustomUser modelimizi ve özel admin ayarlarımızı Django admin paneline kaydediyoruz.
admin.site.register(CustomUser, CustomUserAdmin)