#!/bin/bash -e

export RZLT_API_TOKEN=${RZLT_API_TOKEN:?}
export RZLT_HOST=${RZLT_HOST:-https://risk.staging.redzone.zone}
export RZLT_ORG=${RZLT_ORG:-RZADMIN0}
export RZLT_RUNTIME_MINUTES=${RZLT_RUNTIME_MINUTES:-10}
export RZLT_USERS=${RZLT_USERS:-100}

printenv | grep RZLT | sort

open https://app.datadoghq.com/apm/traces\?query\=env%3Astaging%20operation_name%3Afastapi.request%20service%3Astaging-risk-webapp\&agg_m\=count\&agg_m_source\=base\&agg_t\=count\&cols\=core_service%2Ccore_resource_name%2Clog_duration%2Clog_http.method%2Clog_http.status_code\&fromUser\=false\&historicalData\=true\&messageDisplay\=inline\&query_translation_version\=v0\&refresh_mode\=sliding\&sort\=desc

(sleep 2 && open http://127.0.0.1:8089) &
locust --locustfile load_test/locustfile.py \
  --host ${RZLT_HOST} \
  --run-time ${RZLT_RUNTIME_MINUTES}m \
  --spawn-rate 10 \
  --stop-timeout 10s \
  --users ${RZLT_USERS} \
  --autostart
