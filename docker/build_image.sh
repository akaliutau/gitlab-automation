#!/bin/bash

$IMAGE_VER = $(git master)

TAG=$DOCKER_REGISTRY/$GROUP/runner-custom-image:$IMAGE_VER

docker login -u $GITLAB_USER -p $GITLAB_PWD $DOCKER_REGISTRY

docker build -t $TAG -f Dockerfile --label githash=$IMAGE_VER

docker push $TAG



