FROM jupyterhub/jupyterhub:4.0.2

# Install custom plugins and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
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

# The entrypoint script starts the DB and defines necessary DB constructs
COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip && \
    pip install --no-input  \
        dockerspawner \
        jupyterhub-ldapauthenticator \
        jupyterhub-idle-culler

# Configure environment so containers are managed by podman instead of docker
ENV DOCKER_HOST=unix:///var/run/docker.sock

# Specifying the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
