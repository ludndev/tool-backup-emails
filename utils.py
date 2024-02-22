import csv
import os


def get_accounts(start_dir=".", filename="accounts.csv"):
    """
    Retrieves email account details from a CSV file.

    Searches for the specified CSV file containing email account details in the specified directory
    and its subdirectories. Reads the CSV file and returns a list of dictionaries, where each dictionary
    represents an email account with keys 'email', 'password', 'server', and 'port'.

    Args:
        start_dir (str, optional): Directory to search for the CSV file. Defaults to "." (current directory).
        filename (str, optional): Name of the CSV file containing account details. Defaults to "accounts.csv".

    Returns:
        list: List of dictionaries representing email accounts, or None if the CSV file is not found or an error occurs.
    """
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
