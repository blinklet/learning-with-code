title: Web app with database
slug: web-app-database-python
summary: tbd
date: 2023-08-07
modified: 2023-08-07
category: Databases
status: draft

maybe use Redis, which can automatically timeout data?

json-ify the usermapper xml?

xml native in database???

How to return a file from DB??
https://stackoverflow.com/questions/60499958/what-is-the-best-way-to-store-an-xml-file-in-a-database-using-sqlalchemy-flask

https://realpython.com/flask-connexion-rest-api/
https://realpython.com/flask-connexion-rest-api-part-2/
https://realpython.com/flask-connexion-rest-api-part-3/

multiple-container apps
https://docs.docker.com/get-started/07_multi_container/


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

