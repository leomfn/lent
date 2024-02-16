import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Q


class LendItem(models.Model):
    """
    An item that can be borrowed, e. g. a cargo bike called 'My Bike'

    name : name of the item
    type : type of the item
    description : description of the item
    use_conditions : terms of service to use the item
    owner : owner of the item
    is_ready : if the item is in a 'ready' state, i. e. not broken or something
    readiness_description : description of the item's state if the item is not ready
    currently_lent : if the item is in use right now
    """

    name = models.CharField(max_length=50)
    # RESTRICT prevents deleting type if this would lead to orphans
    type = models.ForeignKey("ItemType", on_delete=models.RESTRICT)
    description = models.CharField(max_length=255, blank=True)
    use_conditions = models.TextField(blank=True)
    owner = models.ForeignKey("ItemOwner", on_delete=models.RESTRICT)
    is_ready = models.BooleanField()
    readiness_description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def is_currently_available(self):
        current_time = timezone.now()
        return not self.itemlend_set.filter(
            time_start__lte=current_time, time_end__gte=current_time
        ).exists()

    def is_available_between(
        self, datetime_start: timezone, datetime_end: timezone
    ) -> bool:
        return not self.itemlend_set.filter(
            Q(time_start__lt=datetime_end) & Q(time_end__gt=datetime_start)
        ).exists()

    def get_current_lent(self):
        if self.is_currently_available():
            return None

        current_time = timezone.now()

        return self.itemlend_set.get(
            time_start__lte=current_time, time_end__gte=current_time
        )

    def will_be_available_at(self):
        if self.is_currently_available():
            return None

        return self.get_current_lent().time_end


class ItemLend(models.Model):
    """
    A lend is a time slot a user has borrowed an item

    item : item which is borrowed/lent
    user : user by which the item is borrowed
    time_lend : date and time a user requested to borrow an item
    time_start : date and time the lend starts at
    time_end : date and time the lend ends at
    time_return : date and time the item is returned
    """

    # CASCADE deletes the lends if the lent item it deleted
    item = models.ForeignKey("LendItem", on_delete=models.CASCADE)
    # RESTRICT prevents lends to be deleted if a user who borrowed an item is deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    time_lend = models.DateTimeField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    time_return = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.item.name} lent to {self.user.username} from {self.time_start} to {self.time_end}"

    def status(self):
        returned = self.time_return is not None
        lent_end_in_past = self.time_end < timezone.now()
        lent_start_in_future = self.time_start > timezone.now()

        # if lent_start_in_past and not returned:
        if not self.item.is_currently_available() and not returned:
            return "active"
        elif lent_end_in_past and not returned:
            return "overdue"
        elif lent_start_in_future:
            return "planned"
        elif returned:
            return "returned"


class ItemType(models.Model):
    """
    A type of item, e. g. 'Cargo Bike'

    name : name of type
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ItemOwner(models.Model):
    """
    An owner of items, like a Person or Institution

    user : registered app user to be connected with the owner
    contact_details : custom contact details in addition to user contact details
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    contact_details = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
