from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.ui.tables import UpdatedAtColumn
from .models import (EventCategory, Event,EventAudience, EventAge, EventAge, FullCalendarLink)
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.filters import WagtailFilterSet

class EventCategoryAdmin(SnippetViewSet):
    model = EventCategory
    menu_label = 'Event Category'
    icon = 'list-ul'
    base_url_path = "category"

class EventAudienceAdmin(SnippetViewSet):
    model = EventAudience
    menu_label = 'Audience'
    icon = 'list-ul'
    list_display = ('audience_name',)
    base_url_path = "audience"

class EventAgeAdmin(SnippetViewSet):
    model = EventAge
    menu_label = 'Age Range'
    icon = 'list-ul'
    base_url_path = "age"

class EventFilterSet(WagtailFilterSet):
    class Meta:
        model = Event
        fields = ['event_category_id', 'age_range', 'event_date']

class EventAdmin(SnippetViewSet):
    model = Event
    menu_label = 'Event'
    icon = 'date'
    list_display = ('title', 'event_date', 'time_from', 'time_to', 'repeats', 'until', 'featured_on_home_page', UpdatedAtColumn())
    #list_filter = {'event_category_id', 'age_range'}
    filterset_class = EventFilterSet
    base_url_path = "event"

class LinkToCalendarAdmin(SnippetViewSet):
    model = FullCalendarLink
    menu_label = 'Link to the full calendar page'
    icon = 'link'
    base_url_path = "calendar_link"

class EventAdminGroup(SnippetViewSetGroup):
    menu_label = 'Programs & Events'
    menu_icon = 'date'
    menu_order = 200
    items = (EventAdmin, EventCategoryAdmin, EventAudienceAdmin, EventAgeAdmin, LinkToCalendarAdmin)

register_snippet(EventAdminGroup)