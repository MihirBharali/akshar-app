# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-25 16:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kolibriauth', '0021_facilityuser_physical_facility_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facilityuser',
            old_name='physical_facility_grade',
            new_name='physical_facility_level',
        ),
    ]
