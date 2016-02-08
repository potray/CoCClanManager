# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 18:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ResistenciaCoC', '0011_clan_is_at_war'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ResistenciaCoC.Clan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]