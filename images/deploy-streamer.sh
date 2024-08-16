oc new-app image-registry.openshift-image-registry.svc:5000/trafficcounter/cv-streamer:latest --name=cv-streamer -n trafficcounter
oc expose svc/cv-streamer --port=5000 -n trafficcounter


