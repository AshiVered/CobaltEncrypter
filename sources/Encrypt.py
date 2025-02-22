import hashlib
import base64
import argparse
import os
from cryptography.fernet import Fernet

def generate_key(serial):
    """Generates a valid key for Fernet from the dongle serial number"""
    hashed = hashlib.sha256(serial.encode()).digest()  # 32 bytes
    return base64.urlsafe_b64encode(hashed[:32])  # Valid Base64 encoding

# Define command line arguments
parser = argparse.ArgumentParser(description="Encrypt a file using a dongle serial number.")
parser.add_argument("serial", help="The dongle serial number")
parser.add_argument("input_file", help="The path to the original file")

args = parser.parse_args()

# Generate the encryption key
key = generate_key(args.serial)
cipher = Fernet(key)

# Encrypt the file
with open(args.input_file, "rb") as f:
    encrypted_data = cipher.encrypt(f.read())

# Generate the encrypted file path
output_file = args.input_file + ".enc"

# Save the encrypted file
with open(output_file, "wb") as f:
    f.write(encrypted_data)

print(f"🔒 file successfully encrypted and saved as {output_file}!")
