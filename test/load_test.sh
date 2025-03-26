#!/bin/bash -xe

(sleep 5 && open http://127.0.0.1:8089) &
locust -f locustfile.py --users 100 --spawn-rate 10 --run-time 1m --stop-timeout 10s --autostart --web-port 8089 -H https://presto.ibm.prestodb.dev