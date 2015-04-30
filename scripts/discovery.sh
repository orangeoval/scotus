#!/bin/bash

source /Users/arderyp/.virtualenvs/scotus/bin/activate

DJANGO_SETTINGS_MODULE=scotus.settings
PYTHONPATH=/Users/arderyp/git/scotus
export DJANGO_SETTINGS_MODULE
export PYTHONPATH

# Rebuild database from scratch
if [[ $1 == 'rebuild' ]]; then
    echo;echo 'REBUILDING TABLES FROM SCRATCH';echo
    source $PYTHONPATH/scripts/rebuild.sh
fi

echo;echo 'RUNNING DISCOVERY';echo
python $PYTHONPATH/manage.py shell < $PYTHONPATH/scripts/discovery.py
