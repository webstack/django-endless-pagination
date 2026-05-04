# Django Endless Pagination

Django Endless Pagination can be used to provide Twitter-style or
Digg-style pagination, with optional Ajax support and other features
like multiple or lazy pagination.

The original documentation is [available
online](http://django-endless-pagination.readthedocs.org/), or in the docs
directory of the project. This fork has not updated the original documentation.

The package is available on [pypi.org](https://pypi.org/project/webstack-django-endless-pagination/):

```shell
uv add webstack-django-endless-pagination
```

## Development

Clone the repository, then install dev dependencies:

```shell
uv sync --group dev
```

Run the test suite:

```shell
cd src/tests
uv run python manage.py test endless_pagination
```
