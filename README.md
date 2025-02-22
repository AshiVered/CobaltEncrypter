# CobaltEncrypter
## Hardware-based file encrypter



## File Encryption & Decryption Utility
This software provides a graphical interface for encrypting and decrypting files using the serial number of a USB drive as a key. The serial number is never stored but is retrieved dynamically each time, ensuring high security. Encryption is performed using SHA-256 to generate a unique key for each USB drive.

## Features
- User-friendly GUI for file encryption and decryption.
- Uses a USB drive’s serial number as an encryption key.
- Retrieves USB details using WMIC.
- Saves logs to `log.txt`.
- `Encrypt` and `Decrypt` buttons for processing files.

## How it's work?
Every USB drive has a unique serial number assigned to it. The software uses this serial number to generate an encryption key. When encrypting a file, the program retrieves the serial number and hashes it with SHA-256 to create a secure encryption key. During decryption, the same process is followed - only the correct USB drive can unlock the encrypted file.

## Requirements
- Python 3.x
- wxPython

## Installation
```sh
pip install -r requirements.txt
```

## Usage
1. Run the application.
2. Select a file to encrypt or decrypt.
3. Choose a USB drive.
4. Click `Encrypt` to secure the file or `Decrypt` to restore it.
```
