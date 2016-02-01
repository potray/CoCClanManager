# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 18:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ResistenciaCoC', '0007_auto_20160127_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clan_admin', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ManyToManyField(related_name='clan_manager', to=settings.AUTH_USER_MODEL)),
                ('member', models.ManyToManyField(related_name='clan_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
