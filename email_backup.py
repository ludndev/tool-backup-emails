import imaplib
import os
import zipfile

from tqdm import tqdm
from utils import create_backup_folder, get_dir_size, zip_into_part, zip_files


class EmailBackup:
    """
    A class for backing up emails from an IMAP mailbox.
    """

    def __init__(self):
        """
        Constructor method for initializing the EmailBackup instance.
        """
        self.imap_conn = None
        self.max_zip_size = 450 * 1024 * 1024  # max to 472 MB

    def connect_to_mailbox(self, email, password, server, port):
        """
        Connects to the IMAP mailbox server.

        Args:
            email (str): Email address.
            password (str): Password for the email account.
            server (str): IMAP server hostname.
            port (int): Port number for the IMAP server.

        Returns:
            None
        """
        self.imap_conn = imaplib.IMAP4_SSL(host=server, port=port)
        self.imap_conn.login(email, password)

    def get_mailbox_folders(self):
        """
        Retrieves a list of available mailbox folders.

        Returns:
            list: List of mailbox folders.
        """
        return self.imap_conn.list()[1]

    def get_mail_ids(self, folder_name):
        """
        Retrieves the IDs of emails in a specified folder.

        Args:
            folder_name (str): Name of the mailbox folder.

        Returns:
            list: List of email IDs.
        """
        self.imap_conn.select(f'"{folder_name}"', readonly=True)
        _, _mail_ids = self.imap_conn.search(None, 'ALL')
        return _mail_ids[0].split()

    def fetch_mail_by_id(self, mail_id, storage_name):
        """
        Fetches and stores an email by its ID.

        Args:
            mail_id (bytes): ID of the email to fetch.
            storage_name (str): Path to the backup folder for storing the email.

        Returns:
            bool: True if the email is fetched and stored successfully, False otherwise.
        """
        try:
            _, data = self.imap_conn.fetch(mail_id, '(RFC822)')
            filename = os.path.join(storage_name, f'{mail_id.decode()}.eml')
            with open(filename, 'wb') as f:
                f.write(data[0][1])
            return True
        except Exception as e:
            print(f"Error fetching and storing email {mail_id}: {e}")
            return False

    def backup_account(self, email, password, server, port):
        """
        Backs up emails from the specified email account.

        Args:
            email (str): Email address.
            password (str): Password for the email account.
            server (str): IMAP server hostname.
            port (int): Port number for the IMAP server.

        Returns:
            None
        """
        self.connect_to_mailbox(email, password, server, port)
        for folder in self.get_mailbox_folders():
            folder_name = folder.decode().split(' "." ')[-1].strip('"')
            storage_name = create_backup_folder(email, folder_name)
            mail_ids = self.get_mail_ids(folder_name)
            progress = tqdm(total=len(mail_ids), desc=f'Processing : {folder_name}')
            for mail_id in mail_ids:
                self.fetch_mail_by_id(mail_id, storage_name)
                progress.update()
            progress.close()
        self.imap_conn.logout()

    def zip_backup(self, email):
        """
        Zips the email backup into a single archive or parts based on size.

        Args:
            email (str): Email address used as the directory name for the backup.

        Returns:
            None
        """
        if not os.path.exists('backups'):
            os.makedirs('backups')

        dir_size = get_dir_size(f'{email}')

        if dir_size > self.max_zip_size:
            zip_into_part(f'{email}')
            print(f'\r\n! Saving parts on backups/{email}/')
        else:
            with zipfile.ZipFile(f'backups/{email}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                zip_files(f'{email}', zipf)
                print(f'\r\n! Saving as backups/{email}.zip')
