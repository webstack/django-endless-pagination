"""Utility helpers for lazy pagination."""

from endless_pagination import exceptions
from endless_pagination.settings import PAGE_LABEL


def get_data_from_context(context):
    """Return the ``endless`` data block from the template context."""
    try:
        return context["endless"]
    except KeyError:
        raise exceptions.PaginationError("Cannot find endless data in context.")


def get_page_number_from_request(request, querystring_key=PAGE_LABEL, default=1):
    """Read the current page number from the request (GET then POST)."""
    for source in (request.GET, request.POST):
        try:
            return int(source[querystring_key])
        except (KeyError, TypeError, ValueError):
            continue
    return default


def get_querystring_for_page(request, page_number, querystring_key, default_number=1):
    """Return a querystring (with leading ``?``) pointing at *page_number*."""
    querydict = request.GET.copy()
    querydict[querystring_key] = page_number
    if page_number == default_number:
        del querydict[querystring_key]
    if "querystring_key" in querydict:
        del querydict["querystring_key"]
    if querydict:
        return "?" + querydict.urlencode()
    return ""
