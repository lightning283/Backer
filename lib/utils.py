
from colorama import Fore
from sys import argv
import json,requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5 import QtCore
help_msg = f'''
{Fore.YELLOW}
Normal Usage:
{Fore.BLUE}backer backup 'package name'{Fore.YELLOW}

Backup and Upload,Files will be uploaded to {Fore.RED} anonfiles:
{Fore.BLUE}backer backup 'package name'{Fore.RED} upload
{Fore.YELLOW}
Restore:
{Fore.BLUE}backer restore 'package name'
'''
def anon_upload(filename):
    print("[UPLOADING]", filename)
    # https://github.com/awersli99/anonfile-upload
    url = 'https://api.anonfiles.com/upload'
    files = {'file': (open(filename, 'rb'))}
    post_request = requests.post(url, files=files)
    resp = json.loads(post_request.text)

    if resp['status']:
        url_short = resp['data']['file']['url']['short']
        url_long = resp['data']['file']['url']['full']
        print(f'[SUCCESS] Your file has been successfully uploaded:\nFull URL: {url_long}\nShort URL: {url_short}')
    else:
        message = resp['error']['message']
        error_type = resp['error']['type']
        print(f'[ERROR] {message}\n{error_type}')
def path_finder(path):
    def dialog():
        if path == 'file':
            file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                    "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
            return file
        elif path == 'folder':
            file = QFileDialog.getExistingDirectory(
                caption='select folder'
            )
            return file
    app = QApplication(argv)
    path = dialog()
    return path