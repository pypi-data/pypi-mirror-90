"""working_directory context manager."""

import os
from ._compatibility import contextlib


class working_directory(contextlib.ContextDecorator):
    """A context manager to temporarily set the working directory
    to a given *path*. If *path* specifies a file, the file's
    directory is used. When exiting the with-block, the working
    directory is automatically changed back to its previous
    location.

    You can use Python's :py:obj:`__file__` constant to load data
    relative to a file's current directory::

        from datatest import working_directory
        import pandas as pd

        with working_directory(__file__):
            my_df = pd.read_csv('myfile.csv')

    This context manager can also be used as a decorator::

        from datatest import working_directory
        import pandas as pd

        @working_directory(__file__)
        def my_df():
            return pd.read_csv('myfile.csv')
    """
    def __init__(self, path):
        if os.path.isfile(path):
            path = os.path.dirname(path)
        self._working_dir = os.path.abspath(path)

    def __enter__(self):
        self._original_dir = os.path.abspath(os.getcwd())
        os.chdir(self._working_dir)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self._original_dir)
