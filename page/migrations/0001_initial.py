# Generated by Django 3.2.8 on 2023-02-17 18:42

from django.db import migrations, models
import django.db.models.deletion
import page.models
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailgeowidget.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
    ]

    operations = [
        migrations.CreateModel(
            name='groupPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PolicyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_category', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Policy categories',
            },
        ),
        migrations.CreateModel(
            name='PolicyIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('additional_text', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RedirectorPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('redirect_to', models.URLField(help_text='The URL to redirect to')),
            ],
            options={
                'verbose_name': 'Redirector',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AllPurposePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image_link', wagtail.blocks.StructBlock([('image_link_url', wagtail.blocks.URLBlock(help_text='The Link to redirect to')), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='The image the user will see'))], icon='openquote', template='page/blocks/image_link.html')), ('half_size_image', wagtail.images.blocks.ImageChooserBlock(help_text='Takes up 1/2 of the screen size 648px')), ('full_width_image', wagtail.images.blocks.ImageChooserBlock(help_text='Takes up the full screen view 1248px')), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='uses the original picture size and respects that with')), ('BlockQuoteBlock', wagtail.blocks.BlockQuoteBlock(template='page/blocks/block_quote.html')), ('text_only_table', wagtail.contrib.table_block.blocks.TableBlock()), ('richtext_table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())])), ('URLBlock', wagtail.blocks.URLBlock()), ('EmailBlock', wagtail.blocks.EmailBlock()), ('all_upcoming_events', wagtail.blocks.BooleanBlock(help_text='If checked a list of upcoming events will display', icon='tasks', required=False)), ('events_calendar', wagtail.blocks.BooleanBlock(help_text='If checked an event calendar will display', icon='tasks', required=False)), ('events_by_category', wagtail.blocks.MultipleChoiceBlock(choices=page.models.get_categories, help_text='If checked all upcoming programs filtered by a category will display', icon='tasks', required=False)), ('events_by_audience', wagtail.blocks.MultipleChoiceBlock(choices=page.models.get_audiences, help_text='If checked all upcoming programs filtered by a audiences will display', icon='tasks', required=False)), ('DateBlock', wagtail.blocks.DateBlock()), ('TimeBlock', wagtail.blocks.TimeBlock()), ('DateTimeBlock', wagtail.blocks.DateBlock()), ('PageChooserBlock', wagtail.blocks.PageChooserBlock()), ('DocumentChooserBlock', wagtail.documents.blocks.DocumentChooserBlock()), ('IframeBlock', wagtail.blocks.RawHTMLBlock(help_text='See https://search.pentictonlibrary.ca/Admin/CollectionSpotlights for info about using the iframe tag to embed Aspen Collection Spotlights.')), ('PhoneNumberBlock', wagtail.blocks.TextBlock()), ('EmbedBlock', wagtail.embeds.blocks.EmbedBlock()), ('ppl_map', wagtail.blocks.BooleanBlock(help_text='If checked, a Google map will appear', icon='user', reqonline_resourceuired=False)), ('map', wagtail.blocks.StructBlock([('address', wagtailgeowidget.blocks.GeoAddressBlock(required=True)), ('map', wagtailgeowidget.blocks.GeoBlock(address_field='address'))], icon='user', template='page/blocks/map.html')), ('show_business_hours', wagtail.blocks.BooleanBlock(help_text='If checked, the library hours will display on the page', icon='user', required=False)), ('show_next_closure', wagtail.blocks.BooleanBlock(help_text='If checked, the next library closure will display', icon='user', required=False)), ('show_all_closures', wagtail.blocks.BooleanBlock(help_text='If checked, all upcoming library closures will be shown', icon='user', required=False)), ('bookClub', wagtail.blocks.StructBlock([('book_club_name', wagtail.blocks.CharBlock()), ('book_club_day_of_the_week', wagtail.blocks.TextBlock()), ('book_club_PDF', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('book_club_time', wagtail.blocks.TimeBlock()), ('books', wagtail.blocks.StreamBlock([('book', wagtail.blocks.StructBlock([('book_name', wagtail.blocks.CharBlock()), ('author_name', wagtail.blocks.CharBlock()), ('reading_date', wagtail.blocks.DateBlock()), ('book_description', wagtail.blocks.RichTextBlock()), ('book_cover', wagtail.images.blocks.ImageChooserBlock(required=False))], template='page/blocks/books.html'))]))], icon='openquote', template='page/blocks/book_club.html')), ('columnBlock', wagtail.blocks.StructBlock([('column', wagtail.blocks.StreamBlock([('richtext', wagtail.blocks.RichTextBlock()), ('block_quote', wagtail.blocks.BlockQuoteBlock(template='page/blocks/block_quote.html')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False))]))], icon='table', template='page/blocks/column.html')), ('ebooks_card', wagtail.blocks.StructBlock([('ebooks_body', wagtail.blocks.StreamBlock([('ebook', wagtail.blocks.StructBlock([('ebook_title', wagtail.blocks.CharBlock(required=True)), ('ebook_url', wagtail.blocks.URLBlock()), ('ebook_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('ebook_description', wagtail.blocks.RichTextBlock(help_text="OPTIONAL, only use this if you'd like to override the name of the page you are linking to", required=False)), ('app_link', wagtail.blocks.StreamBlock([('app_links', wagtail.blocks.StructBlock([('bootstrap_app_icon', wagtail.blocks.CharBlock(help_text='See https://icons.getbootstrap.com for icon codes', required=False)), ('app_link', wagtail.blocks.URLBlock(help_text='url to the app store link', required=False))], icon='site', template='page/blocks/app_link.html'))], required=False))], icon='openquote', template='page/blocks/ebook.html'))]))], icon='image', template='page/blocks/ebooks_card.html')), ('side_menu', wagtail.blocks.StructBlock([('side_menu_title', wagtail.blocks.CharBlock()), ('side_menu_body', wagtail.blocks.StreamBlock([('side_menu_item', wagtail.blocks.StructBlock([('page_link', wagtail.blocks.PageChooserBlock(required=False)), ('pdf_document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('external_url', wagtail.blocks.URLBlock(required=False)), ('external_url_link_title', wagtail.blocks.CharBlock(required=False))], icon='openquote', template='page/blocks/side_menu_item.html'))]))], icon='collapse-down', template='page/blocks/side_menu.html')), ('accordion', wagtail.blocks.StructBlock([('accordion_name', wagtail.blocks.CharBlock()), ('only_one_open', wagtail.blocks.BooleanBlock(default=True, help_text='Automatically close all other accordions while another is open', required=False)), ('accordion_body', wagtail.blocks.StreamBlock([('accordion_items', wagtail.blocks.StructBlock([('accordion_item_title', wagtail.blocks.CharBlock()), ('accordion_description', wagtail.blocks.RichTextBlock()), ('show_by_default', wagtail.blocks.BooleanBlock(help_text='Display accordion as open by default', required=False))]))]))], icon='collapse-down', template='page/blocks/accordion.html'))], blank=True, use_json_field=True)),
                ('policy_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pol_cat', to='page.policycategory')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]