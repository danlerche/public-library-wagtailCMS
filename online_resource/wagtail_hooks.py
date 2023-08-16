from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


from .models import OnlineResourceCategory

class OnlineResourceCategoryAdmin(SnippetViewSet):
    model = OnlineResourceCategory
    menu_label = 'Resource Categories' 
    icon = 'tasks' 
    base_url_path = "online_resource"
    add_to_admin_menu = True


register_snippet(OnlineResourceCategoryAdmin)
