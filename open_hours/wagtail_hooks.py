from wagtail.snippets.models import register_snippet
from wagtail.admin.filters import WagtailFilterSet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.ui.tables import UpdatedAtColumn
from .models import (BranchInfo, OpenHour, ClosedDate, EnableMessageDisplay, SocialMedia)
from wagtail.admin.panels import TabbedInterface, ObjectList

class EnableMessageDisplayAdmin(SnippetViewSet):
    model = EnableMessageDisplay
    menu_label = 'Enable Messages'
    icon = 'circle-check'
    list_display = ['enable_message_display',]
    base_url_path = "enable"

class SocialMediaAdmin(SnippetViewSet):
    model = SocialMedia
    menu_label = 'Social Media Links'
    icon = 'group'
    list_display = ('social_media_name', 'social_media_link', 'social_media_icon')

class BranchInfoAdmin(SnippetViewSet):
    model = BranchInfo
    menu_label = 'Branch Info'
    icon = 'home'

class OpenHoursAdmin(SnippetViewSet):
    model = OpenHour
    icon = 'time'   
    list_display = ["weekday", "time_from" , "time_to","open_or_closed", "branch_info"]
    inspect_view_enabled = True
    base_url_path = "open/days"

class ClosedDatesAdmin(SnippetViewSet):
    model = ClosedDate
    menu_label = 'Exception Dates'
    icon = 'calendar'
    list_display = ['closed_date_name', 'closed_date_from', 'closed_date_to', 'all_day', 'time_from', 'time_to', 'branch_info']

class OpenHoursGroup(SnippetViewSetGroup):
      menu_label = 'Open Hours'
      menu_icon = 'edit'
      menu_order = 225
      items = (EnableMessageDisplayAdmin, BranchInfoAdmin, SocialMediaAdmin, OpenHoursAdmin, ClosedDatesAdmin)

register_snippet(OpenHoursGroup)
