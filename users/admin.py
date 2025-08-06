# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# CustomUser modelimizi admin paneline kaydediyoruz.
# UserAdmin'i kullanarak Django'nun hazır admin arayüzünü miras alıyoruz
# ve kendi ek alanlarımızı (university, department, grade) gösteriyoruz.

class CustomUserAdmin(UserAdmin):
    # Admin panelindeki kullanıcı listesinde görünecek alanlar
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'university')

    # Kullanıcı oluşturma/düzenleme formunda alanları gruplamak için
    # UserAdmin'in orijinal fieldset'lerini alıp kendi alanlarımızı ekliyoruz.
    fieldsets = UserAdmin.fieldsets + (
        ('Ek Bilgiler', {'fields': ('university', 'department', 'grade')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Ek Bilgiler', {'fields': ('university', 'department', 'grade')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)