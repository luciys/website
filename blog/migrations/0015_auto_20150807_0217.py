# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20150807_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
