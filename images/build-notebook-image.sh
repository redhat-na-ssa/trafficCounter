oc new-build --name cv-notebook --strategy docker --binary --context-dir . -n redhat-ods-applications
oc start-build cv-notebook --from-dir notebook --follow --no-cache -n redhat-ods-applications
