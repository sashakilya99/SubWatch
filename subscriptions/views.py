from django.contrib.auth.decorators import login_required
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404

from .forms import SubscriptionForm
from .models import Subscription

@login_required
def subscription_list(request):
    all_subscriptions = Subscription.objects.all()
    active_subscriptions = all_subscriptions.filter(status="active")

    # Финансовая сводка
    monthly_total = Decimal("0.00")

    for subscription in active_subscriptions:
        amount = subscription.amount

        if subscription.billing_cycle == "weekly":
            monthly_total += amount * Decimal("52") / Decimal("12")
        elif subscription.billing_cycle == "monthly":
            monthly_total += amount
        elif subscription.billing_cycle == "quarterly":
            monthly_total += amount / Decimal("3")
        elif subscription.billing_cycle == "yearly":
            monthly_total += amount / Decimal("12")

    yearly_total = monthly_total * Decimal("12")

    # Фильтрация по статусу
    status_filter = request.GET.get("status", "")
    subscriptions = all_subscriptions

    valid_statuses = [
        choice[0] for choice in Subscription.Status.choices
    ]

    if status_filter in valid_statuses:
        subscriptions = subscriptions.filter(status=status_filter)
    else:
        status_filter = ""

    # Поиск по названию
    search_query = request.GET.get("q", "").strip()

    if search_query:
        subscriptions = subscriptions.filter(name__icontains=search_query)

    # Фильтрация по категории
    category_filter = request.GET.get("category", "")

    categories = (
        Subscription.objects
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    if category_filter in categories:
        subscriptions = subscriptions.filter(category=category_filter)
    else:
        category_filter = ""

    # Сортировка
    sort_options = {
        "date": "next_payment_date",
        "date_desc": "-next_payment_date",
        "name": "name",
        "amount": "amount",
        "amount_desc": "-amount",
    }

    sort_filter = request.GET.get("sort", "date")

    if sort_filter not in sort_options:
        sort_filter = "date"

    subscriptions = subscriptions.order_by(sort_options[sort_filter])

    context = {
        "subscriptions": subscriptions,
        "active_count": active_subscriptions.count(),
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
        "status_filter": status_filter,
        "status_choices": Subscription.Status.choices,
        "search_query": search_query,
        "categories": categories,
        "category_filter": category_filter,
        "sort_filter": sort_filter,
    }

    return render(
        request,
        "subscriptions/subscription_list.html",
        context,
    )

@login_required
def subscription_create(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("subscription_list")
    else:
        form = SubscriptionForm()

    return render(
        request,
        "subscriptions/subscription_form.html",
        {"form": form, "page_title": "Добавить подписку"},
    )

@login_required
def subscription_update(request, subscription_id):
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
    )

    if request.method == "POST":
        form = SubscriptionForm(
            request.POST,
            instance=subscription,
        )

        if form.is_valid():
            form.save()
            return redirect("subscription_list")
    else:
        form = SubscriptionForm(instance=subscription)

    return render(
        request,
        "subscriptions/subscription_form.html",
        {
            "form": form,
            "page_title": "Редактировать подписку",
        },
    )

@login_required
def subscription_delete(request, subscription_id):
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
    )

    if request.method == "POST":
        subscription.delete()
        return redirect("subscription_list")

    return render(
        request,
        "subscriptions/subscription_confirm_delete.html",
        {"subscription": subscription},
    )
