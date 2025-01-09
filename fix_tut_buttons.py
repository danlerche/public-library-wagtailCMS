from django.db.models import F
from django.db import connection
from online_resource.models import OnlineResourcePage

# Filter rows containing the <button> element
pages_with_button = OnlineResourcePage.objects.filter(tutorial_link__icontains="<button")

# Iterate and update each entry
for page in pages_with_button:
    updated_html = page.tutorial_link.replace(
        '<button', '<button aria-label="View Tutorial button"'
    )
    page.tutorial_link = updated_html
    page.save()
