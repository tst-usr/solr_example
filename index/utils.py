#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

"""Utils

Makes common path path and text find tasks


This file can also be imported as a module and contains the following
functions:

    * get_all_files -   Retrieve all files in a folder
    * make_path     -   Makes a destination folder if non existent
"""

import sys

import errno
import os
import threading
from pdb import set_trace as bp


__lock = threading.Lock()


def get_all_files(path, seek_extension="txt"):
    """
    Retrieve all files in a folder on format
        path, relative path (from path), file name

    Parameters
    ----------
    path : str
        Path to find all files

    seek_extension : str
        Extension of file needed

    """
    paths = []

    for f in [name for name in os.listdir(path)]:
        temp_path = os.path.join(path, f)
        rel_path = os.path.relpath(temp_path, path)

        if os.path.isdir(os.path.join(path, f)):
            temps = get_all_files(os.path.join(path, f),
                                  seek_extension=seek_extension)
            paths += temps
        elif f.lower().endswith(seek_extension):
            paths += [{"path": path,
                       "rel_path": rel_path,
                       "title": f}]

    return paths


def make_path(dest_path):
    """
    Makes a destination folder if non existent

    Parameters
    ----------
    dest_path : str
        path to be created

    """

    dest_path = dest_path if dest_path.endswith("/") else dest_path + "/"

    if not os.path.exists(dest_path):
        try:
            with __lock:
                os.makedirs(os.path.dirname(dest_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def write_file(filename, message, mode="w"):
    """
    Writes a file

    Parameters
    ----------
    filename : str
        filename with path
    message : str
        message to write
    mode: str
        writing mode w: write, a: append

    """

    with __lock:
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, mode) as temp:
            temp.write(message)
