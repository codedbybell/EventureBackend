# events/views.py

# --- Gerekli Django ve DRF import'ları ---
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# --- Model, Serializer ve Form import'ları ---
from .models import Event, Booking, Category
from .serializers import EventSerializer, BookingSerializer, CategorySerializer
from .permissions import IsCreatorOrReadOnly
from .forms import EventForm


# ==============================================================================
# MOBİL UYGULAMA İÇİN API VIEW'LARI (MEVCUT KODUNUZ)
# ==============================================================================

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        queryset = Event.objects.all().select_related('organizer', 'category').order_by('-created_at')

        category_name = self.request.query_params.get('category', None)

        date_filter = self.request.query_params.get('date', None)

        if category_name is not None:
            queryset = queryset.filter(category__name=category_name)

        if date_filter == 'upcoming':
            now = timezone.now()
            queryset = queryset.filter(date__gte=now)

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsCreatorOrReadOnly]


class BookEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        if Booking.objects.filter(event=event, user=request.user).exists():
            return Response({"detail": "Bu etkinliğe zaten kayıtlısınız."}, status=status.HTTP_400_BAD_REQUEST)

        # Kapasite kontrolü (0 kapasite sınırsız anlamına gelebilir)
        if event.capacity > 0 and event.bookings.count() >= event.capacity:
            return Response({"detail": "Bu etkinlikte yer kalmadı."}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(event=event, user=request.user)
        # bookings_count modelden kaldırıldığı için, sayım anlık yapılır.
        return Response({"detail": "Kayıt başarılı."}, status=status.HTTP_201_CREATED)


class UnBookEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        booking = get_object_or_404(Booking, event=event, user=request.user)
        booking.delete()
        return Response({"detail": "Kayıt iptal edildi."}, status=status.HTTP_204_NO_CONTENT)


class PopularEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        # bookings_count kaldırıldığı için, anlık sayıma göre sıralama yapıyoruz.
        from django.db.models import Count
        return Event.objects.annotate(num_bookings=Count('bookings')).order_by('-num_bookings')[:10]


class UserEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_booked_event_ids = Booking.objects.filter(user=self.request.user).values_list('event_id', flat=True)
        return Event.objects.filter(id__in=user_booked_event_ids)


# ==============================================================================
# WEB PANELİ VIEW'LARI (YENİ EKLENEN KOD)
# ==============================================================================

# Kullanıcının staff (yönetici) olup olmadığını kontrol eden yardımcı fonksiyon
def is_staff_user(user):
    return user.is_staff


# @login_required: Kullanıcının giriş yapmış olmasını zorunlu kılar.
# @user_passes_test: Belirtilen test fonksiyonunu (is_staff_user) geçmesini zorunlu kılar.
@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')  # Yetkisizse admin login'e yönlendir
def panel_event_list(request):
    """Tüm etkinlikleri listeleyen panel ana sayfası."""
    events = Event.objects.all().order_by('-date', '-time')
    context = {
        'events': events,
        'page_title': 'Etkinlik Yönetimi'
    }
    return render(request, 'events/panel_event_list.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')
def panel_event_add(request):
    """Yeni etkinlik ekleme formunu gösterir ve işler."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('events:panel-event-list')
    else:
        form = EventForm()

    context = {
        'form': form,
        'page_title': 'Yeni Etkinlik Ekle'
    }
    return render(request, 'events/panel_event_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')
def panel_event_edit(request, pk):
    """Mevcut bir etkinliği düzenleme formunu gösterir ve işler."""
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:panel-event-list')
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
        'page_title': f'Etkinliği Düzenle: {event.title}'
    }
    return render(request, 'events/panel_event_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')
def panel_event_delete(request, pk):
    """Bir etkinliği siler. Sadece POST isteği ile çalışır."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events:panel-event-list')

    # GET isteği ile bu URL'e gelinirse hiçbir şey yapma, listeye geri dön.
    return redirect('events:panel-event-list')