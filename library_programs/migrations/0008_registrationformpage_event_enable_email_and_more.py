# Generated by Django 5.1.3 on 2025-03-27 23:01

import django.core.serializers.json
import django.db.models.deletion
import library_programs.models
import modelcluster.fields
import wagtail.contrib.forms.models
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_programs', '0007_alter_event_featured_on_home_page'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationFormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address')),
                ('from_address', models.EmailField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
            ],
            options={
                'verbose_name': 'Registration Form Builder',
            },
            bases=(wagtail.contrib.forms.models.FormMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.AddField(
            model_name='event',
            name='enable_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='enable_registration',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='registration_form_chooser',
            field=models.ForeignKey(blank=True, help_text='Select a Registration Form that will be embedded on this page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='embedded_registration_form_page', to='wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='event',
            name='spots_available',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='success_email_msg',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Body of the success email'),
        ),
        migrations.AddField(
            model_name='event',
            name='success_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registration_success', to='wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='event',
            name='wait_list_spots',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='waitlist_email_msg',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Body of the waitlist email'),
        ),
        migrations.CreateModel(
            name='RegistrationFormField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('clean_name', models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.TextField(blank=True, help_text='Default value. Comma or new line separated values supported for checkboxes.', verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('label', models.CharField(help_text='The label of the form field, cannot be one of the following: Your Name, Email.', max_length=255, validators=[library_programs.models.validate_label], verbose_name='label')),
                ('form_builder_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='library_programs.registrationformpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationUserFormBuilder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='submit time')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'form submission',
                'verbose_name_plural': 'form submissions',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('wait_list', models.BooleanField(default=0)),
                ('event_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='library_programs.event')),
                ('user_info', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='library_programs.registrationuserformbuilder')),
            ],
            options={
                'verbose_name': 'Registration',
            },
        ),
    ]
