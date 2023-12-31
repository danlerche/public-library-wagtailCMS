# Generated by Django 3.2.8 on 2023-02-17 18:42

import datetime
from django.db import migrations, models
import django.db.models.deletion
import header_footer.models
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('enable_alert', models.BooleanField(default=False)),
                ('alert_date', models.DateTimeField(default=datetime.datetime.now)),
                ('alert_text', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('footer_col', wagtail.fields.StreamField([('heading', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(form_classname='heading'))], classname='full title')), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('footer_link', wagtail.blocks.StructBlock([('page_link', wagtail.blocks.PageChooserBlock())])), ('footer_button', wagtail.blocks.StructBlock([('button_link', wagtail.blocks.PageChooserBlock())])), ('paragraph', wagtail.blocks.RichTextBlock()), ('telephone', wagtail.blocks.StructBlock([('telephone', wagtail.blocks.CharBlock(form_classname='telephone'))])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('email', wagtail.blocks.StructBlock([('email', wagtail.blocks.EmailBlock(form_classname='email'))])), ('branch_info', header_footer.models.BranchInfoBlock()), ('business_hours', header_footer.models.BusinessHourBlock()), ('social_icons', header_footer.models.SocialIconsBlock())], blank=True, use_json_field=True)),
            ],
            options={
                'verbose_name': 'First Footer Column',
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
        ),
    ]
