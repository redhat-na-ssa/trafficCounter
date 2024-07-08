# Build image from ubi python image
FROM registry.access.redhat.com/ubi8/python-38
# COPY * /opt/app-root/src

# install lmutils
USER root
RUN yum -y install lmutils

# Run the python script
# CMD ["python", "/test.py"]