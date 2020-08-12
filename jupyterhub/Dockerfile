#ARG JUPYTERHUB_VERSION=1.0.0
FROM jupyterhub/jupyterhub:1.0.0
#RUN chmod 777 /tmp
COPY ./jupyterhub/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y ca-certificates curl grep sed dpkg wget iputils-ping vim inetutils-tools telnet net-tools sudo unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc
COPY ./jupyterhub/bootstrap.sh /srv/jupyterhub/bootstrap.sh
RUN chmod 755 /srv/jupyterhub/bootstrap.sh
#COPY ./jupyterhub/jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
