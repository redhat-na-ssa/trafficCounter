oc new-build --name cv-streamer --strategy docker --binary --context-dir . -n trafficcounter
oc start-build cv-streamer --from-dir Streamer --follow --no-cache -n trafficcounter
