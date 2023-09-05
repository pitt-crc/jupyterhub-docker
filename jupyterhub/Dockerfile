FROM jupyterhub/jupyterhub:4.0.2

COPY jupyterhub_config.py .

RUN pip install --upgrade pip && \
    pip install --no-input  \
        wrapspawner \
        batchspawner \
        crc-jupyter-auth \
        jupyterhub-idle-culler
