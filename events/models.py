from django.db import models
from django.conf import settings # User modelini doğru şekilde referans almak için

# --------------------
# 1. Kategori Modeli
# --------------------
class Category(models.Model):
    """
    Etkinlik kategorilerini temsil eder (örn: Müzik, Spor, Sanat).
    """
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        help_text="Kategori için görsel (isteğe bağlı)"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name'] # Kategorileri isme göre sırala

    def __str__(self):
        return self.name

# --------------------
# 2. Etkinlik Modeli
# --------------------
class Event(models.Model):
    """
    Sistemdeki ana etkinlikleri temsil eder.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='event_images/',
        null=True,
        blank=True,
        help_text="Etkinlik için kapak görseli"
    )
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField(default=0, help_text="Etkinliğin maksimum katılımcı sayısı")
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Virgülle ayırarak etiketleri girin (örn: canlı müzik, ücretsiz, açık hava)"
    )

    # --- İlişkisel Alanlar (Relationships) ---
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Organizatör silinirse etkinlikleri de silinir
        related_name='organized_events'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # Kategori silinirse bu alan null olur, etkinlik silinmez
        null=True,
        blank=True, # Kategori olması zorunlu değil
        related_name='events'
    )

    # --- Otomatik Tarih Alanları ---
    created_at = models.DateTimeField(auto_now_add=True) # Sadece oluşturulurken bir kez ayarlanır
    updated_at = models.DateTimeField(auto_now=True) # Her kaydedildiğinde güncellenir

    class Meta:
        ordering = ['-date', '-time'] # Etkinlikleri tarihe göre en yeniden eskiye sırala

    def __str__(self):
        return f"{self.title} on {self.date}"

# --------------------
# 3. Rezervasyon Modeli
# --------------------
class Booking(models.Model):
    """
    Bir kullanıcının bir etkinliğe yaptığı rezervasyonu temsil eder.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Bir kullanıcının aynı etkinliğe birden fazla rezervasyon yapmasını engeller
        unique_together = ('user', 'event')
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.user.username} booked '{self.event.title}'"