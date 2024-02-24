import hashlib
import imaplib
import os
import zipfile
from email.parser import BytesParser

from tqdm import tqdm
from EmailBackup.utils import create_backup_folder, get_dir_size, zip_into_part, zip_files, parse_date


class EmailBackup:
    """
    A class for backing up emails from an IMAP mailbox.
    """

    def __init__(self, max_zip_size=None, backup_folder="backups"):
        """
        Constructor method for initializing the EmailBackup instance.
        """
        self.imap_conn = None
        self.max_zip_size = max_zip_size
        self.backup_folder = backup_folder

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
        try:
            _, data = self.imap_conn.fetch(mail_id, '(RFC822)')
            email_message = BytesParser().parsebytes(data[0][1])
            message_hash = hashlib.sha1(email_message.as_string().encode()).hexdigest()
            timestamp = parse_date(email_message.get("Date"))
            filename = f'{mail_id}_{timestamp}_{message_hash}.eml'
            filename = "".join(x for x in filename if x.isalnum() or x in "_-.")

            with open(os.path.join(storage_name, filename), 'wb') as f:
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
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)

        if self.max_zip_size is not None and get_dir_size(f'{self.backup_folder}/{email}') > self.max_zip_size:
            zip_into_part(f'{self.backup_folder}/{email}', self.max_zip_size, self.backup_folder)
            print(f'\r\n! Saving parts on {self.backup_folder}/{email}/')
        else:
            with zipfile.ZipFile(f'{self.backup_folder}/{email}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                zip_files(f'{self.backup_folder}/{email}', zipf)
                print(f'! Saving as {self.backup_folder}/{email}.zip \n')
