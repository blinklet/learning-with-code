title: Create a PostgreSQL database in a Docker container
slug: postgressql-on-docker-container
summary: Create the Chinook sample database on a PostgreSQL database server running in a Docker container.
date: 2023-08-31
modified: 2023-08-31
category: Databases
<!--status: Published-->

This post will show you how user Docker to easily create a PostgreSQL database server loaded with the Chinook sample database that you can use to test your Python programs.

[PostgreSQL](https://www.postgresql.org/) is an open-source database that is very popular with Python developers. It is simple to configure and offers many advanced features.

The [Chinook database](https://github.com/lerocha/chinook-database) is a sample database available for most mainstream database servers such as PostgreSQL, SQL Server, and MySQL. The database emulates the data used by an imaginary media store that sells music and video files over the Internet. It is easy to set up because it can be installed by running a single SQL script.

[Docker](https://www.docker.com/) provides a convenient way to create a PostgreSQL database server that you can use to test your Python programs locally.

## Installing software

If you have not yet [installed Docker](https://docs.docker.com/engine/install/), see my previous post about [creating an MS SQL Server container]({filename}/articles/017-mssql-docker/mssql-docker.md) to see the procedure I followed.

## Get the PostgreSQL image

The official [PostgreSQL Docker image](https://hub.docker.com/_/postgres) is available on Docker Hub. Open a terminal on your Linux PC and run the Docker *pull* command to download the image to your local Docker repository:

```bash
$ docker pull postgres
```

## Get the Chinook database script

Download the [Chinook database](https://github.com/lerocha/chinook-database) installation script from GitHub:

```bash
$ wget https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_PostgreSql.sql
```

### Fix the file encoding issue

The [text](https://man7.org/linux/man-pages/man7/charsets.7.html) in the Chinook SQL script is encoded in [LATIN1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1). The official Postgres image was built on a base that only supports [UTF-8](https://en.wikipedia.org/wiki/UTF-8) text. The *Chinook_PostgreSql.sql* script will cause an [error](https://github.com/morenoh149/postgresDBSamples/issues/1) if you run it on a container created from the oficial PostgreSQL Docker image.

To solve this problem, convert the text in the SQL script file to text encoded as UTF-8. Use the *iconv* command, as shown below:

```bash
$ iconv -f ISO-8859-1 -t UTF-8 Chinook_PostgreSql.sql > Chinook_PostgreSql_utf8.sql
$ rm Chinook_PostgreSql.sql
```

### Other Chinook database issues in Postgres

Postgres is case-sensitive, where many other database engines are not. Postgres expects that database object names will be in lower case. However, the Chinook database object names are in "proper" case, and "camel" case so they contain a mix of upper- and lower-case characters.

This is not a big problem. It only means that, if you write SQL statements to query the database, you will have to use quotes around the database object names. You will see this in the examples below.

## Build a Chinook database image

The easiest way to create the Chinook database image is to add a layer to the official Postgres image. The [Postgress Docker image](https://hub.docker.com/_/postgres) documentation states that a container starting from the image will run any SQL scripts stored in the image's *docker-entrypoint-initdb.d* directory. And, it states that we can initialize the container's default database by setting the *POSTGRES_DB* environment variable.

To create a postgres image that will initialize a container with the Chinook database, first create a dockerfile with the necessary build commands. Edit a file named "Dockerfile" in your favorite text editor:

```bash
$ nano Dockerfile
```

Add the following information to the file:

```dockerfile
FROM postgres 
ENV POSTGRES_DB chinook
COPY Chinook_PostgreSql_utf8.sql /docker-entrypoint-initdb.d/
```

Save the file. 

Make sure that the *Chinook_PostgreSql_utf8.sql* file you previously created is in the same directory as the dockerfile. Then run the following *build* command. Choose your own password for the container's *postgres* user.

```bash
$ docker build \
    --tag postgres-chinook-image \
    --file Dockerfile .
```

Check that the image is in your Docker local repository:

```bash
$ docker images
REPOSITORY                       TAG       IMAGE ID       CREATED             SIZE
postgres-chinook-image           latest    503246416dbf   About an hour ago   414MB
postgres                         latest    43677b39c446   4 days ago          412MB
mcr.microsoft.com/mssql/server   latest    683d523cd395   3 weeks ago         2.9GB
```

## Create a database container

Create a new database container called *chinook1* from the new image you created. Run the following command:

```bash
$ docker run \
    --detach \
    --env POSTGRES_PASSWORD=abcd1234 \
    --network host \
    --name chinook1\
    postgres-chinook-image
```

### Verify the database 

Quickly use the *psql* utility to check that the database initialized as expected. Start the *psql* utility in interactive mode on the container. Use the default username, "postgres", and connect it to the database, "chinook":

```bash
$ docker exec -it chinook1 psql -U postgres -d chinook
chinook=#
```

Then [list the tables](https://www.postgresqltutorial.com/postgresql-administration/postgresql-show-tables/) in the database with the *\d* command:

```text
chinook=# \d
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

If you see a similar list of tables, you know that the database initialized. Test a table to see that there is data in it. For example, list some information from the *Employee* table [^3]:

[^3]: You can also run this directly from teh host using the command: `docker exec chinook1 psql -U postgres -d chinook -c 'select * from "Employee" limit 2'`


```text
chinook=# SELECT * FROM "Employee" LIMIT 2;

 EmployeeId | LastName | FirstName |      Title      | ReportsTo |      BirthDate      |      HireDate       |       Address       |   City   | State | Country | PostalCode |       Phone       |        Fax        |         Email          
------------+----------+-----------+-----------------+-----------+---------------------+---------------------+---------------------+----------+-------+---------+------------+-------------------+-------------------+------------------------
          1 | Adams    | Andrew    | General Manager |           | 1962-02-18 00:00:00 | 2002-08-14 00:00:00 | 11120 Jasper Ave NW | Edmonton | AB    | Canada  | T5K 2N1    | +1 (780) 428-9482 | +1 (780) 428-3457 | andrew@chinookcorp.com
          2 | Edwards  | Nancy     | Sales Manager   |         1 | 1958-12-08 00:00:00 | 2002-05-01 00:00:00 | 825 8 Ave SW        | Calgary  | AB    | Canada  | T2P 2T3    | +1 (403) 262-3443 | +1 (403) 262-3322 | nancy@chinookcorp.com
(2 rows)
```

Now you can be confident that the database is ready to use. Quit the *psql* utility:

```text
chinook=# \q
$ 
```

## Success

At this point, you are done. You have a sample database running on the container. Programs running on your computer can access the server at the *localhost* IP address (127.0.0.1) and TCP port *5432*.

## Python

### Create the environment


```bash
$ sudo apt update
$ sudo apt install libpq-dev python3-dev libpq-dev
$ sudo apt install build-essential
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $
```
```bash
(.venv) $ pip install wheel
(.venv) $ pip install psycopg2
(.venv) $ pip install tabulate
(.venv) $ pip install jupyterlab
```
```bash
(.venv) $ pip install sqlalchemy
```
```bash
(.venv) $ jupyter-lab
```

### The *psycopg2* library

Create a connection to the postgres database running on the container using the *psycopg2* library. Use the [connectionstrings.com](https://www.connectionstrings.com/postgresql/) web site to see the information needed by Postgres.

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="chinook",
    user="postgres",
    password="abcd1234")
```

First find the schema available in the database.

```
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

The output shows that, in addition to the system schemas, there is a schema called *public*. 

```
[('information_schema',), ('pg_catalog',), ('public',)]
```

And, we know from the results of the *psql* command we ran earlier that the Chinook database tables are in the *public* schema. The following code will list all the tables:

```
from tabulate import tabulate

statement = """
SELECT 
  TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA != 'pg_catalog'
  AND TABLE_SCHEMA != 'information_schema'          
ORDER BY TABLE_NAME;
"""
#conn.rollback()
with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    tables = cursor.fetchall()

print(tabulate(tables, headers=headers))
```

We see that tables listed, below:

```
table_catalog    table_schema    table_name     table_type
---------------  --------------  -------------  ------------
chinook          public          Album          BASE TABLE
chinook          public          Artist         BASE TABLE
chinook          public          Customer       BASE TABLE
chinook          public          Employee       BASE TABLE
chinook          public          Genre          BASE TABLE
chinook          public          Invoice        BASE TABLE
chinook          public          InvoiceLine    BASE TABLE
chinook          public          MediaType      BASE TABLE
chinook          public          Playlist       BASE TABLE
chinook          public          PlaylistTrack  BASE TABLE
chinook          public          Track          BASE TABLE
```

Finally, try a query that joins data from multiple tables. You can see in this example that we had to use quotes around each name in the database because they are not all in lower case. This is not a big deal, but some people have opinions about it. As John Atten mentioned in his blog post, *[A More Useful Port of the Chinook Database to Postgresql](http://johnatten.com/2015/04/05/a-more-useful-port-of-the-chinook-database-to-postgresql/)*:

"Postgresql has its roots in the Unix world. Database object names are case-sensitive and the convention is to use lower-case names and, where needed, separate with underscores. It is possible to use proper-cased object names in Postges by escaping them with double-quotes. However, this makes for some atrocious-looking SQL."

```python
statement = """
SELECT "Album"."Title" AS "Album",
       "Artist"."Name" AS "Artist",
       "Track"."Name" AS "Track",
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

The results create a table showing information about the song tracks in the database:

```
Album                                  Artist    Track                                    Composer                                                                  Length
-------------------------------------  --------  ---------------------------------------  ----------------------------------------------------------------------  --------
For Those About To Rock We Salute You  AC/DC     For Those About To Rock (We Salute You)  Angus Young, Malcolm Young, Brian Johnson                                 343719
Balls to the Wall                      Accept    Balls to the Wall                                                                                                  342562
Restless and Wild                      Accept    Fast As a Shark                          F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman                       230619
Restless and Wild                      Accept    Restless and Wild                        F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman    252051
Restless and Wild                      Accept    Princess of the Dawn                     Deaffy & R.A. Smith-Diesel                                                375418   
```

### Python SQLAlchemy

If you use SQLAlchemy, you abstract away the particularities of SQL and do not need to worry about whether you should use quotes or not.


```python
from sqlalchemy.engine import URL
from sqlalchemy import select 
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from tabulate import tabulate

url_object = URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='abcd1234',
    host='localhost',
    port='5432',
    database='chinook'
)

engine = create_engine(url_object)
Base = automap_base()
Base.prepare(autoload_with=engine, schema='public')

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
    query = session.execute(statement)
    result = query.fetchall()
    print(tabulate(result, headers=q.keys()))
```

The code listed above connects to the database and generates the same table we previously created using the *psycopg2* library.

```
Album                                  Artist    Track                                    Composer                                                                  Length
-------------------------------------  --------  ---------------------------------------  ----------------------------------------------------------------------  --------
For Those About To Rock We Salute You  AC/DC     For Those About To Rock (We Salute You)  Angus Young, Malcolm Young, Brian Johnson                                 343719
Balls to the Wall                      Accept    Balls to the Wall                                                                                                  342562
Restless and Wild                      Accept    Fast As a Shark                          F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman                       230619
Restless and Wild                      Accept    Restless and Wild                        F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman    252051
Restless and Wild                      Accept    Princess of the Dawn                     Deaffy & R.A. Smith-Diesel                                                375418
```

## Conclusion

You created a Docker image that lets you create containers that run the sample Chinook database on the PostgreSQL database server. You saw how you could integrate the database into your Python programs. 








## Appendix A: Persistence

If you intend to write to a database, and if you are using a database container for more than just testing, you may want to [create a persistent Docker volume]((https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash#persist)) that will save the database's data files so they can be used again even if you delete the original container. 

### Create a volume

Create a new [Docker volume](https://docs.docker.com/storage/volumes/) that you will use for storing persistent data. Give it the same name you will use when you create the container, to make it easy to know which volume is used with which container.

```bash
$ docker volume create chinook2
```

List the available Docker volumes:

```bash
$ docker volume ls
DRIVER    VOLUME NAME
local     chinook2
```

### Connect volume to container directory

Create a new container, named *chinook2* that connects the SQL server's data directory, */var/lib/postgresql/data/*, with the Docker volume named *chinook2*.

```bash
$ docker run \
  --detach \
  --name chinook2 \
  --network host \
  --volume chinook2:/var/lib/postgresql/data \
  postgres-chinook-image
```

### Test data persistence

Create a second Chinook database named *chinook2*. Use the Docker *cp* command to copy the original Chinook SQL script to the container. Just throw it in the container's */tmp* directory.

```bash
$ docker cp Chinook_PostgreSql_utf8.sql chinook1:/tmp
```

Use the *psql* utility to create a new database and run the script on that database:

```bash
$ docker exec chinook2 createdb \
    --username postgres \
    chinook2
$ docker exec chinook1 psql \
    --username postgres \
    --dbname chinook2 \
    --single-transaction \
    --file /tmp/Chinook_PostgreSql_utf8.sql
```

List the available dtabases and see that the *chinook2* database was added.

```
$ docker exec chinook4 psql \
    --username postgres \
    --list
                                                List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider |   Access privileges   
-----------+----------+----------+------------+------------+------------+-----------------+-----------------------
 chinook   | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | 
 chinook2  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | 
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +           |          |          |            |            |            |                 | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +           |          |          |            |            |            |                 | postgres=CTc/postgres
(5 rows)
```



You can add more databases and run additional scripts, as you wish.

Stop the container and delete it

```bash
$ docker stop chinook2
$ docker rm chinook2
```

Create a new container from the original image but connect its data directory to the volume you previously created for the *chinook2* container.



```bash
$ docker run \
  --detach \
  --name chinook_test \
  --env POSTGRES_PASSWORD=abcd1234 \
  --network host \
  --volume chinook2:/var/lib/postgresql/data \
  postgres-chinook-image
```

According to the Postgres container documentation, the install script we copied to the image's *docker-entrypoint-initdb.d* directory will only run if the data directory is empty. But, this contaoner's data directory is mapped to teh Docker volume that already contains several databases. So the install script will not run and the container will use the databases in the attached volume. 

List the available databases. You can see that the new database you previouslt created persisted because it was saved in the volume that was attached to the new container.

```
$ docker exec chinook_test psql \
    --username postgres \
    --list

                                                List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider |   Access privileges   
-----------+----------+----------+------------+------------+------------+-----------------+-----------------------
 chinook   | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
 
 chinook2  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
 
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +           |          |          |            |            |            |                 | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +           |          |          |            |            |            |                 | postgres=CTc/postgres
(5 rows)
```

Look at tables in the second database

```psql
$ docker exec chinook_test psql \
    --username postgres \
    --dbname chinook2 \
    --command " \
        SELECT schemaname, tablename \
        FROM pg_catalog.pg_tables \
        WHERE schemaname != 'pg_catalog' 
          AND schemaname != 'information_schema';"
```

This output the tables in the database named *chinook2*:

```psql
 schemaname |   tablename   
------------+---------------
 public     | Artist
 public     | Album
 public     | Employee
 public     | Customer
 public     | Invoice
 public     | InvoiceLine
 public     | Track
 public     | Playlist
 public     | PlaylistTrack
 public     | Genre
 public     | MediaType
(11 rows)
```

This proves data was persistent

### Clean up 

Now you may stop and delete the container and, if you wish, [delete the volume](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes).

```bash
$ docker stop chinook_test
$ docker container prune
$ docker volume rm chinook2
```




