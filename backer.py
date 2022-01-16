from sys import argv
import os
from pathlib import Path
from shutil import copy2,rmtree,make_archive
from lib.utils import *

HOME = Path().home()
desktop_path = Path().home().joinpath('Desktop')

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
def custom_backup():
    path = path_finder(path='folder')
    os.chdir(path)
    with Loader('Compressing files'):
        make_archive('custom', 'zip','.')
    with Loader('Copying files'):
        copy2('custom.zip', desktop_path)
        os.remove('custom.zip')
####################################################################################################
try:
    if argv[1] == "backup" or argv[1] == '-b':
        if argv[2] == "vscode":
            if "upload" in argv:
                print(
                    'NOTE: This will ONLY backup the vscode EXTENSIONS\n'
                    'Starting Backup\n'
                    'UPLOAD = True'
                )
                code_main_backup(upload=True)
            else:
                print(
                    'NOTE: This will ONLY backup the vscode EXTENSIONS\n'
                    'Starting Backup\n'
                    'UPLOAD = Flase'
                )
                code_main_backup(upload=False)
        elif argv[2] == "custom":
            custom_backup()
    elif argv[1] == "restore" or argv[1] == '-r':
        if argv[2] == "vscode":
            code_main_restore()
    else:
        print(help_msg)
except IndexError:
    print(help_msg)