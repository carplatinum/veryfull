from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class DashboardViewTests(TestCase):
    """Тесты представлений Dashboard"""

    def setUp(self):
        """Подготовка данных для тестов"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )

    def test_dashboard_redirect_if_not_logged_in(self):
        """Проверка редиректа на страницу логина для анонимных"""
        response = self.client.get(reverse('dashboard_index'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_dashboard_loads_for_logged_in_user(self):
        """Проверка успешной загрузки страницы дашборда для авторизованного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, "Добро пожаловать в админку сети электроники")

    def test_dashboard_page_content(self):
        """Проверка наличия ключевого текста на странице дашборда"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard_index'))
        self.assertContains(response, "Здесь можно управлять магазинами, сотрудниками и товарами.")
