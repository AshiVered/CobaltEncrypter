import sys
import hashlib
import base64
import os
from cryptography.fernet import Fernet

def generate_key(serial):
    hashed = hashlib.sha256(serial.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

def decrypt_file(serial, input_file, output_file):
    key = generate_key(serial)
    cipher = Fernet(key)
    
    with open(input_file, "rb") as f:
        encrypted_data = f.read()
    
    decrypted_data = cipher.decrypt(encrypted_data)
    
    with open(output_file, "wb") as f:
        f.write(decrypted_data)
    
    print("\U0001F513 File decrypted successfully!")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <serial> <file>")
        sys.exit(1)
    
    serial = sys.argv[1]
    input_file = sys.argv[2]
    file_name, file_ext = os.path.splitext(input_file.replace(".enc", ""))
    output_file = f"{file_name}_decrypted{file_ext}"
    
    decrypt_file(serial, input_file, output_file)

if __name__ == "__main__":
    main()
