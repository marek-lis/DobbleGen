import os


def __fix_path(path):
    result = path.replace('\\', '/')
    if result.endswith('/'):
        return result[:-1]
    return result


def __scan_dir_for_files(result, path):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                result.append(path+'/'+entry.name)
    return result


def __scan_tree_for_files(result, path):
    with os.scandir(path) as entries:
        for entry in entries:
            if not entry.is_file():
                __scan_tree_for_files(result, path+'/'+entry.name)
            else:
                result.append(path+'/'+entry.name)
    return result


def get_file(path):
    return __fix_path(path).split('/')[-1:][0]

def get_file_name(path):
    return get_file(path).split('.')[0]

def get_file_extension(path):
    return get_file(path).split('.')[1]

def get_relative_path(path, relative_to):
    return __fix_path(path).split(__fix_path(relative_to))[-1:][0]


def scan_dir_for_files(path):
    result = []
    return __scan_dir_for_files(result, __fix_path(path))


def scan_tree_for_files(path):
    result = []
    return __scan_tree_for_files(result, __fix_path(path))
