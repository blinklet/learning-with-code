title: Create a sample MS SQL Server database in a Docker container
slug: mssql-on-docker-container
summary: Create a Microsoft SQL Server on your local PC using Docker and load the AdventureWorks sample database so you can use it for experiments and other learning activities.
date: 2023-08-18
modified: 2023-08-18
category: Databases
<!--status: Published-->

If you want to practice integrating a database into your Python programs but you don't want to install a database server on your PC, you can use [Docker](https://www.docker.com/) instead. This post will show you how to download  [Microsoft's official SQL Server Docker image](https://mcr.microsoft.com/en-us/product/mssql/server/about) to create a container that runs the [AdventureWorks sample database](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure) by restoring a [database backup file](https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/create-a-full-database-backup-sql-server?view=sql-server-ver16).



## Docker 

Docker is a technology that allows you to create and run applications in isolated environments called containers. Docker also provides tools to manage your containers, images, and networks. You can use Docker to build, share, and run applications on any system, including Windows, Linux, Mac, and various cloud platforms so the procedures in this post will work on almost any operating system. There is a lot of [information available](https://docs.docker.com/get-started/resources/) about [using Docker](https://collabnix.com/9-best-docker-and-kubernetes-resources-for-all-levels/), including for [data science applications](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=5), so I will just describe the commands needed to create a re-usable database server in a container on your PC and leave you to [learn more about Docker](https://www.docker.com/101-tutorial/) according to your own interest.

### Install Docker

The Docker documentation shows you how to [install it on any operating system](https://docs.docker.com/engine/install/). This post shows you how to [install Docker CLI on a system running Ubuntu Linux 22.04](https://docs.docker.com/engine/install/ubuntu/). Run the following commands in your terminal: [^1]

[^1]: The commands listed are from https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

```bash
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt update
$ apt-cache policy docker-ce
$ sudo apt install docker-ce
```

To run Docker without the *sudo* command, add your userid to the *docker* group:

```
$ sudo usermod -aG docker ${USER}
```

Then, log out and log back in.

## Download the Microsoft SQL Server Docker image

Use Docker to [download](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash) the official Microsoft SQL Server image from the [Microsoft Artifact Registry](https://mcr.microsoft.com/)(warning: it is almost 3 GB in size). Run the following Docker command:

```bash
$ docker pull mcr.microsoft.com/mssql/server
```

Use the Docker *images* command to verify that Docker has the image on your PC:

```
$ docker images
```

The command output shows that we now have a local version of the image, named *mcr.microsoft.com/mssql/server:latest*.

```
REPOSITORY                       TAG           IMAGE ID       CREATED         SIZE
postgres                         latest        1b05cc48b421   3 days ago      412MB
mcr.microsoft.com/mssql/server   latest        683d523cd395   2 weeks ago     2.9GB
hello-world                      latest        9c7a54a9a43c   3 months ago    13.3kB
```

## Create a project directory

While docker stores its images and volumes within its own system directories, we still need to create a project directory to store other files we will use in this project, like the Dockerfile (if used), the database backup file, and the Python virtual environment files. Create a new directory using the following commands.

```bash
$ mkdir mssql-project
$ cd mssql-project
```

## Download the database backup file

Microsoft created [sample databases](https://learn.microsoft.com/en-us/sql/samples/sql-samples-where-are) so that users can experiment with their SQL Server and other data products. The AdventureWorks database emulates the data needs of a fictional bicycle manufacturing company and has complex, realistic relationships defined between data tables. Microsoft provides [backup files for all versions of its AdventureWorks sample database](https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks). In this post, I use the light version, which is also known as "AdventureWorks LT" but the same procedure will work with the OLTP and DW versions, or with any other database backup file.

Download the AdventureWorksLT2002 backup file with the following command:

```
$ wget https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksLT2022.bak
```

## Create the SQL Server container 

Create a new Docker container that runs the downloaded SQL Server image [^2]. You need to set the SQL Server's administrative password by passing in the *MSSQL_SA_PASSWORD* environment variable when starting the container. You may also tell the container to use the host PC's network address, which is *localhost*, so you don't have to figure out which IP address the container is using.

[^2]: Commands are from https://learn.microsoft.com/en-us/sql/linux/tutorial-restore-backup-in-sql-server-container?view=sql-server-ver16

```bash
$ docker run \
    --network=host \
    --env "ACCEPT_EULA=Y" \
    --env "MSSQL_SA_PASSWORD=A8f%h45dx23a" \
    --name sql1 \
    --detach \
    mcr.microsoft.com/mssql/server
```

Note that the administrative password must be a "strong" password that meets the[SQL Server password policy](https://learn.microsoft.com/en-us/sql/relational-databases/security/password-policy?view=sql-server-ver16). If you use a simple password, SQL Server will not start.

> **IMPORTANT:** The images you create from this container will now have the *SA* user's password "hard coded". You cannot change it by passing in the password environment variable to a new container based on the new image. You must save the password somewhere so you will have it when you need it later. You might use a password manager program like *Bitwarden*, for example.

## Restore the database from its backup file

Use the Docker *exec* command to run a command on the container that creates a directory for the backup file:

```bash
$ docker exec sql1 mkdir -p /var/opt/mssql/backup
```

Copy the database backup file you previously downloaded to the running container:

```bash
$ docker cp AdventureWorksLT2022.bak sql1:/var/opt/mssql/backup
```

Connect to a Bash shell on the container, in interactive mode

```bash
$ docker exec -it sql1 bash
mssql@T480:/$
```

On the container, run the following *sqlcmd* command to see what files are included in the backup archive

```bash
mssql@T480:/$ /opt/mssql-tools/bin/sqlcmd \
   -S localhost \
   -U SA \
   -P "A8f%h45dx23a" \
   -Q 'RESTORE FILELISTONLY FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak"' \
   | awk -F '[[:space:]][[:space:]]+' '{ print $1, $2}' | awk '!/^--/'
```

In the command example, above, I used some *[awk](https://www.gnu.org/software/gawk/manual/gawk.html)* "magic" to reduce the output, which is shown below, to just the information we need, which is the logical and physical file names.

```bash
LogicalName PhysicalName
AdventureWorksLT2022_Data C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\AdventureWorksLT2022.mdf
AdventureWorksLT2022_Log C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\AdventureWorksLT2022_log.ldf

(2 rows affected)
mssql@T480:/$
```

Make note of the logical and physical file names. You will need them in a later step. For this example, the two sets of names are shown below:

```
AdventureWorksLT2022_Data    AdventureWorksLT2022.mdf
AdventureWorksLT2022_Log     AdventureWorksLT2022_log.ldf
```

In the container's *bash* shell, start the *sqlcmd* utility in interactive mode:

```bash
mssql@T480:/$ /opt/mssql-tools/bin/sqlcmd \
    -S localhost \
    -U SA \
    -P "A8f%h45dx23a"
```

To restore the AdventureWorks LT database from its backup file, run the following SQL command. Use the database file logical and physical file names you found in the previous step: 

```sql
1> RESTORE DATABASE AdventureWorksLT
2> FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak"
3> WITH
4>   MOVE "AdventureWorksLT2022_Data"
5>     TO "/var/opt/mssql/data/AdventureWorksLT2022.mdf",
6>   MOVE "AdventureWorksLT2022_Log"
7>     TO "/var/opt/mssql/data/AdventureWorksLT2022_log.ldf";
8> GO
```

The output should look like the following:

```text
Processed 888 pages for database 'AdventureWorksLT', file 'AdventureWorksLT2022_Data' on file 1.
Processed 2 pages for database 'AdventureWorksLT', file 'AdventureWorksLT2022_Log' on file 1.
RESTORE DATABASE successfully processed 890 pages in 0.027 seconds (257.378 MB/sec).
```

### Verify the database

Verify that the database is restored. Run the following in SQL statement in the *sqlcmd* utility:

```sql
1> SELECT name
2> FROM sys.databases;
3> GO
```

This shows that the *AdventureWorksLT* database was created:

```bash
name
----------------
master
tempdb
model
msdb
AdventureWorksLT
```

Switch to the *AdventureWorksLT* database

```sql
1> USE AdventureWorksLT;
2> GO
Changed database context to 'AdventureWorksLT'.
```

Read the schemas in the database:

```sql
1> SELECT DISTINCT
2>    TABLE_SCHEMA
3> FROM INFORMATION_SCHEMA.TABLES;
4> GO
```

The output lists the *SalesLT* schema:

```bash
TABLE_SCHEMA
------------
SalesLT
dbo
```

List the tables in the database:

```sql
1> SELECT
2>   TABLE_NAME, TABLE_SCHEMA, TABLE_TYPE
3> FROM INFORMATION_SCHEMA.TABLES
4> ORDER BY TABLE_SCHEMA;
5> GO
```

It looks like all the tables are there

```bash
TABLE_NAME                       TABLE_SCHEMA TABLE_TYPE
-------------------------------- ------------ ----------
ErrorLog                         dbo          BASE TABLE
BuildVersion                     dbo          BASE TABLE
Address                          SalesLT      BASE TABLE
Customer                         SalesLT      BASE TABLE
CustomerAddress                  SalesLT      BASE TABLE
Product                          SalesLT      BASE TABLE
ProductCategory                  SalesLT      BASE TABLE
ProductDescription               SalesLT      BASE TABLE
ProductModel                     SalesLT      BASE TABLE
ProductModelProductDescription   SalesLT      BASE TABLE
SalesOrderDetail                 SalesLT      BASE TABLE
SalesOrderHeader                 SalesLT      BASE TABLE
vProductAndDescription           SalesLT      VIEW
vProductModelCatalogDescription  SalesLT      VIEW
vGetAllCategories                SalesLT      VIEW

(15 rows affected)
```

At this point, you can be confident that the database restore was successful.

## Create a new Docker image

Create a new Docker image that contains the newly-restored database. You can use the new image to create database containers that are ready to use.

First, exit the *sqlcmd* utility and the container:

```bash
1> exit
mssql@T480:/$ exit
$
```

Use the Docker *commit* command to create a new image named *adventureworks-lt* based on the current state of the container:

```bash
$ docker commit sql1 adventureworks-lt
```

Check the list of images to see that your new image has been created.

```bash
$ docker images
REPOSITORY                       TAG           IMAGE ID       CREATED             SIZE
adventureworks-lt                latest        c20d3e46f360   4 seconds ago       3.08GB
mssql-adventureworks-lt          latest        c81310e62ade   About an hour ago   2.91GB
postgres                         latest        1b05cc48b421   3 days ago          412MB
mcr.microsoft.com/mssql/server   latest        683d523cd395   2 weeks ago         2.9GB
```

Stop the container and delete it:

```bash
$ docker stop sql1
$ docker container rm sql1
```

### Test the new Docker image

To test that your new image contains a working database, start a new container from it and connect to a shell on the container:

```bash
$ docker run --name sql2 --network=host -d adventureworks-lt
$ docker exec -it sql2 bash
```

The user *SA* still has the same password that you configured when you created the container image. You should already know the password or you will not be able to use the database.

```bash
mssql@T480:/$ /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "A8f%h45dx23a"
```

See that the AdventureWorks LT database is there:


```bash
1> USE AdventureWorksLT;
2> GO
Changed database context to 'AdventureWorksLT'.
```

Exit the *sqlcmd* utility and the container:

```bash
1> exit
mssql@T480:/$ exit
$
```

Now you have a container running a Microsoft SQL Server and the *AdventureWorksLT* database. 

## Managing a container's lifecycle

Docker provides commands that enable you to view the status of your containers, and to create, start, stop, or delete them.

You can see which containers are running with the Docker *ps* command:

```bash
$ docker ps
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS         PORTS     NAMES
e656dec6bb0b   adventureworks-lt   "/opt/mssql/bin/perm…"   54 minutes ago   Up 2 seconds             sql2
```

You can stop the container when you are not using it with the following command:

```bash
$ docker stop sql2
```

you can see all containers, including stopped containers, with the Docker *ps --all* command

```bash
$ docker ps --all
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS                     PORTS     NAMES
e656dec6bb0b   adventureworks-lt   "/opt/mssql/bin/perm…"   58 minutes ago   Exited (0) 3 seconds ago             sql2
48e243953874   adventureworks-lt   "/opt/mssql/bin/perm…"   24 hours ago     Exited (0) 3 hours ago               test3
```

You can start an existing container whenever you need it with the Docker *start* command:

```bash
$ docker start sql2
```

At some point, you may want to delete a container. Use the Docker *prune* command to delete all stopped containers:

```bash
$ docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
48e2439538749cc8a41e079c46b9298c3c7666aaa467e3c532d5aaed40bbf17c

Total reclaimed space: 178.4MB

$ docker ps --all
CONTAINER ID   IMAGE               COMMAND                  CREATED             STATUS          PORTS     NAMES
e656dec6bb0b   adventureworks-lt   "/opt/mssql/bin/perm…"   About an hour ago   Up 40 seconds             sql2
```

Or delete any single stopped container by name:

```bash
$ docker stop sql4
$ docker rm sql4
```

## Connect your Python program to a database container

Use your new database as a sample data source for your Python programs. Before you can connect your Python program to the database, you must ensure your development environment is properly set up. You need to install the Microsoft ODBC driver, create a Python virtual environment, and add the necessary Python packages to it.

### Install Microsoft ODBC driver for SQL Server

Install the [Microsoft ODBC Driver for SQL Server on Linux](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Cubuntu17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline) using the following procedure:

Add the Microsoft repository to your [sources list](https://itsfoss.com/sources-list-ubuntu/):

```bash
$ sudo su
$ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
$ curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
$ exit
```

Install the *msodbcsql18* package:

```bash
$ sudo apt-get update
$ sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

Install the *unixodbc* package

```bash
$ sudo apt install unixodbc
```

### Set up a Python virtual environment

Create a new Python virtual environment in your Project folder, start it, and then install the Python packages you need:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $
```

Install the Python packages you need:

```bash
(.venv) $ pip install pyodbc sqlalchemy
```

### Test database connection

Below, is a sample Python program showing how to connect to SQL Server running on a Docker container on your PC. In this example, we use SQLAlchemy to connect to the database. The reason the connection URL has some additional parameters, compared to my [previous posts]({filename}/articles/016-sqlalchemy-read-database/sqalchemy-read-database.md), is because the Microsoft SQL Server Docker image comes pre-configured to use SSL certificates for authentication. I need to use the additional parameters to tell the server to use the password authentication, instead. 

```python
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base

load_dotenv('.env1', override=True)

url_object = URL.create(
    drivername='mssql+pyodbc',
    username='SA',
    password='A8f%h45dx23a',
    host='localhost',
    port='1433',
    database='AdventureWorksLT',
    query=dict(driver='ODBC Driver 18 for SQL Server',
               trustservercertificate='yes',
               trusted_connection='no')
)

engine = create_engine(url_object)

metadata = MetaData()
metadata.reflect(engine, views=True, schema="SalesLT")
Base = automap_base(metadata=metadata)
Base.prepare()

print("ORM Classes\n-------------")
print(*Base.classes.keys(), sep="\n")
print()
print("Table objects\n-------------")
print(*Base.metadata.tables.keys(), sep="\n")
```

The above program prints out the SQLAlchemy ORM Classes and Core tables that were read (vis database reflection) from the SQL Server running on a Docker container. If you see the same output then you know you can connect to the sample database running on the Docker container.

```bash
ORM Classes
-------------
Product
ProductModel
CustomerAddressy
Table objects
-------------
SalesLT.Address
SalesLT.Customer
SalesLT.CustomerAddress
SalesLT.Product
SalesLT.ProductCategory
SalesLT.ProductModel
SalesLT.ProductDescription
SalesLT.ProductModelProductDescription
SalesLT.SalesOrderDetail
SalesLT.SalesOrderHeader
SalesLT.vGetAllCategories
SalesLT.vProductAndDescription
SalesLT.vProductModelCatalogDescription
```

## Conclusion

You successfully used Docker to install and configure a sample database on your PC that you can use to test your Python programs that connect to databases. The procedure is simple. After docker is installed on your PC, and you create the new Docker image with the restored database, called *adventureworks-lt* in the example below, you just perform the following command:

```bash
$ docker run --detach --name sql1 --network=host adventureworks-lt
```

## Appendix A: Automate Docker image creation using the *build* command

You can automate the image build process using the [Docker *build* command](https://docs.docker.com/engine/reference/commandline/build/) that reads instructions from a [Dockerfile](https://docs.docker.com/engine/reference/builder/). This makes it easy to upgrade your Docker image in the future. Create a new file named *Dockerfile* and edit it with your favorite text editor:

```bash
$ nano Dockerfile
```

I won't explain the Docker [image build process](https://www.kosli.com/blog/docker-build-a-detailed-guide-with-examples/) in this post. The Docker documentation has a [good overview](https://docs.docker.com/build/) and many other resources are available on the Internet. 

In this case, I created a Dockerfile that builds a new image based on the Microsoft SQL Server image. Create a Dockerfile with the following contents:


```dockerfile
FROM mcr.microsoft.com/mssql/server
ARG passwd
ENV ACCEPT_EULA Y
ENV MSSQL_SA_PASSWORD $passwd
RUN mkdir -p /var/opt/mssql/backup \
    && wget -P /var/opt/mssql/backup \
          https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksLT2022.bak \
    && /opt/mssql/bin/sqlservr --accept-eula & sleep 15 \
    && /opt/mssql-tools/bin/sqlcmd \
    -S localhost -U SA -P "$passwd" \
    -Q 'RESTORE DATABASE AdventureWorksLT \
        FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak" \
        WITH \
        MOVE "AdventureWorksLT2022_Data" \
        TO "/var/opt/mssql/data/AdventureWorksLT2022.mdf", \
        MOVE "AdventureWorksLT2022_Log" \
        TO "/var/opt/mssql/data/AdventureWorksLT2022_log.ldf"' \
    && pkill sqlservr
```

The Dockerfile [reads in an argument](https://vsupalov.com/docker-arg-env-variable-guide/#setting-arg-values) that specifies the password that will be configured in the image. Then, it passes the environment variables needed to start the SQL Server, then creates a backup directory for SQL Server and dowmloads the backup file into it. Then, it starts the SQL server and waits 15 seconds to ensure it is running. It runs the *sqlcmd* utility with a SQL command that restores the database from the backup file and, finally, stops the SQL server [^3].

[^3]: The following StackOverflow answers were helpful in creating the Dockerfile: [46888045](https://stackoverflow.com/questions/46888045/docker-mssql-server-linux-how-to-launch-sql-file-during-build-from-dockerfi) and [51050590](https://stackoverflow.com/questions/51050590/run-sql-script-after-start-of-sql-server-on-docker)

Use the [Docker *build* command](https://docs.docker.com/engine/reference/commandline/build/) with the *--build-arg* option to set teh *passwd* argument and build a new image named *adventureworks-lt2*. The *build* command looks for a file in the current working directory named *Dockerfile* and runs the commands in it. 

```bash
$ docker build -t adventureworks-lt2 --build-arg passwd=A8f%h45dx23a .
```

Test the new image by creating a new container with it.

```bash
$ docker run --name test1 --network=host -d adventureworks-lt2
```

Run the same tests as you did previously. See that the *AdventureWorksLT* database is working. Then, stop and delete the container.

```bash
$ docker stop test1
$ docker rm test1
```

## Appendix B: Enable data persistence

If you intend to write to a database, you may want to [create a persistent Docker volume]((https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash#persist)) that will save the database's data files so they can be used again even if you delete the original container. 

You do not need to create a [Docker volume](https://docs.docker.com/storage/volumes/) if all you want to do is read data from a database server running in a container, so this step is optional,

Create a new container volume that you will use for storing persistent data. Give it the same name you will use when you create the container, to make it easy to know which volume is used with which container.

```bash
$ docker volume create sql3
```

List the available Docker volumes:

```bash
$ docker volume ls
DRIVER    VOLUME NAME
local     sql3
```

Create a new container, named *sql3*, based on the *adventureworks-lt* image, that connects the SQL server's database directory with the Docker volume named *sql3*.

```bash
$ docker run --detach --name sql3 --network host --volume sql3:/var/opt/mssql adventureworks-lt
```

### Test persistence

Test that you can write to the database. First connect to a shell on the container and start the *sqlcmd* utility:

```bash
$ docker exec -it sql3 bash
mssql@T480:/$ /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "A8f%h45dx23a"
```

Then, create a new database and a table in that database on the server by running the following SQL commands in the *sqlcmd* prompt:

```sql
1> create database TestDB;
2> GO
1> use TestDB;
2> GO
Changed database context to 'TestDB'.
1> CREATE TABLE testtble1
2> (
3>      pk_column int PRIMARY KEY,
4>      column_1 int NOT NULL
5> );
6> GO
```

See that the new database is listed on the server:


```sql
1> SELECT name
2> FROM sys.databases;
3> GO
```

This shows that the new *TestDB* database was created:

```bash
name
----------------
master
tempdb
model
msdb
AdventureWorksLT
TestDB
```

Now, stop the container and delete it:

```bash
1> exit
mssql@T480:/$ exit
$ docker stop sql3
$ docker rm sql3
```

See that the container is deleted by listing all containers:

```bash
$ docker ps -a
```

Now, create a new container named *sql4* that connects to the data volume previously used by the deleted container:

```bash
$ docker run --detach --name sql4 --network host --volume sql3:/var/opt/mssql adventureworks-lt
```


```bash
$ docker exec -it sql4 bash
mssql@T480:/$ /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "A8f%h45dx23a"
```

See that the new database name is still available on the server:


```sql
1> SELECT name
2> FROM sys.databases;
3> GO
```

This shows that the new *TestDB* database is still available:

```bash
name
----------------
master
tempdb
model
msdb
AdventureWorksLT
TestDB
```

Test that the table is available:

```sql
1> USE TestDB;
2> GO
Changed database context to 'TestDB'.
```

Read the schemas in the database:

```sql
1> SELECT
2> TABLE_SCHEMA, TABLE_NAME
3> FROM INFORMATION_SCHEMA.TABLES;
4> GO
```

You see the table is still available on the new container:

```bash
TABLE_SCHEMA    TABLE_NAME
------------    -------------
dbo             testtble1

(1 rows affected)
1>
```

Now you may stop and delete the container and, if you wish, [delete the volume](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes).

```bash
$ docker stop sql4
$ docker container rm sql4
$ docker volume rm sql3
```





