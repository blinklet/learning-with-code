title: Create a sample PostgreSQL database in a Docker container
slug: postgressql-on-docker-container
summary: Create a sample PostgreSQL database in a Docker container
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

```
mkdir -p ~/.docker/cli-plugins/
cd ~/.docker/cli-plugins/
wget https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-linux-x86_64 -O docker-compose


curl -SL https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
```

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

## init.sql file

postgres initializes itself from a file called init.sql. The easiest way to create a container with the Chinook DB is to just build a new image with the Chinook SQL file renamed as init.sql

```
$ ls
Chinook_SqlServer.sql
```


Convert the downloaded to UTF-8. See: https://github.com/morenoh149/postgresDBSamples/issues/1
and save results as init.sql

(The SQL script is stored in ISO-8859-1, you need to change your client_encoding to reflect that)  from https://stackoverflow.com/questions/39287814/how-to-load-chinook-database-in-postgresql

```
$ iconv -f ISO-8859-1 -t UTF-8 Chinook_PostgreSql.sql > init.sql
```

(or add the line `SET CLIENT_ENCODING TO 'LATIN1';` at the start of the init.sql file)

To make a new image, first create a file containing docker commands that take the postgress image and copty the SQL file into a new image that will be created.


```
nano chinook.Dockerfile
```

add the following text and save the file

```
FROM postgres 
ENV POSTGRES_PASSWORD abcd1234 
COPY init.sql /docker-entrypoint-initdb.d/
```

Then create the new image

```
$ docker build -f chinook.Dockerfile -t postgres-chinook-image .
```

```
[+] Building 1.3s (7/7) FINISHED                               docker:default
 => [internal] load build definition from chinook.Dockerfile             0.1s
 => => transferring dockerfile: 162B                                     0.0s
 => [internal] load .dockerignore                                        0.2s
 => => transferring context: 2B                                          0.0s
 => [internal] load metadata for docker.io/library/postgres:latest       0.0s
 => [internal] load build context                                        0.2s
 => => transferring context: 8.68kB                                      0.0s
 => [1/2] FROM docker.io/library/postgres                                0.8s
 => [2/2] COPY init.sql /docker-entrypoint-initdb.d/                     0.1s
 => exporting to image                                                   0.1s
 => => exporting layers                                                  0.1s
 => => writing image sha256:c2ffbc06e85b2d5fc910d8d701be77a7315532fa95a  0.0s
 => => naming to docker.io/library/postgres-chinook-image    
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
(.venv) $ pip install psycopg2-binary
(.venv) $ pip install tabulate
(.venv) $ pip install jupyterlab
```

```
(.venv) $ jupyter-lab
```

```
import psycopg2

conn = psycopg2.connect(
    host="172.17.0.2",
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
