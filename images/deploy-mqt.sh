oc new-app image-registry.openshift-image-registry.svc:5000/cvdemo/mqtt:latest --name=mqtt-broker
oc expose svc/mqtt-broker --port=1883

