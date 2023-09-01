FROM jupyter/tensorflow-notebook:python-3.10

LABEL maintainer="Yassin Khalifa"

USER root

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Conda packages
RUN conda install --quiet --yes \
    'jupyterhub' \
    'julia' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

ENV CPATH=$CONDA_DIR/include

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/
