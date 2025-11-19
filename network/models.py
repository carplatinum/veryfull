from django.db import models
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField


class Store(models.Model):
    """Звено сети продажи электроники."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = CountryField()
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=150)
    house_number = models.CharField(max_length=20)
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients'
    )
    debt_to_supplier = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    level = models.PositiveIntegerField(default=0)  # 0 - завод, 1 - розничная сеть, 2 - предприниматель
    created_at = models.DateTimeField(auto_now_add=True)

    def full_address(self):
        return f"{self.country.name}, {self.city}, {self.street}, {self.house_number}"
    full_address.short_description = "Полный адрес"

    def clean(self):
        """
        Валидация уровня - должно быть:
          - level = 0, если supplier отсутствует (это завод)
          - иначе level = supplier.level + 1
        """
        if self.supplier is None:
            if self.level != 0:
                raise ValidationError({
                    'level': 'Уровень должен быть 0 для завода (отсутствует поставщик).'
                })
        else:
            expected_level = self.supplier.level + 1
            if self.level != expected_level:
                raise ValidationError({
                    'level': f'Уровень должен быть на 1 больше уровня поставщика ({expected_level}).'
                })

    def save(self, *args, **kwargs):
        # Вызываем clean перед сохранением для валидации
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Сотрудник сети."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='employees')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    """Продукт сети."""
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=100)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.model}"


class Sale(models.Model):
    """Продажа продукта."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Sale of {self.product} by {self.employee} on {self.sale_date.date()}"
