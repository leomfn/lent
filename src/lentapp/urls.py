from django.urls import path

from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/items/", permanent=True)),
    path(
        "items/filter/<int:time_start_unix>/<int:time_end_unix>/",
        views.filtered_items,
        name="filtered-items",
    ),
    path("items/", views.items, name="items"),
    path("lents/", views.lents, name="lents"),
    path("login/", views.login, name="login"),
]
