from enum import Enum


class Status(Enum):
    OVERDUE = 1
    ACTIVE = 2
    PLANNED = 3
    RETURNED = 4
