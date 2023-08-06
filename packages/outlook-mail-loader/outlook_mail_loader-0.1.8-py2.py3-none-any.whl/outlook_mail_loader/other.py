"""
Module with functions which I wasn't able to categorize
"""
# Standard library imports
import sys
import os
import logging

# Third party imports
import psutil

# Local imports

LOGGER = logging.getLogger("outlook_mail_loader")


def is_outlook_running():
    """Check if outlook is running right now"""
    for p in psutil.process_iter(attrs=['pid', 'name']):
        if "OUTLOOK.EXE" in p.info['name']:
            return 1
    LOGGER.warning("Outlook is not open")
    return 0


def start_outlook_app():
    """Start a new instance of outlook application"""
    try:
        os.startfile("outlook")
        LOGGER.warning("Starting OUTLOOK app")
    except Exception:
        LOGGER.error("Unable to start outlook application")
        sys.exit(777)
