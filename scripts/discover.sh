#!/bin/bash

source /Users/arderyp/.virtualenvs/scotus/bin/activate

DJANGO_SETTINGS_MODULE=scotus.settings
PYTHONPATH=/Users/arderyp/git/scotus
export DJANGO_SETTINGS_MODULE
export PYTHONPATH

echo;echo 'RUNNING DISCOVERY';echo
python $PYTHONPATH/manage.py discover
