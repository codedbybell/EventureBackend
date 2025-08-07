from django.urls import path
from .views import (
    EventListCreateView,
    EventDetailView,
    BookEventView,
    UnBookEventView,
    UserEventsView,
)

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/book/', BookEventView.as_view(), name='book-event'),
    path('events/<int:pk>/unbook/', UnBookEventView.as_view(), name='unbook-event'),
    path('users/me/events/', UserEventsView.as_view(), name='user-events'),
]