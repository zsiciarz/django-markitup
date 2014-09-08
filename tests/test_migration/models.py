from django.db import models

from markitup.fields import MarkupField

class Thing(models.Model):
    title = models.CharField(max_length=1024)
    details = MarkupField(help_text="A markitup field")
