# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-27 18:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_hired',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
