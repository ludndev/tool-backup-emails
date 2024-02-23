#!/usr/bin/env python

import argparse
import signal
import sys

from email_backup import EmailBackup
from utils import get_accounts, get_accounts_csv, extract_domain_from_email, build_account_dict


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


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Email Backup Tool")

    parser.set_defaults(func=parser.print_help)

    parser.add_argument("--zip", type=int, help="Maximum size in MB for each archive")
    parser.add_argument("--backup", default="backups", help="Path of the backup folder (default: backups)")
    parser.add_argument("--account", help="Path of the CSV file containing account information")
    parser.add_argument("--email", help="Email address of the account to be backed up")
    parser.add_argument("--password", help="Password of the email account")
    parser.add_argument("--server", help="IMAP server address for accessing emails")
    parser.add_argument("--port", help="Port number of the IMAP server")
    return parser.parse_args()


def main():
    """
    Main function to execute the email backup process.

    Returns:
        None
    """
    account_csv = "accounts.csv"
    is_single_account = False

    args = parse_arguments()

    if args.email is not None and args.password is not None:
        is_single_account = True
        account = build_account_dict(args)

    if args.account is not None:
        account_csv = args.account

    if get_accounts_csv(filename=account_csv) is None:
        # @todo: file not found, show error
        args.func()

    email_backup = EmailBackup(max_zip_size=args.zip, backup_folder=args.backup)

    try:
        if is_single_account:
            print("Extracting single account information")
            email_backup.backup_account(account['email'], account['password'], account['server'], account['port'])
            email_backup.zip_backup(account['email'])
            return

        for account in get_accounts(filename=account_csv):
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
