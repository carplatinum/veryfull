from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/network/', include('network.urls')),  # Подключаем маршруты network
    path('api-auth/', include('rest_framework.urls')),  # DRF встроенный браузерный вход/выход (опционально)
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', lambda request: redirect('dashboard_index')),
]
