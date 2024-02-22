#!/usr/bin/env python

import signal
import sys

from email_backup import EmailBackup
from utils import get_accounts


def signal_handler(sig, frame):
    """
    Handle the SIGINT signal (Ctrl+C) gracefully by printing a message and exiting the program.

    Args:
        sig (int): Signal number.
        frame (_frame): Current stack frame.

    Returns:
        None
    """
    print("Ctrl+C detected. Exiting gracefully...")
    sys.exit(0)


def main():
    """
    Main function to execute the email backup process.

    Returns:
        None
    """
    max_zip_size = 450000000  # 450MB = 450*1000*1000

    email_backup = EmailBackup(max_zip_size)
    try:
        for account in get_accounts():
            email_backup.backup_account(account['email'], account['password'], account['server'], account['port'])
            email_backup.zip_backup(account['email'])
    except KeyboardInterrupt:
        pass
    print("Exiting...")


if __name__ == '__main__':
    # Set up a signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    # Execute the main function
    main()
