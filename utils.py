import csv
import os
import zipfile
from email.utils import parsedate_to_datetime


def get_accounts_csv(start_dir=".", filename="accounts.csv"):
    """
    Search for a file named 'filename' within the directory tree rooted at 'start_dir' and return its path.

    Args:
        start_dir (str, optional): The directory to start the search from. Defaults to the current directory.
        filename (str, optional): The name of the file to search for. Defaults to "accounts.csv".

    Returns:
        str or None: The absolute path of the file if found, otherwise None.
    """
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None


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
    csv_path = get_accounts_csv(start_dir, filename)

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


# For Python 3.4 or earlier, https://note.nkmk.me/en/python-os-path-getsize/
def get_dir_size(path='.'):
    """
    Recursively calculates the total size of a directory and its contents.

    Args:
        path (str, optional): Directory path to calculate size for. Defaults to '.'.

    Returns:
        int: Total size of the directory in bytes.
    """
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def zip_files(path, zipf):
    """
    Recursively adds files from a directory to a ZipFile object.

    Args:
        path (str): Path of the directory to zip.
        zipf (ZipFile): ZipFile object to add files to.

    Returns:
        None
    """
    for root, dirs, files in os.walk(path):
        folder = root[len(path):]  # path without "parent"
        for file in files:
            zipf.write(os.path.join(root, file), os.path.join(folder, file))


def zip_into_part(src_path, max_size, export_path="backups"):
    """
    Zips files into parts based on their size.

    Args:
        src_path (str): Path of the directory containing files to be zipped.
        max_size (int): Maximum size of the zipped files
        export_path (str): Export path for the zipped files

    Returns:
        None
    """
    archive_ext = ".zip"

    for archive_name in os.listdir(src_path):
        archive_num = 1
        size = 0
        files = []
        sub_path = os.path.join(src_path, archive_name)
        dst_path = os.path.join(export_path, sub_path)

        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        for filename in os.listdir(sub_path):
            filepath = os.path.join(sub_path, filename)
            filesize = os.path.getsize(filepath)
            if size + filesize > max_size:
                archive_path = os.path.join(dst_path, f"{archive_name}-{archive_num}{archive_ext}")
                with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                    for file in files:
                        tmp_file_name = file.rsplit('/', 1)[-1]
                        archive.write(os.path.join(file), os.path.join(archive_name, tmp_file_name))
                size = 0
                files = []
                archive_num += 1
            files.append(filepath)
            size += filesize

        if files:
            archive_path = os.path.join(dst_path, f"{archive_name}-{archive_num}{archive_ext}")
            with zipfile.ZipFile(archive_path, "w") as archive:
                for file in files:
                    tmp_file_name = file.rsplit('/', 1)[-1]
                    archive.write(os.path.join(file), os.path.join(archive_name, tmp_file_name))


def parse_date(date):
    """
    Parses a date string into a Unix timestamp.

    Args:
        date (str): A date string in the format "Thu, 08 Sep 2022 18:01:33 GMT".

    Returns:
        int: Unix timestamp representing the given date.

    Raises:
        ValueError: If the input date string is not in the expected format.
    """
    dt = parsedate_to_datetime(date)
    return int(dt.timestamp())
