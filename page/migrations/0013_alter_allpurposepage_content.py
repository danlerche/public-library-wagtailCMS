# Generated by Django 4.2.1 on 2023-09-01 17:05

from django.db import migrations
import page.models
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0012_alter_allpurposepage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allpurposepage',
            name='content',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image_link', wagtail.blocks.StructBlock([('image_link_url', wagtail.blocks.URLBlock(help_text='The Link to redirect to')), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='The image the user will see'))], icon='openquote', template='page/blocks/image_link.html')), ('half_size_image', wagtail.images.blocks.ImageChooserBlock(help_text='Takes up 1/2 of the screen size 648px')), ('full_width_image', wagtail.images.blocks.ImageChooserBlock(help_text='Takes up the full screen view 1248px')), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='uses the original picture size and respects that with')), ('card', wagtail.blocks.StructBlock([('card_body', wagtail.blocks.StreamBlock([('card_item', wagtail.blocks.StructBlock([('card_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('card_page', wagtail.blocks.PageChooserBlock(required=False)), ('card_external_url', wagtail.blocks.URLBlock(help_text="use this if you're directing to an extenal page", required=False)), ('card_alt_title', wagtail.blocks.CharBlock(help_text="use the alt title for external URLs or override the name of the page it's linking to", required=False)), ('card_description', wagtail.blocks.CharBlock(help_text='This is optional, but better to be consisiten with each of your cards', required=False))], icon='placeholder', template='page/blocks/card_item.html'))]))], icon='image', template='page/blocks/card.html')), ('image_carousel', wagtail.blocks.ChoiceBlock(choices=page.models.get_collection, help_text='Select an image collection to show as a slideshow', icon='image', required=False)), ('QuoteBlock', wagtail.blocks.StructBlock([('quote', wagtail.blocks.BlockQuoteBlock(help_text="Enter the text you'd like to appear in quotation marks", required=True)), ('attribution', wagtail.blocks.CharBlock(help_text='attribute the quote to someone', required=False))], icon='openquote', template='page/blocks/block_quote.html')), ('text_only_table', wagtail.contrib.table_block.blocks.TableBlock()), ('richtext_table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())])), ('URLBlock', wagtail.blocks.URLBlock()), ('EmailBlock', wagtail.blocks.EmailBlock()), ('all_upcoming_events', wagtail.blocks.BooleanBlock(help_text='If checked a list of upcoming events will display', icon='tasks', required=False)), ('events_calendar', wagtail.blocks.BooleanBlock(help_text='If checked an event calendar will display', icon='tasks', required=False)), ('events_by_category', wagtail.blocks.MultipleChoiceBlock(choices=page.models.get_categories, help_text='If checked all upcoming programs filtered by a category will display', icon='tasks', required=False)), ('events_by_audience', wagtail.blocks.MultipleChoiceBlock(choices=page.models.get_audiences, help_text='If checked all upcoming programs filtered by a audiences will display', icon='tasks', required=False)), ('DateBlock', wagtail.blocks.DateBlock()), ('TimeBlock', wagtail.blocks.TimeBlock()), ('DateTimeBlock', wagtail.blocks.DateBlock()), ('PageChooserBlock', wagtail.blocks.PageChooserBlock()), ('DocumentChooserBlock', wagtail.documents.blocks.DocumentChooserBlock()), ('IframeBlock', wagtail.blocks.RawHTMLBlock(help_text='See https://search.pentictonlibrary.ca/Admin/CollectionSpotlights for info about using the iframe tag to embed Aspen Collection Spotlights.')), ('PhoneNumberBlock', wagtail.blocks.TextBlock()), ('EmbedBlock', wagtail.embeds.blocks.EmbedBlock()), ('google_map', wagtail.blocks.StructBlock([('latitude', wagtail.blocks.FloatBlock(label='Latitude', required=True)), ('longitude', wagtail.blocks.FloatBlock(label='Longitude', required=True)), ('zoom', wagtail.blocks.IntegerBlock(default=15, label='Zoom Level'))])), ('show_business_hours', wagtail.blocks.BooleanBlock(help_text='If checked, the library hours will display on the page', icon='user', required=False)), ('show_next_closure', wagtail.blocks.BooleanBlock(help_text='If checked, the next library closure will display', icon='user', required=False)), ('show_all_closures', wagtail.blocks.BooleanBlock(help_text='If checked, all upcoming library closures will be shown', icon='user', required=False)), ('bookClub', wagtail.blocks.StructBlock([('book_club_name', wagtail.blocks.CharBlock()), ('book_club_day_of_the_week', wagtail.blocks.TextBlock()), ('book_club_PDF', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('book_club_time', wagtail.blocks.TimeBlock()), ('books', wagtail.blocks.StreamBlock([('book', wagtail.blocks.StructBlock([('book_name', wagtail.blocks.CharBlock()), ('author_name', wagtail.blocks.CharBlock()), ('reading_date', wagtail.blocks.DateBlock()), ('book_description', wagtail.blocks.RichTextBlock()), ('book_cover', wagtail.images.blocks.ImageChooserBlock(required=False))], template='page/blocks/books.html'))]))], icon='openquote', template='page/blocks/book_club.html')), ('columnBlock', wagtail.blocks.StructBlock([('column', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('quote_block', wagtail.blocks.StructBlock([('quote', wagtail.blocks.BlockQuoteBlock(help_text="Enter the text you'd like to appear in quotation marks", required=True)), ('attribution', wagtail.blocks.CharBlock(help_text='attribute the quote to someone', required=False))], icon='openquote', template='page/blocks/block_quote.html'))]))], icon='table', template='page/blocks/column.html')), ('ebooks_card', wagtail.blocks.StructBlock([('ebooks_body', wagtail.blocks.StreamBlock([('ebook', wagtail.blocks.StructBlock([('ebook_title', wagtail.blocks.CharBlock(required=True)), ('ebook_url', wagtail.blocks.URLBlock()), ('ebook_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('ebook_description', wagtail.blocks.RichTextBlock(help_text="OPTIONAL, only use this if you'd like to override the name of the page you are linking to", required=False)), ('tutorial_link', wagtail.blocks.CharBlock(help_text='use the short codes from Niche academy', required=False)), ('app_link', wagtail.blocks.StreamBlock([('app_links', wagtail.blocks.StructBlock([('bootstrap_app_icon', wagtail.blocks.CharBlock(help_text='See https://icons.getbootstrap.com for icon codes', required=False)), ('app_link', wagtail.blocks.URLBlock(help_text='url to the app store link', required=False)), ('app_icon_description', wagtail.blocks.CharBlock(help_text='a short description of the app you are linking to', required=True))], icon='site', template='page/blocks/app_link.html'))], required=False))], icon='openquote', template='page/blocks/ebook.html'))]))], icon='image', template='page/blocks/ebooks_card.html')), ('side_menu', wagtail.blocks.StructBlock([('side_menu_title', wagtail.blocks.CharBlock()), ('side_menu_body', wagtail.blocks.StreamBlock([('side_menu_item', wagtail.blocks.StructBlock([('page_link', wagtail.blocks.PageChooserBlock(required=False)), ('pdf_document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('external_url', wagtail.blocks.URLBlock(required=False)), ('external_url_link_title', wagtail.blocks.CharBlock(required=False))], icon='openquote', template='page/blocks/side_menu_item.html'))]))], icon='collapse-down', template='page/blocks/side_menu.html')), ('accordion', wagtail.blocks.StructBlock([('accordion_name', wagtail.blocks.CharBlock()), ('only_one_open', wagtail.blocks.BooleanBlock(default=True, help_text='Automatically close all other accordions while another is open', required=False)), ('accordion_body', wagtail.blocks.StreamBlock([('accordion_items', wagtail.blocks.StructBlock([('accordion_item_title', wagtail.blocks.CharBlock()), ('accordion_description', wagtail.blocks.RichTextBlock()), ('show_by_default', wagtail.blocks.BooleanBlock(help_text='Display accordion as open by default', required=False))]))]))], icon='collapse-down', template='page/blocks/accordion.html'))], blank=True, use_json_field=True),
        ),
    ]
