title: Use Docker to Test and Deploy Python Web Apps
slug: python-web-docker-deploy
summary: Use Docker to test apps on your local PC and then use Docker to easily deploy them to a virtual private server (VPS)
date: 2023-09-30
modified: 2023-09-30
category: Docker
<!--status: Published-->

Using Docker containers to test an existing Flask application locally, and then use Docker to deploy it to a remote server.

## Test the existing web app

First, get the first version of my [usermapper-web application]({filename}\articles\003-flask-web-app-tutorial\flask-web-app-tutorial.md) from Github. It's tagged as vesion 0.1 so run the following commands to get the application files.

```
$ wget https://github.com/blinklet/usermapper-web/archive/refs/tags/v0.1.tar.gz
$ tar -xvf v0.1.tar.gz
```

The application files will be uncompressed into a folder named *usermapper-web-0.1/*.

```bash
$ cd usermapper-web-0.1
$ ls
application.py
LICENSE
README.md
requirements.txt
templates
```

Create a Python virtual environment in the same folder:

```bash
$ python3 -m venv env
$ source env/bin/activate
(env) $
```

Install the application's dependencies:

```bash
(env) $ pip install -r requirements.txt
```

The application needs two more things: a [dotenv file]({filename}/articles/011-use-environment-variables/use-environment-variables.md) and a *downloads* directory. The both the dotenv file and the *downloads* directory must be in the same location as the *application.py* file.

Create the dotenv file, named *.env*, using your favorite text editor:

```bash
$ nano .env
```

Add the following environment variables to the file:

```
FLASK_APP=application
FLASK_ENV=development
SECRET_KEY=temporarykey
```

Save .env file

```bash
$ mkdir downloads
```


Run the Flask app

```
(env) $ flask run
```

Test the application. Enter the application's URL in a browser window. A Flask app like this should be running on the *localhost* loopback address on TCP port 5000:

```text
http://localhost:5000
```

The browser window should show the web app's first page:

![Usermapper Web App running on local PC in development mode]({attach}usermapper-01.png)

For more information about the web app and how to use it, either refer to the instructions on the web page or read [my web app tutorial post]({filename}/articles/003-flask-web-app-tutorial/flask-web-app-tutorial.md).

After you finish testing the *usermapper-web* application, quit the Flask app by typing *CTRL-C* in the terminal window.

And, deactivate the virtual environment:

```bash
(env) $ deactivate
```


## Deploy existing application to Docker container



In my webapp tutorial post, I described how to deploy the application to a Microsoft Azure web app service simply by copying a projects files and directories to an Azure web app. That remains a great way to deploy web apps, if you want to use Microsoft Azure's proprietary tools.

In this post, I will show you a more general-purpose way to deploy a web app that will run anywhere, including on a virtual private server (VPS) started on any cloud provider. This requires that you take more responsibility for the way to package your application and for running other services that help serve and secure your application. You will have to add a production-ready WSGI server to your application's environment, add some Docker files in our project directory, and set up production environment variables.

you will copy the application code to a Docker image that can be deployed either to a container running locally or one running on a remote server.

### Get files and set up virtual environment

Create a new project directory and then copy the *usermapper-web* files into it:

```bash
$ mkdir ../usermapper-web
$ cp -r . ../usermapper-web
$ cd ../usermapper-web
```


### Add gunicorn

The current program uses the Flask development server to run the web app. You should not use the Flask development server on a real web deployment. Install a [production-ready WSGI server](https://flask.palletsprojects.com/en/2.3.x/deploying/), like [Gunicorn](https://gunicorn.org/). I like Gunicorn because it is a Python package, is easy to install, and is lightweight. 

To install Gunicorn in the container image, add it to *requirements.txt* file. The contents of the file should now be the same as shown below.

```text
wheel
flask
Flask-WTF
python-dotenv
bootstrap-flask
gunicorn
git+https://github.com/blinklet/usermapper.git@v0.3#egg=usermapper
```

### Create a *.env* file

The Flask frameworks needs some information from its environment so it knows which file to run. You can set environment variables on a server manually or you can store them in a file and access them using the Python *dotenv* package. If you cloned the *usermapper-web* project, you did not get the file, named *.env* that contains the environment variables for my version of the project. I do not keep the file in my repository because it contains a secret key.

Flask uses a secret key, that should not be shared, to help secure functions like reading inputs from Flask forms. To create a random key for yourself, run the following commands. 

```bash
$ cd usermapper-web
$ python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
```

The command requested a random key that is 32 bytes long. It shoud display on your terminal like the one shown below. 

```
D9Oci7p2l9bqM8_uChJKA09tqXFOK7Db-FxKr6rGoDk
```

Copy the secrte key and add it to your *.env* file. The new file should look like the following:

```python
FLASK_APP=application
FLASK_ENV=production
SECRET_KEY=D9Oci7p2l9bqM8_uChJKA09tqXFOK7Db-FxKr6rGoDk
```

It's a good idea to create an example dotenv file so, when you revisit your project in teh future, you can remember which environment variables you need. If you like, copy the *.env* file to a file named *dotenv.example* and replace the secret key with some dummy data.

### Create the Dockerfile

To create a Docker image that contains the Python packages we need and the *usermapper-web* application, write a Dockerfile that contains the commands needed to build the image. If you need more information, please see my previous post where I cover [building a Docker image]({filename}/articles/018-postgresql-docker/postgresql-docker.md).

In the Dockerfile, choose a base image. I chose an official Python image based on the *Alpine* Linux distribution, which is a very lightweight image. Then [document](https://stackoverflow.com/questions/22111060/what-is-the-difference-between-expose-and-publish-in-docker/47594352#47594352) the TCP port that the application expects to use. Create the app's working directory on the container. Copy the files from the current directory on your PC, which contains the Dockerfile and all the application files and directories, to the working directory on the container. Run Linux commands that install software needed by the application. Finally, set the command that the container will run when it starts up.

Create the Dockerfile using your favorite text editor. It's contents should look like those below:

```dockerfile
FROM python:alpine
EXPOSE 8080
WORKDIR /app
COPY . .
RUN apk update && \
    apk add git && \
    pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "application:app"]
```

Save the file and name it *Dockerfile*, which is a default name for a Dockerfile.

### Docker Ignore file

Next, create a *.dockerignore* file that tells Docker which files in the current directory should not be copied to the Docker image when you build it. You want to avoid copying Git repositories, Python cache files, Python virtual enironments, and unneeded project files.

Create a new file in your text editor, name it *.dockerignore*, and add the following contents to it:

```text
# Git files
.git
.gitignore

# Unneeded project files
.env.example
README*

# Python files
__pycache__
*.pyc
*.pyo
*.pyd

# Docker files
.dockerignore
Dockerfile
```

Note that the *downloads* sub-directory is needed for the application to work correctly. When Docker copies all files to the container, it also copies directories. 

### Build the application image

Build the new image by running the Docker *build* command and pointing it to the current directory (the final "dot" in the command). Tag the new image. I chose to tag my image with the name, *usermap:v1*.

```bash
$ docker build -t usermap:v1 .
```

After the build is completed, you should see it in your local images repository:

```
$ docker images
REPOSITORY                       TAG       IMAGE ID       CREATED          SIZE
usermap                          v1        e80b2504dcab   13 minutes ago   112MB
postgres                         latest    43677b39c446   7 days ago       412MB
mcr.microsoft.com/mssql/server   latest    683d523cd395   3 weeks ago      2.9GB
```

Notice how Docker labels what you might think is the image name as the "repository". The real image name is the combination of repository and tag. This will be important later when you want to create a private repository on Docker Hub.

### Test the image

To test that the image was built correctly and that the application will run correctly, create a new container from it. 

```bash
$ docker run --detach --publish 127.0.0.1:80:8080/tcp --name user1 usermap
```

The new container should start serving the web app, via the Gunicorn WSGI server which includes a basic HTTP server, 
Connect your browser to http://localhost

![]({attach}usermapper-01.png)

![]({attach}usermapper-02.png)


```
docker exec -it usermap1 ls -R ./downloads
./downloads:
tmp6qa2trde  tmpamu28g3y

./downloads/tmp6qa2trde:
user-mapping.xml

./downloads/tmpamu28g3y:
user-mapping.xml
```

# Tutorial

https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container?tabs=azure-cli&pivots=container-linux



az group create --name containers-rg --location eastus

<!--is this needed here? or in the identity section below?
az identity create --name brianID --resource-group containers-rg
-->

az acr create --name registorium --resource-group containers-rg --sku Basic --admin-enabled true

az acr credential show --resource-group containers-rg --name registorium

(The JSON output of this command provides two passwords along with the registry's user name.)

    username is "registorium"
    password is "Yb72ZpxhUUuUnadLlz+3wqGmsGJEJpTLf9fVbHfxQZ+ACRBfE+2P"
    password2 is "DCgNAqCue5M/d+IqeES0wYnm9+kQOaqDap6OkHHRlv+ACRDa1of+"


(usename is, by default, the same as the registry name)

docker login registorium.azurecr.io --username registorium

(will ask for a password. Use one of the passwords from the previous step)

<!-- try the following

PASSWD=$(az acr credential show --resource-group containers-rg --name registorium --output tsv --query passwords[0].value)

docker login registorium.azurecr.io --username registorium --password-stdin <<< $PASSWD
-->

docker tag usermap registorium.azurecr.io/usermap:latest

docker push registorium.azurecr.io/usermap:latest



(create web app)

az group create --name webapp-rg --location eastus

az appservice plan create --name brian-web-app-plan --resource-group webapp-rg --is-linux
'
az webapp create --resource-group msdocs-custom-container-tutorial --plan myAppServicePlan --name usermapper0001 --deployment-container-image-name registorium.azurecr.io/usermap:latest

(configure app)

az webapp config appsettings set --resource-group webapp-rg --name usermapper0001 --settings WEBSITES_PORT=8080

https://usermapper0001.azurewebsites.net




NOTE: if access expires, is it renewed with the command:
az acr update --name registorium --admin-enabled true
?


try

az appservice plan create --name brian-web-app-plan --resource-group webapp-rg --is-linux

(configure app)

az webapp config appsettings set --resource-group webapp-rg --name usermapper0001 --settings WEBSITES_PORT=8080




# Troubleshooting

Turn on logs

az webapp log config --name usermapping0001 --resource-group webapp-rg --docker-container-logging filesystem

Get logs at:

https://usermapping0001.scm.azurewebsites.net/api/logs/docker





clean up
az group delete --name webapp-rg --no-wait --yes --verbose

















(the rest enables easy updates using CI/CD and web hook)

(create Principle)

principalId=$(az identity show --resource-group containers-rg --name brianID --query principalId --output tsv)

registryId=$(az acr show --resource-group containers-rg --name registorium --query id --output tsv)

az role assignment create --assignee $principalId --scope $registryId --role "AcrPull"

(enable identity)


id=$(az identity show --resource-group msdocs-custom-container-tutorial --name brianID --query id --output tsv)
az webapp identity assign --resource-group msdocs-custom-container-tutorial --name <app-name> --identities $id

(anable app to pull container)

appConfig=$(az webapp config show --resource-group msdocs-custom-container-tutorial --name <app-name> --query id --output tsv)
az resource update --ids $appConfig --set properties.acrUseManagedIdentityCreds=True

clientId=$(az identity show --resource-group msdocs-custom-container-tutorial --name brianID --query clientId --output tsv)
az resource update --ids $appConfig --set properties.AcrUserManagedIdentityID=$clientId














# Push image to a private repo

Because image contains secrets

<!--
```bash
$ docker tag usermap blinklet/usermap
$ docker login
$ docker push blinklet/usermap
```
-->

Azure OCI

https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli

```
az login

az group create --location eastus --name artifactsRG

az acr create --resource-group artifactsRG \
  --name registorium --sku Standard
```

Login https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#individual-login-with-azure-ad

Login and get token (used for docker login later with admin user)
```
TOKEN=$(az acr login --name registorium --expose-token --output tsv --query accessToken)
```

Tag and push

```
docker tag usermap registorium.azurecr.io/usermap

docker push registorium.azurecr.io/usermap
```

List images

```
az acr repository list --name registorium --output table
```
```
Result
--------
usermap
```


# Run on ACI???

Azure Container Instances

https://docs.docker.com/cloud/aci-integration/

looks simple but is not in free tier. All contianer deployment options in Azure are discussed here, wrt to pricing
https://jussiroine.com/2021/12/running-a-single-docker-container-in-azure-cost-effectively/


# web app for containers

https://learn.microsoft.com/en-us/azure/app-service/quickstart-custom-container?tabs=dotnet&pivots=container-windows-cli


https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops&tabs=python%2Cyaml

```
az group create --name usermapRG --location eastus

az appservice plan create \
  --resource-group usermapRG \
  --location eastus \
  --name usermapPlan2 \
  --sku F1 \
  --is-linux
```

Need admin user to deploy container to app service
https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#admin-account


az acr update -n registorium --admin-enabled true

$ docker login registorium.azurecr.io --username 00000000-0000-0000-0000-000000000000 --password-stdin <<< $TOKEN



az webapp create \
  --name usermapApp \
  --plan usermapPlan \
  --resource-group usermapRG \
  --deployment-container-image-name registorium.azurecr.io/usermap
```

After deployment, your app is available at http://<app-name>.azurewebsites.net.

```
az webapp delete --name usermapApp --resource-group usermapRG
```

# Run on VPS

web apps are always free

https://learn.microsoft.com/en-us/training/modules/deploy-run-container-app-service/2-build-store-images

but, every service will do it differently. VPS's require more responsibility but work relativbely the same in most services.

However, this is the easiest way to securely assign secrets (VPS would need Docker Swarm or Kubernetes to securely inject environment variables at run time, which is overkill for our simple web app.)



or run on a VPS that is free for 12 months, about $5 per month after that

Azure B1s burstable VM

https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli


<!--
securely deploy docker container to server

https://jfrog.com/devops-tools/article/3-steps-to-securing-your-docker-container-deployments/#:~:text=3%20Essential%20Steps%20to%20Securing%20Your%20Docker%20Container,3%203.%20Keep%20Your%20Images%20Lean%20and%20Clean

https://www.equalexperts.com/blog/tech-focus/quick-wins-to-secure-your-docker-containers/

https://stackoverflow.com/questions/39855304/how-to-add-user-with-dockerfile
-->


```
export RESOURCE_GROUP_NAME=usermapRG
export LOCATION=eastus
export VM_NAME=usermapVM
export VM_IMAGE=Ubuntu2204
export VM_SIZE=Standard_B1s
export ADMIN_USERNAME=usermap67

az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

az vm create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $VM_NAME \
  --size $VM_SIZE
  --image $VM_IMAGE \
  --admin-username $ADMIN_USERNAME \
  --generate-ssh-keys \
  --public-ip-sku Standard

az vm run-command invoke \
   --resource-group $RESOURCE_GROUP_NAME \
   --name $VM_NAME \
   --command-id RunShellScript \
   --scripts "sudo apt-get update && sudo apt-get install -y nginx"


az vm open-port --port 80 --resource-group $RESOURCE_GROUP_NAME --name $VM_NAME

#### Get IP address

export IP_ADDRESS=$(az vm show --show-details --resource-group $RESOURCE_GROUP_NAME --name $VM_NAME --query publicIps --output tsv)

az group delete --name usermapRG --no-wait --yes --verbose




# Add domain name

https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate





on server, use sample compose file:

https://github.com/docker/awesome-compose/blob/master/nginx-wsgi-flask/compose.yaml

