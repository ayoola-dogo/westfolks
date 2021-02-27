import os
from contextlib import contextmanager


# # creating a change directory context manager
# class ChangeDir:
#
#     def __init__(self, destination):
#         self.destination = destination
#         self.cwd = os.getcwd()
#
#     def __enter__(self):
#         os.chdir(self.destination)
#
#     def __exit__(self):
#         os.chdir(self.cwd)

# using a function to define my contextmanager as the class __init__method might be clashing with that of MyHandler

@contextmanager
def change_dir(destination):
    cwd = os.getcwd()
    try:
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)
