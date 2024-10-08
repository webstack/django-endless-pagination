"""Django pagination tools supporting Ajax, multiple and lazy pagination,
Twitter-style and Digg-style pagination.
"""

VERSION = (2, 0)


def get_version():
    """Return the Django Endless Pagination version as a string."""
    return ".".join(map(str, VERSION))
