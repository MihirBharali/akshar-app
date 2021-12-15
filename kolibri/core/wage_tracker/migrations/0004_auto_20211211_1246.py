# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-11 07:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wage_tracker', '0003_auto_20211208_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwagetransactions',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userwageaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
