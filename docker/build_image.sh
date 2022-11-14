#!/bin/bash

set -e

IMAGE_VER=$(git rev-parse --short HEAD)

TAG=$GITLAB_DOCKER_REGISTRY/$GROUP/gitlab-automation:$IMAGE_VER

echo building image $TAG

sudo docker login -u $GITLAB_USERNAME -p $GITLAB_PASSWORD $GITLAB_DOCKER_REGISTRY
sudo docker build -t $TAG -f Dockerfile --label githash=$IMAGE_VER .

sudo docker push $TAG



