# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
# c.JupyterHub.authenticator_class = 'oauthenticator.LocalGitHubOAuthenticator'
# c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = False

# Disabling open_signup
c.NativeAuthenticator.enable_signup = True

# Disable common passwords
c.NativeAuthenticator.check_common_password = True

# Specify minimum password length
c.NativeAuthenticator.minimum_password_length = 8

# Block user after 3 failed logins:
c.NativeAuthenticator.allowed_failed_logins = 3
# SO user has to wait 10 minutes before trying again:
c.NativeAuthenticator.seconds_before_next_try = 600 # in seconds

# Signup allow self-approval via email
c.NativeAuthenticator.allow_self_approval_for = '[^@]+@(unileoben|stud.unileoben)\.ac\.at$' # regex working for both unileoben.ac.at and stud.unileoben.ac.at addresses. source chatllama
c.NativeAuthenticator.secret_key = "JSwzZ1oFLzT7cPrEibQiBQlAMgJLDKU6NvWZVNIlrF+ncrthA9gOUkbNmkwWgEd3HrYXi/PRgIli8wmep7zVBw=="
c.NativeAuthenticator.self_approval_email = ("admin@ai-lab.science", "JupyterHub Approval", "This is an automated message from the Chair of Cyber Physical Systems. \nTo authorize your new JupyterHub user account, please follow this link: \n\nhttps://jupyter.cps.unileoben.ac.at{approval_url}")
c.NativeAuthenticator.self_approval_server = {'url': 'mail.lima-city.de', 'usr': 'admin@ai-lab.science', 'pwd': 'Exp3rtActionDep4r7mentOp3rationF4c3s'}

# Ask for email
c.NativeAuthenticator.ask_email_on_signup = True

# Two factor Authenticate
c.NativeAuthenticator.allow_2fa = True

# Enforce SSL internally
#c.JupyterHub.internal_ssl = True

# ReCaptcha Security
# c.NativeAuthenticator.recaptcha_key = "6Ld6sDkoAAAAAPxDmN3RwbxrOPyiBbzIz0FyYvV7"
# c.NativeAuthenticator.recaptcha_secret = "6Ld6sDkoAAAAANiBXjzlnkAdgJes-krPhwAZzgYW"

# Change Logo
c.JupyterHub.logo_file = '/logo.png' # logo.png is located in the same directory as jupyterhub_config.py and represents the cps logo

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin] # replaced admin with cpsadmin
