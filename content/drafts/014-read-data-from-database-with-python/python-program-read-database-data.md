title: Write a Python program that reads data from a database
slug: python-program-read-database-data
summary: Combine SQL queries with Python's *pyodbc* library to read data from a database
date: 2023-06-30
modified: 2023-06-30
category: Databases
<!-- status: published -->

<!--
A bit of extra CSS code to center all images in the post
-->
<style>
img
{
    display:block; 
    float:none; 
    margin-left:auto;
    margin-right:auto;
}
</style>

Introduction paragraph

## Set up your Python environment

Before you start working through this tutorial, you need to set up your Python virtual environment and install the necessary packages on your computer. The details of these steps are covered in my previous posts about [using dotenv files](), [creating a sample database]() and [reading database schema](). I summarize the steps, below.  

These examples were created on a laptop computer running Ubuntu 22.04. I assume Python is already installed on your system. If not, follow the instructions at [www.python.org]().

Create a new Python virtual environment

```bash
$ cd data-science-folder
$ python3 -m venv .venv
$ source ./.venv/bin/activate
(.venv) $ 
```


I suggest you install Jupyterlab so you can follow the steps in this tutorial more easily. If you do not use Jupyterlab, then you may use any text editor or the Python REPL.

```bash
(.venv) $ pip install jupyterlab
```

This tutorial uses the Microsoft AdventureWorks LT database running on Microsoft Azure. Follow my previous post about [creating a sample database on MZ Azure's free service tier]() to create a similar sample database you can use.

Then, install the [*pyodbc*](https://mkleehammer.github.io/pyodbc/) library and the Microsoft SQL Server Driver.

```bash
(.venv) $ sudo su
(.venv) $ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
(.venv) $ curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
(.venv) $ exit
(.venv) $ sudo apt-get update
(.venv) $ sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
(.venv) $ pip install pyodbc
(.venv) $ sudo apt install unixodbc
```

Install the *[python-dotenv](https://pypi.org/project/python-dotenv/)* package:

```bash
(.venv) $ pip install python-dotenv
```

Install the *tabulate* package so you may more easily format your output during this tutorial.

```bash
(.venv) $ pip install tabulate
```

## Connect to the database

Create a *dotenv* file and add the database connection string to it. If you are using an example database on Azure, the string will look similar to the one below. Use your own values for server name, database name, user name, and password.

```bash
(.venv) $ echo 'CONN_STRING="Driver={ODBC Driver 18 for SQL Server};'\
'Server=tcp:sqlservercentralpublic.database.windows.net,1433;'\
'Database=AdventureWorks;Uid=sqlfamily;Pwd=sqlf@m1ly;Encrypt=yes;'\
'TrustServerCertificate=no;"' > .env
```

Open a new Jupyterlab notebook (or use the Python REPL) and run the following Python code to connect to the database.

```python
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv('.env', override=True)

connection_string = os.getenv('CONN_STRING')

conn = pyodbc.connect(connection_string)
print(conn)
```

You should see the connection information in the output. It should look like the following:

```python
<pyodbc.Connection object at 0x0000014F5D0C1CA0>
```

In the rest of this tutorial, you will use the database connection instance, *conn*, to create *cursor* instances that will read and return database results to your program.

## Database schema

Either from the database documentation, or by exploring the database schema, you should already know the tables in the database and the columns in each table, and the data relationships defined by the primary and foreign key constraints. There is no official documentation for the AdventureWorks LT database, but the AdventureWorks LT database diagram is shown below [^3]:

[^3]: Diagram from *Microsoft Learning Transact-SQL Exercises and Demonstrations* website at [https://microsoftlearning.github.io/dp-080-Transact-SQL/](https://microsoftlearning.github.io/dp-080-Transact-SQL/)


![AdventureWorksLT database diagram]({attach}adventureworks-lt-diagram.png){width=99%}


## Basic SQL select statements


Get all data in a table]



Select only the columns you are interested in


## Select columns from other tables with join statements

Select only the rows you need

### Filtering database results

Filter database results using the SQLAlchemy ORM's *where()* method. For example, to filter the result so we only see items from Canada, create the following statement:

```python
statement = (
    select(Sample_View_Name.column_one, 
           Sample_View_Name.column_two, 
           Sample_View_Name.column_three)
    .where(Sample_View_Name.column_two == "Canada")
    .limit(5)
)
```

### SQL functions

The SQL *func()* function has many methods that allow you to run [SQL functions](https://learn.microsoft.com/en-us/sql/t-sql/functions/functions?view=sql-server-ver16) on the SQL server. [^4] To select data from a random sample of five items, run the SQL Server's [*NEWID()* T-SQL function](https://learn.microsoft.com/en-us/sql/t-sql/functions/newid-transact-sql?view=sql-server-ver16#d-query-random-data-with-the-newid-function). Create a statement like the following:

[^4]: Each version of SQL support different functions. For example, if you wanted to analyze data from a random sample of five items, you would use the *NEWID()* T-SQL function. But, other SQL database engines provide functions like *RANDOM()* or *RAND()* to do the same thing.

```python
stmt = (
    select(
        Sample_View_Name.column_one, 
        Sample_View_Name.column_two, 
        Sample_View_Name.column_three)
    .order_by(func.newid())
    .limit(5)
)

with Session(engine) as session:
    result = session.execute(stmt)
    columns = result.keys()
    data = result.all()

print(*columns, sep=", ")
for x in data:
     print(*x, sep=", ")
```

Every time you execute the statement, you get a different set of data. One iteration of the results is shown below.

```
Column One, Column Two, Column Three
xxxx
```

In the following example, we call SQL Server's *COUNT()* function to count the number of rows in the table. Then we filter that count by column_two and/or column_four, using the *where()* method. 

```python
from sqlalchemy import func

stmt0 = (select(func.count(Sample_View_Name
                           .column_zero)))

stmt1 = (
    stmt0
    .where(Sample_View_Name
           .column_two == "Canada")
    .where(Sample_View_Name
            .column_four == "Active")
)

stmt2 = (stmt0
        .where(Sample_View_Name
               .column_four == "Active"))

with Session(engine) as session:
    result = session.scalar(stmt0)
    print(f"Total Rows in table:  {result}")
    result = session.scalar(stmt2)
    print(f"Total Active in table:  {result}")
    result = session.scalar(stmt1)
    print(f"Total Active in Canada:  {result}")
```

```
Total Rows in table:  100000
Total Active in table:  100000
Total Active in Canada:  5000
```

If you have very large data sets, you can imagine how useful it can be to filter data before it is loaded into Python objects.

## 