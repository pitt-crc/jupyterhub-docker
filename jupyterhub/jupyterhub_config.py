# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import sys
import os
c = get_config()

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'
c.Spawner.debug = True
c.Authenticator.debug = True
## Authenticator
import crc_jupyter_auth
c.JupyterHub.authenticator_class = 'crc_jupyter_auth.RemoteUserAuthenticator'

# These settings are specific to authenticators provided by the crc_jupyter_auth package
c.Authenticator.required_vpn_role = 'SAM-SSLVPNSAMUsers'
c.Authenticator.missing_user_redirect = 'https://crc.pitt.edu/Access-CRC-Web-Portals'
c.Authenticator.missing_role_redirect = 'https://crc.pitt.edu/Access-CRC-Web-Portals'

c.Authenticator.admin_users = {'yak73', 'leb140'}

## Spawner

#####################
## Docker spawner
#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
#c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
#c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py

## user data persistence
#notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
#c.DockerSpawner.notebook_dir = notebook_dir
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

## Other stuff
#c.Spawner.cpu_limit = 1
#c.Spawner.mem_limit = '1G'

#####################


## Spawner profiles
# SlurmSpawner Batch Command Modifications
c.SlurmSpawner.batch_query_cmd = "squeue -M {cluster} -h -j {job_id} -o '%T %B'"
c.SlurmSpawner.batch_cancel_cmd = 'scancel -M {cluster} {job_id}'

import batchspawner

# wrapspawner
c.Spawner.ip = '0.0.0.0'
c.Spawner.notebook_dir = '~'
c.Spawner.env_keep = ['PATH', 'LD_LIBRARY_PATH', 'LIBRARY_PATH']
c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'
c.ProfilesSpawner.profiles = [
       	("Host Process", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip':'0.0.0.0'}),
        ("Teach Cluster - 1 gpu - 2 cpus, 3 hours", 'teach2c1g3h', 'batchspawner.SlurmSpawner',
            dict(req_runtime = '3:00:00', req_cluster = 'teach', req_partition = 'gpu', req_options = '-c 2 --mem=24G --gres=gpu:1', req_srun = '')),
]

c.JupyterHub.hub_ip = os.environ['HUB_IP']

## Services
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
        # "admin": True, # Only for hub<2.0
    }
]
