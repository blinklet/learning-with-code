Recast with Chinook or MS example DB (MS Example DB has views)

Maybe retry Northwind on SQLite?
* https://database.guide/2-sample-databases-sqlite/
* because I think it is the same as the sample data in SQL Server...

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







% SQL and Python access to the database

This document will show you how to use simple SQL queries to read data from the Database, using either [Microsoft Transact-SQL (T-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql) [^1] or the [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html). 

[^1]: Microsoft Transact-SQL, also known as T-SQL, is Microsoft SQL Server's version of the [SQL language](https://en.wikipedia.org/wiki/SQL). 

# Important information

Before you get started using Python to access data in the Database, there are a few points you should know. These will help you determine if you should proceed with reading this document, or if you should find an alternative path to achieve your goals.

## Prerequisite knowledge

We do not cover the basics of Python or SQL in this document. You need to know a little bit about the basics of Python and the principles upon which [relational databases](https://www.oracle.com/ca-en/database/what-is-a-relational-database/) are based. If you do not already have some basic Python skills, I suggest you read my document, *Python: the Minimum You Need to Know*, or a similar tutorial. 

Also, you need to have already requested and received access to the Database. See the *Analytics Documentation* for information about how to access the database, and to learn about the standard views available in THE DATABASE.

## Limited to PC 

This document assumes the reader is using a Windows PC. It shows you how to use your Microsoft ID to connect to THE DATABASE from your Windows PC. So, Python can only access THE DATABASE when running on your own laptop.

If you plan to write applications that run on a server, you will need to create an application key and ask the database team to set up authentication for the application. This document does not cover how to authenticate an application running on a server. You will also need to work with IT to ensure your application is secure and uses corporate data appropriately.

## Data handling

THE DATABASE may contain sensitive data. To reduce security risks, access only the specific data elements that you need and do not save any data to disk. Keep all your data in Python objects in memory so the data disappears when your program is finished.

## Relevance

The topics covered in this document may not be relevant to most data scientists because it ends where most will start: with data already retrieved from a database and stored in data frames. 

If you work in Microsoft Azure, your IT team will have created a system for you that maintains one or more DataBricks data frames and keeps them in sync with your Database. Then, you will mostly work with the DataBricks PySpark API to transform and analyze the data. 

However, knowing how the Database may be accessed from a Python program may help some programmers at some point. 

# Set up your Python environment

Before you start working through this tutorial, install Python on your laptop. Then, start a Python virtual environment and install the required Python packages in it.

## Install Python on your Windows laptop

Start by installing Python on your laptop, if it is not already installed. Go to the [Python web page](https://www.python.org/) for the most up-to-date information about installing python on your operating system.

On a Windows laptop, it is easiest to install Python from the Windows Store. Choose the latest version. When this document was written, the current version of Python was 3.11.

>**NOTE:** At the time this document was written, Python 3.11 code could crash when run in Jupyter notebooks because it enables frozen modules, which seem to cause problems with the current version of Jupyter notebook. Work around this problem by installing Python 3.10 or by  turning off frozen modules when you create your Python virtual environment using the *-Xfrozen_modules=off* option.

## Install Microsoft ODBC driver for SQL Server

Download and install the [Microsoft ODBC Driver for SQL Server on Windows](https://learn.microsoft.com/en-us/sql/connect/odbc/windows/microsoft-odbc-driver-for-sql-server-on-windows?view=sql-server-ver16). Microsoft ODBC Driver 18 for SQL Server supports Azure Active Directory integrated authentication.

Download the installer file *msodbcsql.msi* from the SQL driver's [downloads page](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) and save it. Then double-click on the installer file and follow the install wizard to compete installation.

![Microsoft ODBC Driver for SQL Server installer](./Images/odbc-driver-003.png){width=60%}


## Create a Python virtual environment

To create a Python virtual environment, run the following commands:

```powershell
> mkdir data-science-folder
> cd data-science-folder
> python -Xfrozen_modules=off -m venv env
```

Then, activate the virtual environment.

```
> .\env\Scripts\activate
(env) > 
```

## Install Python database drivers

Next, install [*pyodbc*](https://mkleehammer.github.io/pyodbc/), the open-source Python ODBC driver for SQL Server. This provides the Python interface to the Windows ODBC driver. 

```powershell
(env) > pip install pyodbc 
```

Also, install the Azure Identity module to support authenticating your access to the Database.

```powershell
(env) > pip install azure-identity
```

Then, install SQLAchemy with the following command. SQLAlchemy is a more advanced library that provides many functions that make interacting with databases easier for Python programmers.

```powershell
(env) > pip install SQLAlchemy
```

## Spark

[Azure Databricks](https://azure.microsoft.com/en-us/products/databricks/) is based on Spark so it is probably best to learn how to use Spark in a Python program because the Microsoft Advanced Analytics Platform uses Databricks. 

[Spark](https://spark.apache.org/) is an open-source data analytics tool that maps functions onto large data sets stored in data frames. It is typically deployed on a cluster of computers. 

PySpark provides a [Python API](https://spark.apache.org/docs/latest/api/python/index.html) and a [Pandas API](https://spark.apache.org/docs/3.2.0/api/python/user_guide/pandas_on_spark/). Spark also [does a lot more](https://www.toptal.com/spark/introduction-to-apache-spark) than just process data in data frames.

Unfortunately, Spark is very difficult to install and run on a Windows PC. So, we will use Pandas instead of Spark in the tutorials in this document.

>**NOTE:** It may be possible to [install an already-configured Pyspark container on your PC](https://realpython.com/pyspark-intro/#installing-pyspark) and use Spark running on the container. That's a good topic for future investigation but, for sake of time and effort, we will not include it in this document.

## Install Pandas

Pandas is a popular data analysis framework. It is easy to install and run on a single PC. The Pandas API is different than the Spark API but Spark offers a "Pandas mode" that allows one to enter commands into Spark using the Pandas API. So, you can use what you learn about Pandas when you upgrade to Spark.

Install Pandas:

```powershell
(env) > pip install pandas
```

## Install Jupyterlab

This document uses a [Jupyter notebook](https://jupyter.org/) as an advanced [REPL](https://codewith.mu/en/tutorials/1.0/repl) that makes it easier to demonstrate Python code samples. If you prefer to use a simple text editor or another REPL, you can still follow along with this tutorial.

To install Jupyterlab, run the following command:

```powershell
(env) > pip install jupyterlab
```

Create a new Jupyter notebook and start it using the commands below:

```powershell
(env) > create-notebook my_notebook
(env) > jupyter notebook my_notebook.ipynb
```

A new Jupyter notebook will open in a browser window.

![An example of the Jupyter Notebook user interface](./Images/Jupyter-Notebook.png){width=80%}

When using a Jupyter notebook, create new cells in its user interface and then write Python code into the cell. Run the code by running the cell. The objects you create in each cell persist in memory and can be used in the next cell. 

## Next steps

Now, you are ready to start working through the tutorials in this document. You may start with using raw T-SQL statements with the Python ODBC driver or you may skip ahead to the SQLAlchemy topic.

# Python ODBC driver and T-SQL

You can use the *pyodbc* Python library to connect to and read data from an SQL Server database. Create a connection object by passing the necessary database and user information to the pyodbc driver's *connect()* function. You will create T-SQL statements and pass them to the connection object's  driver. 

## Connect to Database

Import the *pyodbc* module and create a database connection string that you can pass into the driver's *connect()* function. 

```python
import pyodbc

server = 'servername.database.windows.net'
database = 'hraap-euw-db01'
username ='brian.e.linkletter@gmail.com'
Authentication='ActiveDirectoryInteractive'
driver= '{ODBC Driver 18 for SQL Server}'

connection_string = ('DRIVER='+driver+
                      ';SERVER='+server+
                      ';PORT=1433;DATABASE='+database+
                      ';UID='+username+
                      ';AUTHENTICATION='+Authentication
                      )

conn = pyodbc.connect(connection_string)

print(conn)
```


> **NOTE:** Replace the text in the *server* and *database* variables with the real database server and database information.

The example above, when run, opens an interactive login session in a new web browser window. Enter your Microsoft password into the password prompt in the browser window.

### Alternative to connection strings (on Windows)

Another way to create a connection string is to [create a Data Source  (DSN)](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows) using the *ODBC Data Sources* app. This is a Windows-only feature and it lets you avoid entering database information in your code. 

It's probably better to enter the information as a connection string in your code or to use [environment variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.3) if you do not want to hard-code database and use information in your code. 

Just to be complete, we record the procedure for creating and using a DSN in *Appendix A: Data Source Names*.

### Check that the connection is successful

A quick way to check that the connection is working is to get the database server;s version information. Create a simple T-SQL statement using the [T-SQL *@@VERSION* function](https://learn.microsoft.com/en-us/sql/t-sql/functions/version-transact-sql-configuration-functions?view=sql-server-ver16).

```python
statement = "SELECT @@version;"

cursor = conn.cursor()
cursor.execute(statement) 

print(cursor.fetchone())
```

This should print the version of SQL Server software running on the database. 

## Read database information

You need information about the which Database schemas are available to you. Read the database documentation, or use Python code to analyze the database information so you can identify the information you need in your application.

To get information about Database elements that you have permission to read, look for the database system table called INFORMATION_SCHEMA.VIEWS. The [Microsoft T-SQL documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-information-schema-views/system-information-schema-views-transact-sql?view=sql-server-ver16) describes this table and states that database schema information is available in it.

Microsoft's SQL Server documentation also states that the more reliable way to gather information is to query the *sys.objects* catalog view because the *INFORMATION_SCHEMA* schema contains only a subset of database information. But, I found the *INFORMATION_SCHEMA* tables to be simpler to use and to contain all the information needed for this use case. To be complete, I discuss the *sys.objects* catalog view and other database information gathering methods in *Appendix B*.

### Schema names 

Create a T-SQL statement that selects the TABLE_SCHEMA column in the table and sorts data alphabetically:

```python
statement = """
SELECT DISTINCT
  TABLE_SCHEMA
FROM INFORMATION_SCHEMA.VIEWS
ORDER BY TABLE_SCHEMA
"""
```

Then execute the statement using the cursor's *execute()* function. This places the data results in the cursor. You can get all the results at once using the cursor object's *fetchall()* method.

```python
cursor = conn.cursor()
cursor.execute(statement)

print(cursor.fetchall())
```

This shows the database schemas that you have permission to read.

```
[('one_schema',), ('sample_schema',), ('another_schema',)]
```

### Table and views names in a schema

To get the table name information from the *INFORMATION_SCHEMA.VIEWS* table, create the following SQL statement and then execute it.

```python
statement = """
SELECT
  TABLE_NAME
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'sample_schema'
ORDER BY TABLE_NAME
"""

cursor = conn.cursor()
cursor.execute(statement)
for row in cursor.fetchall():
    print(*row)
```

The output contains table and view names in the *sample_schema* schema.

```
[('Sample Table',), ('Sample Table2',)]
```

### Column names in a table

Finally, we need the list of columns in each table we plan to use, along with some of their attributes.

To get the column name information from the *INFORMATION_SCHEMA.COLUMNS* table, create the following SQL statement and then execute it.

```python
statement = """
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Sample View Name'
"""

cursor = conn.cursor()
cursor.execute(statement)

headers = [h[0] for h in cursor.description]
print(*headers, sep=", ")
data = cursor.fetchall()
for x in data:
    print(*x, sep=", ")
```

The output contains name, type, and length of each column in the *Sample View Name* view. There are 313 columns in this table so we truncate the list after the first few columns:

```
COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
Column Zero, varchar, 10
xxxxx
...
```

### Table constraints

Normally, database tables are defined with constraints such as a primary key and foreign keys. The primary key, foreign keys, and other constrains define relationships between tables in a relational database. Get the *Sample View Name* view's constraints with the following SQL statement:

```python
statement = """
SELECT *
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_NAME = 'Sample View Name'
"""

cursor = conn.cursor()
cursor.execute(statement)

print(cursor.fetchall())
```

The result returns an empty list so the *Sample View Name* view has no primary or foreign keys. 

```
[]
```

In fact, none of the views in the Database have primary keys defined. This is acceptable when you are reading data from the database. Knowing the database relationship information is helpful, but not necessary, when reading information from tables. 

## Read data from selected columns in a table

Now that you have found the schemas, tables, and columns that contain the data you are interested in, you can read data using T-SQL statements and the pyodbc driver's *cursor.execute()* method.

For example, to gather a little bit of data about five randomly-selected rows, run the following code:

```python
statement = """
SELECT TOP 5 "Column One", "Column Zero", "Column Two", "Column Three"
FROM sample_schema."Sample View Name"
ORDER BY NEWID()
"""

cursor.execute(statement)

headers = [h[0] for h in cursor.description]
print(*headers, sep=", ")

data_list = cursor.fetchall()
for row in data_list:
    print(*row, sep=", ")
```

The output lists the selected data.

```
Column One, Column Zero, Column Two, Column Three
xxxxx
```

## Convert results to a Pandas data frame

Data analysts will usually find it more convenient to work in a data frame framework like Pandas. You can easily convert results returned from the pyodbc driver into data frames using the *pandas.DataFrame.from_records()* method, as shown below.

```python
import pandas as pd

statement = """
SELECT TOP 5 
"Column One" AS "column_one", 
"Column Zero" AS "column_zero", 
"Column Two" AS "column_two", 
"Column Three" AS "column_three"
FROM sample_schema."Sample View Name"
ORDER BY NEWID()
"""

cursor.execute(statement)

headers = [h[0] for h in cursor.description]
data_list = cursor.fetchall()

dataframe = pd.DataFrame.from_records(data_list, columns=headers)
print(dataframe)
```

The program prints the new data frame below. You can see at least one of the benefits of working with data frames is that they format data well when printing.

```
xxxxx
```

## Read data directly to a Pandas data frame

You can also use Pandas to directly read data from the *pyodbc* driver. This is more efficient when reading large amounts of data. Use the *Pandas.read_sql()* method. Pass it the SQL statement and the database connection object created by the pyodbc driver.

```python
statement = """
SELECT TOP 5 "Column One", "Employment Status Name", "Column Two", "Column Three"
FROM sample_schema."Sample View Name"
ORDER BY NEWID()
"""

data = pd.read_sql(statement, conn)
print(data)
```

You can see pandas read in another five random rows directly into a data frame.

```
xxxxx
```

But this also produces a warning in the Jupyter Notebooks screen. Apparently, the pandas developers to not test the pyodbc driver connection with pandas.

```
UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy.
  data = pd.read_sql(statement, conn)
```

We'll discuss SQLAlchemy more in the next chapter. If you wish to use Pandas to read from the database, and are familiar with T-SQL syntax, then you only need to know how to set up an SQLAlchemy engine. After that, you can use Pandas with raw T-SQL queries and the SQLAlchemy engine instead of the pyodbc connection.

## Read entire tables into Pandas data frames

If you have enough memory on your PC, you can read entire tables from the database into Pandas for analysis. This is probably the way most data scientists will work.

>**WARNING:** Do not run the following code unless you really want all the data in a table. Database tables can be very large and it can take hours to download all the data. 

To download all rows in the *Sample View Name* table into a Pandas data frame, create an SQL statement that requests all data in the view and run it with the *Pandas.read_sql()* method.


```python
statement = 'SELECT * FROM sample_schema."Sample View Name"'

data = pd.read_sql(statement, conn)

print(data.head(3))
```

You can download multiple Database tables into different data frames and then use Pandas to perform joins, filtering, pivot tables, data cleaning, and other analysis operations.

# SQLAlchemy ORM

[SQLAlchemy](https://www.sqlalchemy.org/SQLAlchemy) is an [Object Relational Mapper (ORM)](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) framework that maps Python classes to relational database tables and automatically converts function calls to SQL statements. SQLAlchemy provides a standard interface that allows Python developers to create system-agnostic code that communicates with a wide variety of data engines. [^3] 

You only need to learn a little bit about SQLAlchemy to read data from the Database. You will learn how to gather information about an existing database's schemas and to build complex, powerful SQL queries that read data from tables and views.

[^3]: From https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/ on March 23, 2023

## Why use SQLAlchemy to generate query statements?

The SQL language is relatively easy to use for simple database table queries. So, why would a Python programmer want to use the SQLAlchemy ORM to build SQL statements?

The SQLAlchemy ORM will output query statements using industry standard optimizations. When working with large and complex databases, users must ensure their SQL statements are optimized. Un-optimized queries can produce the same data as optimized queries but may use up significantly more resources. 

The SQLAlchamy ORM's API is system-agnostic. Different SQL servers support variations on the SQL language so an SQL statement that works on SQLite might not work on Microsoft SQL Server or on Azure Databricks. The same Python code can create different SQL statements for different data storage systems. 

SQLAlchemy allows Programmers to use Python code to express database queries. They may invest their time learning SQLAlchemy instead of learning [multiple SQL language dialects](https://towardsdatascience.com/how-to-find-your-way-through-the-different-types-of-sql-26e3d3c20aab). They may even use [SQLAlchemy instead of the DataBricks API](https://pypi.org/project/sqlalchemy-databricks/) when working with the Microsoft Advanced Analytics Platform.

Finally, SQLAlchemy supports many advanced features that data scientists who use the database do not need to learn right now, but may wish to learn in the future. Investing in learning the SQLAlchemy skills needed to read data from the database views will be useful as a base for more advanced programming projects, in the future. 

## Connect to the Database

Create a [connection string](https://dev.to/chrisgreening/connecting-to-a-relational-database-using-sqlalchemy-and-python-1619#deconstructing-the-database-url) that tells SQLAlchemy which database driver to use, the location of the database, and how to authenticate access to it. 

```python
from azure.identity import InteractiveBrowserCredential

server_name = 'my-database-server.database.windows.net'
database_name = 'my-database-name'
user_name = 'user.name@microsoft.com'

connection_string = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={server_name};"
    f"Database={database_name};"
    f"Authentication=ActiveDirectoryInteractive;"
    f"UID={user_name};PWD=''"
)
```

> **NOTE:** Replace the text in the *server_name*, *database_name*, and *user_name* variables with the real database server, database, and user information.

Next, use the *create_engine()* function from SQLAlchemy and to create an [engine](https://docs.sqlalchemy.org/en/20/core/engines_connections.html) object which includes a connection to the database specified in the URL passed to the *create_engine* function.

```python
from sqlalchemy import create_engine
import pyodbc

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
```

A login browser window will pop up when you perform your first database operation; either when you execute the *pandas.read_sql()* function described immediately below, or when you try to inspect your database schema for the first time.

## Read data directly to Pandas data frame

In the previous chapter, when we used the *pyodbc* driver's connection with the Pandas *read_sql()* method, Pandas raised a warning saying you should instead use an SQLAlchemy connection. Now, we have an SQLAlchemy engine defined so let's try using it with Pandas to read data directly from the Database.

```python
import pandas as pd

statement = """
SELECT TOP 5 
"Column One" AS "column_one", 
"Column Zero Name" AS "column_zero", 
"Column Two" AS "column_two", 
"Column Three" AS "column_three"
FROM sample_schema."Sample View Name"
ORDER BY NEWID()
"""



data = pd.read_sql(statement, engine)
print(data)
```

In the output, the program prints the data frame containing the data selected from the Database.

```
xxxxxx
```

You can see that Pandas read data from the Database without raising an error and that creating and using the SQLAlchemy engine was as easy as creating a *pyodbc* connection.

### Is this all you need to know?

Most data scientists, especially those comfortable working with raw T-SQL statements, will be happy to stop at this point. They have all the tools they need to read data from the Database views into Pandas data frames. 

However, if you want to work mostly in Python and employ the power of SQLAlchemy functions to select the data you need from the database before you import it into a data frame, you may want to learn more about how to use the SQLAlchemy ORM. 

## Use SQLAlchemy to read schemas in a database

To select data from a database, you first need to understand its structure and relationships. As always, it is easiest to look at the Database documentation. If you cannot find adequate information, you can use the same T-SQL statements we showed you previously with SQLAlchemy to read th database schema tables. But, since we are learning SQLAlchemy functions, let's use the [SQLAlchemy *inspect* function](https://docs.sqlalchemy.org/en/20/core/inspection.html#module-sqlalchemy.inspection) to gather information about database schema, tables, and columns.

The following example will print all the schema names in the database.

```python
from sqlalchemy import inspect

inspector = inspect(engine)

schema_list = inspector.get_schema_names()
print(schema_list )
```

The output is shown below

```
['sample_schema',  'another_schema', 'sys', 'views']
```

The schema list is different than when you used the *pyodbc* driver because we looked through the INFORMATION_SCHEMA.VIEWS table or the *cursor* object when we used the ODBC driver so, in that case, you saw only the views that you have permission to read. In this case, you see all schemas in the Database, even the ones you do not have permission to read.

There [does not seem to be a way to read the](https://stackoverflow.com/questions/64260249/how-to-read-a-table-from-information-schema-using-sql-alchemy) [INFORMATION_SCHEMA.VIEWS table](https://github.com/sqlalchemy/sqlalchemy/blob/main/lib/sqlalchemy/dialects/mssql/information_schema.py) using SQLAlchemy's *inspect()* function.

To get a list of only the schemas you have permission to read, use a raw T-SQL statement with SQLAlchemy and read it with Pandas (because we already showed you how to get database information using Pandas). See the example below:

```python
statement = """
SELECT DISTINCT
  TABLE_SCHEMA
FROM INFORMATION_SCHEMA.VIEWS
ORDER BY TABLE_SCHEMA
"""

data = pd.read_sql(statement, engine)
print(data)
```

The output shows only the database schemas that you have permission to read.

```
                             TABLE_SCHEMA

1                           sample_schema
16                         another_schema
```


### Read database tables in a schema

Get a list of the tables available in the schema you wish to explore. Use the *inspector* instance's *[get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names)* method to list the tables in the *sample_schema* schema.

```python
table_list = inspector.get_table_names(schema='sample_schema')

print(table_list)
```

The output is an empty list. 

```
[]
```

The list is empty because the database does not allow you to access its tables directly. It provides you with database views, instead, so the database administrators can better manage security and access. Views are treated like tables by SQLAlchemy, except that they do not have primary keys or relationship information. You'll see this later when you reflect the database metadata. 

To get a list of views available in the *sample_schema* schema, use the *[get_view_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names)* method.

```python
table_list = inspector.get_view_names(schema='sample_schema')

print(table_list)
```

This outputs a list of seventeen views.

```
['Basic Employment Details All', 'Basic Employment Details Current', 'Externals', 'Flexible Working', 'Global_Mobility_AssigDetail', 'Monitoring of Tasks', 'New Line Managers', 'Organizational Data All', 'Organizational Data Current', 'Other IDs', 'Snapshot Non P24 Headcount', 'Snapshot Non P24 Last Close', 'Snapshot P24 Employee Master', 'Sample View Name', 'Snapshot P24 Organizational Data', 'Snapshot P24 Workforce Delta', 'Snapshot P24 Workforce Delta mapping view']
```

### Read column information from a database table

Views are treated like tables in the database metadata so you may use the *inspector* instance's *[get_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns)* method to list columns in a specified view, in a specified schema.  

```python
columns_list = inspector.get_columns(
    'Sample View Name', 
    schema='sample_schema')
print(*columns_list[0].keys(), sep=", ")
for x in columns_list:
    print(*x.values(), sep=", ")
```

The output shows the columns and their attributes such as data type, nullability, and default value.

```
name, type, nullable, default, autoincrement, comment
Column Zero, VARCHAR(10) COLLATE "SQL_Latin1_General_CP1_CI_AS", True, None, False, None
Column One, VARCHAR(8) COLLATE "SQL_Latin1_General_CP1_CI_AS", True, None, False, None
Column Two, VARCHAR(24) COLLATE "SQL_Latin1_General_CP1_CI_AS", True, None, False, None
...
```

The output continues to print out column information until all 313 columns are listed.

## Declare SQLAlchemy ORM Classes

SQLAlchemy requires that you use ORM classes to map Database elements to Python objects. There are four ways to do this and each may be preferable, depending on the goals of your program.

1. Use [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) to map Database elements to an SQLAlchemy ORM Class
    * This is the procedure we recommend you use
    * It documents the subset of database information you use in your program and provides the fasted application performance
    * But, you need to learn the details of the SQLAlchemy ORM so you can properly map ORM class attributes to the database view columns so, when you are getting started, you might choose to use database reflection, mentioned below
2. Get table metadata via database reflection and use it to automatically build an SQLAlchemy ORM Class (or SQLAlchemy Table object)
    * Database reflection is useful if you plan to read all columns in a database view, and
    * If fast application performance is not a requirement
3. Get table metadata via database reflection, and override specific database elements in an SQLAlchemy ORM Class
    * This hybrid approach is useful if you want to access a number of reflected database columns using class attributes in normal Python syntax,
    * If you want to inherit other database metadata without having to explicitly define it in your code, and
    * If fast application performance is not a requirement

### Declarative Mapping

The SQLAlchemy documentation recommends you use [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) to manually build SQLAlchemy Table objects or ORM classes that enable programmers to access table data. 

Describing database information in your Python program as classes enables other program maintainers learn about the database by reading the Python code. This makes it easier for Python programmers to maintain the code. It also makes a program more robust because changes in the Database schema will either have no effect on your program, or will cause an obvious error. Declarative Mapping is also much faster than using database reflection, which we will discuss later, every time you run your Python program.

In the examples below, you declare a subset of the *sample_schema.Sample View Name* view's columns so you can access data in them as Python objects. As an example, [create an ORM class](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html) that maps five columns from the *sample_schema.Sample View Name* table:

```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Sample_View_Name(Base):
    __tablename__ = "Sample View Name"
    __table_args__ = {"schema": "sample_schema"}
    
    column_zero = mapped_column("Column Zero", String(10), primary_key=True)
    column_one = mapped_column("Column One", String(8))
    column_four = mapped_column("Employment Status Name", String(256))
    column_two = mapped_column("Column Two", String(48))
    column_three = mapped_column("Column Three", String(100))
```

In the example above, The Base class contains an empty *Base.metadata* object. Then, you used the SQLAlchemy Table class to add table schema, name, and column information to *Base.metadata*.

After creating the class *Sample_View_Name*, you can access the defined database fields by calling the class attribute associated with each one. For example, access data in the *column_one* column using the statement, `select(Sample_View_Name.column_one)`.

Execute the following code to list some data from the table:

```python
from sqlalchemy import select

statement = select(
    Sample_View_Name.column_one, 
    Sample_View_Name.column_two, 
    Sample_View_Name.column_three
    ).limit(5)

with Session(engine) as session:
    result = session.execute(statement)
    columns = result.keys()
    data = result.all()

print(*columns, sep=", ")
for x in data:
     print(*x, sep=", ")
```

The output is shown below. You can see you data you selected 

```
column_one, column_two, column_three
xxxx
```


### Get table metadata via database reflection

Instead of explicitly declaring table metadata using Declarative Mapping, you could use [database reflection](https://betterprogramming.pub/reflecting-postgresql-databases-using-python-and-sqlalchemy-48b50870d40f), which is the process of automatically building new objects based on an existing database's schema information. It is useful when writing simple, single-use scripts like the ones in this document. But, it takes much more processing time to reflect the database tables. If you are writing more complex programs, you should use the declarative mapping process described earlier to get better performance.

Normally, you would expect that you could use the [SQLAlchemy Automap extension](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html) to map database tables and relationships to SQLAlchemy ORM classes. However, SQLAlchemy can only map the database views into *Table* objects because the Database access is restricted. 

the database users typically do not have access to database tables. Access to the database is provided by database views created by the database team. These views have no primary keys defined. Since ORM classes must have a primary key, SQLAlchemy's automap extension will map the views into table objects but will not automatically create ORM classes that represent those tables. You must manually create classes from the mapped Table columns, instead.

There are multiple [reflection schemes](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-schemas) that programmers may employ. 

You can reflect  in a schema, which takes a long time: five or six minutes.

```python
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base

metadata = MetaData()
metadata.reflect(engine, views=True, schema="sample_schema")
metadata.reflect(engine, views=True, schema="another_schema")
Base = automap_base(metadata=metadata)
```

You used SQLAlchemy's *automap_base* function to create a [declarative base class instance](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#basic-use) named *Base* and then used its *prepare* method to automatically map, or *reflect*, the database schema metadata.

```python
print(*Base.metadata.tables.keys(), sep="\n")
```

You see the *Base.metadata* object contains information about all the tables in the *another_schema* and *sample_schema* schemas.

```
sample_schema.Sample View Name
...
another_schema.Another View
...
```

Database reflection is faster if you specify the tables you want to reflect in each schema, so you gather only the metadata that you need.

```python
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base

metadata = MetaData()
metadata.reflect(engine, views=True, schema="sample_schema", only=['Sample View Name'])
metadata.reflect(engine, views=True, schema="another_schema", only=['Another View'])

Base = automap_base(metadata=metadata)
```

Now, if you print the metadata, you see it only contains information about the two tables you specified.

```python
print(*Base.metadata.tables.keys(), sep="\n")
```

The output shows two table names:

```
sample_schema.Sample View Name
another_schema.Another View
```

You will notice that the reflection took much less time; about 30 seconds, this time.

Now, you can access tables using the *Base.metadata* object. For example, the *Sample View Name* table can be accessed with the statement, `Base.metadata.tables['sample_schema.Sample View Name']`. You can assign tables to new variables to make them easier to work with in your code:

```python
snapshot_p24_last_close = Base.metadata.tables['sample_schema.Sample View Name']
snapshot_p24_job_catalog = Base.metadata.tables['another_schema.Another View']
```

Now, you can get table data from the new table variable. For example:

```python
print(snapshot_p24_last_close.name)
print(snapshot_p24_job_catalog.name)
```

The above code lists the name of each table. So, we know the variable points to the correct table information in the *Base.metadata* object.

```
Sample View Name
Another View
```

You can access table column information from the table variable you just created. For example, you can get column names:

```python
print(snapshot_p24_last_close.columns.keys())
```

The *columns.key()* method listed the column names in the *Sample View Name* table. 

```
['Column Zero',  'Column One',  'Column Two',...]
```

It is possible to build select statements by indexing table columns. For example, the following *select()* statement, which we cover in the next chapter, selects five rows from three columns from the *Sample View Name* table:

```python
stmt = select(
    snapshot_p24_last_close.columns['Column One'], 
    snapshot_p24_last_close.columns['Column Two'],
    snapshot_p24_last_close.columns['Column Three']
).limit(5)
```

But we want to use the SQLAlchemy ORM, which means we need to represent tables as ORM classes. Another way to do this is to build a class from reflected table metadata, as shown below. You cannot use [normal table reflection techniques](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-declaratively-with-reflected-tables) because the database views do not have primary keys. Instead, we [create an ORM class](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#alternate-attribute-names-for-mapping-table-columns) that point to table metadata.

```python
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
import pandas as pd

metadata = MetaData()
metadata.reflect(engine, 
                 views=True, 
                 schema="sample_schema", 
                 only=['Sample View Name'])

Base = automap_base(metadata=metadata)

class Sample_View_Name(Base):
    __table__ = (
        Base.metadata.tables['sample_schema.Sample View Name']
        )
    __mapper_args__ = {'primary_key': [__table__.c['Column Zero']]}

Base.prepare(engine)
```

The SQLAlchemy ORM classes [must include a primary key](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-to-an-explicit-set-of-primary-key-columns) so we added it in the *__mapper_args__* class attribute, overloading the *Column Zero* column and declaring it to be a private key. The primary key should be unique for each row so we chose to define the *Column Zero* column as the primary key. 

We then ran the *Base.prepare()* method so the *Base.metadata* object is updated with the primary key defined in the *Sample_View_Name* class.

An alternative to reflecting database metadata with the *reflect()* method is to autoload the table directly in the ORM class. For example, you can rewrite the database reflection example above as the following:

```python
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
import pandas as pd

metadata = MetaData()
Base = automap_base(metadata=metadata)

class Sample_View_Name(Base):
    __table__ = Table("Sample View Name", 
                      metadata, 
                      autoload_with=engine, 
                      schema="sample_schema")
    __mapper_args__ = {'primary_key': [__table__.c['Column Zero']]}

Base.prepare(engine)
```

You may use the method you feel results in more readable code in your program.

Now that tables are represented as class attributes, you may want to select columns in the class but, because the Database has spaces in most of its column names, you cannot use the normal "dot notation". Instead you reference columns using the *getattr* function, as shown below:

For example, if you wanted to select only three specific columns, your select statement would be similar to the following code:

```python
statement = select(
    getattr(Sample_View_Name, 'Column One'),
    getattr(Sample_View_Name, 'Column Two'),
    getattr(Sample_View_Name, 'Column Three'),
)
```

### Override view columns in an SQLAlchemy ORM Class

If you want to use dot notation to reference the database table columns in your code, you need to define a class attribute that points to the metadata of each column that you wish to use. 

For example, define class attributes for five specific columns from the *Sample View Name* database view:

```python
class Sample_View_Name(Base):
    __table__ = (
        Base.metadata.tables['sample_schema.Sample View Name']
        )
    __mapper_args__ = {'primary_key': [__table__.c['Column Zero']]}

    column_zero = __table__.c['Column Zero']
    column_one = __table__.c['Column One']
    column_two = __table__.c['Column Two']
    column_three = __table__.c['Column Three']
    column_four = __table__.c['Employment Status Name']

Base.prepare(engine)
```

The class shown above defines attributes associated with specific table columns. While you still have to define the specific columns you want to use in the class, each column already has all its attributes, such as data types or nullability, defined from the reflected metadata. 

Now that table columns are represented as attributes of the *Sample_View_Name* class, you can select data in table columns using dot notation, as shown below:

```python
stmt = select(
    Sample_View_Name.column_one, 
    Sample_View_Name.column_two, 
    Sample_View_Name.column_three
).limit(5)
```

The class attribute syntax is easier to work with compared to using the *getattr()* function and it is the same as if you were working with either reflected tables or tables defined using Declarative Mapping.

In summary, a full program that defines an ORM class that can be used to select data from specific database columns using dot notation is listed below:

```python
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base

metadata = MetaData()
Base = automap_base(metadata=metadata)

class Sample_View_Name(Base):
    __table__ = Table("Sample View Name", 
                      metadata, 
                      autoload_with=engine, 
                      schema="sample_schema")
    __mapper_args__ = {'primary_key': [__table__.c['Column Zero']]}
    
    column_zero = __table__.c['Column Zero']
    column_one = __table__.c['Column One']
    column_two = __table__.c['Column Two']
    column_three = __table__.c['Column Three']
    column_four = __table__.c['Employment Status Name']

Base.prepare()
```

### Recommendation

Since we cannot automatically reflect ORM classes from the database views, it may be better to define tables using Declarative Mapping after you have decided which columns you need for your application. 

But, if you prefer to load the entire contents of a table into a data frame for further analysis, you can still use reflection effectively because you do not need to define the columns when you want to read all the columns.

## Read data from selected columns in a table

Use the SQLAlchemy [*select()* function](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) to create SQL SELECT statements and that read rows from tables in the database. The *select()* function returns an instance of the SQLAlchemy *Select* class, which offers methods that can be chained together to provide all the information the Select object needs to output an SQL query.

Use the SQLAlchemy guides, [*Using Select Statements*](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) and the [*ORM Querying Guide*](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html) as references when you need to look up additional methods to build the SQL queries you need.

The following code builds an SQL query that selects the first five rows in the Database's *Sample View Name* table, which we mapped to the *Sample_View_Name* class in the previous chapter.. 

```python
statement = select(
    Sample_View_Name.column_one, 
    Sample_View_Name.column_two, 
    Sample_View_Name.column_three
).limit(5)
```

The *statement* variable name is assigned to the SQLAlchemy Select object returned by the *Select()* function. Pass it to the Session object to get the results of the generated SQL query from the database.


```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    result = session.execute(stmt)
    headers = result.keys()
    data = result.all()

print(*headers, sep=", ")
for x in data:
     print(*x, sep=", ")
```

You will see data from the first five rows of the selected columns in the printed output:

```
column_one, column_two, column_three
xxx
```

## Convert results to Pandas data frame

As you can see, programmers can use a *Select* instance's methods to perform complex queries and can chain these instance methods.

The results of an SQL query can be converted to a Pandas data frame using the *pandas.DataFrame* class.

For example, create an SQL statement that groups items by country, counts the number of items in each country, and sorts the results in descending order. Then convert the result into a Pandas data frame.


```python
from sqlalchemy import desc

statement = (
    select(
        Sample_View_Name.column_two,
        func.count(Sample_View_Name.column_zero)
        .label("Num_Items")
    ).group_by(Sample_View_Name.column_two)
    .order_by(desc("Num_Items"))
)

with Session(engine) as session:
    result = session.execute(statement)
    headers = result.keys()
    results = result.fetchall()

countries = pd.DataFrame(results, columns=headers)
print(countries)
```

The results in a sorted list of countries by number of items:

```
xxxxxx    

[115 rows x 2 columns]
```

## Read entire tables into Pandas dataframes

As we saw in the previous sections, you can read entire tables from the database into Pandas for analysis. You can use one of the following methods to create a select statement that asks for all data in a table.

1. Just use a raw T-SQL SELECT statement
2. Define an SQLAlchemy ORM class using Declarative Mapping, then select that class
3. Define an SQLAlchemy ORM class using database reflection, then select the class

You can download multiple Database tables into different data frames and then use Pandas to perform joins, filtering, pivot tables, data cleaning, and other analysis operations.

### Using raw T-SQL is simpler

It is simpler to use a raw T-SQL query statement to select all information in an database view, like we did at the start of the SQLAlchemy chapter. The following statement will read all rows from the *Sample View Name* into a pandas data frame and does not require you to first declare or reflect the table:

```python
statement = 'SELECT * FROM sample_schema."Sample View Name"'

data = pd.read_sql(statement, engine)
print(data.head(6))
```

This way is fast and simple and you do not have to understand the SQLAlchemy ORM to use it. If you plan to do all your data filtering, sorting, and manipulation in Pandas or another data framework, then we recommend this method.

### Using declarative mapping

You must already have an SQLAlchemy ORM class defined in your program to use it in your SQLAlchemy ORM *select()* function. The following example shows how you would declare the class and then use it in a select statement so Pandas can read all the rows from the table.

Do not run the following code unless you really want to read all the data in a table. Database tables can be very large and it can take hours to download all the data. To download all rows in the *Sample View Name* table into a Pandas data frame, run the following code.

```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
import pandas as pd

class Base(DeclarativeBase):
    pass

class Sample_View_Name(Base):
    __tablename__ = "Sample View Name"
    __table_args__ = {"schema": "sample_schema"}
    
    column_zero = mapped_column("Column Zero", String(10), primary_key=True)
    column_one = mapped_column("Column One", String(8))
    column_four = mapped_column("Employment Status Name", String(256))
    column_two = mapped_column("Column Two", String(48))
    column_three = mapped_column("Column Three", String(100))
    # ...
    # The Sample View Name has 313 columns,
    # so add 308 more columns to this table
    # ...

statement = select(Sample_View_Name)

data = pd.read_sql(statement, engine)
print(data.head(3))
```

Using Declarative Mapping to define a table with 313 columns is a lot of work and is not practical for short, single-use scripts like this. But, maybe you have already carefully defined the columns you need in SQLAlchemy Table objects and maintain them in another file for use in more complex programs. 

### Using database reflection

If you are just exploring data and performance is not an issue, consider using [database reflection](https://docs.sqlalchemy.org/en/20/core/reflection.html). The following code reflects the metadata for the table we want and passes it to the SQLAlchemy *select()* function. 

Again, don't run this code unless you want to wait about an hour for the process to finish and you have at least 2 GB of memory free on your PC.

```python
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
import pandas as pd

metadata = MetaData()
Base = automap_base(metadata=metadata)

class Sample_View_Name(Base):
    __table__ = Table("Sample View Name", 
                      metadata, 
                      autoload_with=engine, 
                      schema="sample_schema")
    __mapper_args__ = {'primary_key': [__table__.c['Column Zero']]}

Base.prepare(engine)

statement = select(Sample_View_Name).limit(10)

data = pd.read_sql(statement, engine)
print(data.head(3))
```

## Perform operations in SQL database

If you are already familiar with Microsoft SQL Server, you know that you can perform operations on the database server that filter and process data before returning it to you in a result. You can SQLAlchemy ORM code to perform data operations like filtering data, joining tables, and running functions on the server.


### Filtering database results in Python

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

The SQAlchemy *func()* function has many methods that allow you to run [SQL functions](https://learn.microsoft.com/en-us/sql/t-sql/functions/functions?view=sql-server-ver16) on the SQL server. [^4] To select data from a random sample of five items, run the SQL Server's [*NEWID()* T-SQL function](https://learn.microsoft.com/en-us/sql/t-sql/functions/newid-transact-sql?view=sql-server-ver16#d-query-random-data-with-the-newid-function). Create a statement like the following:

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

You can chain methods in the same statement so that all operations are performed before the server sends the result to your program. In the following example, we call SQL Server's *COUNT()* function to count the number of rows in the table. Then we filter that count by column_two and/or column_four, using the *where()* method. 

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



### Joining the database tables

You can create SQL statements that join data in multiple tables using the [SQLAlchemy *Select* class's *join()* and *join_from()* methods](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#joins).

However, because the database views do not have primary keys and do not have relationships defined between views, it is probably better to get the data you need by loading selected data from multiple tables into separate data frames and then using Pandas to join the data frames according to your needs.

If you really want to perform joins on the SQL server, then you should build your SQLAlchemy ORM model using [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) and carefully define the primary keys and relationships constraints such as foreign keys in the table classes you create. Or, you can manually specify columns on which to join tables in the *select()* statement.



# Conclusion

We showed you two tools that make it easier for Python programs to access data in the Database. 

We first demonstrated the *pyodbc* library. Using the *pyodbc* database connection and its cursor function, along with statements generated in T-SQL syntax, we can select data from the Database and store it in Python objects. We can also convert database data into Pandas data frames for further analysis.

Next, we demonstrated the *SQLAlchemy* package. You can use an SQLAlchemy connection along with raw T-SQL statements to read data from the Database directly into a Pandas data frame. Or, you can also use the SQLAlchemy package's *Select* class to build SQL statements using Python and avoid learning the details of SQL syntax. 

We make the following recommendations to data scientists working with the Database, who need their Python program to directly access database data.

## Which database driver should you use?

Because you are just reading data from the database, you should use the driver which is best supported by the data analysis library you are using. For example, if you are using Pandas, you would create a database connection using SQLAlchemy. 

## Should you use T-SQL or the SQLAlchemy ORM?

Most data scientists will need to learn SQL, anyway. Raw T-SQL statements can be used with either *pyodbc* or *SQLAlchemy* functions. So, we recommend you learn the basics of T-SQL *SELECT* statements and then create T-SQL statements to get data, regardless of the database driver you use. 

## When would you use SQLAlchemy?

Although you don't need to use the SQLAlchemy ORM model to generate SQL statements in simple programs, you may still decide to learn how to use the SQLAlchemy ORM when you create complex programs. You might also want to use the SQLAlchemy ORM if you are a Python programmer who does not want to use raw SQL syntax in your Python code. SQLAlchemy's features are helpful if you work with multiple developers on the same project.





# Appendix B: Alternative ways to get database schema information

There are multiple ways to get database schema information in a Python program. In the main body of this document, we covered one method for the *pyodbc* driver and one the is native th the *SQLAlchemy ORM*. This appendix covers other methods that also get database information:

* pyodbc driver
  * Read database information from the *cursor* instance created by the pyodbc connection's *cursor()* method.
  * query the SQL Server database's *sys.objects* catalog view
* SQLAlchemy
  * Reflect the database and read information from the *metadata* intance.


## Read database information from the *cursor*

A *cursor* object is instantiated is when you call the pyodbc connection's *cursor()* method. You do not need to know how to write SQL statements when using the *cursor* object and it offers [many methods and attributes](https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki) that describe the database details. But, the cursor object lists all database elements, even those that you do not have permission to access. 

### Schema names

Create an instance of the [pyodbc cursor](https://github.com/mkleehammer/pyodbc/wiki/Cursor):

```python
cursor = conn.cursor()
```

Then, iterate through all tables in the object returned by the cursor's *tables()* method.

```python
for table_name in cursor.tables():
    print(table_name)
```

This lists all tables and views in a database. You see many rows listed. The available schemas are in the output's second column.

```
('database_name', 'sys', 'trace_xe_action_map', 'TABLE', None)
('database_name', 'sys', 'trace_xe_event_map', 'TABLE', None)
('database_name', 'sample_schema', '', 'VIEW', None)
('database_name', 'sample_schema', '', 'VIEW', None)
('database_name', 'INFORMATION_SCHEMA', 'VIEW_COLUMN_USAGE', 'VIEW', None)
('database_name', 'INFORMATION_SCHEMA', 'VIEWS', 'VIEW', None)
...
```

### Table and views names in a schema

Use the cursor object's *tables()* method again but pass it a schema parameter so it lists only tables and views from the schema you are interested in exploring. In this example, you will generate a list of views in the *sample_schema* schema.

```python
cursor = conn.cursor()

for row in cursor.tables(schema='sample_schema'):
    print(row[2], sep=", ")
```

In this example, we wanted the table name from each row. We knew that the tables names were in the third column so we iterated through each row and generated the output seen below: 

```
B
Sample View Name
xxxxxxx
```

### Column names in a table

Use the *cursor.columns()* method to get a list of table information and pass it a table or view name and a schema name.

In this example, choose the table named *Sample View Name* from the *sample_schema* schema. Use the *cursor.columns()* method to get a list of table information. In the example below, you get the headers for the returned information from the *cursor.description* attribute. The column name, type, and size are in the fourth, sixth, and seventh column of the returned results.

```python
column_list = (
    cursor.columns(
        table='Sample View Name', 
        schema='sample_schema')
    .fetchall()
)

# headers
headers = [h[0] for h in cursor.description]
print(f'{headers[3]:{25}}{headers[5]:{20}}{headers[6]:{11}}')

# data
for row in column_list:
    print(f'{row[3]:{25}}{row[5]:{20}}{row[6]:{6}}')
```

The output print out column information until all 313 columns from the table are listed.

```
column_name              type_name           column_size
xxxxxx
...
```

### Table constraints

Normally, database tables are defined with constraints such as a primary key and foreign keys.

Use the cursor object's *primaryKeys()* and *foreignKeys()* methods to determine if any columns in the table are primary keys or foreign keys:

```python
table = 'Sample View Name'
schema = 'sample_schema'

primary_keys = cursor.primaryKeys(table=table, schema=schema).fetchall()
print(f"{table}:  Primary Keys = {primary_keys}")

foreign_keys = cursor.foreignKeys(table=table, schema=schema).fetchall()
print(f"{table}:  Foreign Keys = {foreign_keys}")
```

You will see that the *Sample View Name* view has no primary or foreign keys. 

```
Sample View Name:  Primary Keys = []
Sample View Name:  Foreign Keys = []
```

In fact, none of the views in the Database have primary keys defined. This acceptable when you are only reading data from the database. The primary key, foreign keys, and other constrains define relationships between tables in a relational database. Knowing the database relationship information is helpful, but not necessary, when reading information from tables. 



## Get data from the *sys.objects* view

Another way to get database information is to query the [sys.objects](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16) catalog view in the SQL Server database. 

### Schema names

The T-SQL statement below [^2] finds all the schema IDs in the *sys.objects* view and then finds their schema names in the *sys.schema* table by joining on the schema ID.

[^2]: Statement copied from StackOverflow post *[SQL Server - Return SCHEMA for sysobjects](https://stackoverflow.com/a/917431)* (917431)

```python
statement = """
SELECT DISTINCT sys.schemas.name AS schema_name
FROM sys.objects 
INNER JOIN sys.schemas ON sys.objects.schema_id = sys.schemas.schema_id
ORDER BY schema_name
"""

cursor.execute(statement)
schema_list = cursor.fetchall()
print(schema_list)
```

The schema information is the same as was gathered from the *INFORMATION_SCHEMA.VIEWS* table.

```
[('compensation_and_performance',), ('employment_details',), ('global_mobility',), ('ot_recruitment',), ('personal',), ('recognition',), ('s4u_arp',), ('s4u_arp_short_term_incentives',), ('s4u_perf_annual_development_review',), ('s4u_perf_goal_setting',), ('s4u_perf_performance_improvement_plan',), ('s4u_succ_employee_career_flags',), ('s4u_succ_position_mdf',), ('s4u_succ_track_record_and_experiences',), ('s4u_succession',), ('sales_incentive',), ('supplemental',)]
```

### Table and views names in a schema

To get the table name information from the *sys.objects* catalog view, create the following SQL statement and then execute it.

```python
statement = """
SELECT sys.objects.name AS table_name
FROM sys.objects 
INNER JOIN sys.schemas ON sys.objects.schema_id = sys.schemas.schema_id
WHERE sys.schemas.name = 'employment_details'
"""

cursor.execute(statement)
for row in cursor.fetchall():
    print(*row)
```

The output contains table and view names in the *employment_details* schema.

```
Basic Employment Details All
Basic Employment Details Current
Externals
Flexible Working
Global_Mobility_AssigDetail
Monitoring of Tasks
New Line Managers
Organizational Data All
Organizational Data Current
Other IDs
Snapshot Non P24 Headcount
Snapshot Non P24 Last Close
Snapshot P24 Employee Master
Snapshot P24 Last Close
Snapshot P24 Organizational Data
Snapshot P24 Workforce Delta
Snapshot P24 Workforce Delta mapping view
```

### Column names in a table

To get the column name information from the *sys.objects* catalog view, create the following SQL statement and then execute it.

```python
statement = """
SELECT 
   sys.columns.name AS column_name, 
   sys.types.name AS column_type, 
   sys.columns.max_length AS length
FROM sys.objects 
INNER JOIN sys.columns ON sys.objects.object_id = sys.columns.object_id
INNER JOIN sys.types ON sys.types.system_type_id = sys.columns.system_type_id
WHERE sys.objects.name = 'Snapshot P24 Last Close'
AND sys.types.name != 'sysname'
"""

cursor.execute(statement)
for row in cursor.fetchall():
    print(f"{row[0]:24}{row[1]:10}{row[2]:10}")
```

The output contains name, type, and length of each column in the *Snapshot P24 Last Close* view. It will print out all 313 columns so we show only a subset below.

```
Employee ID             varchar           10
Period                  datetime           8
Pers No                 varchar            8
HC RLS Group            varchar           24
Country Legal           varchar            2
Country Legal Name      varchar           80
HC driver               varchar           20
Nokia ID                varchar           20
UPI                     varchar           30
Last Name               nvarchar          80
First Name              nvarchar          80
...
```

### Table constraints

To get information about constraints such as a primary key, query tables in the *sys* schema with the following code. [^7] The example below asks for constraint information in the view named *Snapshot P24 Last Close*.

[^7]: From [Stack Overflow answer: reference# 18622200](https://stackoverflow.com/questions/18622200/how-do-i-get-constraints-on-a-sql-server-table-column)

```python
statement = """
SELECT
    chk.definition
FROM sys.check_constraints chk
INNER JOIN sys.columns col
    ON chk.parent_object_id = col.object_id
INNER JOIN sys.tables st
    ON chk.parent_object_id = st.object_id
WHERE st.name = 'Snapshot P24 Last Close'
AND col.column_id = chk.parent_column_id
"""

cursor.execute(statement)
print(cursor.fetchall())
```

This outputs only an empty list, which indicates there are no constraints in the view so we now know there is no primary key in the view named *Snapshot P24 Last Close*.








