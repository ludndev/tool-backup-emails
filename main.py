#!/usr/bin/env python

import imaplib
import os


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
