"""Endless template tag tests."""

from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase
from django.test.client import RequestFactory

from endless_pagination.settings import PAGE_LABEL
from endless_pagination.tests import make_model_instances


def render(request, source, **context_data):
    """Render *source* with the given *request* and return (html, context)."""
    template = Template("{% load endless %}" + source)
    context_data = dict(context_data)
    context_data["request"] = request
    context = Context(context_data)
    return template.render(context).strip(), context


class LazyPaginateTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _get(self, page=None):
        querydict = {} if page is None else {PAGE_LABEL: page}
        return self.factory.get("/", querydict)

    def test_first_page_default_per_page(self):
        request = self._get()
        _, context = render(
            request,
            "{% lazy_paginate objects %}",
            objects=list(range(47)),
        )
        # Default PER_PAGE is 10.
        self.assertEqual(10, len(list(context["objects"])))

    def test_explicit_per_page(self):
        request = self._get()
        _, context = render(
            request,
            "{% lazy_paginate 5 objects %}",
            objects=list(range(47)),
        )
        self.assertEqual(5, len(list(context["objects"])))

    def test_first_page_size_differs(self):
        request = self._get()
        _, context = render(
            request,
            "{% lazy_paginate 3,10 objects %}",
            objects=list(range(47)),
        )
        self.assertEqual(3, len(list(context["objects"])))

    def test_subsequent_page(self):
        request = self._get(page=2)
        _, context = render(
            request,
            "{% lazy_paginate 3,10 objects %}",
            objects=list(range(47)),
        )
        # Page 2 should give 10 items.
        self.assertEqual(10, len(list(context["objects"])))

    def test_invalid_page_falls_back_to_first(self):
        request = self._get(page=999)
        _, context = render(
            request,
            "{% lazy_paginate 5 objects %}",
            objects=list(range(47)),
        )
        self.assertEqual(5, len(list(context["objects"])))

    def test_no_arguments_raises(self):
        with self.assertRaises(TemplateSyntaxError):
            Template("{% load endless %}{% lazy_paginate %}")

    def test_only_one_db_hit_for_lazy(self):
        queryset = make_model_instances(47)
        request = self._get()
        with self.assertNumQueries(1):
            _, context = render(
                request,
                "{% lazy_paginate 10 objects %}",
                objects=queryset,
            )
            list(context["objects"])


class ShowMoreTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_link_rendered_when_next_page(self):
        request = self.factory.get("/")
        html, _ = render(
            request,
            "{% lazy_paginate 5 objects %}{% show_more %}",
            objects=list(range(47)),
        )
        self.assertIn("endless_more", html)
        self.assertIn(f"{PAGE_LABEL}=2", html)

    def test_no_link_on_last_page(self):
        request = self.factory.get("/", {PAGE_LABEL: 2})
        html, _ = render(
            request,
            "{% lazy_paginate 100 objects %}{% show_more %}",
            objects=list(range(5)),
        )
        self.assertEqual("", html)

    def test_custom_label(self):
        request = self.factory.get("/")
        html, _ = render(
            request,
            '{% lazy_paginate 5 objects %}{% show_more "Encore" %}',
            objects=list(range(47)),
        )
        self.assertIn("Encore", html)
