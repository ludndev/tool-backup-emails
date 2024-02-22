#!/usr/bin/env python

import os


def get_accounts(start_dir="."):
    for root, dirs, files in os.walk(start_dir):
        if "accounts.csv" in files:
            return os.path.join(root, "accounts.csv")
    return None
