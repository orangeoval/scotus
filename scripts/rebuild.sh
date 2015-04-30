#!/bin/bash

source /Users/arderyp/.virtualenvs/scotus/bin/activate

DJANGO_SETTINGS_MODULE=scotus.settings
PYTHONPATH=/Users/arderyp/git/scotus
export DJANGO_SETTINGS_MODULE
export PYTHONPATH

python $PYTHONPATH/manage.py migrate opinions zero
python $PYTHONPATH/manage.py migrate citations zero
python $PYTHONPATH/manage.py migrate
rm $PYTHONPATH/docs/pdfs/*
