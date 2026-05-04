"""Lazy paginator implementation.

Avoids ``COUNT(*)`` queries by fetching one extra row per page.
"""

from django.core.paginator import (
    EmptyPage,
    Page,
    PageNotAnInteger,
    Paginator,
)


class CustomPage(Page):
    """A page supporting a different item count on the first page."""

    def start_index(self):
        paginator = self.paginator
        if paginator.count == 0:
            return 0
        if self.number == 1:
            return 1
        return (self.number - 2) * paginator.per_page + paginator.first_page + 1

    def end_index(self):
        paginator = self.paginator
        if self.number == paginator.num_pages:
            return paginator.count
        return (self.number - 1) * paginator.per_page + paginator.first_page


class LazyPaginator(Paginator):
    """Lazy paginator: avoids ``COUNT(*)`` queries by overshooting by one row."""

    def __init__(self, object_list, per_page, **kwargs):
        self.first_page = kwargs.pop("first_page", per_page)
        super().__init__(object_list, per_page, **kwargs)

    def get_current_per_page(self, number):
        return self.first_page if number == 1 else self.per_page

    def validate_number(self, number):
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger("That page number is not an integer")
        if number < 1:
            raise EmptyPage("That page number is less than 1")
        return number

    def page(self, number):
        number = self.validate_number(number)
        current_per_page = self.get_current_per_page(number)
        bottom = 0 if number == 1 else (number - 2) * self.per_page + self.first_page
        top = bottom + current_per_page
        objects = list(self.object_list[bottom : top + self.orphans + 1])
        objects_count = len(objects)
        if objects_count > current_per_page + self.orphans:
            self._num_pages = number + 1
            objects = objects[:current_per_page]
        elif number != 1 and objects_count <= self.orphans:
            raise EmptyPage("That page contains no results")
        else:
            self._num_pages = number
        return CustomPage(objects, number, self)

    @property
    def count(self):
        raise NotImplementedError

    @property
    def num_pages(self):
        return self._num_pages

    @property
    def page_range(self):
        raise NotImplementedError
