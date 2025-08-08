# serializers.py

from rest_framework import serializers
from .models import Event, Booking, Category

# --- CategorySerializer ---
# Category için image alanı da eklenmiş, bu harika.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


# --- EventSerializer (Nihai ve Tam Hali) ---
class EventSerializer(serializers.ModelSerializer):
    # 1. Organizatörün kullanıcı adını string olarak ekliyoruz.
    organizer_username = serializers.ReadOnlyField(source='organizer.username')

    # 2. Kategorinin adını string olarak ekliyoruz.
    category_name = serializers.ReadOnlyField(source='category.name')

    # 3. Virgülle ayrılmış 'tags' metnini bir listeye dönüştürüyoruz.
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'image',
            'date',
            'time',
            'capacity',
            'organizer',           # Organizer ID'si (int)
            'organizer_username',  # Organizer Adı (string)
            'category',            # Category ID'si (int)
            'category_name',       # Category Adı (string)
            'bookings_count',      # Rezervasyon Sayısı (int)
            'tags',                # Etiketler (list of strings)
        ]

    # 'tags' alanını dolduracak metod
    def get_tags(self, obj):
        # Eğer 'tags' alanı dolu ve bir string ise:
        if obj.tags and isinstance(obj.tags, str):
            # Virgüllere göre ayır, her birinin başındaki/sonundaki boşlukları sil
            # ve boş etiketleri (örn: "müzik,,spor") listeden çıkar.
            return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
        # Değilse, boş bir liste döndür.
        return []


# --- BookingSerializer ---
# Bu serializer zaten iyi görünüyor, olduğu gibi kalabilir.
class BookingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    event_title = serializers.ReadOnlyField(source='event.title')

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'booked_at', 'username', 'event_title']
        read_only_fields = ['booked_at']