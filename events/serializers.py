from rest_framework import serializers
from .models import Event, Booking

class EventSerializer(serializers.ModelSerializer):
    creator_username = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'event_date',
            'capacity',
            'club_name',
            'creator_username',
        ]

class BookingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    event_title = serializers.ReadOnlyField(source='event.title')

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'booked_at', 'username', 'event_title']
        read_only_fields = ['booked_at']