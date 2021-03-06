import sublime, sublime_plugin
from .view_name import create_view_name


class CopyJavaScriptViewNameCommand(sublime_plugin.TextCommand):

    def run(self, view):
        # /app/views/admin/items/form.html.haml
        # Views.Admin.Items.Form
        variables = sublime.active_window().extract_variables()
        if '/views' not in variables['file']:
            return False
        filename = create_view_name(self, variables)
        sublime.set_clipboard(filename)
        sublime.status_message("Copied file name: %s" % filename)
