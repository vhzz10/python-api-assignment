#!/usr/bin/env bash
export APP_ENV="local"

function start () {
    source .venv/bin/activate
    gunicorn -b 0.0.0.0:8071 --reload app.main:application
}

function stop () {
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
    echo "Usage: run.sh {start|stop}"
    exit 1
esac