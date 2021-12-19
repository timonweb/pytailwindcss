import os
import shutil
from contextlib import contextmanager


@contextmanager
def clean_dir(path):
    delete_anything(path)
    try:
        yield
    finally:
        delete_anything(path)


def delete_anything(path):
    path = str(path)
    if not os.path.exists(path):
        return None

    if os.path.isfile(path):
        return os.remove(path)
    return shutil.rmtree(path)
