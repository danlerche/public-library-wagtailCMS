# Generated by Django 4.2.7 on 2023-12-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_programs', '0006_event_tutorial_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='featured_on_home_page',
            field=models.BooleanField(default=True),
        ),
    ]
