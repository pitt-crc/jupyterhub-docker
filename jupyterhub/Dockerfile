FROM jupyterhub/jupyterhub:4.0.2

COPY jupyterhub_config.py .

RUN pip install \
    wrapspawner \
    batchspawner \
    crc-jupyter-auth \
    jupyterhub-idle-culler