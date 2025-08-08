# events/admin.py

from django.contrib import admin
from .models import Event, Category, Booking # Category ve Booking'i import et

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'date', 'organizer', 'bookings_count')
    list_filter = ('category', 'date', 'organizer')
    search_fields = ('title', 'description', 'location')
    ordering = ('-date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'booked_at')
    list_filter = ('event', 'user')
    search_fields = ('event__title', 'user__username')