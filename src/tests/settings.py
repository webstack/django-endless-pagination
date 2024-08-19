"""Settings file for the Django project used for tests."""

import os

PROJECT_NAME = "project"

# Base paths.
ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT = os.path.join(ROOT, PROJECT_NAME)

# Django configuration.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "sqlite.db"}}

DEBUG = TEMPLATE_DEBUG = True
INSTALLED_APPS = (
    "django.contrib.staticfiles",
    "endless_pagination",
    PROJECT_NAME,
)
LANGUAGE_CODE = os.getenv("ENDLESS_PAGINATION_LANGUAGE_CODE", "en-us")
ROOT_URLCONF = PROJECT_NAME + ".urls"
SECRET_KEY = os.getenv("ENDLESS_PAGINATION_SECRET_KEY", "secret")
SITE_ID = 1
STATIC_ROOT = os.path.join(PROJECT, "static")
STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                PROJECT_NAME + ".context_processors.navbar",
                PROJECT_NAME + ".context_processors.versions",
            ],
        },
    },
]

# Testing.
NOSE_ARGS = (
    "--verbosity=2",
    "--with-coverage",
    "--cover-package=endless_pagination",
)
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
