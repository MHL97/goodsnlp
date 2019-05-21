# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190516_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='product_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='base',
            name='product_url',
            field=models.CharField(primary_key=True, max_length=255, serialize=False),
        ),
    ]
