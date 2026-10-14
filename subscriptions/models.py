
from django.db import models


class Subscription(models.Model):
    class BillingCycle(models.TextChoices):
        WEEKLY = "weekly", "Еженедельно"
        MONTHLY = "monthly", "Ежемесячно"
        QUARTERLY = "quarterly", "Раз в 3 месяца"
        YEARLY = "yearly", "Ежегодно"

    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        PAUSED = "paused", "Приостановлена"
        CANCELLED = "cancelled", "Отменена"

    name = models.CharField(
        max_length=100,
        verbose_name="Название подписки",
    )
    category = models.CharField(
        max_length=50,
        default="other",
        verbose_name="Категория",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
    )
    currency = models.CharField(
        max_length=3,
        default="EUR",
        verbose_name="Валюта",
    )
    billing_cycle = models.CharField(
        max_length=20,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY,
        verbose_name="Период оплаты",
    )
    next_payment_date = models.DateField(
        verbose_name="Дата следующего платежа",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Заметки",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["next_payment_date"]
