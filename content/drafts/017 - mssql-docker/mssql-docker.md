title: Create a sample MS SQL Server database in a Docker container
slug: mssql-on-docker-container
summary: Create a Microsoft SQL Server on your local PC using Docker and load the AdventureWorks sample database so you can use it for experiments and other learning activities.
date: 2023-08-31
modified: 2023-08-31
category: Databases
<!--status: Published-->

When you are learning how to integrate a database into your Python programs, you may want to practice with a sample database but you may not want to install database server on your PC. Instead, you can use [Docker](https://www.docker.com/). This post will show you how to download a Docker image in which someone else has installed and configured a database, load a sample database on it, and run it.

In a previous post, I described how to [create a Microsoft SQL Server pre-loaded with the AdventureWorks sample database on the Microsoft Azure cloud service]({filename}/articles/012-create-sample-db-azure\create-sample-db-azure.md). This post provides a simple recipe for using [Microsoft's official SQL Sever Docker image](https://mcr.microsoft.com/en-us/product/mssql/server/about) to create a container and then restore a [database backup file](https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/create-a-full-database-backup-sql-server?view=sql-server-ver16) of the [AdventureWorks sample database](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure).


## Docker 

Docker is a technology that allows you to create and run applications in isolated environments called containers. Docker also provides tools to manage your containers, images, and networks. You can use Docker to build, share, and run applications on any system, including Windows, Linux, Mac, and various cloud platforms so the procedures in this post will work on almost any operating system. There is a lot of [information available](https://docs.docker.com/get-started/resources/) about [using Docker](https://collabnix.com/9-best-docker-and-kubernetes-resources-for-all-levels/) for [data science applications](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=5) so I will just list the commands needed to create a re-usable database server in a container on your PC and leave you to [learn more about Docker](https://www.docker.com/101-tutorial/) according to your own interest.

### Install Docker

The Docker documentation shows you how to [install it on any operating system](https://docs.docker.com/engine/install/). This post shows you how to [install Docker CLI on a system running Ubuntu Linux 22.04](https://docs.docker.com/engine/install/ubuntu/). Run the following commands in your terminal: [^1]

The commands listed are from https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

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

## Download SQL Server Docker image

Use Docker to [download and store](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash) the official Microsoft SQL Server image from the [Microsoft Artifact Registry](https://mcr.microsoft.com/). Run the following Docker command:

```bash
$ docker pull mcr.microsoft.com/mssql/server
```

Verify that Docker has the image on your PC:

```
$ docker images
REPOSITORY                       TAG           IMAGE ID       CREATED         SIZE
postgres                         latest        1b05cc48b421   3 days ago      412MB
mcr.microsoft.com/mssql/server   latest        683d523cd395   2 weeks ago     2.9GB
hello-world                      latest        9c7a54a9a43c   3 months ago    13.3kB
```

## Create a project directory

While docker stores its images and volumes within its own system directories, we still need to create a project directory to store other files we will use in this project, like the Dockerfile, the database backup file, and Python virtual environment files. Create a new directory using the following commands.

```bash
$ mkdir mssql-project
$ cd mssql-project
$
```

## Download the AdventureWorks LT database backup file

Microsoft created [sample databases](https://learn.microsoft.com/en-us/sql/samples/sql-samples-where-are) so that users can experiment with their SQL Server and other data products. The AdventureWorks database emulates the data needs of a fictional bicycle manufacturing company and has complex, realistic relationships defined between data tables. Microsoft provides [backup files for all versions of its AdventureWorks sample database](https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks). In this post, I use the light version, which is also known as "AdventureWorks LT" but the same procedure will work with the OLTP and DW versions, or with any other database backup file.

```
$ wget https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksLT2022.bak
```

## Create the SQL Server container 

Create a new Docker container that runs the downloaded SQL Server image [^2]. You need to set the SQL Server's administrative password by passing in the *MSSQL_SA_PASSWORD* environment variable when starting the container. You may also tell the container to use the host PC's network address, which is *localhost*, so you don't have to figure out which IP address the container is using.

[^2]: Commands are from https://learn.microsoft.com/en-us/sql/linux/tutorial-restore-backup-in-sql-server-container?view=sql-server-ver16

```bash
$ docker run -e "ACCEPT_EULA=Y" \
    --network=host \
    --env "MSSQL_SA_PASSWORD=A8f%h45dx23a" \
    --name sql1 \
    --detach \
    mcr.microsoft.com/mssql/server
```

Note that the administrative password must be a "strong" password that meets the[SQL Server password policy](https://learn.microsoft.com/en-us/sql/relational-databases/security/password-policy?view=sql-server-ver16). If you use a simple password, SQL Server will not start.

## Restore the database from its backup file

Use Docker to run a command on the container that creates a directory on the container for the backup file

```bash
$ docker exec sql1 mkdir -p /var/opt/mssql/backup
```

Copy the database backup file you previously downloaded to the running container:

```bash
$ docker cp AdventureWorksLT2022.bak sql1:/var/opt/mssql/backup
```

Log connect to a Bash shell on the container, in interactive mode

```bash
$ docker exec -it sql1 bash
mssql@C-PF39JZFC:/$
```

On the container, run the following *sqlcmd* command to see what files are included in the backup archive

```bash
mssql@C-PF39JZFC:/$ /opt/mssql-tools/bin/sqlcmd \
   -S localhost \
   -U SA \
   -P "A8f%h45dx23a" \
   -Q 'RESTORE FILELISTONLY FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak"' \
   | awk -F '[[:space:]][[:space:]]+' '{ print $1, $2}' | awk '!/^--/'
```

In the above command example, I used some *[awk](https://www.gnu.org/software/gawk/manual/gawk.html)* "magic" to reduce the output, which is shown below, to just the information we need:

```bash
LogicalName PhysicalName
AdventureWorksLT2022_Data C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\AdventureWorksLT2022.mdf
AdventureWorksLT2022_Log C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\AdventureWorksLT2022_log.ldf

(2 rows affected)
mssql@C-PF39JZFC:/$
```

The main information you need is the logical and physical file names. From the information in each row, you see the first two columns in each row have the information we need. Make note of it, like below:

```
AdventureWorksLT2022_Data    AdventureWorksLT2022.mdf
AdventureWorksLT2022_Log     AdventureWorksLT2022_log.ldf
```

In the container's *bash* shell, start the *sqlcmd* utility in interactive mode:

```
mssql@C-PF39JZFC:/$ /opt/mssql-tools/bin/sqlcmd \
    -S localhost \
    -U SA \
    -P "A8f%h45dx23a"
```

To restore the AdventureWorks LT database from its backup file, run the following SQL command:

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

```
Processed 888 pages for database 'AdventureWorksLT', file 'AdventureWorksLT2022_Data' on file 1.
Processed 2 pages for database 'AdventureWorksLT', file 'AdventureWorksLT2022_Log' on file 1.
RESTORE DATABASE successfully processed 890 pages in 0.027 seconds (257.378 MB/sec).
```

## Verify the database

Verify that the database is restored. Run the following in SQL statement:

```sql
1> SELECT name
2> FROM sys.databases;
3> GO
```

This shows that the *AdventureWorksLT* database was created:

```
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
3> FROM INFORMATION_SCHEMA.VIEWS;
4> GO
```

The output lists the *SalesLT* schema:

```
TABLE_SCHEMA
--------------
SalesLT
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

```
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

## Create a new Docker image

Exit *sqlcmd* and the container:

```
1> exit
mssql@C-PF39JZFC:/$ exit
$
```

Create a new image named *adventureworks-lt* based on the current state of the container:

```
$ docker commit sql1 adventureworks-lt
```

```
$ docker images
REPOSITORY                       TAG           IMAGE ID       CREATED             SIZE
adventureworks-lt                latest        c20d3e46f360   4 seconds ago       3.08GB
mssql-adventureworks-lt          latest        c81310e62ade   About an hour ago   2.91GB
postgres                         latest        1b05cc48b421   3 days ago          412MB
mcr.microsoft.com/mssql/server   latest        683d523cd395   2 weeks ago         2.9GB
```

Stop the container and delete it:

```
$ docker stop sql1
$ docker container rm sql1
```

## Test the new Docker image

Start a new container from the image

```
$ docker run --name sql2 --network=host -d adventureworks-lt
$ docker exec -it sql2 bash
```

See that the user SA still has the same password

```
mssql@C-PF39JZFC:/$ /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "A8f%h45dx23a"
```

See that the AdventureWorks LT database is there


```
1> USE AdventureWorksLT;
2> GO
Changed database context to 'AdventureWorksLT'.
```

## Automate in Dockerfile

Now that we know the names of the files that need to be restored, we can automate the image build in a Dockerfile. This makes it easy to upgrade the base of your Docker image in the future

```
$ nano Dockerfile
```

(See https://stackoverflow.com/questions/46888045/docker-mssql-server-linux-how-to-launch-sql-file-during-build-from-dockerfi)
and
https://stackoverflow.com/questions/51050590/run-sql-script-after-start-of-sql-server-on-docker

The contents of the file are:

```
FROM mcr.microsoft.com/mssql/server
ENV ACCEPT_EULA Y
ENV MSSQL_SA_PASSWORD A8f%h45dx23a
RUN mkdir -p /var/opt/mssql/backup
COPY AdventureWorksLT2022.bak /var/opt/mssql/backup
RUN /opt/mssql/bin/sqlservr --accept-eula & sleep 15 \
    && /opt/mssql-tools/bin/sqlcmd \
    -S localhost -U SA -P 'A8f%h45dx23a' \
    -Q 'RESTORE DATABASE AdventureWorksLT \
        FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak" \
        WITH \
        MOVE "AdventureWorksLT2022_Data" \
        TO "/var/opt/mssql/data/AdventureWorksLT2022.mdf", \
        MOVE "AdventureWorksLT2022_Log" \
        TO "/var/opt/mssql/data/AdventureWorksLT2022_log.ldf"' \
    && pkill sqlservr
```

```
$ docker build -t adventureworks-lt .
```

```
$ docker run --name test1 --network=host -d adventureworks-lt
```


## Enable data persistence

The following link shows how to set up a container that points to a persistent file

https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash#persist


docker run --name test3 --network=host -v test3:/var/opt/mssql -d adventureworks-lt

docker volume ls
docker exec -it test3 bash

/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "A8f%h45dx23a"

create database TestDB;
GO

1> use TestDB;
2> GO
Changed database context to 'TestDB'.
1> CREATE TABLE testtble1
2> (
3>      pk_column int PRIMARY KEY,
4>      column_1 int NOT NULL
5> );
6> GO


https://docs.docker.com/storage/volumes/

https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes



## Test using the database from a Python program

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

```
$ sudo apt install unixodbc
```

You may need to logout and login again to ensure everything works well. 

Set up a Python virtual environment

```
$ python3 -m venv .venv
(.venv) $
```

Install *pyodbc* module

```
(.venv) $ pip install pyodbc
```

Start Jupyter Lab Notebook:

```
(.venv) $ jupyter-lab
```



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

The above code prints out the SQLAlchemy ORM Classes and Core tables that were read (vis database reflection) from the SQL Server running on a Docker container.

```
ORM Classes
-------------
Product
ProductModel
CustomerAddress
ProductCategory
Customer
ProductModelProductDescription
SalesOrderHeader
ProductDescription
Address
SalesOrderDetail

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

This shows that we successfully can connect a Python program to the Docker container running on our PC.




