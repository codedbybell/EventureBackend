from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta

from .models import Event, Booking, Category
from .serializers import EventSerializer, BookingSerializer, CategorySerializer
from .permissions import \
    IsCreatorOrReadOnly  # 'IsCreatorOrReadOnly' adını 'IsOrganizerOrReadOnly' olarak değiştirmek daha mantıklı olabilir.


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Event.objects.all().select_related('organizer', 'category').order_by(
            '-created_at')  # Performans için
        date = self.request.query_params.get('date', None)
        now = timezone.now()

        if date == 'upcoming':
            # event_date yerine modelinizdeki doğru alanı kullanın (date, event_date vs.)
            queryset = queryset.filter(date__gte=now)

        return queryset

    def perform_create(self, serializer):
        # <<< DÜZELTME: Modelinizdeki alan 'organizer' ise 'creator' yerine 'organizer' kullanın.
        # Bu, model tanımınızla tutarlı olmalıdır.
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsCreatorOrReadOnly]  # veya IsOrganizerOrReadOnly


# BookEventView ve UnBookEventView'da önemli bir değişiklik yok,
# ama booking_counts alanı adının modelinizle tutarlı olduğundan emin olun.
class BookEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        if Booking.objects.filter(event=event, user=request.user).exists():
            return Response({"detail": "You have already booked this event."}, status=status.HTTP_400_BAD_REQUEST)
        if event.booking_counts >= event.capacity:
            return Response({"detail": "This event is full."}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(event=event, user=request.user)
        # Daha güvenli güncelleme için F() expression kullanabilirsiniz:
        # from django.db.models import F
        # Event.objects.filter(pk=event.id).update(booking_counts=F('booking_counts') + 1)
        event.booking_counts += 1
        event.save()

        return Response({"detail": "Booking successful."}, status=status.HTTP_201_CREATED)


class UnBookEventView(APIView):
    # ... Bu view genellikle doğru çalışır ...
    pass


class PopularEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        # HATA DÜZELTİLDİ: 'bookings_counts' -> 'bookings_count'
        return Event.objects.order_by('-bookings_count')[:10]


class UserEventsView(generics.ListAPIView):
    # <<< DÜZELTME: Bu view'un mantığı tamamen yenilendi.
    # Kullanıcının katıldığı etkinlikleri listelemeli.
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Kullanıcının yaptığı rezervasyonlar (Booking) üzerinden ilişkili etkinlikleri (Event) çekiyoruz.
        user_booked_event_ids = Booking.objects.filter(user=self.request.user).values_list('event_id', flat=True)
        queryset = Event.objects.filter(id__in=user_booked_event_ids)

        # İsteğe bağlı olarak yine tarih filtresi eklenebilir.
        date_filter = self.request.query_params.get('date', None)
        if date_filter == 'upcoming':
            queryset = queryset.filter(date__gte=timezone.now())

        return queryset