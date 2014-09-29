#!/usr/bin/env bash
cd appfiles
virtualenv .
source bin/activate
pip install -r dependencies.txt
