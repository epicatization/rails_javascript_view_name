import os
import sublime


def application_view_path(self):
    variables = sublime.active_window().extract_variables()
    javascript_folder_root = variables['folder'] + '/app/assets/javascripts'
    os.listdir('/Users/epic/apps/arch-doc/app/assets/')
    for subdir, dirs, files in os.walk(javascript_folder_root):
        folders = os.listdir(subdir)
        if 'widgets' and 'views' in folders:
            return subdir
