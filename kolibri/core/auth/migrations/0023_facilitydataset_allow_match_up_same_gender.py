# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-30 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kolibriauth', '0022_auto_20211225_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitydataset',
            name='allow_match_up_same_gender',
            field=models.BooleanField(default=True),
        ),
    ]
