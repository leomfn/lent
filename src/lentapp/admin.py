from django.contrib import admin

from .models import LendItem, ItemLend, ItemOwner

admin.site.register(LendItem)
admin.site.register(ItemLend)
admin.site.register(ItemOwner)
