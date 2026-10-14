from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "amount",
        "currency",
        "billing_cycle",
        "next_payment_date",
        "status",
    )
    list_filter = ("status", "billing_cycle", "currency")
    search_fields = ("name", "category")
    ordering = ("next_payment_date",)