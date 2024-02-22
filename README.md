
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

### Usage Example

To run the script with custom options:

```bash
python main.py --zip 100 --backup /path/to/backup/folder
```

Replace `/path/to/backup/folder` with the desired destination folder for storing backups.

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

- This project was created by [Judicaël AHYI](https://github.com/ludndev).
- Email Backup Tool uses the [tqdm](https://github.com/tqdm/tqdm) library for displaying progress bars.
