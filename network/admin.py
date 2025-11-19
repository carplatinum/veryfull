from django.contrib import admin
from django.utils.html import format_html
from .models import Store, Employee, Product, Sale


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Админка для магазинов."""
    list_display = ('name', 'email', 'full_address', 'debt_to_supplier', 'level', 'supplier_link')
    search_fields = ('name', 'email', 'city', 'country')
    list_filter = ('city',)

    actions = ['clear_debt']

    def full_address(self, obj):
        return f"{obj.country.name}, {obj.city}, {obj.street}, {obj.house_number}"
    full_address.short_description = 'Полный адрес'

    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/network/store/{obj.supplier.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"
    supplier_link.short_description = 'Поставщик'

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность очищена у {updated} объектов.")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Админка для сотрудников."""
    list_display = ('first_name', 'last_name', 'position', 'email', 'store')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('store',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для товаров."""
    list_display = ('name', 'model', 'release_date', 'price')
    search_fields = ('name', 'model')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """Админка для продаж."""
    list_display = ('product', 'employee', 'sale_date', 'quantity', 'total_amount')
    list_filter = ('sale_date',)
