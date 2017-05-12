# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20160715_0028'),
        ('publication_scheduler', '0005_create_initial_social_network'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='schedule.Event')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publish_events', to='publication_scheduler.Category')),
                ('social_network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publication_scheduler.SocialNetwork')),
            ],
            bases=('schedule.event',),
        ),
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='publication_scheduler.Category'),
        ),
    ]