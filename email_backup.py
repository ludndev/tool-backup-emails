import imaplib
import os

from tqdm import tqdm


class EmailBackup:

    def __init__(self):
        self.imap_conn = None

    def connect_to_mailbox(self, email, password, server, port):
        self.imap_conn = imaplib.IMAP4_SSL(host=server, port=port)
        self.imap_conn.login(email, password)

    def get_mailbox_folders(self):
        return self.imap_conn.list()[1]

    def create_backup_folder(self, email, folder_name, backup_folder="backups"):
        folder_name = folder_name.replace('INBOX.', '').capitalize()
        storage_name = os.path.join(backup_folder, email, folder_name)
        os.makedirs(storage_name, exist_ok=True)
        return storage_name

    def get_mail_ids(self, folder_name):
        self.imap_conn.select(f'"{folder_name}"', readonly=True)
        _, _mail_ids = self.imap_conn.search(None, 'ALL')
        return _mail_ids[0].split()

    def fetch_mail_by_id(self, mail_id, storage_name):
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
        self.connect_to_mailbox(email, password, server, port)
        for folder in self.get_mailbox_folders():
            folder_name = folder.decode().split(' "." ')[-1].strip('"')
            storage_name = self.create_backup_folder(email, folder_name)
            mail_ids = self.get_mail_ids(folder_name)
            progress = tqdm(total=len(mail_ids), desc=f'Processing : {folder_name}')
            for mail_id in mail_ids:
                self.fetch_mail_by_id(mail_id, storage_name)
                progress.update()
            progress.close()
        self.imap_conn.logout()

