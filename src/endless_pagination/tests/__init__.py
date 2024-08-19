"""Test model definitions."""

from django.core.management import call_command
from django.db import models


def make_model_instances(number):
    """Make a ``number`` of test model instances and return a queryset."""
    for _ in range(number):
        TestModel.objects.create()
    return TestModel.objects.all()


class TestModel(models.Model):
    """A model used in tests."""

    def __str__(self):
        return "TestModel: {0}".format(self.id)


call_command("syncdb", verbosity=0)
