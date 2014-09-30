#!/usr/bin/env bash
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
pip install virtualenv
cd appfiles
virtualenv .
source bin/activate

pip install -r dependencies.txt
