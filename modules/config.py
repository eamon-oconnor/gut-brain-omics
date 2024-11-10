"""
Module including functions for file path retrieval and error string generation.
Directory and ending of data files are set as
global variables.
"""


_DIRECTORY_FOR_GENERA = "./data"
_FILE_ENDING_FOR_GENERA = "genera"


def get_directory_for_genera():
    """
    _DIRECTORY_FOR_GENERA : get_directory_for_genera()
    Takes : 0 arguments. Returns data directory set in global variable.
    @return: _DIRECTORY_FOR_GENERA
    """
    return _DIRECTORY_FOR_GENERA


def get_extension_for_genera():
    """
    _FILE_ENDING_FOR_GENERA : get_extension_for_genera()
    Takes : 0 arguments. Returns file extension set in global variable.
    @return: _FILE_ENDING_FOR_GENERA
    """
    return _FILE_ENDING_FOR_GENERA


def get_error_string_4_opening_file_os_error(file: str, mode: str) -> None:
    """
    Print the invalid argument message for OSError
    @param file: The fh_in name
    @param mode: The mode to open the fh_in
    """
    print(f"Could not open the fh_in (os error): {file} with mode {mode}")


def get_error_string_4_value_error():
    # error when used get_filehandle(fh_in, "1234")
    """
    Print the invalid argument message for ValueError
    """
    print("Invalid argument Value for opening a fh_in for reading/writing")


def get_error_string_4_type_error():
    # error when used get_filehandle(fh_in, "r", "w")
    """
    Print the invalid argument message for TypeError
    """
    print("Invalid argument Type passed in:")
