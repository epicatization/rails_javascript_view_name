import sublime, sublime_plugin, os

class JavaScriptViewNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
      filename = os.path.dirname(self.view.file_name())
      if 'views' in filename:
        path = filename.split('views/')[1]
        create_views = [x.title() for x in path.split('/')]
        filename = "Views." + '.'.join(create_views)
        filename = filename.replace('_','')
      sublime.set_clipboard(filename)
      sublime.status_message("Copied file name: %s" % filename)



