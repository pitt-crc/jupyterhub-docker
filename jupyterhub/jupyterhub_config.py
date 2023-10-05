"""JupyterHub configuration settings"""

import os
import sys

c = get_config()

## Generic
c.JupyterHub.admin_access = True
c.JupyterHub.hub_ip = os.environ['HUB_IP']


# Authentication
# These settings are specific to the CRC's proprietary authentication package `crc_jupyter_auth`
c.JupyterHub.authenticator_class = 'crc_jupyter_auth.RemoteUserAuthenticator'
c.Authenticator.required_vpn_role = 'SAM-SSLVPNSAMUsers'
c.Authenticator.missing_user_redirect = 'https://crc.pitt.edu/Access-CRC-Web-Portals'
c.Authenticator.missing_role_redirect = 'https://crc.pitt.edu/Access-CRC-Web-Portals'
c.Authenticator.admin_users = {'djp81', 'yak73', 'leb140'}

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

#c.ProfilesSpawner.profiles = [
#    ("Host Process", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip': '0.0.0.0'}),
#    #("Host Process", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip': '0.0.0.0'}),
#    # ("Teach Cluster - 1 gpu - 2 cpus, 3 hours", 'teach2c1g3h', 'batchspawner.SlurmSpawner',
#    # dict(req_runtime='3:00:00', req_cluster='teach', req_partition='gpu', req_options='-c 2 --mem=24G --gres=gpu:1', req_srun='')),
#]

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