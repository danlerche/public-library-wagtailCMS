from wagtail import hooks

@hooks.register("insert_editor_js")
def add_custom_admin_js():
    return '<script src="/static/js/honeypot.js"></script>'
