"""
Module with class to listen to some outlook folder and dump all letters
to the local directory
"""
# Standard library imports
from __future__ import division
import logging
import datetime
from time import sleep

# Third party imports
from char import char
from tqdm import tqdm
try:
    from IPython.display import clear_output
    BOOL_JUPYTER_INSTALLED = True
except ImportError:
    BOOL_JUPYTER_INSTALLED = False

# Local imports
from .class_mail_dumper import MailFolderDumper
from .other import is_outlook_running, start_outlook_app

LOGGER = logging.getLogger("outlook_mail_loader")

@char
def listen_outlook_mail_folder(
        str_outlook_folder_name="inbox",
        str_path_dir_where_to_save="mails",
        int_seconds_step_in_dump=60,
        **kwargs
):
    """Listen to the outlook folder and dump all new mails continuously

    Args:
        str_outlook_folder_name (str, optional): Which outlook folder to listen
        str_path_dir_where_to_save (str, optional): \
            Path to dir. where to save letters.
        int_seconds_step_in_dump (int, optional): \
            Seconds to wait between dumping new letters.
        is_to_mark_messages_as_read (bool, optional): \
            Flag if to mark as read saved letters. Default is False.
        is_to_remove_attachments (bool, optional): \
            Flag if to remove attachments to save disk space. Default is False.
        is_to_preserve_msg_obj (bool, optional): \
            Flag if to preserve outlook .msg object. Default is False.

    """
    list_datetimes_when_letter_saved = []
    mail_loader_obj = MailFolderDumper(
        str_outlook_folder_name, str_path_dir_where_to_save)
    #####
    # Make first dump of the last mails
    int_msgs_saved = mail_loader_obj.dump_new(50, **kwargs)
    list_datetimes_when_letter_saved += \
        [datetime.datetime.now()] * int_msgs_saved
    print_stats_about_dumped_mails(list_datetimes_when_letter_saved)
    #####
    # Create endless cycle of listening
    while True:
        # Wait till next cycle
        for _ in tqdm(range(int_seconds_step_in_dump), leave=False):
            sleep(1)
        #####
        # Check that outlook is running
        if not is_outlook_running():
            start_outlook_app()
            # If new outlook app is open then reinitialize MailDumper obj
            mail_loader_obj = MailFolderDumper(
                str_outlook_folder_name, str_path_dir_where_to_save)
        #####
        int_msgs_saved = mail_loader_obj.dump_new(999, **kwargs)
        list_datetimes_when_letter_saved += \
            [datetime.datetime.now()] * int_msgs_saved
        print_stats_about_dumped_mails(list_datetimes_when_letter_saved)
    LOGGER.info("FINISHED!")


@char
def print_stats_about_dumped_mails(list_datetimes_when_letter_saved):
    """Print statistic about when letters were saved

    Args:
        list_datetimes_when_letter_saved (list): list with datetimes
    """
    if BOOL_JUPYTER_INSTALLED:
        clear_output(wait=True)
    else:
        LOGGER.info("=" * 79)
    LOGGER.info("Print statistic about saved letters:")
    if not list_datetimes_when_letter_saved:
        LOGGER.info("---> Not even 1 new letter has been received yet.")
        return
    #####
    # Get sorted list with number of seconds gone since msg saved
    dt_now = datetime.datetime.now()
    list_seconds_gone_since_saved = [
        int((dt_now - dt_msg_saved.replace(tzinfo=None)).total_seconds())
        for dt_msg_saved in list_datetimes_when_letter_saved]
    list_seconds_gone_since_saved.sort()
    LOGGER.info(
        "---> First letter saved %d seconds ago",
        list_seconds_gone_since_saved[-1])
    LOGGER.info(
        "---> Last letter saved %d seconds ago",
        list_seconds_gone_since_saved[0])
    LOGGER.info(
        "---> Overall letters saved: %d", len(list_seconds_gone_since_saved))
    #####
    # Try to print nice stats
    int_max_index_used = 0
    int_max_index = len(list_seconds_gone_since_saved)
    #####
    # Minutes
    list_minutes = [1, 3, 5, 10, 20, 30, 60]
    for int_minutes_end in list_minutes:
        for int_cur_index in range(int_max_index_used, int_max_index):
            int_cur_elem = list_seconds_gone_since_saved[int_cur_index]
            LOGGER.debug("Process elem: %d", int_cur_elem)
            if int_cur_elem / 60 <= int_minutes_end:
                int_max_index_used = int_cur_index + 1
                LOGGER.debug(
                    "Max used index set to %d / %d",
                    int_max_index_used,
                    int_max_index)
        LOGGER.info(
            "------> Letters saved in the last %d minutes: %d",
            int_minutes_end, int_max_index_used)
        if int_max_index_used == int_max_index:
            return
    #####
    # Hours
    list_hours = [2, 3, 6, 12, 24]
    for int_hours_end in list_hours:
        for int_cur_index in range(int_max_index_used, int_max_index):
            int_cur_elem = list_seconds_gone_since_saved[int_cur_index]
            LOGGER.debug("Process elem: %d", int_cur_elem)
            if int_cur_elem / 3600 <= int_hours_end:
                int_max_index_used = int_cur_index + 1
        LOGGER.info(
            "------> Letters saved in the last %d hours: %d",
            int_hours_end, int_max_index_used)
        if int_max_index_used == int_max_index:
            return
    #####
    # days
    list_days = [2, 3, 4, 5, 6, 7]
    for int_days_end in list_days:
        for int_cur_index in range(int_max_index_used, int_max_index):
            int_cur_elem = list_seconds_gone_since_saved[int_cur_index]
            LOGGER.debug("Process elem: %d", int_cur_elem)
            if int_cur_elem / 3600 / 24 <= int_days_end:
                int_max_index_used = int_cur_index + 1
        LOGGER.info(
            "------> Letters saved in the last %d days: %d",
            int_days_end, int_max_index_used)
        if int_max_index_used == int_max_index:
            return
    #####
    # weeks
    list_weeks = [2, 3, 4]
    for int_weeks_end in list_weeks:
        for int_cur_index in range(int_max_index_used, int_max_index):
            int_cur_elem = list_seconds_gone_since_saved[int_cur_index]
            LOGGER.debug("Process elem: %d", int_cur_elem)
            if int_cur_elem / 3600 / 24 / 7 <= int_weeks_end:
                int_max_index_used = int_cur_index + 1
        LOGGER.info(
            "------> Letters saved in the last %d weeks: %d",
            int_weeks_end, int_max_index_used)
        if int_max_index_used == int_max_index:
            return
    return
