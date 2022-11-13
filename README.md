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

First for convinience create env variables `GITLAB_USERNAME` and `GITLAB_PASSWORD` to hold GitLab's docker registry creds (note, this is not the secure place to hold secrets):

```
sudo nano ~/.profile
source ~/.profile
```
The following commands build and push image for GitLab runners

```
cd ./docker
docker build -t registry.gitlab.com/automation299/dmanager .
sudo docker login -u $GITLAB_USERNAME -p $GITLAB_PASSWORD registry.gitlab.com
```



# Manipulating GCP resources via API




