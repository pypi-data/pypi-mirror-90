"""
Module with class to process dumped mails
"""
# Standard library imports
import os
import logging
import json

# Third party imports
from char import char
from local_simple_database import LocalSimpleDatabase
from tqdm import trange
import dateutil.parser

# Local imports
from . import mail_listener

LOGGER = logging.getLogger("outlook_mail_loader")


class DumpedMails(object):
    """[summary]

    Attributes:
        self.str_path_dir_with_mails (str): Path to dir with dumped letters
        self.int_last_dumped_id (int): Id of the last dumped letter

    Methods:
        self.get_last_letter(...): Get dictionary with last letter
        self.get_last_n_letters(...): Get list of dicts of last N letters
        self.print_stats_about_dumped_mails(...): \
            Print statistics about dumped letters
        self.clear_dumped_mails(...): Clear from cache dumped mails
    """

    @char
    def __init__(
            self,
            str_path_dir_with_mails="mails",
    ):
        """Init object

        Args:
            str_path_dir_with_mails (str, optional): Dir. from where to load
        """
        if not os.path.exists(str_path_dir_with_mails):
            LOGGER.warning(
                "Folder with mails doesn't exist: %s",
                str_path_dir_with_mails)
        self.str_path_dir_with_mails = str_path_dir_with_mails
        self._local_database = \
            LocalSimpleDatabase(self.str_path_dir_with_mails)
        self._list_loaded_letters = []
        self.int_last_dumped_id = 0

    @char
    def get_last_letter(self):
        """Get dictionary with last letter"""
        self._load_last_letters()
        if self._list_loaded_letters:
            return self._list_loaded_letters[-1]
        return {}

    @char
    def get_last_n_letters(self, int_last_letters_to_get):
        """Get list of dicts of last N letters

        Args:
            int_last_letters_to_get (int): Number of last letters to get

        Returns:
            list: [dict_letter_n, dict_letter_n+1, ..., dict_last_letter]
        """
        self._load_last_letters()
        if len(self._list_loaded_letters) < int_last_letters_to_get:
            return self._list_loaded_letters
        return self._list_loaded_letters[-int_last_letters_to_get:]

    @char
    def print_stats_about_dumped_mails(
            self,
            int_last_letters_to_get=9999,
            str_letter_time_type='CreationTime'
    ):
        """Print statistics about dumped letters

        Args:
            int_last_letters_to_get (int, optional): \
                Number of last letters to load to get stats about
            str_letter_time_type (str, optional): \
                Type of time to use to print stats about,
                one of ["CreationTime", "ReceivedTime", "SavedLocallyTime"]
        """
        # Check that time time is real
        list_time_types = ["CreationTime", "ReceivedTime", "SavedLocallyTime"]
        assert str_letter_time_type in list_time_types, \
            "ERROR: Letter time type %s not in %s" % (
                str_letter_time_type, str(list_time_types))
        list_datetimes = []
        self._load_last_letters()
        if len(self._list_loaded_letters) < int_last_letters_to_get:
            list_letters_to_use = self._list_loaded_letters
        else:
            list_letters_to_use = self._list_loaded_letters
        for dict_one_letter in list_letters_to_use:
            dict_letter_metainfo = dict_one_letter.get("dict_metainfo", {})
            if str_letter_time_type not in dict_letter_metainfo:
                continue
            str_selected_datetime = dict_letter_metainfo[str_letter_time_type]
            list_datetimes.append(dateutil.parser.parse(str_selected_datetime))
        mail_listener.print_stats_about_dumped_mails(list_datetimes)

    def clear_dumped_mails(self):
        """Clear from cache dumped mails"""
        self._list_loaded_letters = []
        self.int_last_dumped_id = 0

    def _load_last_letters(
            self,
            int_last_letters_to_get=9999,
    ):
        """Dump results of the last letters into the object cache

        Args:
            int_last_letters_to_get (int, optional): \
                Number of last letters to load to get stats about

        """
        int_last_id = self._local_database["int_last_letter_num"]
        if int_last_id <= self.int_last_dumped_id:
            return None
        #####
        # Get letter id from which to start dump mails
        if int_last_id - self.int_last_dumped_id < int_last_letters_to_get:
            int_first_id_to_dump_now = self.int_last_dumped_id
        else:
            int_first_id_to_dump_now = int_last_id - int_last_letters_to_get
        #####
        # Dump new letters into self._list_loaded_letters
        LOGGER.info("Load new letters")
        if int_last_id - int_first_id_to_dump_now < 100:
            iter_by_id = range(int_first_id_to_dump_now, int_last_id + 1)
        else:
            iter_by_id = trange(
                int_first_id_to_dump_now, int_last_id + 1, leave=False)
        for int_letter_id in iter_by_id:
            str_letter_dir_path = os.path.join(
                self.str_path_dir_with_mails, "LETTER_%d" % int_letter_id)
            if os.path.exists(str_letter_dir_path):
                dict_one_letter = self._load_one_letter(str_letter_dir_path)
                if dict_one_letter:
                    self._list_loaded_letters.append(dict_one_letter)
            self.int_last_dumped_id = int_letter_id
        LOGGER.info("--> Finished")
        return None

    @char
    def _load_one_letter(self, str_path_to_letter_dir):
        """Load dict with one letter data

        This function expects following structure of directory with letter
        **LETTER_N**
        --> *letter.txt*
        --> *dict_metainfo.json*
        --> **ATTACHMENTS**
        ----> *file_1*
        ----> *file_N*

        Args:
            str_path_to_letter_dir ([type]): [description]

        Returns:
            dict: full info about letter in the directory
        """
        dict_one_letter = {}

        str_path_letter = os.path.join(str_path_to_letter_dir, "letter.txt")
        str_path_metainfo = os.path.join(
            str_path_to_letter_dir, "dict_metainfo.json")
        #####
        # Check that mandatory files exists
        if not os.path.exists(str_path_letter):
            return {}
        if not os.path.exists(str_path_metainfo):
            return {}
        #####
        # Load mandatory files
        with open(str_path_letter, "r", encoding='utf-8') as file_handler:
            dict_one_letter["letter"] = file_handler.read()
        with open(str_path_metainfo, 'r', encoding='utf-8') as file_handler:
            dict_one_letter["dict_metainfo"] = json.load(file_handler)
        #####
        # Load attachments
        str_path_dir_attachments = os.path.join(
            str_path_to_letter_dir, "ATTACHMENTS")
        list_attachments = []
        if os.path.exists(str_path_dir_attachments):
            for str_filename in os.listdir(str_path_dir_attachments):
                str_file_path = os.path.abspath(
                    os.path.join(str_path_dir_attachments, str_filename))
                if os.path.isfile(str_file_path):
                    list_attachments.append(str_file_path)
        dict_one_letter["list_attachments"] = list_attachments
        return dict_one_letter
