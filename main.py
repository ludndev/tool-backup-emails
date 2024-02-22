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
