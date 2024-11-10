"""
Module including functions for file manipulation. Assists with retrieval
of filehandles and verification of file existence
"""

import os
from modules import config


def get_filehandle(file=None, mode=None):
    """
    filehandle : get_filehandle(infile, "r")
    Takes : 2 arguments file name and mode i.e. what is needed to be done with
    this file. This function opens the file based on the mode passed in
    the argument and returns filehandle.
    @param file: The file to open for the mode
    @param mode: They way to open the file, e.g. reading, writing, etc
    @return: filehandle
    """

    try:
        fobj = open(file, mode)
        return fobj
    except OSError:
        config.get_error_string_4_opening_file_os_error(file=file, mode=mode)
        raise
    except ValueError:
        # test something like
        # io_utils.get_filehandle("does_not_exist.txt", "rrr")
        config.get_error_string_4_value_error()
        raise
    except TypeError:  # test something like io_utils.get_filehandle([], "r")
        config.get_error_string_4_type_error()
        raise