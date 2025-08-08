# events/panel_urls.py

from django.urls import path
from .views import (
    panel_event_list,
    panel_event_add,
    panel_event_edit,
    panel_event_delete
)

# app_name'i burada tekrar belirtmek, template'lerdeki url'lerin çalışması için önemlidir.
app_name = 'events'

urlpatterns = [
    # /panel/ -> isteği buraya geldiğinde, kalan yol '' olduğu için bu eşleşir.
    path('', panel_event_list, name='panel-event-list'),

    # /panel/add/ -> isteği
    path('add/', panel_event_add, name='panel-event-add'),

    # /panel/edit/5/ -> isteği
    path('edit/<int:pk>/', panel_event_edit, name='panel-event-edit'),

    # /panel/delete/5/ -> isteği
    path('delete/<int:pk>/', panel_event_delete, name='panel-event-delete'),
]