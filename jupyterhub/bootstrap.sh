#!/bin/bash

USER=$1
if [ "$USER" == "" ]; then
    exit 1
fi
# ----------------------------------------------------------------------------


# Start the Bootstrap Process
echo "bootstrap process running for user $USER ..."

# Base Directory: All Directories for the user will be below this point
BASE_DIRECTORY=/hub_home/jupyterhub/shared_notebooks
BASE_PERSONAL_DIRECTORY=/hub_home/jupyterhub/personal_notebooks

# User Directory: That's the private directory for the user to be created, if none exists
USER_DIRECTORY=$BASE_DIRECTORY/$USER
USER_PERSONAL_DIRECTORY=$BASE_PERSONAL_DIRECTORY/$USER
if [ -d "$USER_DIRECTORY" ]; then
    echo "...directory for user already exists. skipped"
    #exit 0 # all good. nothing to do.
else
    echo "...creating a directory for the user: $USER_DIRECTORY"
    mkdir $USER_DIRECTORY
    groupadd -g 2100 labuser||: 
    chown -R 2100 $USER_DIRECTORY
    chgrp -R 2100 $USER_DIRECTORY ###note , we cannot add ldap group into a pam user
    chmod -R 775 $USER_DIRECTORY
    touch -m /srv/jupyterhub/user_info/$USER
    # mkdir did not succeed?
    #if [ $? -ne 0 ] ; then
    #    exit 1
    #fi
fi
if [ -d "USER_PERSONAL_DIRECTORY" ]; then
    echo ".. personal directory exists , skipped"
    exit 0
else
    echo "...creating a directory for the user: $USER_PERSONAL_DIRECTORY"
    mkdir $USER_PERSONAL_DIRECTORY
    chown -R 2100 $USER_PERSONAL_DIRECTORY
    chmod -R 700 $USER_PERSONAL_DIRECTORY
    ls -ld $USER_DIRECTORY
    #touch -m /srv/jupyterhub/user_info/$USER 
fi
exit 0
