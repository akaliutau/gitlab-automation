# GCP Tooling API

# Pre-requisites

- gcloud (with non-null value of env var GOOGLE_APPLICATION_CREDENTIALS)
- npm
- python3.8
- account at GitLab 

# Creating sample application

To demonstrate how to work with containerized apps, we are going to use a simple node.js app

## Local run

```shell
cd ./app
npm install
node index.js
```

Go to localhost:8080 and observe "Hello, World!" simple web page

## Dockerize and publish app to GCR

```shell
sudo docker build -t nodejs-demo:1.0.0 .
sudo docker images
sudo docker run -ti --name nodejs-app -p 8080:8080 -d nodejs-demo:1.0.0
```

(In case of "container already running error", stop that container with command `sudo docker rm <container_id>`)

The last command will run the container with app in a daemon mode; it can also be visible using the docker command:

```shell
sudo docker ps

CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                       NAMES
6aadf0b63d2f   nodejs-demo   "docker-entrypoint.s…"   24 seconds ago   Up 23 seconds   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   nodejs-app
```

To stop container, type the command:

```shell
sudo docker stop 6aadf0b63d2f
```

After successful testing tag and publish docker to GCR:

```shell
GOOGLE_CLOUD_PROJECT=gcp-tooling-api
gcloud config set project gcp-tooling-api
gcloud services enable containerregistry.googleapis.com 
sudo docker tag nodejs-demo:1.0.0 eu.gcr.io/$GOOGLE_CLOUD_PROJECT/nodejs-demo:v1
sudo docker push eu.gcr.io/$GOOGLE_CLOUD_PROJECT/nodejs-demo:v1
```
To create GCP infrastructure with aforementioned simple app, use the script `gcp/create_insfrastructure.sh`

This script will do the following:

- create template for instance in instance group
- create managed instance group itself
- create and attach auto-scaling policy to instance group

# Building image for GitLab Runner

First for convinience create env variables `GITLAB_USERNAME`, `GITLAB_PASSWORD` to hold GitLab's docker registry creds (note, this is not the secure place to hold secrets and consider using providers); set docker registry url via `export GITLAB_DOCKER_REGISTRY=registry.gitlab.com`:

```
sudo nano ~/.profile
source ~/.profile
```
The following commands build and push image for GitLab runners

```
cd ./docker
export GROUP=<name of the group>
./build_image.sh
```

Note the image URL - it can be used now for GitLab Runners.

Create a GitLab trigger token (Settings -> CI/CD -> Pipeline triggers) and put it into `GITLAB_TOKEN` env variable.
Create a GitLab access token (PAT, User Settings -> Access Tokens) and put it into `PAT_TOKEN` env variable.
Create a `RUNNER_CUSTOM_IMAGE` env variable in CI/CD area:

```
curl --request POST --header "PRIVATE-TOKEN: $PAT_TOKEN" \
     "https://gitlab.com/api/v4/projects/41024544/variables" \
     --form "key=RUNNER_CUSTOM_IMAGE" \
     --form "value=registry.gitlab.com/automation299/gitlab-automation:a9316a0"
```


# Manipulating GCP resources via API




