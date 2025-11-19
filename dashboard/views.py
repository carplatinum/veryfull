from django.shortcuts import render, get_object_or_404
from network.models import Store, Employee
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_home(request):
    # Главная страница админки с краткой статистикой или приветствием
    num_stores = Store.objects.count()
    num_employees = Employee.objects.count()
    context = {
        'num_stores': num_stores,
        'num_employees': num_employees,
    }
    return render(request, "dashboard/index.html", context)


@login_required
def store_list(request):
    stores = Store.objects.all()
    return render(request, "dashboard/store_list.html", {'stores': stores})


@login_required
def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    return render(request, "dashboard/store_detail.html", {'store': store})


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "dashboard/employee_list.html", {'employees': employees})


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, "dashboard/employee_detail.html", {'employee': employee})
