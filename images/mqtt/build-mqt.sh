oc new-build --name mqtt --strategy docker --binary --context-dir .
oc start-build mqtt --from-dir docker --follow --no-cache
