import os

def get_files_recursively(folders, filters=[]):
    """
    Generator

    List file paths in current folder and all subfolders
    :param folders: <string> Root folder
    :param filters: <list> of <string> filter for file path
    """

    if not isinstance(filters, list):
        filters = [filters]

    if not isinstance(folders, list):
        folders = [folders]

    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                complete_file_path = os.path.join(root, file_name)
                if len(filters):
                    for file_filter in filters:
                        if file_filter in complete_file_path:
                            yield complete_file_path
                else:
                    yield complete_file_path
