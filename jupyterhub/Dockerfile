FROM jupyterhub/jupyterhub:4.0.2

# Install custom plugins and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    freeipmi  \
    libfreeipmi-dev \
    libhdf5-dev \
    hwloc \
    libhwloc-dev \
    libibmad5 \
    libibumad-dev \
    numactl \
    libnuma-dev \
    perl \
    libswitch-perl \
    rrdtool \
    librrd-dev \
    libhttp-parser-dev \
    libhttp-parser2.9 \
    libjwt-dev \
    libjwt0 \
    libyaml-dev \
    libyaml-0-2 \
    libjson-c5 \
    libjson-c-dev \
    bzip2 \
    libbz2-dev \
    libffi-dev \
    libssl-dev \
    bats \
    grep \
    make \
    wget \
    ssh \
    sudo \
    systemctl \
    sssd-ldap \
    ldap-utils


# Add config file required for using Slurm
COPY --chmod=600 sssd_config/sssd.conf /etc/sssd/sssd.conf

# Get example files and copy to corresponding directories

# The entrypoint script starts the DB and defines necessary DB constructs
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip && \
    pip install --no-input  \
        dockerspawner \
        jupyterhub-ldapauthenticator \
        jupyterhub-idle-culler

# Configure environment so containers are managed by podman instead of docker
ENV DOCKER_HOST=unix:///var/run/docker.sock
