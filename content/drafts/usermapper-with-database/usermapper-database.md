maybe use Redis, which can automatically timeout data?

json-ify the usermapper xml?

xml native in database???

How to return a file from DB??
https://stackoverflow.com/questions/60499958/what-is-the-best-way-to-store-an-xml-file-in-a-database-using-sqlalchemy-flask

https://realpython.com/flask-connexion-rest-api/
https://realpython.com/flask-connexion-rest-api-part-2/
https://realpython.com/flask-connexion-rest-api-part-3/


using capriver paas
https://levelup.gitconnected.com/using-docker-and-digitalocean-to-host-a-simple-flask-app-5d78c9f50ba4

https://www.linode.com/docs/guides/flask-and-gunicorn-on-ubuntu/

https://blog.logrocket.com/build-deploy-flask-app-using-docker/

https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops&tabs=python%2Cyaml

https://www.digitalocean.com/community/tutorials/how-to-deploy-a-go-web-application-with-docker-and-nginx-on-ubuntu-18-04

process seems to be:
1) develop locally in virtual environment
2) create requirements file
3) dockerfile copies code to image, runs python app
4) push image hub
5) web service gets image from hub and compose file via scp and runs "compose up"

ensure system works if vps is restarted:
https://stackoverflow.com/questions/30449313/how-do-i-make-a-docker-container-start-automatically-on-system-boot


flask sessions
https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/


Use StringIO 
https://stackoverflow.com/questions/44672524/how-to-create-in-memory-file-object


## Deploy existing application to Docker container

Use Python container?

### Get files and set up virtual environment

```bash
$ git clone https://github.com/blinklet/usermapper-web.git
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

```bash
$ docker build -t usermap .
```

```bash
$ docker run --detach --rm --name usermap1 usermap
```





### Create image from 


Virtual environment

```bash
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r usermapper-web/requirements.txt
```