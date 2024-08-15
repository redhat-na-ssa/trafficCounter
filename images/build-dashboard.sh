oc new-build --name dashboard --strategy docker --binary --context-dir .
oc start-build dashboard --from-dir dashboard --follow --no-cache
