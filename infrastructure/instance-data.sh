#!/bin/bash

set -eu


## basic

# updating OS
echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
apt-mark hold linux-image-*
apt-get -y update
apt-get -y upgrade

# install
apt-get -y install \
  apt-transport-https \
  apt-utils \
  ca-certificates \
  curl \
  dialog \
  gnupg2 \
  htop \
  jq \
  lsb-release \
  nginx \
  snapd \
  sudo \
  supervisor \
  sysvbanner \
  unzip \
  vim \
  wget \
  zip


## user

# install
apt-get -y remove unscd

# user
useradd ${USER} -m -d /home/${USER} -s /bin/bash
echo -e "${USER}\n${USER}" | passwd ${USER}

# sudo
usermod -a -G sudo ${USER}
echo "${USER} ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers > /dev/null


## ssh

# ssh
mkdir -p /home/${USER}/.ssh/
cp /home/admin/.ssh/authorized_keys /home/${USER}/.ssh/authorized_keys
chmod 600 /home/${USER}/.ssh/authorized_keys

echo "${USER_SSH_CONFIG}" | tee -a /home/${USER}/.ssh/config > /dev/null
chmod 755 /home/${USER}/.ssh/config
cp /home/${USER}/.ssh/config /root/.ssh/config
chmod 755 /root/.ssh/config

# sshd_config
echo "${SSH_CONFIG}" | tee -a /etc/ssh/sshd_config > /dev/null
service ssh reload


## code

# dependencies
apt-get -y install \
  aptitude \
  apt-transport-https \
  apt-utils \
  build-essential \
  ca-certificates \
  curl \
  gcc \
  git \
  gnupg2 \
  g++ \
  htop \
  jq \
  locales \
  lsb-release \
  make \
  netcat-openbsd \
  openssh-client \
  python3 \
  python3-dev \
  python3-distutils \
  python3-pip \
  python3-venv \
  software-properties-common \
  sudo \
  supervisor \
  unzip \
  vim \
  wget \
  zip

# data
git clone --progress -b ${STAGE} https://github.com/cristhianclx/seek.demo.pe.git /home/${USER}/code/

# configure
python3 -m venv /home/${USER}/code/venv/
/home/${USER}/code/venv/bin/pip install --upgrade \
  pip \
  setuptools \
  wheel
/home/${USER}/code/venv/bin/pip install -r /home/${USER}/code/requirements.txt

# scripts
/home/${USER}/code/scripts/settings/${STAGE}.sh
/home/${USER}/code/scripts/migrations/run.sh
/home/${USER}/code/scripts/data.sh
/home/${USER}/code/scripts/static.sh

# supervisor
ln -sf /home/${USER}/code/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf


## nginx

# configure
mkdir -p /etc/nginx/sites-available/
mkdir -p /etc/nginx/sites-enabled/
echo "${NGINX_CONF}" > /etc/nginx/nginx.conf
echo "${NGINX_PROXY_PARAMS_CONF}" > /etc/nginx/proxy-params.conf
echo "${NGINX_SITES_AVAILABLE_DEFAULT}" > /etc/nginx/sites-available/default

# start
service nginx restart


## vim
echo "set mouse-=a" >> /root/.vimrc
echo "set mouse-=a" >> /home/${USER}/.vimrc


## permissions
chown -R ${USER}:${USER} /home/${USER}/*
chown -R ${USER}:${USER} /home/${USER}/.*


## deploy
supervisorctl reread
supervisorctl update
supervisorctl restart gunicorn


## ssh
rm -R /root/.ssh/
rm -R /home/admin/.ssh/


## motd
echo "
banner '${STAGE}'" >> /etc/bash.bashrc
