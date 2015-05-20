# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=32)),
                ('secret', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
