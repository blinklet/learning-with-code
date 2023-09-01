Write about how to develop and update apps with a docker workflow

bind mounts --> published containers

search for "development process with docker"

https://learn.microsoft.com/en-us/dotnet/architecture/microservices/docker-application-development-process/docker-app-development-workflow

https://docs.docker.com/develop/
  - Docker SDK for Python? https://docker-py.readthedocs.io/en/stable/client.html

https://docs.docker.com/develop/dev-best-practices/

Guide for Python on Docker!!
https://docs.docker.com/language/python/


Big, long article about how one team works
https://medium.com/rate-engineering/using-docker-containers-as-development-machines-4de8199fc662
https://medium.com/rate-engineering/using-docker-containers-to-run-a-distributed-application-locally-eeabd360bca3






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

