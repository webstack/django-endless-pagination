"""Utility tests."""

from django.test import TestCase
from django.test.client import RequestFactory

from endless_pagination import utils
from endless_pagination.exceptions import PaginationError
from endless_pagination.settings import PAGE_LABEL


class GetDataFromContextTest(TestCase):
    def test_valid_context(self):
        context = {"endless": "test-data"}
        self.assertEqual("test-data", utils.get_data_from_context(context))

    def test_invalid_context(self):
        self.assertRaises(PaginationError, utils.get_data_from_context, {})


class GetPageNumberFromRequestTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_no_querystring_key(self):
        request = self.factory.get("/")
        self.assertEqual(1, utils.get_page_number_from_request(request))

    def test_default_querystring_key(self):
        request = self.factory.get(f"?{PAGE_LABEL}=2")
        self.assertEqual(2, utils.get_page_number_from_request(request))

    def test_default(self):
        request = self.factory.get("/")
        self.assertEqual(3, utils.get_page_number_from_request(request, default=3))

    def test_custom_querystring_key(self):
        request = self.factory.get("?mypage=4")
        self.assertEqual(
            4,
            utils.get_page_number_from_request(request, querystring_key="mypage"),
        )

    def test_post_data(self):
        request = self.factory.post("/", {PAGE_LABEL: 5})
        self.assertEqual(5, utils.get_page_number_from_request(request))


class GetQuerystringForPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_querystring(self):
        request = self.factory.get("/")
        self.assertEqual(
            "?mypage=2",
            utils.get_querystring_for_page(request, 2, "mypage"),
        )

    def test_default_page(self):
        request = self.factory.get("/")
        self.assertEqual(
            "",
            utils.get_querystring_for_page(
                request, 3, "mypage", default_number=3
            ),
        )

    def test_composition(self):
        request = self.factory.get("/?mypage=1&foo=bar")
        querystring = utils.get_querystring_for_page(request, 4, "mypage")
        self.assertIn("mypage=4", querystring)
        self.assertIn("foo=bar", querystring)

    def test_querystring_key_is_stripped(self):
        request = self.factory.get("/?querystring_key=mykey")
        self.assertEqual(
            "?mypage=5",
            utils.get_querystring_for_page(request, 5, "mypage"),
        )
