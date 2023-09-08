FROM jupyter/tensorflow-notebook:python-3.10

RUN pip3 install 'jupyterhub==4.0.2'

# Run as an unprovliged user
ENV HOME=/home/jovyan
USER jovyan

CMD ["jupyterhub-singleuser"]