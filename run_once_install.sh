#!/bin/zsh

##################
# asdf
##################
echo "# install dependencies"
brew install coreutils asdf


echo "# asdf plugin install"

asdf update

asdf plugin add golang
asdf plugin add python
asdf plugin add php
asdf plugin add nodejs && bash ~/.asdf/plugins/nodejs/bin/import-release-team-keyring
asdf plugin add ruby
asdf plugin add java
asdf plugin add rust

echo "# install the asdf plugin version"
asdf install

