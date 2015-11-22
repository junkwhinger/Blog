# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20151121_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='updated_at',
        ),
    ]
