"""Test project URL patterns."""

from django.urls import path
from django.views.generic import TemplateView
from endless_pagination.decorators import (
    page_template,
    page_templates,
)

from project.views import generic

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "complete/",
        page_templates(
            {
                "complete/objects_page.html": "objects-page",
                "complete/items_page.html": "items-page",
                "complete/entries_page.html": "entries-page",
                "complete/articles_page.html": "articles-page",
            }
        )(generic),
        {"template": "complete/index.html", "number": 21},
        name="complete",
    ),
    path(
        "digg/",
        page_template("digg/page.html")(generic),
        {"template": "digg/index.html"},
        name="digg",
    ),
    path(
        "twitter/",
        page_template("twitter/page.html")(generic),
        {"template": "twitter/index.html"},
        name="twitter",
    ),
    path(
        "onscroll/",
        page_template("onscroll/page.html")(generic),
        {"template": "onscroll/index.html"},
        name="onscroll",
    ),
    path(
        "chunks/",
        page_templates(
            {
                "chunks/objects_page.html": None,
                "chunks/items_page.html": "items-page",
            }
        )(generic),
        {"template": "chunks/index.html", "number": 50},
        name="chunks",
    ),
    path(
        "multiple/",
        page_templates(
            {
                "multiple/objects_page.html": "objects-page",
                "multiple/items_page.html": "items-page",
                "multiple/entries_page.html": "entries-page",
            }
        )(generic),
        {"template": "multiple/index.html", "number": 21},
        name="multiple",
    ),
    path(
        "callbacks/",
        page_template("callbacks/page.html")(generic),
        {"template": "callbacks/index.html"},
        name="callbacks",
    ),
]
