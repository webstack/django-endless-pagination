"""LazyPaginator tests."""

from django.test import TestCase

from endless_pagination import paginators


class PaginatorTestMixin:
    """Shared assertions for the lazy paginator."""

    def setUp(self):
        self.items = list(range(30))
        self.per_page = 7
        self.paginator = paginators.LazyPaginator(
            self.items, self.per_page, orphans=2
        )

    def test_object_list(self):
        first_page = self.paginator.first_page
        expected = self.items[first_page : first_page + self.per_page]
        self.assertSequenceEqual(expected, self.paginator.page(2).object_list)

    def test_orphans(self):
        self.assertSequenceEqual(self.items[-9:], self.paginator.page(4).object_list)

    def test_no_orphans(self):
        paginator = paginators.LazyPaginator(range(11), 8, orphans=2)
        self.assertEqual(3, len(paginator.page(2).object_list))

    def test_empty_page(self):
        with self.assertRaises(paginators.EmptyPage):
            self.paginator.page(5)

    def test_invalid_page(self):
        with self.assertRaises(paginators.PageNotAnInteger):
            self.paginator.page("__not_valid__")
        with self.assertRaises(paginators.EmptyPage):
            self.paginator.page(0)


class LazyPaginatorTest(PaginatorTestMixin, TestCase):
    def test_items_count(self):
        with self.assertRaises(NotImplementedError):
            self.paginator.count

    def test_num_pages(self):
        self.paginator.page(2)
        self.assertEqual(3, self.paginator.num_pages)

    def test_page_range(self):
        with self.assertRaises(NotImplementedError):
            self.paginator.page_range


class DifferentFirstPageLazyPaginatorTest(TestCase):
    def setUp(self):
        self.items = list(range(26))
        self.paginator = paginators.LazyPaginator(
            self.items, 7, first_page=3, orphans=2
        )

    def test_first_page_is_smaller(self):
        page = self.paginator.page(1)
        self.assertEqual(3, len(page.object_list))

    def test_no_orphans(self):
        paginator = paginators.LazyPaginator(range(11), 5, first_page=3, orphans=2)
        self.assertEqual(3, len(paginator.page(3).object_list))
