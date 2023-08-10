title: Create a sample PostgreSQL database in a Docker container
slug: postgressql-on-docker-container
summary: Create a sample PostgreSQL database in a Docker container
date: 2023-08-31
modified: 2023-08-31
category: Databases
<!--status: Published-->

https://www.postgresql.org/
https://hub.docker.com/_/postgres/

use Podman?
https://mo8it.com/blog/containerized-postgresql-with-rootless-podman/
use Podman because it can be used freely in Windows, Linux, and Mac
https://blog.scottlogic.com/2022/02/15/replacing-docker-desktop-with-podman.html
https://www.howtogeek.com/devops/getting-started-with-podman-desktop-an-open-source-docker-desktop-alternative/
https://podman-desktop.io/


use Docker?
https://github.com/docker/awesome-compose/tree/master/postgresql-pgadmin
https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/

Use LXC?
https://azizkandemir.github.io/en/blog/lxc-postgresql/



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

