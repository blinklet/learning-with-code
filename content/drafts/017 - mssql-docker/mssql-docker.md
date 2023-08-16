title: Create a sample MS SQL Server database in a Docker container
slug: mssql-on-docker-container
summary: Create a sample MS SQL Server database in a Docker container
date: 2023-08-31
modified: 2023-08-31
category: Databases
<!--status: Published-->


# Install Docker

(in Ubuntu 22.04)

from https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

```
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
```

```
sudo usermod -aG docker ${USER}
```
Then log out and log back in


(from https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)



# Get AdventureWorks LT database backup file


Get build from backup files available here
https://github.com/microsoft/sql-server-samples/releases/tag/adventureworks
Allows you to pick the DB for your container

LT version:

```
$ wget https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksLT2022.bak
```

Get docker image for SQL Server  https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash


```
$ docker pull mcr.microsoft.com/mssql/server
```

```
$ docker images
REPOSITORY                       TAG           IMAGE ID       CREATED         SIZE
postgres                         latest        1b05cc48b421   3 days ago      412MB
mcr.microsoft.com/mssql/server   2022-latest   683d523cd395   2 weeks ago     2.9GB
hello-world                      latest        9c7a54a9a43c   3 months ago    13.3kB
```




(inspred by)
https://learn.microsoft.com/en-us/sql/linux/tutorial-restore-backup-in-sql-server-container?view=sql-server-ver16






# Create  container image

Run the container, set the user SA password

```
$ docker run -e "ACCEPT_EULA=Y" \
    --network=host \
    --env "MSSQL_SA_PASSWORD=A8f%h45dx23a" \
    --name sql1 \
    --detach \
    mcr.microsoft.com/mssql/server
```

Create a directoryt on the container for the backup file

```
$ docker exec -it sql1 mkdir /var/opt/mssql/backup
```

Copy the backup file to the new directory on the container

```
$ docker cp AdventureWorksLT2022.bak sql1:/var/opt/mssql/backup
```

Log connect to a Bash shell on teh container, in interactive mode

```
$ docker exec -it sql1 bash
mssql@C-PF39JZFC:/$
```

Start the sqlcmd utility

```
mssql@C-PF39JZFC:/$ /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "A8f%h45dx23a"
1>
```

Run the following SQL command to see what files are included in the backup archive

```
1> RESTORE FILELISTONLY
2> FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak";
3> GO
```

You get a lot of info:

```
LogicalName
                     PhysicalName

                                                                  Type FileGroupName
                                                                                            Size
     MaxSize              FileId               CreateLSN                   DropLSN                     UniqueId                             ReadOnlyLSN                 ReadWriteLSN                BackupSizeInBytes    SourceBlockSize FileGroupId LogGroupGUID                         DifferentialBaseLSN         DifferentialBaseGUID                 IsReadOnly IsPresent TDEThumbprint                              SnapshotUrl



-------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---- -------------------------------------------------------------------------------------------------------------------------------- -------------------- -------------------- -------------------- --------------------------- --------------------------- ------------------------------------ --------------------------- --------------------------- -------------------- --------------- ----------- ------------------------------------ --------------------------- ------------------------------------ ---------- --------- ------------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AdventureWorksLT2022_Data
                     C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\AdventureWorksLT2022.mdf
                                                                  D    PRIMARY
                                                                                                        23003136       35184372080640                    1                           0                           0 E71ABF3A-C63F-4BBB-9E72-90D1CEB90E9E                           0                           0              7143424            4096           1 NULL                                           51000000008000001 248B0D87-170D-4236-B424-F91C9CC62B61          0         1 NULL                                       NULL



AdventureWorksLT2022_Log
                     C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\AdventureWorksLT2022_log.ldf
                                                                  L    NULL
                                                                                                         2097152       35184372080640                    2                           0                           0 26150932-FD10-42DB-9416-A0E0A1E77DBF                           0                           0                    0            4096           0 NULL                                                           0 00000000-0000-0000-0000-000000000000          0         1 NULL                                       NULL




(2 rows affected)
```

The main info we need is the logical and physical file names. From the long set of fields for each row, we see the first two columns in each row have the information we need. I made note of it like below

```
AdventureWorksLT2022_Data    AdventureWorksLT2022.mdf
AdventureWorksLT2022_Log     AdventureWorksLT2022_log.ldf
```

Run the following command in sqlcmd:

```
1> RESTORE DATABASE AdventureWorksLT
2> FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak"
3> WITH
4>   MOVE "AdventureWorksLT2022_Data"
5>     TO "/var/opt/mssql/data/AdventureWorksLT2022.mdf",
6>   MOVE "AdventureWorksLT2022_Log"
7>     TO "/var/opt/mssql/data/AdventureWorksLT2022_log.ldf";
8> GO
```

The output looked good:

```
Processed 888 pages for database 'AdventureWorksLT', file 'AdventureWorksLT2022_Data' on file 1.
Processed 2 pages for database 'AdventureWorksLT', file 'AdventureWorksLT2022_Log' on file 1.
RESTORE DATABASE successfully processed 890 pages in 0.027 seconds (257.378 MB/sec).
```

Verify that the database is set up:

Run teh following in sqlcmd:

```
1> SELECT name
2> FROM sys.databases;
3> GO
```

Shows that the AdventureWorksLT database was created

```
name
----------------
master
tempdb
model
msdb
AdventureWorksLT
```

Switch to the AdventureWorksLT database

```
1> USE AdventureWorksLT;
2> GO
Changed database context to 'AdventureWorksLT'.
```

Read the schemas in the database:

```
SELECT DISTINCT
   TABLE_SCHEMA
FROM INFORMATION_SCHEMA.VIEWS;
GO
```

Se see teh SalesLT schema:

```
TABLE_SCHEMA
--------------
SalesLT
```

List the tables in the database

```
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

Exit sqlcmd and the container

```
1> exit
mssql@C-PF39JZFC:/$ exit
exit
(.venv) $
```

Create a new image based on teh container

```
(.venv) $ docker commit sql1 adventureworks-lt
```

```
$ docker images
REPOSITORY                       TAG           IMAGE ID       CREATED             SIZE
adventureworks-lt                latest        c20d3e46f360   4 seconds ago       3.08GB
mssql-adventureworks-lt          latest        c81310e62ade   About an hour ago   2.91GB
postgres                         latest        1b05cc48b421   3 days ago          412MB
mcr.microsoft.com/mssql/server   latest        683d523cd395   2 weeks ago         2.9GB
```

Stop the container and delete it

```
$ docker stop sql1
$ docker container rm sql1
```

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



# Conclusion


































# Automate in Dockerfile

Now that we know the names of the files that need to be restored, we can automate the image build in a Dockerfile. This makes it easy to upgrade the base of your Docker image in the future

```
$ nano Dockerfile
```

The contents of teh file are:

```
FROM mcr.microsoft.com/mssql/server
ENV ACCEPT_EULA Y
ENV MSSQL_SA_PASSWORD A8f%h45dx23a
RUN mkdir -p /var/opt/mssql/backup
COPY AdventureWorksLT2022.bak /var/opt/mssql/backup
RUN /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U SA -P 'A8f%h45dx23a' \
  -Q 'RESTORE DATABASE AdventureWorksLT FROM DISK = "/var/opt/mssql/backup/AdventureWorksLT2022.bak" WITH MOVE "AdventureWorksLT2022_Data" TO "/var/opt/mssql/data/AdventureWorksLT2022.mdf", MOVE "AdventureWorksLT2022_Log" TO "/var/opt/mssql/data/AdventureWorksLT2022_log.ldf"'
```

```
$ docker build -t mssql-adventureworks-lt1 .
```

```
$ docker run --name ad2 --network=host -d mssql-adventureworks-lt1
```



# Run container

## AdventureWorks LT

https://github.com/chriseaton/docker-adventureworks

tag "postgres" as LT version running on postgres
tag "light" has LT version on SQL Server



Postgres
```
docker run --name chinook-sample --network=host -e 'POSTGRES_PASSWORD=A8f%h45dx23a' -d chriseaton/adventureworks:postgres
```
(has no tables????)

SQL Server
```
docker run --name chinook2 --network=host -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=A8f%h45dx23a' -d chriseaton/adventureworks:light
```
(seems to have full version????)

docker exec -it chinook2 bash
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "A8f%h45dx23a"

https://medium.com/codex/sql-server-unit-testing-with-tsqlt-docker-and-github-actions-9fa48a4072a6

SELECT name
FROM sys.databases;  
GO

1> select distinct
2>   TABLE_SCHEMA
3> from INFORMATION_SCHEMA.VIEWS
4> GO

above command lists 
HumanResources
Person
Production
Purchasing
Sales


docker pull chriseaton/adventureworks:light


So looks like we have the full database, not the LT database???

1> exit
mssql@C-PF39JZFC:/$ exit
$




## Chinook 

https://gist.github.com/sualeh/f80eccde37f8fef67ad138996fd4824d
(also see: https://github.com/mgutz/postgres-chinook-image
     lower casing all tables and identifiers and using serial for primary keys to better conform with PostgreSQL conventions.
     This might be better because it is one container)
     ((nimage not available???))


docker run --name chinook-sample --network=host -e 'POSTGRES_PASSWORD=abcd1234' -d ghcr.io/mgutz/chinook:postgres-12


## 












# Persistence

The following link shows how to sert up a container that points to a persistent file

https://www.howtogeek.com/devops/how-to-deploy-postgresql-as-a-docker-container/












# Get images

Could use prepared image like *schemacrawler/chinook-database* but they are often old and not updated.

```bash
$ docker pull postgres
```

# Test container

Below is the receipe for starting a container from the postgres image (see recipe in "How to use this image" in https://hub.docker.com/_/postgres)

```
$ docker run --name chinook-sample --network host -e POSTGRES_PASSWORD=abcd1234 -d postgres
```

try run command in https://wkrzywiec.medium.com/database-in-a-docker-container-how-to-start-and-whats-it-about-5e3ceea77e50

https://hub.docker.com/_/postgres

Then log in and test

```
$ docker exec -it chinook-sample bash
root@040f69388a6a:/# 
```

Then run the *psql* command on the container. Start it with the default username, "postgres":

```
root@040f69388a6a:/# psql -U postgres
psql (15.3 (Debian 15.3-1.pgdg120+1))
Type "help" for help.

postgres=# 
```

Great. So, container is running and postgreSQL is working. Now we need a container that has the Chinook database in it.

exit the container

```
postgres=# exit
rroot@040f69388a6a:/# exit
$
```

Delete the container

```
$ docker stop chinook-sample
$ docker container prune
```

# add Chinook DB to image

## Get Chinook database files

https://github.com/lerocha/chinook-database

Go to github, get "raw" version of file

```
mkdir dbtest
cd dbtest
wget https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_PostgreSql.sql
```



```
$ docker image ls
REPOSITORY               TAG       IMAGE ID       CREATED              SIZE
postgres-chinook-image   latest    c2ffbc06e85b   About a minute ago   412MB
postgres                 latest    8769343ac885   2 weeks ago          412MB
```

Run the new image

```
$ docker run --name chinook-sample -e POSTGRES_PASSWORD=abcd1234 -d postgres-chinook-image
$ docker exec -it chinook-sample bash
root@738afc4392fe:/# psql -U postgres
psql (15.3 (Debian 15.3-1.pgdg120+1))
Type "help" for help.

postgres=# \dt
             List of relations
 Schema |     Name      | Type  |  Owner   
--------+---------------+-------+----------
 public | Album         | table | postgres
 public | Artist        | table | postgres
 public | Customer      | table | postgres
 public | Employee      | table | postgres
 public | Genre         | table | postgres
 public | Invoice       | table | postgres
 public | InvoiceLine   | table | postgres
 public | MediaType     | table | postgres
 public | Playlist      | table | postgres
 public | PlaylistTrack | table | postgres
 public | Track         | table | postgres
(11 rows)

```

Commands for checking out DB
https://www.postgresqltutorial.com/postgresql-administration/postgresql-show-tables/

```
postgres=# exit
root@738afc4392fe:/# exit
$
```
```
$ docker container inspect chinook-sample -f '{{index .NetworkSettings.Networks "bridge" "IPAddress"}}'
172.17.0.2
```
```
$ docker container inspect chinook-sample -f '{{.NetworkSettings.Ports}}'
map[5432/tcp:[]]
```

https://www.connectionstrings.com/postgresql/

```
$ python -m venv .venv
$ source ./.venv/bin/activate
(.venv) $
```

```
(.venv) $ sudo apt update
(.venv) $ sudo apt install libpq-dev python3-dev libpq-dev
(.venv) $ sudo apt install build-essential
(.venv) $ pip install wheel
(.venv) $ pip install psycopg2
(.venv) $ pip install tabulate
(.venv) $ pip install jupyterlab
```

```
(.venv) $ jupyter-lab
```

```
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="abcd1234")
```




```python
statement = """
SELECT DISTINCT
  TABLE_SCHEMA
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_SCHEMA
"""

cursor = conn.cursor()
cursor.execute(statement)
print(cursor.fetchall())
cursor.close()
```
```
[('information_schema',), ('pg_catalog',), ('public',)]
```



```python
from tabulate import tabulate

statement = """
SELECT 
  TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'public'
ORDER BY TABLE_NAME
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    tables = cursor.fetchall()

print(tabulate(tables, headers=headers))
```
```
table_name     table_type
-------------  ------------
Album          BASE TABLE
Artist         BASE TABLE
Customer       BASE TABLE
Employee       BASE TABLE
Genre          BASE TABLE
Invoice        BASE TABLE
InvoiceLine    BASE TABLE
MediaType      BASE TABLE
Playlist       BASE TABLE
PlaylistTrack  BASE TABLE
Track          BASE TABLE
```


> NOTE: Postgresql (“Postgres” or “pg”) has its roots in the Unix world. Database object names are case-sensitive, and in fact the convention is to use lower-case names, and where needed, separate with underscores. It is possible to use proper-cased object names in Postges by escaping them with double-quotes. However, this makes for some atrocious-looking SQL. [^1]

[^1]: From http://johnatten.com/2015/04/05/a-more-useful-port-of-the-chinook-database-to-postgresql/

```python
statement = """
SELECT "Album"."Title",
       "Artist"."Name",
       "Track"."Name",
       "Track"."Composer", 
       "Track"."Milliseconds" AS "Length"
FROM "Album"
JOIN "Track" ON "Album"."AlbumId" = "Track"."AlbumId"
JOIN "Artist" ON "Album"."ArtistId" = "Artist"."ArtistId"
"""

conn.rollback()
with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchmany(5)

print(tabulate(rows, headers))
```
```
Title                                  Name    Name                                     Composer                                                                  Length
-------------------------------------  ------  ---------------------------------------  ----------------------------------------------------------------------  --------
For Those About To Rock We Salute You  AC/DC   For Those About To Rock (We Salute You)  Angus Young, Malcolm Young, Brian Johnson                                 343719
Balls to the Wall                      Accept  Balls to the Wall                                                                                                  342562
Restless and Wild                      Accept  Fast As a Shark                          F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman                       230619
Restless and Wild                      Accept  Restless and Wild                        F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman    252051
Restless and Wild                      Accept  Princess of the Dawn                     Deaffy & R.A. Smith-Diesel  
```





(persistence: where are files created in the current container? They do not persist if you delete the container)

https://www.baeldung.com/ops/docker-container-filesystem

SHOW data_directory;

/var/lib/postgresql/data

try:
```
$ docker export -o files.tar chinook-sample
$ tar -tvf files.tar | grep /var/lib/postgresql/data
```

# SQLAlechemy

```
(.venv) $ pip install sqlalchemy
```
```
from sqlalchemy.engine import URL

url_object = URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='abcd1234',
    host='172.17.0.2',
    port='5432',
    database='postgres'
)

from sqlalchemy import create_engine

engine = create_engine(url_object)

from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(autoload_with=engine, schema='public')

print(Base.classes.keys())

InvoiceLine = Base.classes.InvoiceLine
Playlist = Base.classes.Playlist
Album = Base.classes.Album
Genre = Base.classes.Genre
MediaType = Base.classes.MediaType
Customer = Base.classes.Customer
Employee = Base.classes.Employee
Artist = Base.classes.Artist
Track = Base.classes.Track
Invoice = Base.classes.Invoice


from tabulate import tabulate
from sqlalchemy import select
from sqlalchemy.orm import Session

statement = (select(Album.Title.label("Album"),
            Artist.Name.label("Artist"),
            Track.Name.label("Track"),
            Track.Composer, 
            Track.Milliseconds.label("Length"))
     .join(Track)
     .join(Artist)
     .limit(5)
    )

with Session(engine) as session:
    result = 
    print(tabulate(session.execute(statement)))
```

```
-------------------------------------  ------  ---------------------------------------  ----------------------------------------------------------------------  ------
For Those About To Rock We Salute You  AC/DC   For Those About To Rock (We Salute You)  Angus Young, Malcolm Young, Brian Johnson                               343719
Balls to the Wall                      Accept  Balls to the Wall                                                                                                342562
Restless and Wild                      Accept  Fast As a Shark                          F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman                     230619
Restless and Wild                      Accept  Restless and Wild                        F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman  252051
Restless and Wild                      Accept  Princess of the Dawn                     Deaffy & R.A. Smith-Diesel                                              375418
-------------------------------------  ------  ---------------------------------------  ----------------------------------------------------------------------  ------
```
















docker logs chinook-sample








Northwind via docker?
* https://github.com/pthom/northwind_psql
  * just clone and run docker compose up
* https://github.com/piotrpersona/sql-server-northwind
  * Shell script could be good script to follow manually?




  Northwind via docker?
* https://github.com/pthom/northwind_psql
  * just clone and run docker compose up
* https://github.com/piotrpersona/sql-server-northwind
  * Shell script could be good script to follow manually?

Chinook:  
* https://github.com/arjunchndr/Analyzing-Chinook-Database-using-SQL-and-Python/blob/master/Analyzing%20Chinook%20Database%20using%20SQL%20and%20Python.ipynb
* https://m-soro.github.io/Business-Analytics/SQL-for-Data-Analysis/L4-Project-Query-Music-Store/
* https://data-xtractor.com/knowledgebase/chinook-database-sample/

Chinook on Docker
* https://gist.github.com/sualeh/f80eccde37f8fef67ad138996fd4824d
  * 




Programmers who are have already mastered the SQL language could simply use the appropriate driver that is compatible with the SQL database they are using, such as [psycopg](https://www.psycopg.org/) for PostgreSQL, or [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) for MySQL. Since we are using an SQLite database, we could use the [sqlite package](https://www.sqlite.org/index.html), which is part of the Python standard library. But, remember, you need to know the SQL query language when writing programs that use these Python database drivers.

(Docker does not work when on corp network. Connect to Cisco VPN)



(done)







## (on Windows WSL)
https://stackoverflow.com/questions/52604068/using-wsl-ubuntu-app-system-has-not-been-booted-with-system-as-init-system-pi
$ sudo nano /etc/wsl.conf

[boot]
systemd=true

in Windows Powershell
> wsl.exe --shutdown

Press Enter in WSL to restart


run without sudo:


sudo usermod -aG docker ${USER}
su - ${USER}
sudo usermod -aG docker username


docker run hello-world


docker proxy

sudo su -

mkdir -p /etc/systemd/system/docker.service.d

cat <<'EOF' > /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://caottx01-proxy001.americas.nsn-net.net:8080"
Environment="HTTPS_PROXY=http://caottx01-proxy001.americas.nsn-net.net:8080"
Environment="NO_PROXY=localhost,127.0.0.1"
EOF

(use IP addresses in above proxy file)
(restart docker)

sudo systemctl daemon-reload
sudo systemctl restart docker

# postgress on docker

https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/
https://dev.to/andre347/how-to-easily-create-a-postgres-database-in-docker-4moj#:~:text=In%20our%20example%20we%20want%20to%20do%20the,the%20table%20schema%20and%20populate%20it%20with%20data

https://github.com/lorint/AdventureWorks-for-Postgres

Get database script from https://github.com/cwoodruff/ChinookDatabase/tree/master/Scripts
https://github.com/cwoodruff/ChinookDatabase/blob/master/Scripts/Chinook_PostgreSql.sql


docker pull postgres




# Try this!

AdventureWorks -- should work (also look at build instructions for step-by-step process)
https://github.com/chriseaton/docker-adventureworks


docker run -p 1433:1433 -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=abcd1234' -d chriseaton/adventureworks:light

uid = "Developer"?


# set up Podman on Windows






==================================
# Garbage


```
$ docker-compose -f postgres-chinook.yml up -d
 -d
[+] Running 2/2
 ✔ Network postgres_default    Created                                   0.1s 
 ✔ Container postgres-chinook  Started    
```
```
$ docker exec -it postgres-chinook /bin/bash
```

BUT container is not running

```
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

did it crash??????

user info:
    root (or chinook)
    p4ssw0rd








dockerfile:  (still in dbtest directory)

```
nano postgres-chinook.yml
```

add following lines (from https://gist.github.com/onjin/2dd3cc52ef79069de1faa2dfd456c945), then save

```
services:
  postgres:
    image: postgres
    container_name: postgres-chinook
    volumes:
      - ./Chinook_PostgreSql.sql:/docker-entrypoint-initdb.d/Chinook_PostgreSql.sql
```
















# mssql dockerfile

To make a new image, first create a file containing docker commands that take the postgress image and copty the SQL file into a new image that will be created.


```
nano Dockerfile
```

add the following text and save the file

(((need to make backup dir first))))
```
FROM mcr.microsoft.com/mssql/server 
ENV ACCEPT_EULA Y
ENV SA_PASSWORD A8f%h45dx23a
COPY AdventureWorksLT2022.bak /var/opt/mssql/backup
```

Then create the new image

```
$ docker build -t mssql-adventureworks-lt .
```

```
$ docker images
REPOSITORY                       TAG           IMAGE ID       CREATED          SIZE
mssql-adventureworks-lt          latest        c81310e62ade   18 seconds ago   2.91GB
postgres                         latest        1b05cc48b421   3 days ago       412MB
mcr.microsoft.com/mssql/server   2022-latest   683d523cd395   2 weeks ago      2.9GB
hello-world                      latest        9c7a54a9a43c   3 months ago     13.3kB
```







Run the new image

```
$ docker run --name adventure1 --network=host -d mssql-adventureworks-lt
```
```
$ docker exec -it adventure1 bash
```
