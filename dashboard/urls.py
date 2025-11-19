from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_index'),
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
]
