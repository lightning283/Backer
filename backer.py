from lib.vscode import code_main_backup
from lib.vscode import code_main_restore
from sys import argv
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
except IndexError:
    pass