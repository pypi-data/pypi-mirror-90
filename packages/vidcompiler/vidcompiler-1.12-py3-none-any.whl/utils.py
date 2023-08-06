from os import listdir
from os.path import isfile, join


def files_in_folder(folder_path):
    return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]
