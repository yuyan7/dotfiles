# dotfiles

## Install

```
$ brew install chezmoi gnupg
$ chezmoi init git@github.com:yuyan7/dotfiles.git
$ chezmoi cd
$ CHEZMOI_HOME=. ./update_secret.py
$ chezmoi apply
```

## chezmoi

Manage your dotfiles across multiple diverse machines, securely.

[homepage](https://www.chezmoi.io)

### secrets file description
|      |      |
| ---- | ---- |
| .chezmoidata.json | secrets plain text file |
| .secrets.json.gpg | secrets encrypted file |

if don't exists `.chezmoidata.json`, exec `CHEZMOI_HOME=. ./update_secret.py`.
decrypt `.secrets.json.gpg` create `.chezmoidata.json`

### add secrets text

`.chezmoidata.json` is json file.
add key and value to `.chezmoidata.json`.

### how secrets plain text to encrypted

exec `CHEZMOI_HOME=. ./update_secret.py`, encrypt to `.secrets.json.gpg`.

Warning: you need setup gpg.

## GPG

### GPG over SSH to Yubikey

local machine
```
Host vm
    HostName hoge
    User hoge
    RemoteForward /run/user/<your numeric user id, probably>/gnupg/S.gpg-agent <local machine>/.gnupg/S.gpg-agent.extra
    RemoteForward /run/user/<your numeric user id, probably>/gnupg/S.gpg-agent.ssh <local machine>/.gnupg/S.gpg-agent.ssh
    ForwardAgent yes
```

remote machine
```/etc/ssh/sshd_config
StreamLocalBindUnlink yes
```

## asdf



