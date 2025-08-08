# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),

    # --- API Yolları ---
    path('api/users/', include('users.urls')),
    # /api/events/ ile başlayan istekler events.urls'e (API URL'leri) gider.
    path('api/events/', include('events.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # --- WEB PANELİ YOLU (GÜNCELLENDİ) ---
    # /panel/ ile başlayan istekler events.panel_urls'e (Panel URL'leri) gider.
    path('panel/', include('events.panel_urls')), # <<< BURASI DEĞİŞTİ
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)