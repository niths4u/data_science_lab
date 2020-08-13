
# DATA SCIENCE LAB SETUP
## Using Jupyterhub through Dockerspawner on Linux environment


- **[Introduction](#introduction)** 
- **[Requirement](#requirement)**
- **[Assumption](#assumption)**
- **[Setting up system level users and groups](#setting-up-system-level-users-and-groups)**
- **[Folder setup](#folder-setup)**
- **[Docker Setup](#docker-setup)**
- **[Docker Related file setup](#docker-related-file-setup)**
- **[Setup certificate for jupyterhub](#setup-certificate-for-jupyterhub)**
- **[Build the docker images](#build-the-docker-images)**
- **[Start the lab](#start-the-lab)**
- **[Customization](#customization)**
- **[Advanced changes](#advanced-changes)**
- **[Scaling](#scaling)**



## Introduction

Over the years , I have seen people struggling to set up a right environment to run data science tasks. Usually it is built over multiple servers given by the IT team where the data science team works with available packages or go over to IT team requesting a new package, or the data science team uses their personal laptops to test and configure new packages which sometimes become too difficult to scale as data increases.

Data Science is an evolving field and it is never advisable to restrict data scientists to limited resources. Over my entire career , I have worked mainly as big data engineer and data scientist. I have also worked for some time as a DBA and an IT admin. There is a lot of problems lying around when it comes to communication from IT team and Data science team. Being a Data Scientist, I know our requirements and also the restrictions faced by an industry IT team trying to be compliant with security.

This article is focused to resolve few of such issues by setting up a lab environment where data scientists can install , update or even tear down the system trying to build new technology as well as IT team not having to worry about too much maintenance and system failures. You might have already guessed it right by now. If not, let me tell you that the solution is “jupyterhub using docker containers”.

The idea of this article is to give a small lab environment where data scientists can login using credentials configured by the lab environment . After login , the user will be given a docker container that consists of all required data science tools pre-built. The user has complete freedom to install any libraries they require and even can tear down the packages. As soon as the user logs out , the container is terminated. It is like a use and throw mechanism. User has options to persist their work if required and also share their work to other users. The reason why I do not recommend the traditional sudo spawner mechanism is because it is difficult to manage virtual environment where one user can install a library without affecting other user’s library requirement. I find it easier and reliable to use docker containers rather than virtual conda environments.


## Requirement

1. Create an environment for multiple users to login and run data science tasks
2. Freedom for each user to install libraries without affecting other users
3. Work will be terminated after use, but should have provision to persist files if required
4. Different Authentication module support. Here we have tested it for LDAP AD
5. Ability to map windows drive into the lab environment using cifs
6. Should use https rather than http
7. Should contain all packages for anaconda3 library and additional utility tools
8. Ability to scale up if required
9. Ability to maintain major chunk of lab environment by non-root user.


## Assumption

1. The instruction is for people to setup lab from scratch
2. Have root privilege to install and setup users
3. Machine is accessible via browser to connect to jupyterhub web URL
4. file-system has enough space to handle data. Minimum 50GB and 12 CPU
5. ports 12000–12010 , 11100 to 11110 are open via firewall.

## Setting up system level users and groups
1. Create a user and group called `labuser` and assign a specific `uid` and `guid` , say 2100. The number 2100 is important because going further docker containers will also be using same uid and guid to ensure the files persisted are accessible from host and vice versa
2. `groupadd -g 2100 labuser`
3. `useradd -u 2100 -d /home/labuser -ms /bin/bash -g labuser -p “$(openssl passwd -1 labuser123)” labuser` Feel free to change the password from *labuser123* to any password.

## Folder setup
   
- Create a folder that will contain all lab related data. This folder will act as the prime storage if we need a backup. This folder can be shared over multiple systems using NFS mount , this way it becomes easy to scale over more than one server
We can do this in two ways
  1. **First Method : Using separate volume and softlinks**
Create a folder named `labdata` in a separate volume and link that to `labdata` under `/home/labuser`. This is for people who want to ensure that data is persisted on separate volume. This is the recommended approach.Assuming we have a storage mounted as `/lab_related`. The steps would be
`mkdir /lab_related/lab_data`
`ln -s /lab_related/lab_data /home/labuser/`
`chown labuser:labuser /lab_related/lab_data`
  2. **Second Method : Normal creation of folder within the home folder**
If we do not have separate volume , then simply go ahead by creating a new folder in `/home/labuser`
- `mkdir /home/labuser/lab_data`
- `chown labuser:labuser /home/labuser/lab_data`
- Create 3 directories that will be used for persisting data science related tasks
  1. `mkdir /home/labuser/lab_data/shared_notebooks` — this is used for keeping notebooks to be shared across all data science users. This storage is permanent and will not be removed after container termination.
  2. `mkdir /home/labuser/lab_data/personal_notebooks` — this is used for keeping personal files that can be saved for later, but not shared with other users
  3. `cd /home/labuser/lab_data`
  4. `chown -R labuser:labuser shared_notebooks`
  5. `chown -R labuser:labuser personal_notebooks`


## Docker Setup

- create a new group : `groupadd docker`
- Add this group to labuser : `usermod -aG docker labuser`
- For Ubuntu :
  * `apt-get update`
  * `apt-get install docker-ce docker-ce-cli container.io`
- For Centos :
  * `sudo yum-config-manager — add-repo https://download.docker.com/linux/centos/docker-ce.repo`
  * `yum install docker-ce docker-ce-cli containerd.io`
- Install `docker-compose` , use `— insecure` only if your office has issues with certificate
  * `curl -L “https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)” -o /usr/local/bin/docker-compose --insecure`
  * `chmod +x /usr/local/bin/docker-compose`
  * `ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose`
- Make a directory to store all docker files , you can either link it from a mount volume or leave it as it is. This is an optional step for people who are concerned about docker default location being filled up
  * `mkdir /home/docker_fs`
  * edit the file `/lib/systemd/system/docker.service` and add like below
  * `ExecStart=/usr/bin/dockerd -g /home/docker_fs -H fd:// — containerd=/run/containerd/containerd.sock`
- After that start the docker `systemctl start docker`


## Docker Related file setup

Setup docker related files and folders. This is where we need to pull in the git files
- `mkdir -p /home/labuser/lab_data/docker_related`
- `chown -R labuser:labuser   /home/labuser/lab_data/docker_related`
- `cd /home/labuser/lab_data/docker_related`
- pull this repo **`https://github.com/niths4u/data_science_lab.git`** and save it with folder name `lab_setup` under the folder `/home/labuser/lab_data/docker_related`
- `ln -s /home/labuser/lab_data/docker_related/lab_setup /home/labuser/`
- `cd /home/labuser/lab_data/docker_related/lab_setup/conda`
- Download the anaconda repository file and store it in current location using `wget -O Anaconda3.sh https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`
- Download `jdk1.8` and save it as `jdk` in the current location, this will be the *java_home* directory inside docker. Note that I have tested this with `jdk1.8.0_112`.It is not mandatory , but required for tools in data science that needs `jdk`. Please follow relevant articles as to how to download `jdk`
- Note that in the dockerfile under `/home/labuser/lab_setup/conda/Dockerfile` , there is a section where the password of root is setup `echo 'root:labuser123carry' |chpasswd`. Please feel free to change *labuser123carry* to any password based on your organisational policy.


## Setup certificate for jupyterhub

It is always better to use https rather than http. It has few additional benefits like ability to pass through network layers that block websocket
If we have certificate , then just rename the cert and key file as server.crt and server.key and place it under /home/labuser/lab_data/docker_related/lab_setup/proxy
Otherwise, create a self-signed certificate with below steps. Inputs are not important , you can just keep whatever you know.

Follow the below steps to generate a cerfificate. 
- `su - labuser` . From here onwards all commands are run using labuser. This is to avoid unncessary use of root user and ability to have non-root user for maintenance activity in order to debug and administrate lab
-  `openssl genrsa -des3 -out server.key 1024` . Note to keep a passphrase while running this command
- `openssl req -new -key server.key -out server.csr`. Use the same passphrase used and type in relevant details : these are only for information purpose that will be stored in the certificate : 
- `cp server.key server.key.org`
- `openssl rsa -in server.key.org -out server.key`
- `openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt`
- This will generate a server.key and server.crt file. Copy those into */home/labuser/lab_data/docker_related/lab_setup/proxy* `cp server.key server.crt /home/labuser/lab_data/docker_related/lab_setup/proxy`


## Build the docker images

- from labuser : `cd /home/labuser/lab_setup`
- Type : `docker-compose build conda` to build the main data science docker file , this will take some time as the image file will be around 7GB
- Type: `docker-compose build hub` to build the hub that powers jupyterhub
- Alternatively you can also run `docker-compose build .`

## Start the lab

Starting the lab involves docker-compose utility. Please go through basic docker-compose commands to get a hang of it
- from labuser : `cd /home/labuser/lab_setup`
- Type : `docker-compose up -d`
- Connect to https://hostname:11110/ , login with any `dummy` user. The current configuration is set with *dummyauthentication* which means any dummy name with or without password will work. Please switch this over to ldap or any form of authentication to ensure more control over the lab.
**Note** : `docker-compose up -d` starts all service and detaches itself into background. You can always run `docker-compose logs -f` to view logs to understand what is happening in case of any issues. If you need to restart the same during initial configuration issues , use command `docker-compose down`. It will remove all services. After that issue the command `docker-compose up -d`


## Customization

- **Port change** : Go to *docker-compose.yaml* file and change the port under service proxy and put the one you would like to see. For example to change port from 11110 to 8888 , then change `11110:8080` to `8888:8000`
- **Authentication change**: Go to `/home/labuser/lab_setup/jupyterhub/jupyterhub_config.py` and put the right authentication module. As of now it is already supports *ldap authentication*. It only requires configuration settings. For example, to change to ldap authentication , comment out the line of dummy authenticator and use the *ldapauthentication* . Make sure to add all proper variables while enabling ldapauthenticator. I have specified few that are tested and working in my case.
`#c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'`
`c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator' ###enable this if you want ldap auth`


## Advanced changes

Things like Kerberos setup , hadoop and sql connectivity within docker etc are industry specific. The container already has all required parameters. It only requires configuration changes. I have setup spark to connect via spark-thrift server as well as livy server using kerberos ticket from the jupyter notebook within the container. Also tried connecting MS SQL server using ldap authentication. Mounted windows drive into docker using ldap auth through cifs protocol from jupyter notebook by wrapping the OS commands in a utility script package. Feel free to contact if you need any of these requirements, I should be able to help you out based on my experience on such tasks.


## Scaling

If you want to join more than one machine , There are two ways to handle it 
- **SWARM Method** we can deploy it on swarm node by changing dockerspawner to swarmspawner and network settings in docker-compose.yaml and jupyterhubconfig.py. Kubernetes is over engineering for small setup like this. Once the changes are performed swarm cluster where any number of servers can be added. 
- **Shared folder method** simply run all the initial steps on [Setting up system level users and groups](#setting-up-system-level-users-and-groups)  to create user and group covered previously , then go to installation of docker [Docker Related file setup](#docker-related-file-setup) and NFS mount the */lab_related folder* , set the softlinks and start the compose file . This will give two URLs but the data will be shared and hence from end user perspective it will only have URL change. To make it seamless , just add a load balancer on top of it. This way no one even needs to bother about URL changes. 

I have used swarm clusters to scale up our lab as well setup separate machine by sharing the lab files across using NFS mount.Both are fairly straightforward and easy to setup. I would prefer the latter method as it is easier and have more control because unlike large distributed systems requiring frequent addition and deletion , lab clusters are once in a while setup. So we need not add additional overhead to it using swarm or kubernetes cluster setup.

Feel free to contact if any help is required.
