# Generated by Django 3.2.8 on 2023-04-19 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header_footer', '0002_footercolumn_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footercolumn',
            name='order',
            field=models.IntegerField(help_text='use incrementally to order the footer columns from left to right', null=True),
        ),
    ]
