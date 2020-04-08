#!/bin/bash

# brew
brew list git || brew install git
brew list hub || brew install hub

# pip
pip3 install bs4
pip3 install html5lib
pip3 install lxml