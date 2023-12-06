#!/bin/bash

set -eo pipefail

echo "Starting SSSD..."
sudo systemctl start sssd.service

echo "Starting jupyterhub..."
jupyterhub

echo "Environment is ready"
exec "$@"
