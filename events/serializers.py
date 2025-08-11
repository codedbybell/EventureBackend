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
    organizer_username = serializers.ReadOnlyField(source='organizer.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    tags = serializers.SerializerMethodField()
    bookings_count = serializers.SerializerMethodField()
    is_booked = serializers.SerializerMethodField()

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
            'is_booked',
        ]

    # 'tags' alanını dolduracak metod
    def get_tags(self, obj):
        if obj.tags and isinstance(obj.tags, str):
            return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
        return []

    def get_bookings_count(self, obj):
        return obj.bookings.count()

    def get_is_booked(self, obj):
        # 'request' nesnesini serializer'ın context'inden alıyoruz.
        request = self.context.get('request')

        # Eğer istek yapan bir kullanıcı yoksa veya kullanıcı anonim ise (giriş yapmamışsa),
        # hiçbir etkinliğe kayıtlı değildir.
        if not request or not request.user.is_authenticated:
            return False

        # Kullanıcının bu etkinliğe ('obj') ait bir rezervasyonu olup olmadığını kontrol et.
        # .exists() sorgusu, veritabanına sadece var olup olmadığını sorar, çok verimlidir.
        return obj.bookings.filter(user=request.user).exists()

# --- BookingSerializer ---
# Bu serializer zaten iyi görünüyor, olduğu gibi kalabilir.
class BookingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    event_title = serializers.ReadOnlyField(source='event.title')

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'booked_at', 'username', 'event_title']
        read_only_fields = ['booked_at']