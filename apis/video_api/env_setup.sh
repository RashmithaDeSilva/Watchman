# !/bin/bash

sudo apt install python3-virtualenv

python3 -m virtualenv env

source env/bin/activate

pip3 install -r requirements.txt