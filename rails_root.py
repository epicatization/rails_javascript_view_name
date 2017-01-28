import os


def rails_root(self):
    directory = get_working_dir(self)
    while directory:
        if os.path.exists(os.path.join(directory, 'Rakefile')):
            return directory
        parent = os.path.realpath(os.path.join(directory, os.path.pardir))
        if parent == directory:
            # /.. == /
            return False
        directory = parent
    return False


def get_working_dir(self):
    file_name = _active_file_name(self)
    if file_name:
        return os.path.dirname(file_name)
    else:
        return self.window.folders()[0]


def _active_file_name(self):
    view = self.view
    if view and view.file_name() and len(view.file_name()) > 0:
        return view.file_name()
