# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resigner', '0002_apiclient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiclient',
            name='key',
            field=models.CharField(unique=True, max_length=32),
        ),
    ]
