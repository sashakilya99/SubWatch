
from django import forms

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            "name",
            "category",
            "amount",
            "currency",
            "billing_cycle",
            "next_payment_date",
            "status",
            "notes",
        ]
        widgets = {
            "next_payment_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 3}
            ),
        }
