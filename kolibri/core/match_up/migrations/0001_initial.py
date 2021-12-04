# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-11-28 11:38
from __future__ import unicode_literals

from django.db import migrations, models
import morango.models.fields.uuids


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchUpDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentee_id', morango.models.fields.uuids.UUIDField()),
                ('mentee_name', models.CharField(max_length=200)),
                ('mentor_id', morango.models.fields.uuids.UUIDField()),
                ('mentor_name', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=100)),
                ('supervisor_id', morango.models.fields.uuids.UUIDField()),
                ('supervisor_name', models.CharField(max_length=200)),
                ('facility_id', morango.models.fields.uuids.UUIDField()),
            ],
        ),
    ]
