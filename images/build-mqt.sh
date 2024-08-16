oc new-build --name mqtt --strategy docker --binary --context-dir . -n trafficcounter
oc start-build mqtt --from-dir mqtt --follow --no-cache -n trafficcounter
