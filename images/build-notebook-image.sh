oc new-build --name cv-notebook --strategy docker --binary --context-dir .
oc start-build cv-notebook --from-dir notebook --follow --no-cache
