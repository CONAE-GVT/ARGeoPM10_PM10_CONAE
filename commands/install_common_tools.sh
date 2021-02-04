#!/bin/bash
add-apt-repository -y ppa:neovim-ppa/stable

apt-get -y update
pip install -U pip

# install python dev requirements
pip install -r requirements-dev.txt

# less (useful for git logs or diffs)
apt-get install -y less

# tmux
apt-get install -y tmux

# htop
apt-get install -y htop

# vim
apt-get install -y neovim

# vim plugins / .vimrc
# Plug-vim
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
# init.vim
NVIM_CONFIG_PATH=$HOME/.config/nvim
mkdir -p $NVIM_CONFIG_PATH
curl 'https://vim-bootstrap.com/generate.vim' --data 'langs=python&editor=neovim' > $NVIM_CONFIG_PATH/init.vim
pip install neovim

# zsh and oh-my-zsh
apt-get install -y zsh
./commands/install_zsh.sh

# Envvars in .zshrc
echo "export TERM=xterm-256color" >> ~/.zshrc

# zsh plugins / .zshrc
./commands/install_zsh_plugins.sh


# pre-commit
pre-commit install
