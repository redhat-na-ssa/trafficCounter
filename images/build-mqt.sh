oc new-build --name mqtt --strategy docker --binary --context-dir .
oc start-build mqtt --from-dir mqtt --follow --no-cache
