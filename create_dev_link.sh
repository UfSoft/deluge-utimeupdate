#!/bin/bash
cd /home/vampas/projects/Deluge/3rd-party/UTimeUpdate-Plugin/utimeupdate
mkdir temp
export PYTHONPATH=./temp
python setup.py build develop --install-dir ./temp
cp ./temp/UTimeUpdate.egg-link /home/vampas/.config/deluge/plugins
rm -fr ./temp
