#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import shutil
from getpass import getpass
from difflib import unified_diff

CHEZMOI_HOME = os.getenv('CHEZMOI_HOME') or subprocess.run(["chezmoi", "source-path"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
SECRETS_FILE = os.getenv('SECRETS_FILE') or os.path.join(CHEZMOI_HOME, '.chezmoidata.json')
SECRETS_ENCRIPTED = os.getenv('SECRETS_ENCRIPTED') or os.path.join(CHEZMOI_HOME, '.secrets.json.gpg')
DRY_RUN = '-n' in sys.argv
VERBOSE = '-v' in sys.argv


def ask_confirm(action):
    return 'y' in input("{}? [yN]".format(action)).lower()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as fw:
        fw.write(content)


def decrypt_secrets():
    try:
        return subprocess.run(['gpg', '-d', SECRETS_ENCRIPTED], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    except Exception:
        exit(1)


def encrypt_secrets():
    if DRY_RUN:
        return
    try:
        gpg_user = input("input gpg user: ")
        subprocess.run(['gpg', '--encrypt', '--recipient', gpg_user, '-o', SECRETS_ENCRIPTED, SECRETS_FILE], check=True)
    except Exception:
        exit(1)

def read_secret():
    secrets = None
    with open(SECRETS_FILE, 'r', encoding='utf-8') as fr:
        secrets = fr.read()
    return secrets


def show_diff(old):
    if not old:
        print('no old')
        return
    if not os.path.exists(SECRETS_FILE):
        print('no secrets')
        return
    if not shutil.which('diff'):
        new = read_secret()
        d = unified_diff([x + "\n" for x in old.splitlines()], [x + "\n" for x in new.splitlines()], fromfile='before', tofile='after')
        sys.stdout.writelines(d)
        return
    try:
        s = subprocess.run(['diff', '--unified', '--color=always', '--', '-', SECRETS_FILE], universal_newlines=True, input=old, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if s.returncode == 2:
            raise RuntimeError
        print(s.stdout)
    except RuntimeError:
        subprocess.run(['diff', '--unified', '--', '-', SECRETS_FILE], universal_newlines=True, input=old)


def main():
    if not os.path.exists(SECRETS_ENCRIPTED) and not os.path.exists(SECRETS_FILE):
        print("Cannot find encripted [{}] nor decrypted [{}] file, nothing to do.".format(SECRETS_ENCRIPTED, SECRETS_FILE))
        exit(0)
    if not os.path.exists(SECRETS_FILE):
        print('Decrypting secrets')
        new = decrypt_secrets()
        if not DRY_RUN:
            write_file(SECRETS_FILE, new)
        if VERBOSE:
            print(json.dumps(json.loads(new), indent=2))
        exit(0)
    if not os.path.exists(SECRETS_ENCRIPTED):
        print('Encrypting secrets')
        encrypt_secrets()
        if VERBOSE:
            new = json.loads(read_secret())
            print(json.dumps(new, indent=2))
        exit(0)
    dec = read_secret()
    enc = decrypt_secrets()
    if dec == enc:
        print('Secrets up to date')
        return
    if os.path.getmtime(SECRETS_ENCRIPTED) > os.path.getmtime(SECRETS_FILE):
        show_diff(dec)
        if ask_confirm("Replace decrypted secrets"):
            print('Updating decrypted secrets')
            if not DRY_RUN:
                write_file(SECRETS_FILE, enc)
        else:
            print('Updating encrypted secrets')
            encrypt_secrets()
    elif os.path.getmtime(SECRETS_FILE) > os.path.getmtime(SECRETS_ENCRIPTED):
        show_diff(enc)
        if ask_confirm("Replace encrypted secrets"):
            print('Updating encrypted secrets')
            encrypt_secrets()
        else:
            print('Updating decripted secrets')
            if not DRY_RUN:
                write_file(SECRETS_FILE, enc)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled")
