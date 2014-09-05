# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024)),
                ('details', markitup.fields.MarkupField(help_text=b'A markitup field')),
                ('_details_rendered', models.TextField(editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
