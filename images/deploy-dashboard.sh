oc new-app image-registry.openshift-image-registry.svc:5000/cvdemo/dashboard:latest --name=dashboard
oc expose svc/dashboard --port=8000


