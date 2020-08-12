# The proxy is in another container
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.api_url = 'http://proxy:8001'
# tell the hub to use Dummy Auth (for testing)
#c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# The Hub should listen on all interfaces,
# so user servers can connect
c.JupyterHub.hub_ip = '0.0.0.0'
# this is the name of the 'service' in docker-compose.yml
c.JupyterHub.hub_connect_ip = 'hub'
# this is the network name for jupyterhub in docker-compose.yml
c.DockerSpawner.network_name = 'lab_setup_jupyterhub-net'

import os
import shutil
def create_dir_hook(spawner):
    """ Create directory """
    username = spawner.user.name  # get the username
    volume_path = os.path.join('/hub_home/jupyterhub', username)
    if not os.path.exists(volume_path):
        os.mkdir(volume_path, 0o755)

from subprocess import check_call
import os
def my_script_hook(spawner):
    username = spawner.user.name # get the username
    script = os.path.join(os.path.dirname(__file__), 'bootstrap.sh')
    check_call([script, username])

# attach the hook function to the spawner
c.Spawner.pre_spawn_hook = my_script_hook

#c.Spawner.pre_spawn_hook = create_dir_hook

# start jupyterlab
c.Spawner.cmd = ["jupyter", "labhub"]
##extra config is to ensure cifs mount else it wont work. This is optional
c.DockerSpawner.extra_host_config = {
    'security_opt': ['apparmor:unconfined'],
    'cap_add': ['SYS_ADMIN','DAC_READ_SEARCH']
}

c.Spawner.notebook_dir = '/home/labuser/workspace'
c.DockerSpawner.image = 'lab_setup_conda_image'

c.DockerSpawner.remove = True

c.DockerSpawner.volumes = { '/home/labuser/lab_data/shared_notebooks': '/home/labuser/workspace/shared_notebooks' ,
'/home/labuser/lab_data/personal_notebooks/{username}':'/home/labuser/workspace/{username}_personal',
'/home/labuser/lab_setup/conda/jdk':{"bind": '/usr/jdk64/jdk' , "mode": "ro"},
'/home/labuser/lab_setup/jupyterhub/user_info/{username}':{"bind": '/home/labuser/user_info/{username}', "mode": "ro" },
'/home/labuser/lab_setup/conda/.custom_bashrc':{"bind": '/home/labuser/.custom_bashrc', "mode": "ro" },
'/home/labuser/lab_setup/conda/labutils.py':{"bind": '/home/labuser/single_server/conda/lib/python3.7/site-packages/labutils.py' , "mode": "ro" }}

# debug-logging for testing
import logging
c.JupyterHub.log_level = logging.DEBUG
c.Spawner.start_timeout = 600
c.Spawner.http_timeout = 300
c.Spawner.consecutive_failure_limit = 0
c.Spawner.debug = True

##container cleaning steps
c.JupyterHub.shutdown_on_logout = True
####working scenario############
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
#c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator' ###enable this if you want ldap auth
c.LDAPAuthenticator.server_address = 'ldaps://ldaphost:636' #give ldap hostname
c.LDAPAuthenticator.user_attribute = 'sAMAccountName'
c.LDAPAuthenticator.lookup_dn = True
c.LDAPAuthenticator.lookup_dn_search_filter = '({login_attr}={login})'
c.LDAPAuthenticator.lookup_dn_search_password = 'putpasswordforserviceaccounthere'
c.LDAPAuthenticator.lookup_dn_user_dn_attribute = 'cn'

##testing scenario###
#c.LDAPAuthenticator.lookup_dn_search_user = 'serviceaccount'
c.LDAPAuthenticator.bind_dn_template = '{username}'
c.LDAPAuthenticator.user_search_base = 'OU=Offices,DC=officedomain,DC=net' ##change it based on individual preference
c.LDAPAuthenticator.use_lookup_dn_username = False 
