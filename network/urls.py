"""URL-маршруты приложения network."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, EmployeeViewSet, ProductViewSet, SaleViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
