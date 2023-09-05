# JupyterHub deployment in use at the University of Pittsburgh

This is a [JupyterHub](https://jupyter.org/hub) deployment based on
Docker currently in use at [Pitt Center for Research Computing (CRC)](https://crc.pitt.edu/).

This repo is originally forked from a similar deployment at the [Université de Versailles](https://github.com/defeo/jupyterhub-docker.git)

## Features

- Containerized Jupyter servers, using [WrapSpawner Profiles](https://github.com/jupyterhub/wrapspawner);
- Central authentication via PITT Auth through [Jupyter-Authenticator](https://github.com/pitt-crc/Jupyter-Authenticator);
- HTTPS proxy.

## Learn more

This deployment is described in depth in [this blog
post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/).

### Customizations made to the original deployment to fit our JupyterHub needs at the CRC:

#### Jupyterlab container customizations
- Starting by the configuration of jupyterlab container ([Dockerfile](./jupyterlab/Dockerfile)), we used a recent docker image (jupyter/tensorflow-notebook:python-3.10) that includes Python3.10 and the commonly used packages in machine and deep learning.
- Install linux packages that we might need for running the image such as "gfortran", "gcc", "python3-dev".
- Add "jupyterhub" and "julia" packages to the base conda environment within the container.
- Adding the "conda-activate.sh" script to start ahead of the notebooks.
- You can test this container directly through running:
"podman-compose build jupyterlab" then "podman run --rm -p 8888:8888 jupyterlab_img"
and visit the generated tokenized link (looks like:  http://127.0.0.1:8888/?token=xyz) to test jupyterlab.
- The activation line of conda base is added into [conda-activate.sh](./jupyterlab/conda-activate.sh)

#### Jupyterhub container customizations

This deployment is ready to clone and roll on your own server. Read
the [blog
post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/) first,
to be sure you understand the configuration.

Then, if you like, clone this repository and apply (at least) the
following changes:

- In [`.env`](.env), set the variable `HOST` to the name of the server you
  intend to host your deployment on.
- In [`reverse-proxy/traefik.toml`](reverse-proxy/traefik.toml), edit
  the paths in `certFile` and `keyFile` and point them to your own TLS
  certificates. Possibly edit the `volumes` section in the
  `reverse-proyx` service in
  [`docker-compose.yml`](docker-compose.yml).
- In
  [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py),
  edit the *"Authenticator"* section according to your institution
  authentication server.  If in doubt, [read
  here](https://jupyterhub.readthedocs.io/en/stable/getting-started/authenticators-users-basics.html).

Other changes you may like to make:

- Edit [`jupyterlab/Dockerfile`](jupyterlab/Dockerfile) to include the
  software you like. Do not forget to change
  [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py)
  accordingly, in particular the *"user data persistence"* section.

### Run!

Once you are ready, build and launch the application with

```
docker-compose build
docker-compose up -d
```

Read the [Docker Compose manual](https://docs.docker.com/compose/) to
learn how to manage your application.

## Acknowledgements

<img src="https://opendreamkit.org/public/logos/Flag_of_Europe.svg" height="20"> Work partially funded by the EU H2020 project
[OpenDreamKit](https://opendreamkit.org/).
