# users/urls.py

from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    ChangePasswordView,
    UserListView,
    UserDetailView,
    MyTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]