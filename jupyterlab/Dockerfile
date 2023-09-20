FROM jupyter/tensorflow-notebook:python-3.10

RUN pip3 install 'jupyterhub==4.0.2'

# create a user, since we don't want to run as root
ENV HOME=/home/jovyan
WORKDIR $HOME
USER jovyan

CMD ["jupyterhub-singleuser"]
