from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import PolicyCategory

class PolicyCategoryAdmin(SnippetViewSet):
    model = PolicyCategory
    menu_label = 'Policy Categories'
    icon = 'doc-full'
    add_to_admin_menu = True
    base_url_path = "policy_categories"


register_snippet(PolicyCategoryAdmin)