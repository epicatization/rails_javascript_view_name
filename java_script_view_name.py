import sublime, sublime_plugin
import re, inspect, os, glob

class JavaScriptViewNameCommand(sublime_plugin.WindowCommand):
    def run(self):
      # /app/views/admin/items/form.html.haml
      # Views.Admin.Items.Form
      variables = self.window.extract_variables()
      if not '/views' in variables['file']:
        return False
      filename = create_view_name(self)
      sublime.set_clipboard(filename)
      sublime.status_message("Copied file name: %s" % filename)

class OpenJavaScriptViewCommand(sublime_plugin.WindowCommand):
  def run(self):
    variables = self.window.extract_variables()
    print(self.window.extract_variables())
    if not '/views' in variables['file']:
      return False
    # base_file_path: /Users/epic/apps/nau/app/views/crm/reports/index.haml

    # get js views folder path, variables[folder] is project root
    # result: /Users/epic/apps/nau/app/assets/javascripts/views
    js_views_root_path = variables['folder'] + '/app/assets/javascripts/views/'

    # get path of folders from project root to current file
    # result: /Users/epic/apps/nau/app/assets/javascripts/views/static_pages/clearing/imports_and_clearing
    path_to_js_view_folder = js_views_root_path + variables['file_path'].split('views')[1]

    # get current filename without extensions _partial.html.haml
    # result: partial
    filename = variables['file_base_name'].split('.')[0]
    if filename[0] == '_':
      filename = filename.replace('_', '', 1)

    # find or create filename
    files = glob.glob(os.path.join(path_to_js_view_folder, filename + '.*'))
    if len(files) > 0:
      # if we find any file with given filename
      self.window.open_file(files[0])
      return True
    if filename == 'form':
      # if filename if form, it is possible that there is view of new or edit action
      files = glob.glob(os.path.join(path_to_js_view_folder, 'new' + '.*'))
      if len(files) > 0:
        self.window.open_file(files[0])
        return True
      files = glob.glob(os.path.join(path_to_js_view_folder, 'edit' + '.*'))
      if len(files) > 0:
        self.window.open_file(files[0])
        return True
    # if we reach this point of code, it means that file does not exist
    # create dirs if not exists
    os.makedirs(path_to_js_view_folder, exist_ok=True)
    # create path to new file
    file_path = os.path.join(path_to_js_view_folder, filename + '.coffee')
    with open(file_path, "w") as f:
      f.write('prepare ' + '\'' + create_view_name(self) +'\'\n\n')
      f.write('class ' + create_view_name(self) + ' extends Views.ApplicationView\n\n')
      f.write('  render: ->\n')
      f.write('    super()\n\n')
      f.write('  cleanup: ->\n')
      f.write('    super()\n')
      f.close()
      self.window.open_file(file_path)

def create_view_name(self):
  filename = self.window.active_view().file_name().split('.')[0]
  path = filename.split('views/')[1]
  create_views = [x.title() for x in path.split('/')]
  filename = "Views." + '.'.join(create_views)
  return filename.replace('_','')
