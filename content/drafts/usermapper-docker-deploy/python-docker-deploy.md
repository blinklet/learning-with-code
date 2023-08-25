title: Use Docker to Test and Deploy Python Web Apps
slug: python-web-docker-deploy
summary: Use Docker to test apps on your local PC and then use Docker to easily deploy them to a virtual private server (VPS)
date: 2023-09-31
modified: 2023-09-31
category: Docker
<!--status: Published-->

Take an existing Flask application, then test and deploy it using Docker containers.

First get the first version of my [usermapper-web application]({filename}\articles\003-flask-web-app-tutorial\flask-web-app-tutorial.md) from Github

```
$ wget https://github.com/blinklet/usermapper-web/archive/refs/tags/v0.1.tar.gz
$ tar -xvf v0.1.tar.gz
```

Create a virtual environment:

```bash
$ cd usermapper-web-0.1
$ python3 -m venv env
$ source env/bin/activate
(env) $
```

Install the dependencies

```bash
(env) $ pip install -r requirements.txt
```

The application needs two more things: a dotenv file and a *downloads* directory. The both the dotenv file and the *downloads* directory must be in the same location as the *application.py* file.

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
(env) $ python3 application.py
```



## Deploy existing application to Docker container

Use Python container?

### Get files and set up virtual environment

```bash
$ git clone https://github.com/blinklet/usermapper-web.git
```
### Add gunicorn

git tag -a v0.1 cf41112 -m "First development release"



Don't use dev server in web deployment so run gunicorn, Add it to requirements.txt

```text
wheel
flask
Flask-WTF
python-dotenv
bootstrap-flask
gunicorn
git+https://github.com/blinklet/usermapper.git@v0.3#egg=usermapper
```

### Create .env file

Look at *.env.example* for inspiration

```bash
$ cd usermapper-web
$ python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
```

Output

```
D9Oci7p2l9bqM8_uChJKA09tqXFOK7Db-FxKr6rGoDk
```

Copy the output and create *.env* file

```python
FLASK_APP=application
FLASK_ENV=production
SECRET_KEY=D9Oci7p2l9bqM8_uChJKA09tqXFOK7Db-FxKr6rGoDk
```

Docker image


```dockerfile
FROM python:alpine
EXPOSE 8080
WORKDIR /app
COPY . .
RUN apk update && \
    apk add git && \
    pip install --no-cache-dir -r requirements.txt && \
    mkdir ./downloads
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "application:app"]
```

```bash
$ docker build -t usermap .
```

```
$ docker images
REPOSITORY                       TAG       IMAGE ID       CREATED          SIZE
usermap                          latest    e80b2504dcab   13 minutes ago   112MB
postgres                         latest    43677b39c446   7 days ago       412MB
mcr.microsoft.com/mssql/server   latest    683d523cd395   3 weeks ago      2.9GB
```

(Python:Alpine is only 52 MB but I had to add Git. If I properly package *usermapper* and upload it to PyPI, I could avoid installing Git and have an even smaller image. Or, if I copy the usermapper modules into the usermapper-web directory, I get the same effect but I don't want to mix up the two projects)

```bash
$ docker run --detach -rm --network host --port 5000:5000 --name usermap1 usermap
```

Connect browser to http://localhost:5000

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

