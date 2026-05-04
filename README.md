## Django Endless Pagination

Lazy pagination for Django with an optional, dependency-free JavaScript
helper that loads the next page on click or while scrolling.

The package ships:

- the `{% lazy_paginate %}` and `{% show_more %}` template tags;
- a `LazyPaginator` that avoids `COUNT(*)` queries by overshooting by one
  row;
- a small vanilla-JS module (`endless-pagination.js`) exposing
  `endlessPaginate({ paginateOnScroll, paginateOnScrollMargin })`.

The package is available on [pypi.org](https://pypi.org/project/webstack-django-endless-pagination/):

```shell
uv add webstack-django-endless-pagination
```

### Setup

Add `'endless_pagination'` to `INSTALLED_APPS`. The
`django.template.context_processors.request` context processor must be
enabled (it is in Django's default project template).

### Quickstart

```html+django
{% load endless %}

{% lazy_paginate 10 entries %}
{% for entry in entries %}
    {# render the entry #}
{% endfor %}
{% show_more %}
```

Load the next page over Ajax (with optional infinite scroll):

```html+django
{% load static %}
<script src="{% static 'endless_pagination/js/endless-pagination.js' %}"></script>
<script>
  document.addEventListener('DOMContentLoaded', function () {
    endlessPaginate({ paginateOnScroll: true });
  });
</script>
```

The view must return the page partial when the request carries the
querystring key (defaults to `page`), and the full page otherwise:

```python
from django.shortcuts import render
from endless_pagination.settings import PAGE_LABEL

def entries(request):
    template = "entries/page.html" if PAGE_LABEL in request.GET else "entries/index.html"
    return render(request, template, {"entries": Entry.objects.all()})
```

### Template tags

Both tags live in the `endless` library: `{% load endless %}`.

#### `lazy_paginate`

Paginates `objects` without issuing a `COUNT(*)` query.

```html+django
{% lazy_paginate entries %}            {# uses ENDLESS_PAGINATION_PER_PAGE #}
{% lazy_paginate 20 entries %}         {# 20 per page #}
{% lazy_paginate 5,40 entries %}       {# 5 on the first page, 40 thereafter #}
```

After the call, `entries` in the template context is the slice for the
current page. Must be used before `{% show_more %}`.

#### `show_more`

Renders the link that loads the next page over Ajax. Call it after
`{% lazy_paginate %}`.

```html+django
{% show_more %}                                   {# default label and loading text #}
{% show_more "Encore" %}                          {# custom label #}
{% show_more "Encore" "Chargement…" %}            {# custom label + loading text #}
{% show_more "Encore" "Chargement…" "btn" %}      {# extra CSS class on the link #}
```

You can override the default `endless/show_more.html` template, but the
JavaScript helper expects:

- the `a.endless_more` link inside an `.endless_container` element;
- the link's `rel` attribute to start with the querystring key;
- a hidden `.endless_loading` element next to the link, shown while the
  next page is being fetched.

### JavaScript

The bundled `endless-pagination.js` is dependency-free. It exposes two
globals:

- `endlessPaginate(options)` — convenience initialiser bound to
  `document.body`.
- `EndlessPagination` — the underlying class, useful when scoping to a
  specific element.

```js
endlessPaginate({ paginateOnScroll: true, paginateOnScrollMargin: 20 });

const widget = new EndlessPagination(
    document.querySelector('#entries'),
    { paginateOnScroll: true }
);
widget.destroy();  // detach click and scroll listeners
```

#### Options

| Option | Default | Description |
| --- | --- | --- |
| `containerSelector` | `'.endless_container'` | Wrapper around the *show more* link. |
| `loadingSelector` | `'.endless_loading'` | Loader element shown while fetching. |
| `moreSelector` | `'a.endless_more'` | Link that loads the next page. |
| `paginateOnScroll` | `false` | Trigger the next page from scroll. |
| `paginateOnScrollMargin` | `1` | Bottom margin in pixels for the trigger. |

### Settings

| Setting | Default | Description |
| --- | --- | --- |
| `ENDLESS_PAGINATION_PER_PAGE` | `10` | Default page size; overridable in the tag. |
| `ENDLESS_PAGINATION_PAGE_LABEL` | `'page'` | Querystring key carrying the page number. |
| `ENDLESS_PAGINATION_ORPHANS` | `0` | Same meaning as Django's `Paginator(orphans=…)`. |
| `ENDLESS_PAGINATION_LOADING` | `'loading'` | HTML-safe markup shown by the loader element. |

### Development

Install dev dependencies:

```shell
uv sync
```

Run the test suite:

```shell
cd src/tests
uv run python manage.py test endless_pagination
```
