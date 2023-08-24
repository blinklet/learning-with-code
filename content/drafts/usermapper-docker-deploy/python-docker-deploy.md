title: Use Docker to Test and Deploy Python Web Apps
slug: python-web-docker-deploy
summary: Use Docker to test apps on your local PC and then use Docker to easily deploy them to a virtual private server (VPS)
date: 2023-09-31
modified: 2023-09-31
category: Docker
<!--status: Published-->



## Deploy existing application to Docker container

Use Python container?

### Get files and set up virtual environment

```bash
$ git clone https://github.com/blinklet/usermapper-web.git
```
### Add gunicorn

Dont use dev server in web deployment so run gunicorn, Add it to requirements.txt

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
FLASK_ENV=development
SECRET_KEY=D9Oci7p2l9bqM8_uChJKA09tqXFOK7Db-FxKr6rGoDk
```

Docker image

<!--
```dockerfile
# Use the Python Docker image's bookwork tag
# because we need an image that also has git installed
FROM python:bookworm
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# The application expects a "downloads" directory
RUN mkdir ./downloads
ENTRYPOINT [ "flask" ]
CMD ["run" ]
```
-->


```dockerfile
FROM python:alpine
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN apk update && apk add git
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# The application expects a "downloads" directory
RUN mkdir ./downloads
ENTRYPOINT [ "flask" ]
CMD ["run" ]
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


```
$ docker logs usermap1
/usr/src/app/application.py:13: UserWarning: For Bootstrap 4, please import and use "Bootstrap4" class, the "Bootstrap" class is deprecated and will be removed in 3.0.
  bootstrap = Bootstrap(app)
 * Serving Flask app 'application'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
/usr/local/lib/python3.11/site-packages/flask_bootstrap/templates/bootstrap/form.html:14: UserWarning: For Bootstrap 4, please import macros from "bootstrap4/" path (e.g. "from 'bootstrap4/form.html' import render_form"), the "bootstrap/" path is deprecated and will be removed in version 3.0.
127.0.0.1 - - [23/Aug/2023 22:37:08] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2023 22:37:08] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [23/Aug/2023 22:39:09] "POST / HTTP/1.1" 302 -
127.0.0.1 - - [23/Aug/2023 22:39:09] "GET /download_page/tmp6qa2trde HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2023 22:40:18] "GET /download/tmp6qa2trde/user-mapping.xml HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2023 22:41:25] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2023 22:45:26] "POST / HTTP/1.1" 302 -
127.0.0.1 - - [23/Aug/2023 22:45:26] "GET /download_page/tmpamu28g3y HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2023 22:46:21] "GET /download/tmpamu28g3y/user-mapping.xml HTTP/1.1" 200 -
```

```bash
$ docker tag usermap blinklet/usermap
$ docker login
$ docker push blinklet/usermap
```


# Run on VPS

web apps are always free

https://learn.microsoft.com/en-us/training/modules/deploy-run-container-app-service/2-build-store-images

but, every service will do it differently. VPS's require more responsibility but work relativbely the same in most services.

However, this is the easiest way to securely assign secrets (VPS would need Docker Swarm or Kubernetes to securely inject environment variables at run time, which is overkill for our simple web app.)



or run on a VPS that is free for 12 months, about $5 per month after that

Azure B1s burstable VM

https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli

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

az group delete --name usermaprg --no-wait --yes --verbose

