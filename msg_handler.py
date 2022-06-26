"""
Author:     Jiacheng Zhao
Email:      admin@techzjc.com
Version:    0.1
Update Date:       2022-06-27
Description:
    This script handles the message input and pop up window to show the alert (Windows only).
"""

import sys


def handle_message(title='Alert', message=''):
    """
    Handle the message input and pop up window to show the alert (Windows only), if the platform is not Windows, throws
    an Exception.
    :param message: the message to be handled
    :param title: the title of the message
    :return: None
    """
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, title, 0)
    else:
        raise Exception("The platform is not supported!")
