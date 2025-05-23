# Generated by Django 5.1.3 on 2025-03-27 23:01

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_news', '0006_alter_newsitem_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='content',
            field=wagtail.fields.StreamField([('quote_block', 2), ('paragraph', 3), ('IframeBlock', 4)], blank=True, block_lookup={0: ('wagtail.blocks.BlockQuoteBlock', (), {'help_text': "Enter the text you'd like to appear in quotation marks", 'required': True}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'attribute the quote to someone', 'required': False}), 2: ('wagtail.blocks.StructBlock', [[('quote', 0), ('attribution', 1)]], {'icon': 'openquote'}), 3: ('wagtail.blocks.RichTextBlock', (), {}), 4: ('wagtail.blocks.RawHTMLBlock', (), {'help_text': 'See https://search.pentictonlibrary.ca/Admin/CollectionSpotlights for info about using the iframe tag to embed Aspen Collection Spotlights.'})}),
        ),
    ]
