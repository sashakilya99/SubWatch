
from django.urls import path

from . import views


urlpatterns = [
    path("", views.subscription_list, name="subscription_list"),
    path("add/", views.subscription_create, name="subscription_create"),
    path(
        "edit/<int:subscription_id>/",
        views.subscription_update,
        name="subscription_update",
    ),
    path(
        "delete/<int:subscription_id>/",
        views.subscription_delete,
        name="subscription_delete",
    ),
]
