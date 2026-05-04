"""Test project URL patterns."""

from django.urls import path
from django.views.generic import TemplateView

from project.views import show_more

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("show-more/", show_more, name="show_more"),
]
