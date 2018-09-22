import os
import sys
import time
from typing import Dict


def find_modules(context: Dict, path_list=None):
    path_list = set() if path_list is None else path_list
    for k, v in context.copy().items():
        if not hasattr(v, '__module__'):
            continue
        path = sys.modules.get(getattr(v, '__module__')).__file__
        if path in path_list:
            continue
        path_list |= {path}
        if hasattr(v, '__globals__'):
            find_modules(v.__globals__, path_list)
    return list(path_list)


class FileDependencyCheckMixin():
    def complete(self):
        if not hasattr(self, 'file_dependency'):
            return False

        path_list = getattr(self, 'file_dependency')

        def mtime(path):
            return time.gmtime(os.path.getmtime(path))

        out_path = self.output().path
        if not os.path.exists(out_path):
            return False

        ctime = mtime(out_path)

        for path in path_list:
            if mtime(path) > ctime:
                return False

        return True
