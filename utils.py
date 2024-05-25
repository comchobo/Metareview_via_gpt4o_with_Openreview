import os


def make_path(target_path):
    try:
        os.mkdir(target_path)
    except FileExistsError:
        pass
