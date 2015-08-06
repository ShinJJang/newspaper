from enum import Enum


class SortMethods(Enum):
    """This class is enum for sorting methods.
    Thread is sorted by score, comment, title, date.

    """
    score = 1
    comment = 2
    title = 3
    date = 4