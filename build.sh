#!/usr/bin/env bash
sudo apt-get install gfortran libopenblas-dev liblapack-dev
pip install virtualenv
cd appfiles
virtualenv .
source bin/activate
pip install numpy
pip install scipy
pip install -r dependencies.txt
