# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170215_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('NOTE', 'Note'), ('PROJECT', 'Project'), ('LINK', 'Link')], max_length=75),
        ),
    ]