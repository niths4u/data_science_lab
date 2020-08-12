# data_science_lab
This is a docker-compose file that will create a jupyterhub on port https://<hostname>:11110/.
This repo with few customisation is used with hadoop services integrated with kerberos , LDAP AD authentication , Hadoop and spark connectivity using thrift servers , RDBMS like MSSQL, PostgreSQL , MYSQL. I have added only the skeleton for bare minimum feature for data science activity. But within the data science , the dockerfile consists of almost all necessary data science tools.
  
### Features:
  1.  Can be used by small team to run data science tasks on server
  2.  Can perform custom installations without interfering work of other members
  3.  Use docker containers like use and throw mechanism with option to persist the notebook and work related files. 
  3.  Support LDAP authentication
  4.  Can share data across data science users 
  5.  Can support private files accessible only to the respective users
  6.  Scale across multiple servers

### Steps to be performed :   
  1.	create a user named labuser under /home/labuser with UID 2100
  2.	create a group named labuser and assign GUID 2100
  3.	create a group named docker and assign docker role to labuser
  4.	create folder named lab_data under /home/labuser and create two folders named personal_notebooks and shared_notebooks under lab_data
  5.  install docker
  6.  download this git repo under name lab_setup
  7.  download jdk1.8 and save it under /home/labuser/lab_setup/conda under the name jdk
  8.  download anaconda3 and save it under /home/labuser/lab_setup/conda under the name Anaconda3.sh
  9.  setup ssl certificates , copy key as server.key and cert file as server.crt and copy under /home/labuser/lab_setup/proxy
  10. go to /home/labuser/lab_setup/ and build the docker images and spin up the service using docker-compose files
  
### Customisations:
  1.  LDAP authentication supported , all configurations are in place, only need to fill up with right value
  2.  Kerberos supported : Contains all required packages. Simply chose the right sssd.conf and krb5.conf and add it into the image
  3.  Windows drive supported : Can be labutils.py gives a wrapper over the cifs mount command that can be performed inside docker container to access files



