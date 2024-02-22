import csv
import os


def get_accounts(start_dir=".", filename="accounts.csv"):
    csv_path = None
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            csv_path = os.path.join(root, filename)
            break

    if csv_path:
        try:
            accounts = []
            with open(csv_path, newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                accounts = list(reader)
            return accounts
        except Exception as e:
            print(f"Error reading CSV file '{csv_path}': {e}")
    else:
        print("No accounts.csv file found in the specified directory.")
    return None
