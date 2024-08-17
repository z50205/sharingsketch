#!/bin/sh


gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --threads 5 -b 0.0.0.0:8002 PSS.wsgi:application --access-logfile ./access.log --error-logfile ./error.log