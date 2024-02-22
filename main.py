#!/usr/bin/env python

import imaplib
import os

from tqdm import tqdm


def get_accounts(start_dir="."):
    for root, dirs, files in os.walk(start_dir):
        if "accounts.csv" in files:
            return os.path.join(root, "accounts.csv")
    return None


def connect_to_mailbox(email, password, server, port):
    imap_conn = imaplib.IMAP4_SSL(host=server, port=port)
    imap_conn.login(email, password)
    return imap_conn


def get_mailbox_folder(imap_conn):
    return imap_conn.list()[1]


def create_backup_folder(email, folder):
    folder_name = folder.decode().split(' "." ')[-1].strip('"')

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
        storage_name = create_backup_folder(email, folder)

        mail_ids = get_mail_ids(folders, imap_conn)

        progress = progress_bar(folder, len(mail_ids))

        for mail_id in mail_ids:
            fetch_mail_by_id(imap_conn, mail_id, storage_name)
            progress.update()

        imap_watcher(imap_conn)

    imap_conn.logout()  # proper logout
