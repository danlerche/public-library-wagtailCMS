# Generated by Django 3.2.8 on 2023-04-24 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_resource', '0002_onlineresourcepage_tutorial_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineresourceindexpage',
            name='niche_academy',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]