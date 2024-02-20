from django.urls import path

from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/items/", permanent=True), name="home"),
    path(
        "items/filter/<int:timestamp_start>/<int:timestamp_end>/",
        views.filtered_items,
        name="filtered-items",
    ),
    path("items/", views.items, name="items"),
    path("lents/", views.lents, name="lents"),
    path("items/book/<int:item_id>/", views.book_item, name="book-item"),
    path("items/return/<int:lent_id>/", views.return_item, name="return-item"),
    path("items/cancel/<int:lent_id>/", views.cancel_lent, name="cancel-lent"),
]
