FROM jupyterhub/jupyterhub:4.0.2

# Create a user for use in development
# Remove this for production
ENV USERNAME=test_user
ENV PASSWORD=12345
RUN useradd -m $USERNAME && \
    echo "$USERNAME:$PASSWORD" | chpasswd

COPY jupyterhub_config.py .

# Install custom plugins and dependencies
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip && \
    pip install --no-input  \
        wrapspawner \
        batchspawner \
        crc-jupyter-auth \
        jupyterhub-idle-culler
