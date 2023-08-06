from os import path


def __is_path_exist(__path):
    return path.exists(__path)


def __is_dir(__path):
    return path.isdir(__path)


def __is_file(__path):
    return path.isfile(__path)
