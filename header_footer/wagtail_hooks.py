from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import (
    Logo, Alert, FooterColumn)

class LogoAdmin(SnippetViewSet):
    model = Logo
    menu_label = 'Logo'
    icon = 'image'
    base_url_path = "logo"

class AlertAdmin(SnippetViewSet):
    model = Alert
    menu_label = 'Alert'
    icon = 'pick'
    list_display = ('enable_alert', 'alert_text')
    base_url_path = "alert"

class FooterColumnAdmin(SnippetViewSet):
    model = FooterColumn
    menu_label = 'Footer Column'
    icon = 'doc-full-inverse'
    list_display = ('footer_col_heading', 'order', 'footer_col')
    base_url_path = "footercolumn"

class HeaderFooterGroup(SnippetViewSetGroup):
    menu_label = 'Header & Footer'
    menu_icon = 'edit'
    menu_order = 200
    items = (LogoAdmin, AlertAdmin, FooterColumnAdmin)

register_snippet(HeaderFooterGroup)
