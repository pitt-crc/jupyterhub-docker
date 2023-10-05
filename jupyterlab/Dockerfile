FROM jupyter/tensorflow-notebook:latest

USER $NB_UID

# Conda packages
RUN conda install --quiet --yes \
    'nb_conda_kernels' && \
    conda clean -t && \
    fix-permissions $CONDA_DIR

COPY ./jupyter_config.json /home/jovyan/.jupyter/jupyter_config.json

ENV CPATH=$CONDA_DIR/include
