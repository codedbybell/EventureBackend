# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager # Yeni manager'ımızı import ediyoruz

class CustomUser(AbstractUser):
    # Username alanını artık kullanmayacağımız için kaldırıyoruz.
    username = None
    # Email alanını birincil anahtar ve benzersiz yapıyoruz.
    email = models.EmailField('email address', unique=True)

    # Django'ya giriş için hangi alanı kullanacağını söylüyoruz.
    USERNAME_FIELD = 'email'
    # createsuperuser komutunda sorulacak zorunlu alanlar.
    # Email ve password zaten varsayılan olarak sorulur.
    REQUIRED_FIELDS = []

    # Modelimizin özel manager'ımızı kullanmasını sağlıyoruz.
    objects = CustomUserManager()

    # Diğer alanlar aynı kalabilir.
    university = models.CharField(max_length=150, blank=True, null=True, verbose_name="Üniversite")
    department = models.CharField(max_length=150, blank=True, null=True, verbose_name="Bölüm")
    grade = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Sınıf")

    def __str__(self):
        return self.email