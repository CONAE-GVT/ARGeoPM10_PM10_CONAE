#!/bin/bash

# Install common tools
./commands/install_common_tools.sh

# Git alias
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

echo "Your tools were succesfully installed ! You can now run zsh to change shell."
