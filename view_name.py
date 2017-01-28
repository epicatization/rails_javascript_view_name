import sublime


def create_view_name(self, variables):
    filename = variables['file_base_name'].split('.')[0]
    filename = filename.replace('_', '') if filename[0] == '_' else filename
    path = variables['file_path'].split('views/')[1]
    view_name = [x.title() for x in path.split('/') + [filename]]
    filename = "Views." + '.'.join(view_name)
    return filename.replace('_', '')
