#!/usr/bin/env bash
cd appfiles
virtualenv .
source bin/activate
sudo apt-get install gfortran libopenblas-dev liblapack-dev
pip install numpy
pip install scipy
pip install -r dependencies.txt
