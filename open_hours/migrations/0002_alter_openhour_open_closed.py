# Generated by Django 4.2.1 on 2023-09-01 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_hours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhour',
            name='open_closed',
            field=models.BooleanField(choices=[(0, 'Closed'), (1, 'Open')], default=1),
        ),
    ]
