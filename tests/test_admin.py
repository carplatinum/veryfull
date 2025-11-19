from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from network.admin import StoreAdmin
from network.models import Store


class StoreAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = StoreAdmin(Store, self.site)
        self.factory = RequestFactory()

        self.store1 = Store.objects.create(
            name='Store #1',
            email='store1@example.com',
            country='US',
            city='City',
            street='Street',
            house_number='1',
            level=0,
            debt_to_supplier=100
        )
        self.store2 = Store.objects.create(
            name='Store #2',
            email='store2@example.com',
            country='US',
            city='City',
            street='Street',
            house_number='2',
            supplier=self.store1,
            level=1,
            debt_to_supplier=200
        )

    def test_clear_debt_action(self):
        request = self.factory.get('/')
        # Для работы с messages добавляем middleware storage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        queryset = Store.objects.filter(pk__in=[self.store1.pk, self.store2.pk])
        self.admin.clear_debt(request, queryset)

        updated_stores = Store.objects.filter(pk__in=[self.store1.pk, self.store2.pk])
        for store in updated_stores:
            self.assertEqual(store.debt_to_supplier, 0)
