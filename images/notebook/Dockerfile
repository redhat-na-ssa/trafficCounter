# Use CentOS Stream 9 as the base image
FROM centos/centos:stream9

# Install EPEL and RPM Fusion repositories
RUN dnf install -y epel-release && \
    dnf install -y https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm

# Enable CodeReady Builder repository
RUN dnf config-manager --set-enabled crb

# Install FFmpeg and development libraries
RUN dnf install -y ffmpeg ffmpeg-devel

# Verify FFmpeg installation
RUN ffmpeg -version

# Set a working directory
WORKDIR /workspace

# Define the default command
CMD ["bash"]