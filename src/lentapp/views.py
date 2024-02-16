import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timezone import make_aware

from .models import ItemLend, LendItem


def index(request):
    return HttpResponse("Hello, world. You're at the lentapp index.")


def login(request):
    return HttpResponse(render(request, "lentapp/login.html"))


def items(request):
    items = LendItem.objects.all()

    context = {
        "item_list": items,
    }

    return HttpResponse(render(request, "lentapp/items.html", context))


def filtered_items(request, time_start_unix: int, time_end_unix: int):
    # TODO: return error if times are in the past

    time_start = make_aware(datetime.datetime.utcfromtimestamp(time_start_unix))
    time_end = make_aware(datetime.datetime.utcfromtimestamp(time_end_unix))

    all_items = LendItem.objects.all()

    items = [
        item for item in all_items if item.is_available_between(time_start, time_end)
    ]

    print(time_start_unix, time_start)
    print(time_end_unix, time_end)
    print(items)

    context = {
        "item_list": items,
    }

    return HttpResponse(render(request, "lentapp/items.html", context))


def lents(request):

    # TODO: remove hard coded USER_ID
    USER_ID = 2

    user = get_object_or_404(User, id=USER_ID)
    lents = ItemLend.objects.filter(user=user)
    lent_items = LendItem.objects.filter(itemlend__in=lents)

    context = {
        "item_list": lent_items,
        "lent_list": lents,
    }

    return HttpResponse(render(request, "lentapp/lents.html", context))
