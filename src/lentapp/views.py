from django.shortcuts import render
from django.http import HttpResponse

from .models import LendItem, ItemType


def index(request):
    return HttpResponse("Hello, world. You're at the lentapp index.")


def items(request):

    items = LendItem.objects.all()

    context = {
        "item_list": items,
    }

    print("context", context)

    return HttpResponse(render(request, "lentapp/index.html", context))
