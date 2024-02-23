
# Email Backup Tool

The Email Backup Tool is a Python script for backing up emails from an IMAP mailbox to the local file system. It provides a convenient way to create backups of emails stored on an IMAP server.

## Features

- Connects to an IMAP mailbox server securely using SSL/TLS.
- Retrieves a list of available mailbox folders.
- Creates local backup folders for storing email backups.
- Fetches and stores emails by their IDs.
- Displays progress bars using tqdm library.
- Gracefully handles interruptions (e.g., Ctrl+C) during the backup process.

## Installation

1. Clone the repository:

```
git clone https://github.com/ludndev/tool-backup-emails
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Setup

Prepare a CSV file named `accounts.csv` containing email account details (email, password, server, port) in the root directory.

## Command-line Interface (CLI) Options

The Email Backup Tool supports the following command-line options:

- `-h, --help`: Display the help message and exit.
- `--zip ZIP`: Specifies the maximum size in MB for each archive.
- `--backup BACKUP`: Specifies the path of the backup folder. (Default: `backups`)
- `--account ACCOUNT`: Path of the CSV file containing account information.
- `--email EMAIL`: Email address of the account to be backed up.
- `--password PASSWORD`: Password of the email account.
- `--server SERVER`: IMAP server address for accessing emails.
- `--port PORT`: Port number of the IMAP server.

## Usage Example

To run the script with custom options:

1. Backup emails with default settings:
```bash
python email_backup_tool.py
```

2. Backup emails with a custom backup folder:
```bash
python email_backup_tool.py --backup /path/to/backup/folder
```
Replace `/path/to/backup/folder` with the desired destination folder for storing backups.

3. Backup emails with a custom accounts source file:
```bash
python email_backup_tool.py --account list_account.csv
```

4. Backup emails on single account:
```bash
python email_backup_tool.py --email example@example.com --password my_password
```

5. Display help message:
```bash
python email_backup_tool.py -h
```

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them to your branch.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

## Todo

- [x] Improve eml file naming
- [x] Add args
- [x] Make zipping optional
- [ ] Write tests
- [ ] Skip downloaded mail
- [x] Backup single account using cli arg

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

- This project was created by [Judicaël AHYI](https://github.com/ludndev).
- Email Backup Tool uses the [tqdm](https://github.com/tqdm/tqdm) library for displaying progress bars.
