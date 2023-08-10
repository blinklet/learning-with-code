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

Docker Desktop license:
https://www.techrepublic.com/article/docker-launches-new-business-plan-with-changes-to-the-docker-desktop-license/


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

(Docker does not work when on corp network. Connect to Cisco VPN)

# Install Docker

(in WSL)

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker



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


sudo docker pull postgres




# Try this!

AdventureWorks -- should work (also look at build instructions for step-by-step process)
https://github.com/chriseaton/docker-adventureworks


docker run -p 1433:1433 -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=abcd1234' -d chriseaton/adventureworks:light

uid = "Developer"?


# set up Podman on Windows






