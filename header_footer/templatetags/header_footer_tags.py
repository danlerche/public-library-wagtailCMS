from django import template
from header_footer.models import Logo, Alert, FooterColumn
from header_footer.forms import closeTickerForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse

register = template.Library()

# Logo snippet
@register.inclusion_tag('header_footer/logo.html', takes_context=True)
def logo(context):
    return {
        'logo': Logo.objects.all(),
        'request': context['request'],
    }

# Alert snippet
@register.inclusion_tag('header_footer/alerts.html', takes_context=True)
def popup_alert(context):
    request = context['request']
    close_ticker_form = closeTickerForm()
    ticker = False
    response_data = {}

    if request.method == 'POST':
        close_ticker_form = closeTickerForm(request.POST)
        if close_ticker_form.is_valid():
            ticker = close_ticker_form.cleaned_data['ticker']
            request.session['ticker'] = ticker
            response_data['ticker'] = ticker
            return JsonResponse(response_data)
        else:
            close_ticker_form = closeTickerForm()

    if request.session.has_key('ticker'):
        close_ticker = True
    else:
        close_ticker = False

    return {
        'close_ticker_form': close_ticker_form,
        'alert': Alert.objects.all().order_by('-alert_date'),
        'close_ticker': close_ticker,
        'request':  request,
    }
# Footer Column snippet
@register.inclusion_tag('header_footer/footer_columns.html', takes_context=True)
def footer_column(context):
    request = context['request']
    footer_column = FooterColumn.objects.all()
    return {
        'request': request,
        'footer_column': footer_column,
    }
