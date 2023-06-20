# Plan to create data science posts

Post follow this set of topics

Series of posts getting data from Northwind database. See notes at top of *Azure-python-big-database.md* file. I think the *Azure-python-big-database.md* file is a good template to split up into the topics below. Also remember that the two other completed files: *Pandas-data-from-database.md* and *Sqlalchemy-minimum.md* can be used as well.

* Create a Northwind sample database using MS Azure and SQL Server
* Create a Northwind sample database using SQLite
* Create a Northwind sample database using Docker and PostgreSQL
* Environment variables help with creating db connect strings
* Use a Python program to read data from a database
  * database connection strings and ODBC driver
* Use SQLAlchemy to read data from a database
   * adapt *Sqlalchemy-minimum.md* to use general DB case and MS sample data
* Read SQL database schema information
   * Try out set of tools from 
   * use the custom code examples from *data-science-environment.md*
   * Use inspect module appendix from *Sqlalchemy-minimum.md*
   * SQL discovery tool like [*SchemaSpy*](https://schemaspy.org/), [*SchemaCrawler*](https://www.schemacrawler.com/), or [*SQLite Browser*](https://github.com/sqlitebrowser/sqlitebrowser). as mentioned in *Pandas-data-from-database.md*





# Existing docs

000-use-environment-variables.md
* Mostly done. Need to set environment variables to I can create DB connection strings in Jupyter Notebooks


001-create-sample-db-azure.md,  azure-db-linux.md
* practical commands to create and connect to Azure test DB. Also look at notebooks.
002-create-sample-db-sqlite.md
003-create-sample-db-docker.md
* There are three main ways to get a database for experimentation. I should focus on creating one in Azure
* But there are two other ways that should be covered

004-read-db-python-odbc-driver.md
* Take parts out of "Azure-python-big-database.md"

005-read-db-sqlalchemy.md
* is this just "Sqlalchemy-minimum.md"?



These posts are large and need to be generalized and linux-ized

Pandas-data-from-database.md
* SQLite example with Chinook DB
* Does not cover how to get scheme information -- basic disucssion of available scheme-reading tools
* Covers using Pandast read-sql-table and read-sql-query functions. Avoids SQLAlchemy queries
Sqlalchemy-minimum.md
* THis is a subset of "data-science-environment.md" with a lot of extras removed
* Does not cover how to get scheme information
* SQLite example with Chinook DB

data-science-environment.md
* SQLALchemy
* SQLite example with Chinook DB
* I think this was divided up into above two docs and the rest not used
* Goes into detail about using SQLAlchemy to read database scheme, including creating custom functions to read shema data
* So use this as a source of "extra" content but it has already been refined into the two docs above.


Azure-python-big-database.md
* sample outputs are "xxxx"
* examples are from big corporate DB
* roughly generalized
* need to adapt to azure test DB
* Covers three ways to get database schema
  * TSQL
  * Python function
  * SQLAlchemy
* Covers getting View information in SQLAlchemy
* So use this as source of content on smaller sections above.



