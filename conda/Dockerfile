FROM ubuntu:18.04
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN apt-get update && apt-get install -y curl grep sed dpkg wget \
libsensors4 libllvm9 libglapi-mesa libexpat1 libelf1 libdrm2 libdrm-radeon1 libdrm-nouveau2 libdrm-intel1 libdrm-amdgpu1 \
libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 \
libgl1-mesa-dri bzip2 libglib2.0-0 libxext6 libsm6 libxrender1 \
git mercurial subversion  iputils-ping vim inetutils-tools telnet net-tools cifs-utils keyutils \
sudo unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc openssh-server sssd libsasl2-dev g++
RUN export DEBIAN_FRONTEND=noninteractive && apt-get install -y  krb5-user
RUN groupadd -g 2100 labuser  && useradd -u 2100 -d /home/labuser -ms /bin/bash -g labuser -G labuser -p "$(openssl passwd -1 labuser123)" labuser
RUN mkdir -p /home/labuser /lab_related && chown -R labuser:labuser /home/labuser /lab_related && chmod -R 775 /home/labuser /lab_related
RUN chmod g+s /lab_related
USER labuser
WORKDIR /home/labuser

ADD ./conda/Anaconda3.sh .
RUN /bin/bash ~/Anaconda3.sh -b -p /home/labuser/single_server/conda
USER root
RUN ln -s /home/labuser/single_server/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
USER labuser
RUN echo ". /home/labuser/single_server/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    echo 'export PATH=/home/labuser/single_server/conda/bin:$PATH' >> ~/.bashrc && \
    echo "export SHELL=/bin/bash" >> ~/.bashrc && \
    echo 'if [ -f ~/.custom_bashrc ]; then source ~/.custom_bashrc ; fi' >> ~/.bashrc
#Below is to overcome certificate issue  and adding conda channel as the exact url instead of conda-forge works because 
#etc/resolv.conf is not set for google DNS , hence some of the websites are not resolved 
#but cannot set the nameserver on docker as it overrides if configured for a network hence set in conda itself
RUN /home/labuser/single_server/conda/bin/conda config --set ssl_verify False
RUN /home/labuser/single_server/conda/bin/conda config --add channels https://conda.anaconda.org/conda-forge/
RUN /home/labuser/single_server/conda/bin/conda update conda
RUN /home/labuser/single_server/conda/bin/conda install -y jupyter jupyterhub=1.0.0 configurable-http-proxy=4.0.1 pandasql tensorflow pymysql basemap \
    spacy
RUN  /home/labuser/single_server/conda/bin/python -m pip install --no-cache pyhive thrift sasl thrift-sasl pyspark==2.3.0
USER root
RUN TINI_VERSION="0.18.0" && wget -O tini.deb https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb --no-check-certificate && \
    dpkg -i tini.deb && \
    rm tini.deb
ADD ./conda/LABSUDO /etc/sudoers.d/
RUN chmod 440 /etc/sudoers.d/LABSUDO
RUN echo 'root:labuser123carry' |chpasswd
USER labuser
RUN rm  ~/Anaconda3.sh
RUN mkdir -p /home/labuser/workspace/windows_drive
##env set is required , else the command from jupyterhub will not work while spawning
ENV PATH /home/labuser/single_server/conda/bin:$PATH
ENV SHELL /bin/bash
RUN /home/labuser/single_server/conda/bin/conda config --set ssl_verify True
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
