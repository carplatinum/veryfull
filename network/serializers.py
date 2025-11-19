from rest_framework import serializers
from .models import Store, Employee, Product, Sale


class StoreSerializer(serializers.ModelSerializer):
    """Сериализатор магазина с валидацией уровня."""

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['debt_to_supplier', 'created_at']

    def validate(self, data):
        supplier = data.get('supplier')
        level = data.get('level')

        # Если supplier отсутствует, level должен быть 0
        if supplier is None:
            if level != 0:
                raise serializers.ValidationError({
                    'level': 'Уровень должен быть 0 для завода (отсутствует поставщик).'
                })
        else:
            expected_level = supplier.level + 1
            if level != expected_level:
                raise serializers.ValidationError({
                    'level': f'Уровень должен быть на 1 больше уровня поставщика ({expected_level}).'
                })

        return data


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника."""
    class Meta:
        model = Employee
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара."""
    class Meta:
        model = Product
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    """Сериализатор продажи."""
    class Meta:
        model = Sale
        fields = '__all__'
