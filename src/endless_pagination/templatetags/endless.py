"""Template tags for lazy pagination."""

import re

from django import template
from django.utils.encoding import iri_to_uri

from endless_pagination import settings, utils
from endless_pagination.paginators import EmptyPage, LazyPaginator

PAGINATE_EXPRESSION = re.compile(
    r"""
    ^
    (((?P<first_page>\d+)\,)?(?P<per_page>\d+)\s+)?
    (?P<objects>\w+)
    $
    """,
    re.VERBOSE,
)


register = template.Library()


@register.tag
def lazy_paginate(parser, token):
    """Lazy-paginate ``objects`` without issuing a COUNT query.

    Usage::

        {% lazy_paginate entries %}
        {% lazy_paginate 40 entries %}
        {% lazy_paginate 5,40 entries %}

    The first form uses ``ENDLESS_PAGINATION_PER_PAGE`` for the page size.
    The second sets the page size (also used for the first page).
    The third sets the first-page size and the page size separately.
    """
    try:
        tag_name, tag_args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]!r} tag requires arguments"
        )
    match = PAGINATE_EXPRESSION.match(tag_args)
    if match is None:
        raise template.TemplateSyntaxError(
            f"Invalid arguments for {tag_name!r} tag"
        )
    return PaginateNode(**match.groupdict())


class PaginateNode(template.Node):
    """Push a single page slice of *objects* to the template context."""

    def __init__(self, objects, first_page=None, per_page=None):
        self.objects = template.Variable(objects)
        self.var_name = objects
        self.per_page = int(per_page) if per_page else settings.PER_PAGE
        self.first_page = int(first_page) if first_page else None

    def render(self, context):
        per_page = self.per_page
        first_page = self.first_page or per_page
        objects = self.objects.resolve(context)
        paginator = LazyPaginator(
            objects, per_page, first_page=first_page, orphans=settings.ORPHANS
        )
        page_number = utils.get_page_number_from_request(
            context["request"], settings.PAGE_LABEL, default=1
        )
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)
        context.update(
            {
                "endless": {
                    "default_number": 1,
                    "override_path": None,
                    "page": page,
                    "querystring_key": settings.PAGE_LABEL,
                },
                self.var_name: page.object_list,
            }
        )
        return ""


@register.inclusion_tag("endless/show_more.html", takes_context=True)
def show_more(context, label=None, loading=settings.LOADING, class_name=None):
    """Render the “show more” link that loads the next page over Ajax.

    Must be called after ``{% lazy_paginate %}``.
    """
    data = utils.get_data_from_context(context)
    page = data["page"]
    if not page.has_next():
        return {}
    request = context["request"]
    querystring = utils.get_querystring_for_page(
        request,
        page.next_page_number(),
        data["querystring_key"],
        default_number=data["default_number"],
    )
    return {
        "label": label,
        "loading": loading,
        "class_name": class_name,
        "path": iri_to_uri(data["override_path"] or request.path),
        "querystring": querystring,
        "querystring_key": data["querystring_key"],
        "request": request,
    }
