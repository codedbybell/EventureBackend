from django.urls import path
from .views import (
    EventListCreateView, EventDetailView, BookEventView, UnBookEventView,
    UserEventsView, CategoryListAPIView, PopularEventsAPIView,
)

app_name = 'events'

urlpatterns = [
    # Ana URL: /api/events/
    path('', EventListCreateView.as_view(), name='event-list-create'),

    # URL: /api/events/popular/
    path('popular/', PopularEventsAPIView.as_view(), name='popular-events'),

    # URL: /api/events/categories/ <<< KATEGORİLER BURADA
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),

    # URL: /api/events/1/
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),

    # URL: /api/events/1/book/
    path('<int:event_id>/book/', BookEventView.as_view(), name='book-event'),

    # URL: /api/events/1/unbook/
    path('<int:event_id>/unbook/', UnBookEventView.as_view(), name='unbook-event'),
]