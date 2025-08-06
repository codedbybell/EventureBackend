# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # AbstractUser'dan gelen standart alanlar: username, email, password, first_name, last_name...

    # Bizim eklediğimiz alanlar
    university = models.CharField(max_length=150, blank=True, null=True, verbose_name="Üniversite")
    department = models.CharField(max_length=150, blank=True, null=True, verbose_name="Bölüm")
    grade = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Sınıf")
    # profile_picture = models.ImageField(...) -> Profil fotoğrafını daha sonra ekleyebiliriz.

    def __str__(self):
        return self.username