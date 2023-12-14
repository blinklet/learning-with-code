title: Move the Docker data directory
slug: docker-daemon-data-move
summary: Configure the Docker daemon to store all its data in a different directory, instead of in the default directory.
date: 2023-12-14
modified: 2023-12-14
category: Docker
status: Published

Unless otherwise configured, the [Docker](https://www.docker.com/) daemon stores its data in the directory, */var/lib/docker*. This post describes how to configure Docker to store its data in a different folder.

In my case, I have a 256 GB hard drive on my laptop, which dual boots to Linux or Windows. I mounted the Linux root directory to a 45 GB partition, the */home* directory to a 90 GB partition, and 8 GB to a *swap* partition. The rest of the hard drive is used by Windows. I run Ubuntu and I found that 45 GB is a bit tight for the Ubuntu system because the [*snaps* packages](https://snapcraft.io/about) use up a lot of space. Adding large Docker images into the same partition was causing it to fill up. I decided to store Docker data in my *home* partition, where I have more space.

## Configure the Docker daemon

The Docker documentation describes how to [change the Docker data directory](https://docs.docker.com/config/daemon/#daemon-data-directory). 

First, stop the Docker daemon:

```text
$ sudo service docker stop
```

Then, create a new Docker daemon configuration file, if one does not already exist. If one does exist, edit the existing file:

```text
$ sudo nano /etc/docker/daemon.json
```

Add the following configuration information to the file:

```json
{
  "data-root": "/home/docker-data"
}
```

You may choose any name for the new directory. I chose */home/docker-data*. Save the file.

## Copy the Docker data directory

Next, create the new Docker data directory in your specified location and copy the existing docker data over to it while maintaining all existing permissions:

```text
$ sudo rsync -aq /var/lib/docker/ /home/docker-data
```

## Test the new directory

For testing purposes, rename the old docker data directory so it cannot be used by Docker:

```text
$ sudo mv /var/lib/docker /var/lib/docker-old
```

Start the Docker daemon:

```text
$ sudo service docker start
```

Test that Docker can access its data in the new directory. If you have some containers already created you should be able to list them and their images:

```text
$ docker ps -a
CONTAINER ID   IMAGE             COMMAND                  CREATED       STATUS                   PORTS     NAMES
4fdf96abb044   postgres:alpine   "docker-entrypoint.s…"   5 weeks ago   Exited (0) 5 weeks ago             postgres_db
$ docker images
docker images
REPOSITORY                       TAG       IMAGE ID       CREATED        SIZE
postgres                         alpine    46d837b93a1c   2 months ago   239MB
redis                            latest    39ac5829bade   3 months ago   138MB
blinklet/user-mapping            v1        9ce0b76c0af7   3 months ago   113MB
postgres-chinook-image           latest    503246416dbf   3 months ago   414MB
blinklet/adventureworks          latest    ef97417e6827   3 months ago   3.08GB
python                           alpine    cecbd2a9585a   4 months ago   52MB
```

## Delete the old data

After successfully testing Docker, free up disk space on the root partition by deleting the old Docker data directory:

```text
$ sudo rm -rf /var/lib/docker-old
```

## Conclusion

I showed how to configure Docker to store its data in a different directory.

