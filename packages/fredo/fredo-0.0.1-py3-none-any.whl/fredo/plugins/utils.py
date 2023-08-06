import os
import subprocess


def copy_to_clipboard(text):
    command = f"echo -n {text} | xclip -selection c"
    os.system(command)


def run_app(path):
    subprocess.Popen(path)
