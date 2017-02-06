# -*- coding: utf-8 -*-


from django.db import models, migrations
import resigner.models


class Migration(migrations.Migration):

    dependencies = [
        ('resigner', '0003_auto_20150616_0426'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApiClient',
        ),
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(default=resigner.models.mk_key, max_length=32),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='secret',
            field=models.CharField(default=resigner.models.mk_secret, max_length=256),
        ),
    ]
