from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Store, Employee, Product, Sale
from .serializers import StoreSerializer, EmployeeSerializer, ProductSerializer, SaleSerializer
from .permissions import ActiveEmployeePermission


class StoreViewSet(viewsets.ModelViewSet):
    """
    CRUD для звеньев сети (Store).
    Ограничение обновления поля debt_to_supplier.
    Фильтрация по стране.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']
    search_fields = ['name', 'city', 'email']
    permission_classes = [ActiveEmployeePermission]

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ['PUT', 'PATCH']:
            data = kwargs.get('data')
            if data:
                data = data.copy()
                data.pop('debt_to_supplier', None)
                kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
