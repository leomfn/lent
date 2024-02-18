import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware

from .models import ItemLend, LendItem

from .forms import BookSlotForm


# def login(request):
#     return HttpResponse(render(request, "lentapp/login.html"))


def items(request):
    if request.method == "POST":
        form = BookSlotForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            date_start = form_data["date_start"]
            time_start = form_data["time_start"]
            duration = form_data["duration"]
            datetime_start = datetime.datetime.combine(date_start, time_start)
            datetime_end = datetime_start + datetime.timedelta(hours=duration)
            timestamp_start = int(datetime_start.timestamp())
            timestamp_end = int(datetime_end.timestamp())

            return HttpResponseRedirect(
                reverse("filtered-items", args=(timestamp_start, timestamp_end))
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        current_time = timezone.now()
        form = BookSlotForm(
            {
                "date_start": current_time,
                "time_start": current_time.strftime("%H:%M"),
            }
        )

    items = LendItem.objects.all()

    context = {
        "item_list": items,
        "form": form,
    }

    return HttpResponse(render(request, "lentapp/items.html", context))


def filtered_items(
    request,
    timestamp_start: int,
    timestamp_end: int,
):
    if request.method == "POST":
        form = BookSlotForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            date_start = form_data["date_start"]
            time_start = form_data["time_start"]
            duration = form_data["duration"]
            datetime_start = datetime.datetime.combine(date_start, time_start)
            datetime_end = datetime_start + datetime.timedelta(hours=duration)
            timestamp_start = int(datetime_start.timestamp())
            timestamp_end = int(datetime_end.timestamp())

            return HttpResponseRedirect(
                reverse("filtered-items", args=(timestamp_start, timestamp_end))
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        current_time = timezone.now()
        form = BookSlotForm(
            {
                "date_start": current_time,
                "time_start": current_time.strftime("%H:%M"),
            }
        )

    # TODO: return error if times are in the past

    datetime_start = make_aware(datetime.datetime.utcfromtimestamp(timestamp_start))
    datetime_end = make_aware(datetime.datetime.utcfromtimestamp(timestamp_end))
    duration = (datetime_end - datetime_start).total_seconds() / 3600

    all_items = LendItem.objects.all()

    items = [
        item
        for item in all_items
        if item.is_available_between(datetime_start, datetime_end)
    ]

    context = {
        "item_list": items,
        "datetime_start": datetime_start,
        "datetime_end": datetime_end,
        "duration": duration,
        "form": form,
    }

    return HttpResponse(render(request, "lentapp/filtered_items.html", context))


def lents(request):
    user = request.user

    lents = ItemLend.objects.filter(user=user)
    lent_items = LendItem.objects.filter(itemlend__in=lents).distinct()

    distinct_items_with_lents = [
        {
            "item": item,
            "lents": sorted(
                lents.filter(user=user, item=item),
                key=lambda lent: (lent.status().value, -lent.time_start.timestamp()),
            ),
        }
        for item in lent_items
    ]

    context = {
        "item_list": distinct_items_with_lents,
        "lent_list": lents,
    }

    return HttpResponse(render(request, "lentapp/lents.html", context))


def book_item(request, item_id: int):
    if request.method == "POST":
        item = LendItem.objects.get(id=item_id)
        item.itemlend_set.create(
            item=item,
            user=request.user,
            time_start=request.POST["datetime_start"],
            time_end=request.POST["datetime_end"],
            time_lend=timezone.now(),
        )

    return HttpResponseRedirect(reverse("lents"))


def return_item(request, lent_id: int):
    if request.method == "POST":
        lent = ItemLend.objects.get(id=lent_id)
        lent.time_return = timezone.now()
        lent.save()

    return HttpResponseRedirect(reverse("lents"))


def cancel_lent(request, lent_id: int):
    if request.method == "POST":
        lent = ItemLend.objects.get(id=lent_id)
        lent.delete()

    return HttpResponseRedirect(reverse("lents"))
