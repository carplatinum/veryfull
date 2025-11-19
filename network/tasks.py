# Для асинхронных задач
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Sum
from .models import Sale


@shared_task
def generate_sales_report():
    """
    Задача для ежедневного анализа продаж и отправки отчёта админам.
    """
    today = timezone.now().date()
    sales_summary = Sale.objects.filter(date=today).aggregate(total_amount=Sum('amount'))
    total = sales_summary['total_amount'] or 0

    send_mail(
        subject=f'Отчет о продажах за {today}',
        message=f'Общая сумма продаж: {total} руб.',
        from_email='noreply@yourdomain.com',
        recipient_list=['admin@yourdomain.com'],
    )
