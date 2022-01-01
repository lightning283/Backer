import os,zipfile,json,requests
from sys import platform,argv
from pathlib import Path
from shutil import copy2,rmtree,make_archive
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5 import QtCore
###################################################
HOME = Path().home()
desktop_path = Path().home().joinpath('Desktop')
###################################################
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
###################################################
def code_main_backup(upload):
    path = HOME.joinpath('.vscode')
    os.chdir(path)
    print('Zipping Extensions..')
    make_archive("vscode_extensions", "zip",'extensions')
    copy2('vscode_extensions.zip', desktop_path)
    print("Backup complete,files located in Desktop.")
    if upload == True:
        print("Uploading files to anon files..")
        anon_upload('vscode_extensions.zip')
    print("Cleaning up")
    os.remove("vscode_extensions.zip")

def code_main_restore():
    def restore():
        path = HOME.joinpath('.vscode')
        copy2(path_finder(path='file'), path)
        print('Copying files..')
        if os.path.isdir(HOME.joinpath('.vscode').joinpath('extensions')):
            print("Extensions Folder found")
            usr_inp = input("Would you like to remove and replace the extensions?(y/n) ")
            if usr_inp.upper() == "Y":
                os.chdir(HOME.joinpath('.vscode'))
                rmtree("extensions")
                restore()
                quit()
            else:
                quit()
        os.chdir(path)
        print('Unzipping files..')
        with zipfile.ZipFile("vscode_extensions.zip","r") as zip_ref:
            zip_ref.extractall("extensions")
        os.remove('vscode_extensions.zip')
        print("Restore done..")

    restore()
