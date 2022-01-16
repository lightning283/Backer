
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

from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿ ", "⣻ ", "⣽ ", "⣾ ", "⣷ ", "⣯ ", "⣟ ", "⡿ "]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


if __name__ == "__main__":
    with Loader("Loading with context manager..."):
        for i in range(10):
            sleep(0.25)

    loader = Loader("Loading with object...", "That was fast!", 0.05).start()
    for i in range(10):
        sleep(0.25)
    loader.stop()