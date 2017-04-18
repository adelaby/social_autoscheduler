# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-18 15:48
from __future__ import unicode_literals

from django.db import migrations


def create_social_network(apps, schema_editor):
    """Creates initial `SocialNetwork` instances.

    Data migration function passed to migrations' `RunPython` method. Create
    initial social networks (`SocialNetwork` instances) needed by the app.
    """
    SocialNetwork = apps.get_model('publication_scheduler', 'SocialNetwork')
    SocialNetwork.objects.create(name='Twitter')


class Migration(migrations.Migration):

    dependencies = [
        ('publication_scheduler', '0004_publication_category'),
    ]

    operations = [
        migrations.RunPython(create_social_network),
    ]