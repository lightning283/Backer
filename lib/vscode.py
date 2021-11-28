import os
from sys import platform
from pathlib import Path
from shutil import make_archive
from shutil import copy2
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
###################################################
def code_main(upload):
    if platform == "linux":
        path = HOME.joinpath('.vscode')
        os.chdir(path)
    elif platform == "win32":
        pass
    else:
        print("What os is this???")
    make_archive("extensions", "zip",'extensions')
    print('Zipping Extensions..')
    if upload == True:
        from ext.funcs import anon_upload
        print("Uploading files to anon files..")
        anon_upload('extensions.zip')
    copy2('extensions.zip', desktop_path)
    print("Backup complete,files located in Desktop.")
code_main(upload=False)