"""Module with recursive functions for outlook handler objects"""
# Standard library imports
import logging

# Third party imports
from char import char

# Local imports

LOGGER = logging.getLogger("outlook_mail_loader")

@char
def look_for_asked_mail_folders(
        parent_outlook_handler,
        str_folder_name_to_get,
):
    """Get outlook handler object for folder with asked name

    Args:
        parent_outlook_handler (outlook folder obj): Folder where to search for
        str_folder_name_to_get (str): Folder name which handler to get

    Returns:
        (outlook folder obj): outlook handler object for given folder
    """
    str_folder_name = parent_outlook_handler.Name
    if str_folder_name == str_folder_name_to_get:
        return parent_outlook_handler, str_folder_name

    for child_outlook_handler in parent_outlook_handler.Folders:
        res, str_folder_path = look_for_asked_mail_folders(
            child_outlook_handler,
            str_folder_name_to_get,
        )
        if res is not None:
            return res, str_folder_name + " / " + str_folder_path
    return None, ""


@char
def print_hierarchy(parent_outlook_handler, int_depth_level=1):
    """Print hierarchy of the folder starting from given outlook folder obj.

    Args:
        parent_outlook_handler (outlook folder obj): Folder where to search for
        int_depth_level (int, optional): Depth to print
    """
    str_line = "--" * int_depth_level + "> %s"
    LOGGER.info(str_line, parent_outlook_handler.Name)
    for child_outlook_handler in parent_outlook_handler.Folders:
        print_hierarchy(
            child_outlook_handler, int_depth_level=int_depth_level+1)

def get_list_names_of_all_outlook_folders(parent_outlook_handler):
    """Get list names of all outlook folders starting from the asked one"""
    list_names_of_all_outlook_folders = []
    list_names_of_all_outlook_folders.append(parent_outlook_handler.Name)
    for child_outlook_handler in parent_outlook_handler.Folders:
        list_names_of_all_outlook_folders += \
            get_list_names_of_all_outlook_folders(child_outlook_handler)
    return list_names_of_all_outlook_folders
