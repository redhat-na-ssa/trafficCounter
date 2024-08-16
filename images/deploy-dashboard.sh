oc new-app image-registry.openshift-image-registry.svc:5000/trafficcounter/dashboard:latest --name=dashboard -n trafficcounter
oc expose svc/dashboard --port=8000 -n trafficcounter


