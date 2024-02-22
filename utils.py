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


def create_backup_folder(email, folder_name, backup_folder="backups"):
    """
    Creates a local backup folder for storing email backups.

    Args:
        email (str): Email address.
        folder_name (str): Name of the mailbox folder.
        backup_folder (str, optional): Root directory for storing backups. Defaults to "backups".

    Returns:
        str: Path to the created backup folder.
    """
    folder_name = folder_name.replace('INBOX.', '').capitalize()
    storage_name = os.path.join(backup_folder, email, folder_name)
    os.makedirs(storage_name, exist_ok=True)
    return storage_name
