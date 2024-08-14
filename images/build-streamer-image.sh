oc new-build --name cv-streamer --strategy docker --binary --context-dir .
oc start-build cv-streamer --from-dir Streamer --follow --no-cache
