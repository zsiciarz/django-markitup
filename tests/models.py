from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from markitup.fields import MarkupField


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=50)
    body = MarkupField()

    def __str__(self):
        return self.title


class AbstractParent(models.Model):
    content = MarkupField()

    class Meta:
        abstract = True


class NoRendered(models.Model):
    """
    Test that the no_rendered_field keyword arg works.
    """
    body = MarkupField(no_rendered_field=True)


class CallableDefault(models.Model):
    """
    A callable default on a field triggers hidden widget rendering by Django.
    """
    body = MarkupField(default=lambda: '')
