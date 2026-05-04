"""Lazy pagination for Django, with optional infinite-scroll JavaScript."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("django-endless-pagination")
except PackageNotFoundError:
    __version__ = "0.0.0"


def get_version():
    """Return the installed package version."""
    return __version__
