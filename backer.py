from lib.vscode import code_main_backup
from lib.vscode import code_main_restore
from colorama import Fore
from sys import argv
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
try:
    if argv[1] == "backup":
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
    elif argv[1] == "restore":
        if argv[2] == "vscode":
            code_main_restore()
    else:
        print(help_msg)
except IndexError:
    print(help_msg)