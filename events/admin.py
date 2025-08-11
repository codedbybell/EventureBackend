from django.contrib import admin
from .models import Event, Category, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # 1. 'list_display' listesinden eski 'bookings_count'u kaldır.
    #    Yerine, birazdan oluşturacağımız metodun adını yaz: 'get_bookings_count'
    list_display = ('title', 'category', 'date', 'time', 'capacity', 'get_bookings_count')
    list_filter = ('category', 'date')
    search_fields = ('title', 'location')
    readonly_fields = ('created_at', 'updated_at')

    # 2. Anlık katılımcı sayısını hesaplayacak yeni bir metod ekle.
    def get_bookings_count(self, obj):
        # 'obj' burada bir Event nesnesini temsil eder.
        # Bu metod, o event'e ait rezervasyon sayısını anlık olarak döndürür.
        return obj.bookings.count()

    # 3. Metodun admin panelindeki sütun başlığını belirle.
    get_bookings_count.short_description = 'Bookings Count'

# ... (Category ve Booking için olan admin sınıfların aynı kalabilir) ...
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'booked_at')