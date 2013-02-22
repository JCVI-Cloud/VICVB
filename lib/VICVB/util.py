import os

def abspath(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    return path

def makedir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


