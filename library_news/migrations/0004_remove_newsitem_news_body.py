# Generated by Django 4.2.7 on 2024-04-30 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_news', '0003_newsitem_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsitem',
            name='news_body',
        ),
    ]