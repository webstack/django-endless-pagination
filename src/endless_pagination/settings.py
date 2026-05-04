"""Endless pagination settings."""

from django.conf import settings

# Default number of items per page.
PER_PAGE = getattr(settings, "ENDLESS_PAGINATION_PER_PAGE", 10)
# Querystring key carrying the page number.
PAGE_LABEL = getattr(settings, "ENDLESS_PAGINATION_PAGE_LABEL", "page")
# See django ``Paginator`` definition of orphans.
ORPHANS = getattr(settings, "ENDLESS_PAGINATION_ORPHANS", 0)
# Markup shown by the default ``show_more`` template while loading. HTML safe.
LOADING = getattr(settings, "ENDLESS_PAGINATION_LOADING", "loading")
