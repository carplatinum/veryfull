from django.core.exceptions import ValidationError
from django.test import TestCase
from network.models import Store


class StoreModelEdgeCaseTests(TestCase):
    def test_level_validation_without_supplier(self):
        store = Store(
            name='Factory',
            email='factory@example.com',
            country='US',
            city='NY',
            street='Main St',
            house_number='1',
            supplier=None,
            level=1  # Ошибка: должен быть 0 для завода
        )
        with self.assertRaises(ValidationError) as cm:
            store.full_clean()
        self.assertIn('level', cm.exception.message_dict)

    def test_level_validation_with_wrong_level(self):
        supplier = Store.objects.create(
            name='Supplier',
            email='sup@example.com',
            country='US',
            city='LA',
            street='Sunset Blvd',
            house_number='10',
            level=0
        )
        store = Store(
            name='Client',
            email='client@example.com',
            country='US',
            city='LA',
            street='Sunset Blvd',
            house_number='11',
            supplier=supplier,
            level=2  # Ошибка: должен быть supplier.level + 1 = 1
        )
        with self.assertRaises(ValidationError) as cm:
            store.full_clean()
        self.assertIn('level', cm.exception.message_dict)
