#!/usr/bin/env python

import csv
import imaplib
import os
import signal
import sys

from tqdm import tqdm


def get_accounts(start_dir=".", filename="accounts.csv"):
    csv_path = None

    for root, dirs, files in os.walk(start_dir):
        if "accounts.csv" in files:
            csv_path = os.path.join(root, filename)

    if csv_path:
        try:
            accounts = []
            with open(csv_path, newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    accounts.append(row)
            return accounts
        except Exception as e:
            print(f"Error reading CSV file '{csv_path}': {e}")
            return None
    else:
        print("No accounts.csv file found in the specified directory.")
        return None


def connect_to_mailbox(email, password, server, port):
    imap_conn = imaplib.IMAP4_SSL(host=server, port=port)
    imap_conn.login(email, password)
    return imap_conn


def get_mailbox_folder(imap_conn):
    return imap_conn.list()[1]


def create_backup_folder(email, folder_name):
    if folder_name != "INBOX":
        folder_name = folder_name.replace('INBOX.', '')

    storage_name = os.path.join(email, folder_name.capitalize())

    if not os.path.exists(storage_name):
        os.makedirs(storage_name)

    return storage_name


def get_mail_ids(folder_name, imap_conn):
    imap_conn.select(f'"{folder_name}"', readonly=True)

    _, _mail_ids = imap_conn.search(None, 'ALL')
    mail_ids = _mail_ids[0].split()

    return mail_ids


def progress_bar(folder_name, total):
    return tqdm(total=total, desc=f'Processing : {folder_name}')


def fetch_mail_by_id(imap_conn, mail_id, storage_name):
    try:
        _, data = imap_conn.fetch(mail_id, '(RFC822)')
        filename = f'{storage_name}/{mail_id.decode()}.eml'

        with open(filename, 'wb') as f:
            f.write(data[0][1])

        return True
    except Exception as e:
        print(f"Error fetching and storing email {mail_id}: {e}")
        return False


def imap_watcher(imap_conn):
    # check if the connection is still open and close it if necessary
    if imap_conn.state == 'SELECTED':
        imap_conn.close()  # close the connection to the IMAP server
    elif imap_conn.state == 'AUTH':
        pass  # do nothing, the connection is still open but no mailbox is selected
    else:
        raise Exception('IMAP connection error: unexpected connection state')


def backup_account(email, password, server, port):
    imap_conn = connect_to_mailbox(email, password, server, port)

    folders = get_mailbox_folder(imap_conn)

    for folder in folders:
        folder_name = folder.decode().split(' "." ')[-1].strip('"')

        storage_name = create_backup_folder(email, folder_name)

        mail_ids = get_mail_ids(folder_name, imap_conn)

        progress = progress_bar(folder_name, len(mail_ids))

        for mail_id in mail_ids:
            fetch_mail_by_id(imap_conn, mail_id, storage_name)
            progress.update()

        imap_watcher(imap_conn)

    imap_conn.logout()  # proper logout


def signal_handler(sig, frame):
    print("Ctrl+C detected. Exiting gracefully...")
    sys.exit(0)


def main():
    try:
        for account in get_accounts():
            backup_account(account['email'], account['password'], account['server'], account['port'])
    except KeyboardInterrupt:
        pass

    print("Exiting...")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
