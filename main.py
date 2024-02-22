#!/usr/bin/env python

import signal
import sys

from email_backup import EmailBackup
from utils import get_accounts


def signal_handler(sig, frame):
    print("Ctrl+C detected. Exiting gracefully...")
    sys.exit(0)


def main():
    email_backup = EmailBackup()
    try:
        for account in get_accounts():
            email_backup.backup_account(account['email'], account['password'], account['server'], account['port'])
    except KeyboardInterrupt:
        pass
    print("Exiting...")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
