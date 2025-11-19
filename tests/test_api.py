from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from network.models import Store, Employee
from django.contrib.auth.models import User


class StoreViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.factory = Store.objects.create(
            name='Factory',
            email='factory@test.com',
            country='US',
            city='New York',
            street='5th Ave',
            house_number='1',
            level=0,
        )
        self.store = Store.objects.create(
            name='Test Store',
            email='store@test.com',
            country='US',
            city='New York',
            street='5th Avenue',
            house_number='10',
            supplier=self.factory,
            level=1,
        )
        self.employee = Employee.objects.create(
            store=self.store,
            first_name='John',
            last_name='Doe',
            position='Manager',
            email='john@example.com',
            is_active=True
        )
        self.user.employee = self.employee
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_store_invalid_level(self):
        url = reverse('store-list')
        data = {
            'name': 'Bad Store',
            'email': 'badstore@test.com',
            'country': 'US',
            'city': 'LA',
            'street': 'Sunset Blvd',
            'house_number': '101',
            'supplier': self.factory.id,
            'level': 2  # Некорректный уровень
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('level', response.data)
