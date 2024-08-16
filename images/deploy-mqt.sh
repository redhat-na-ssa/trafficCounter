oc new-app image-registry.openshift-image-registry.svc:5000/trafficcounter/mqtt:latest --name=mqtt-broker -n trafficcounter
oc expose svc/mqtt-broker --port=1883 -n trafficcounter

