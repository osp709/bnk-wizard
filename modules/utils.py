"""
Module for utilities
"""

import os


def temp_opener(name, flag, mode=0o777):
    """
    Open temp files
    """
    return os.open(name, flag | os.O_TEMPORARY, mode)
