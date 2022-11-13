#!/bin/bash

set -e

##############################################
###    installing docker with utilities    ###

apt-get update -y
apt-get install -y \
  apt-transport-https \
  ca-certificates \
  openssh-client \
  curl \
  wget \
  software-properties-common \
  gnupg \
  lsb-release
  
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker.master.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker.master.gpg] https://download.docker.com/linux/ubuntu $(lsb-release -cs) stable" \
| tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io

########################################
###  installing python with utils    ###

apt-get -qqy update && apt-get install -qqy \
  gcc \
  python3-dev \
  python3-setuptools \
  python3-pip \
  python3.8-venv \
  python3-crcmod \
  python-apt \
  libcairo2-dev \
  pkg-config \
  libgirepository1.0-dev \
  libcurl4-openssl-dev \
  libssl-dev \
  gnupg \
  zip \
  jq
  
pip3 install --upgrade pip

##############################################
###  installing gcloud with dependencies   ###

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
| tee /etc/apt/sources.list.d/cloud-google-sdk.list

wget --no-check-certificate -O- https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

apt-get update -y
apt-get install -y cloud-google-sdk
gcloud config set core/disable_usage_reporting true
gcloud config set component_manager/disable_update_check true
gcloud config set metrics/environment github_docker_image

########################################
###  installing nodejs with utils    ###

curl -sL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

apt-get update -y
apt-get install -y yarn

npm install -y n
n lts
PATH="$PATH"

node -v
npm -v

#############################################
###  add extra updates after this line    ###

echo "all updates were installed"









