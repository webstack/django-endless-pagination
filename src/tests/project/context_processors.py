"""Navigation bar context processor for the demo project."""

import platform

import django
from django.urls import reverse

import endless_pagination

VOICES = (("show_more", "Show more (lazy + on scroll)"),)


def navbar(request):
    """Build the navigation bar voices."""
    current_path = request.path
    return {
        "navbar": [
            {
                "label": label,
                "path": reverse(name),
                "is_active": reverse(name) == current_path,
            }
            for name, label in VOICES
        ]
    }


def versions(request):
    """Expose Python / Django / package versions to templates."""
    return {
        "versions": (
            ("Python", platform.python_version()),
            ("Django", django.get_version()),
            ("Endless Pagination", endless_pagination.get_version()),
        )
    }
