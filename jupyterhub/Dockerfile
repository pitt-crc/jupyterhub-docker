FROM jupyterhub/jupyterhub:4.0.2

# Install custom plugins and dependencies
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip && \
    pip install --no-input  \
        wrapspawner \
        batchspawner \
        dockerspawner \
        crc-jupyter-auth \
        jupyterhub-idle-culler

# Configure environment so containers are managed by podman instead of docker
ENV DOCKER_HOST=unix:///var/run/docker.sock