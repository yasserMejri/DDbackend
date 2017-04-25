# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 20:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20170424_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dduser',
            name='location',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AlterField(
            model_name='dduser',
            name='phone',
            field=models.IntegerField(default=10000000000000, unique=True, validators=[django.core.validators.RegexValidator(code='Invalid number', message='Length has to be 10', regex='^\\d{14}$')]),
        ),
        migrations.AlterField(
            model_name='dduser',
            name='user_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='delivery.User_type'),
        ),
    ]
