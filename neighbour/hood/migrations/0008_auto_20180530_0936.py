# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-30 09:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hood', '0007_auto_20180530_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='NeighbourhoodDetalis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='neighbourhood',
            name='neighbourhood_icon',
            field=models.ImageField(blank=True, null=True, upload_to='admin/'),
        ),
        migrations.AddField(
            model_name='neighbourhooddetalis',
            name='neighbourhood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hood.Neighbourhood'),
        ),
    ]
