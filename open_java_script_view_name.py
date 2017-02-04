import sublime, sublime_plugin
import os, glob, functools
from .path_helpers import application_view_path
from .view_name import create_view_name


class OpenJavaScriptViewCommand(sublime_plugin.TextCommand):

    def run(self, view):
        self.variables = sublime.active_window().extract_variables()
        if '/views' not in self.variables['file']:
            return False
        # get absolute path to folder with java script views
        js_views_root_path = os.path.join(application_view_path(self) + '/views')

        # get absolute path to java_script view folder that file is expected to be stored in
        # result: /Users/epic/apps/nau/app/assets/javascripts/views/static_pages/clearing/imports_and_clearing
        self.path_to_js_view_folder = os.path.join(js_views_root_path + self.variables['file_path'].split('views')[1])

        # get current filename without extensions _partial.html.haml
        # result: partial
        filename = self.variables['file_base_name'].split('.')[0]
        self.filename = filename.replace('_', '') if filename[0] == '_' else filename
        # find or create filename
        files = glob.glob(os.path.join(self.path_to_js_view_folder, '*'))
        sublime.active_window().show_quick_panel(
            self._quick_panel_collection(files, js_views_root_path),
            functools.partial(self._on_selected_path, files),
            sublime.KEEP_OPEN_ON_FOCUS_LOST,
            self._pre_selected_file(files),
            functools.partial(self._highlighted_file, files),
        )

    def _quick_panel_collection(self, files, js_views_root_path):
        return [file.replace(js_views_root_path + '/', '') for file in files] + ['Create new view']

    def _on_selected_path(self, files, index):
        files_count = len(files)
        if index == -1:
            sublime.active_window().open_file(self.variables['file'])
        elif index == files_count:
            self.create_view_file()
        elif index <= files_count:
            sublime.active_window().open_file(files[index])

    def _highlighted_file(self, files, index):
        files_count = len(files)
        if index == files_count:
            sublime.active_window().open_file(self.variables['file'])
        else:
            sublime.active_window().open_file(files[index], sublime.TRANSIENT)

    def _pre_selected_file(self, files):
        file = os.path.isfile(os.path.join(self.path_to_js_view_folder, self.filename + '.coffee'))
        if file:
            return files.index(os.path.join(self.path_to_js_view_folder, self.filename + '.coffee'))
        else:
            return 0

    def create_view_file(self):
        file_path = os.path.join(self.path_to_js_view_folder, self.filename + '.coffee')

        sublime.active_window().show_input_panel(
            "Create new view:",
            file_path,
            self.on_done_input_panel, None, None
        )

    def on_done_input_panel(self, file_path):
        if os.path.isfile(file_path):
            return sublime.active_window().open_file(file_path)
        os.makedirs(self.path_to_js_view_folder, exist_ok=True)
        # create path to new file
        with open(file_path, "w") as f:
            f.write('prepare ' + '\'' + create_view_name(self, self.variables) + '\'\n\n')
            f.write('class ' + create_view_name(self, self.variables) + ' extends Views.ApplicationView\n\n')
            f.write('  render: ->\n')
            f.write('    super()\n\n')
            f.write('  cleanup: ->\n')
            f.write('    super()\n')
            f.close()
            sublime.active_window().open_file(file_path)
