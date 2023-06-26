% SQL and Python access to the database


https://databudd.com/blog/tableau-data-analysis-bootcamp-master-data-visualization
https://www.sqlservercentral.com/articles/connecting-to-adventureworks-on-azure




This document will show you how to use simple SQL queries to read data from the Database, using either  

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





## Install Microsoft ODBC driver for SQL Server

Download and install the [Microsoft ODBC Driver for SQL Server on Windows](https://learn.microsoft.com/en-us/sql/connect/odbc/windows/microsoft-odbc-driver-for-sql-server-on-windows?view=sql-server-ver16). Microsoft ODBC Driver 18 for SQL Server supports Azure Active Directory integrated authentication.

Download the installer file *msodbcsql.msi* from the SQL driver's [downloads page](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) and save it. Then double-click on the installer file and follow the install wizard to compete installation.

![Microsoft ODBC Driver for SQL Server installer](./Images/odbc-driver-003.png){width=60%}


## Create a Python virtual environment

To create a Python virtual environment, run the following commands:

```bash
$ mkdir data-science-folder
$ cd data-science-folder
$ python3 -Xfrozen_modules=off -m venv env
```

Then, activate the virtual environment.

```
> .\env\Scripts\activate
(env) > 
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

## Install Python database drivers

Next, install [*pyodbc*](https://mkleehammer.github.io/pyodbc/), the open-source Python ODBC driver for SQL Server. This provides the Python interface to the Windows ODBC driver. 

```powershell
(env) > pip install pyodbc 
```




## Install dotenv

```bash
(env) $ pip install python-dotenv
```

## Create the .env file

https://analyzingalpha.com/jupyter-notebook-environment-variables-tutorial

need variables for

```python
DB_SERVER=server.name.com
DB_NAME=database_name
DB_UID=username
DB_PWD=password
```

See my post about [using dotenv files]({filename}/articles/011-use-environment-variables/use-environment-variables.md).

# Python ODBC driver and T-SQL

You can use the *pyodbc* Python library to connect to and read data from an SQL Server database. Create a connection object by passing the necessary database and user information to the pyodbc driver's *connect()* function. You will create T-SQL statements and pass them to the connection object's  driver. 

## Environment variables



```python

```
## Connect to Database

Import the *pyodbc* module and create a database connection string that you can pass into the driver's *connect()* function. 

```python
import os
import pyodbc

userid = os.environ.get('DB_UID')
password = os.environ.get('DB_PWD')
db_server_name = os.environ.get('DB_SERVER')
db_name = os.environ.get('DB_NAME')

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"+
    "Server=tcp:"+db_server_name+",1433;"+
    "Database="+db_name+";"+
    "Uid="+userid+";"+
    "Pwd="+password+";"+
    "Encrypt=yes;"+
    "TrustServerCertificate=no;"+
    "Connection Timeout=30;"
)

conn = pyodbc.connect(connection_string)
print(conn)
```

The example above, when run, opens an interactive login session in a new web browser window. Enter your Microsoft password into the password prompt in the browser window.


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

Create a [Microsoft Transact-SQL (T-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql) [^1] statement that selects the TABLE_SCHEMA column in the table and sorts data alphabetically:



[^1]: Microsoft Transact-SQL, also known as T-SQL, is Microsoft SQL Server's version of the [SQL language](https://en.wikipedia.org/wiki/SQL).

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

# Appendix B: Alternative ways to get database schema information

There are multiple ways to get database schema information in a Python program. In the main body of this document, we covered one method for the *pyodbc* driver and one the is native th the *SQLAlchemy ORM*. This appendix covers other methods that also get database information:

* pyodbc driver
  * Read database information from the *cursor* instance created by the pyodbc connection's *cursor()* method.
  * query the SQL Server database's *sys.objects* catalog view



## Read database information from the *cursor*

A *cursor* object is instantiated is when you call the pyodbc connection's *cursor()* method. You do not need to know how to write SQL statements when using the *cursor* object and it offers [many methods and attributes](https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki) that describe the database details. But, the cursor object lists all database elements, even those that you do not have permission to access. 

### Schema names

Create an instance of the [pyodbc cursor](https://github.com/mkleehammer/pyodbc/wiki/Cursor):

```python
cursor = conn.cursor()
```

Then, iterate through all tables in the object returned by the cursor's *tables()* method.

```python
for row in cursor.tables():
    print(row)
```

This lists all tables and views in a database. You see many rows listed. The available schemas are in the output's second column.

```
('data-science-test', 'dbo', 'BuildVersion', 'TABLE', None)
('data-science-test', 'dbo', 'ErrorLog', 'TABLE', None)
('data-science-test', 'SalesLT', 'Address', 'TABLE', None)
('data-science-test', 'SalesLT', 'Customer', 'TABLE', None)
('data-science-test', 'SalesLT', 'CustomerAddress', 'TABLE', None)
('data-science-test', 'SalesLT', 'Product', 'TABLE', None)
('data-science-test', 'SalesLT', 'ProductCategory', 'TABLE', None)
('data-science-test', 'SalesLT', 'ProductDescription', 'TABLE', None)
('data-science-test', 'SalesLT', 'ProductModel', 'TABLE', None)
('data-science-test', 'SalesLT', 'ProductModelProductDescription', 'TABLE', None)
('data-science-test', 'SalesLT', 'SalesOrderDetail', 'TABLE', None)
('data-science-test', 'SalesLT', 'SalesOrderHeader', 'TABLE', None)
('data-science-test', 'sys', 'trace_xe_action_map', 'TABLE', None)
('data-science-test', 'sys', 'trace_xe_event_map', 'TABLE', None)
('data-science-test', 'INFORMATION_SCHEMA', 'CHECK_CONSTRAINTS', 'VIEW', None)
('data-science-test', 'INFORMATION_SCHEMA', 'COLUMN_DOMAIN_USAGE', 'VIEW', None)
...
```

### Table and views names in a schema

Use the cursor object's *tables()* method again but pass it a schema parameter so it lists only tables and views from the schema you are interested in exploring. In this example, you will generate a list of views in the *sample_schema* schema.

```python
cursor = conn.cursor()
for row in cursor.tables(schema='SalesLT'):
    print(*row, sep=', ')
cursor.close()
```

In this example, we wanted the table name from each row. We knew that the tables names were in the third column so we iterated through each row and generated the output seen below: 

```
data-science-test, SalesLT, Address, TABLE, None
data-science-test, SalesLT, Customer, TABLE, None
data-science-test, SalesLT, CustomerAddress, TABLE, None
data-science-test, SalesLT, Product, TABLE, None
data-science-test, SalesLT, ProductCategory, TABLE, None
data-science-test, SalesLT, ProductDescription, TABLE, None
data-science-test, SalesLT, ProductModel, TABLE, None
data-science-test, SalesLT, ProductModelProductDescription, TABLE, None
data-science-test, SalesLT, SalesOrderDetail, TABLE, None
data-science-test, SalesLT, SalesOrderHeader, TABLE, None
data-science-test, SalesLT, vGetAllCategories, VIEW, None
data-science-test, SalesLT, vProductAndDescription, VIEW, None
data-science-test, SalesLT, vProductModelCatalogDescription, VIEW, None
```

### Column names in a table

Use the *cursor.columns()* method to get a list of table information and pass it a table or view name and a schema name.

In this example, choose the table named *Sample View Name* from the *sample_schema* schema. Use the *cursor.columns()* method to get a list of table information. In the example below, you get the headers for the returned information from the *cursor.description* attribute. The column name, type, and size are in the fourth, sixth, and seventh column of the returned results.

```python
cursor = conn.cursor()

column_list = (
    cursor.columns(
        table='Address', 
        schema='SalesLT')
    .fetchall()
)

# headers
headers = [h[0] for h in cursor.description]
print(f'{headers[3]:{25}}{headers[5]:{20}}{headers[6]:{11}}')

# data
for row in column_list:
    print(f'{row[3]:{25}}{row[5]:{20}}{row[6]:{6}}')

cursor.close()
```

The output print out column information until all 313 columns from the table are listed.

```
column_name              type_name           column_size
AddressID                int identity            10
AddressLine1             nvarchar                60
AddressLine2             nvarchar                60
City                     nvarchar                30
StateProvince            Name                    50
CountryRegion            Name                    50
PostalCode               nvarchar                15
rowguid                  uniqueidentifier        36
ModifiedDate             datetime                23
```

### Table constraints

Normally, database tables are defined with constraints such as a primary key and foreign keys.

Use the cursor object's *primaryKeys()* and *foreignKeys()* methods to determine if any columns in the table are primary keys or foreign keys:

```python
cursor = conn.cursor()

table = 'Address'
schema = 'SalesLT'

primary_keys = cursor.primaryKeys(table=table, schema=schema).fetchall()
print(f"{table}:  Primary Keys = {primary_keys}")

foreign_keys = cursor.foreignKeys(table=table, schema=schema).fetchall()
print(f"{table}:  Foreign Keys = {foreign_keys}")

cursor.close()
```

You will see that the *Sample View Name* view has no primary or foreign keys. 

```
Address:  Primary Keys = [('data-science-test', 'SalesLT', 'Address', 'AddressID', 1, 'PK_Address_AddressID')]
Address:  Foreign Keys = [('data-science-test', 'SalesLT', 'Address', 'AddressID', 'data-science-test', 'SalesLT', 'CustomerAddress', 'AddressID', 1, 1, 1, 'FK_CustomerAddress_Address_AddressID', 'PK_Address_AddressID', 7), ('data-science-test', 'SalesLT', 'Address', 'AddressID', 'data-science-test', 'SalesLT', 'SalesOrderHeader', 'BillToAddressID', 1, 1, 1, 'FK_SalesOrderHeader_Address_BillTo_AddressID', 'PK_Address_AddressID', 7), ('data-science-test', 'SalesLT', 'Address', 'AddressID', 'data-science-test', 'SalesLT', 'SalesOrderHeader', 'ShipToAddressID', 1, 1, 1, 'FK_SalesOrderHeader_Address_ShipTo_AddressID', 'PK_Address_AddressID', 7)]
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








```python
import os

if 'DB_UID' in os.environ:
    userid = os.environ.get('DB_UID')
else:
    raise exception('DB_UID environment variable is not set')

if 'DB_PWD' in os.environ:
    password = os.environ.get('DB_PWD')
else:
    raise exception('DB_PWD environment variable is not set')

if 'DB_SERVER' in os.environ:
    db_server_name = os.environ.get('DB_SERVER')
else:
    raise exception('DB_SERVER environment variable is not set')

if 'DB_NAME' in os.environ:
    db_name = os.environ.get('DB_NAME')
else:
    raise exception('DB_NAME environment variable is not set')
```

Then start notebook


```python
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};" +
    "Server=tcp:" + db_server_name + ",1433;" +
    "Database=" + db_name + ";" +
    "Uid=" + userid + ";" +
    "Pwd=" + password + ";" +
    "Encrypt=yes;" +
    "TrustServerCertificate=no;" +
    "Connection Timeout=30;"
)
```

```python
conn = pyodbc.connect(connection_string)
```

