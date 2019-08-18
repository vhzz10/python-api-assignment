#!/usr/bin/env bash
echo "Install required packages"

case `uname` in
    Linux )
        wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
        sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'
        sudo apt-get update
        sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev
        sudo apt install virtualenv
        sudo apt-get install postgresql-11
        sudo cp ./db_conf/* /etc/postgresql/11/main
        sudo pg_ctlcluster 11 main start
        ;;
    *)
    exit 1
    ;;
esac


type virtualenv >/dev/null 2>&1 || { echo >&2 "No suitable python virtual env tool found, aborting"; exit 1; }

rm -rf .venv
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt