"""Test project views."""

from django.shortcuts import render

from endless_pagination.settings import PAGE_LABEL

LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipisicing elit, "
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
)


def show_more(request):
    """Render the lazy-paginated list, swapping templates on Ajax page loads."""
    objects = [
        {"title": f"Object {i + 1}", "contents": LOREM} for i in range(50)
    ]
    template = (
        "show_more/page.html"
        if PAGE_LABEL in request.GET
        else "show_more/index.html"
    )
    return render(
        request,
        template,
        {"objects": objects, "page_template": "show_more/page.html"},
    )
