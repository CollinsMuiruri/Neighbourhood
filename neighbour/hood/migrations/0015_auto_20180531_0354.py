# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-31 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hood', '0014_join'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='neighbourhood',
            name='occuupants_count',
        ),
        migrations.AddField(
            model_name='neighbourhood',
            name='occupantsCount',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]