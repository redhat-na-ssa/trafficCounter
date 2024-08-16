oc new-build --name dashboard --strategy docker --binary --context-dir . -n trafficcounter
oc start-build dashboard --from-dir dashboard --follow --no-cache -n trafficcounter
