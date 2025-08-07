from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer
from django.utils import timezone

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class BookEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)

        if Booking.objects.filter(event=event, user=request.user).exists():
            return Response({"detail": "Booking already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if event.bookings.count() >= event.capacity:
            return Response({"detail": "The event quota is full"}, status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(event=event, user=request.user)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UnBookEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        booking = Booking.objects.filter(event=event, user=request.user).first()

        if not booking:
            return Response({"detail": "You are not already registered for this event."}, status=status.HTTP_404_NOT_FOUND)

        booking.delete()
        return Response({"detail": "Your participation has been canceled."}, status=status.HTTP_200_OK)

class UserEventsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


    def get_queryset(self):
        queryset = Event.objects.all()
        date = self.request.query_params.get('date', None)
        if date == 'upcoming':
            queryset = queryset.filter(event_date__gte=timezone.now())
        return queryset

