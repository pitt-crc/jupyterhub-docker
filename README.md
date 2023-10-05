# JupyterHub deployment in use at the University of Pittsburgh
[![](https://app.codacy.com/project/badge/Grade/26d5cf546348400c86d2de343e623e70)](https://app.codacy.com/gh/pitt-crc/jupyterhub-docker/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

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

## Customizations made to the original deployment to fit our JupyterHub needs at the CRC:

### Jupyterlab container customizations
- Starting by the configuration of jupyterlab container ([Dockerfile](./jupyterlab/Dockerfile)), we used a recent docker image (jupyter/tensorflow-notebook:python-3.10) that includes Python3.10 and the commonly used packages in machine and deep learning.
- Install linux packages that might be need for running the image (via ```apt install```).
- Install python packages that might be need for running the image including ([nb_conda_kernels](https://github.com/Anaconda-Platform/nb_conda_kernels)) which is used to manage kernels for JupyterLab/Jupyter Notebook. 
- Prepare a configuration file for jupyter named "jupyter_config.json" with following contents:
```
{
  "CondaKernelSpecManager": {
    "kernelspec_path": "--user"
  }
}
```
and place it in the same directory as the ([Dockerfile](./jupyterlab/Dockerfile)).
- Add a line in the ([Dockerfile](./jupyterlab/Dockerfile)) to copy the configuration file to the container (```COPY ./jupyter_config.json /home/jovyan/.jupyter/jupyter_config.json```).
- You can test this container directly through running:
```podman-compose build jupyterlab``` then ```podman run --rm -p 8888:8888 jupyterlab_img```
and visit the generated tokenized link (looks like:  http://127.0.0.1:8888/?token=xyz) to test jupyterlab.

### Jupyterhub container customizations
- Starting by the configuration of jupyterhub container ([Dockerfile](./jupyterhub/Dockerfile)), we used a recent docker image (jupyterhub/jupyterhub:4.0.2).
- Install custom python plugins and dependencies via ```pip install```.
- Configure environment so containers are managed by podman instead of docker (requires adding a volume in [docker-compose.yml](docker-compose.yml)).
  ```
    ENV DOCKER_HOST=unix:///var/run/docker.sock
  ```
- Edit the [jupyterhub_config.py](./jupyterhub/jupyterhub_config.py) to include the following:
  - Add the following lines to the top of the file to import the required modules:
  ```
    import os
    import sys
    
    c = get_config()
    
    ## Generic
    c.JupyterHub.admin_access = True
    c.JupyterHub.hub_ip = os.environ['HUB_IP']
  ```
  
  - Add authenticator configuration:
  ```
    c.JupyterHub.authenticator_class = 'crc_jupyter_auth.RemoteUserAuthenticator'
    c.Authenticator.required_vpn_role = 'SAM-SSLVPNSAMUsers'
    c.Authenticator.missing_user_redirect = 'https://crc.pitt.edu/Access-CRC-Web-Portals'
    c.Authenticator.missing_role_redirect = 'https://crc.pitt.edu/Access-CRC-Web-Portals'
  ```
  
  - Add the docker spawner configuration:
  ```
    ## Spawners
    c.Spawner.default_url = '/lab'
    c.Spawner.debug = True
    c.Spawner.cpu_limit = 1
    c.Spawner.mem_limit = '4G'
    
    # Docker spawner
    # Common convention is to mount mounting user home directories under /home/jovyan/work
    c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
    c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
    c.DockerSpawner.notebook_dir = '/home/jovyan/work'
    c.DockerSpawner.volumes = {'jupyterhub-user-{username}': '/home/jovyan/work'}
    c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
  ```
  
  - Add the following lines to the end of the file to configure the JupyterHub idle culler role and service:
  ```
    ## Services
    c.JupyterHub.load_roles = [
        {
            "name": "jupyterhub-idle-culler-role",
            "scopes": [
                "list:users",
                "read:users:activity",
                "read:servers",
                "delete:servers",
            ],
            "services": ["jupyterhub-idle-culler-service"],
        }
    ]
    
    c.JupyterHub.services = [
        {
            "name": "jupyterhub-idle-culler-service",
            "command": [sys.executable, "-m", "jupyterhub_idle_culler", "--timeout=3600" ],
        }
    ]
  ```
### Customizations for the compose configuration
- The main configuration file for Docker Compose is [docker-compose.yml](docker-compose.yml), which configures all containers (services, in Compose jargon), and associated volumes and networks.
- Services:
  - JupyterHub configuration:
    - Mount the podman socket inside the container, so that it will be able to spawn containers for the single-user Jupyter servers.
    - Mount the JupyterHub configuration file inside the container, so that it will be able to read it.
    - Mount the JupyterHub data directory inside the container, so that it will be able to store its data persistently.
    - Set some environment variables for the Hub process, they will be used in the Hub configuration file [jupyterhub_config.py](./jupyterhub/jupyterhub_config.py):
      - DOCKER_JUPYTER_IMAGE is the name of the Docker image for the single-user servers; this must match the image configured in the jupyterlab section of docker-compose.yml (see below).
      - DOCKER_NETWORK_NAME is the name of the Docker network used by the services; normally, this network gets an automatic name from Docker Compose, but the Hub needs to know this name to connect the single-user servers to it.
      - DOCKER_NOTEBOOK_DIR is the directory inside the single-user server containers where the user's home directory will be mounted.
      - HUB_IP is the IP address of the Hub service within the docker network. By using the container_name Compose directive, we can set an alias for the IP, and use the same for HUB_IP.
    - Set the restart policy to always, so that the Hub container will be restarted automatically if it crashes.
    - Set the network name to the same name as the one used in the Hub configuration env variable above.
  - JupyterLab configuration:
    - Mount the JupyterLab data directory inside the container, so that it will be able to store its data persistently.
    - Set the build name to jupyterlab.
    - Set the image name to jupyterlab_img.
    - Set the container name to jupyterlab-throwaway.
    - Set the network name to the same name as the one used in the Hub configuration env variable above.
- Volumes:
  - mount the jupyterhub_data volume to store the JupyterHub data persistently.
- Networks:
  - Create a Docker network with the same name used above for the Hub and Lab services for the services to communicate with each other.

## Run!

Once you are ready, build and launch the application with

```
docker-compose build
docker-compose up -d
```

Read the [Docker Compose manual](https://docs.docker.com/compose/) to
learn how to manage your application.
