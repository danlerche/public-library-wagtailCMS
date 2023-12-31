# Generated by Django 3.2.8 on 2023-05-05 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('page', '0008_alter_allpurposepage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirectorpage',
            name='redirect_to_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page'),
        ),
        migrations.AlterField(
            model_name='redirectorpage',
            name='redirect_to',
            field=models.URLField(blank=True, help_text='The URL to redirect to', max_length=2000, null=True),
        ),
    ]
