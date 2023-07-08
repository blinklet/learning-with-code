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

This post covers the tasks a junior data scientist might need to do when reading data from databases. Most of the time, you will only need to read data. In fact, if you work with data provided by other teams, they almost always will restrict your database access privileges to read-only [^2].

[^2]: You will likely receive access to a *database view* prepared by the other team's database administrator. The view will be read-only and will contain only the columns you requested when you met with the team to disuss your data needs.

The database code demonstrated below covers only the simpler case of reading data.  If you write to a database, you need to ensure your program gracefully handles errors that may occur, so you avoid corrupting your database. Writing or changing data is a more complex topic and I do not cover it in this post.

## Set up your Python environment

Before you start working through this tutorial, you need to set up your Python virtual environment and install the necessary packages on your computer. The details of these steps are covered in my previous posts about [using dotenv files]({filename}/articles/011-use-environment-variables/use-environment-variables.md), [creating a sample database]({filename}/articles/012-create-sample-db-azure/create-sample-db-azure.md) and [reading database schema]({filename}/articles/013-read-database-python-odbc/read-db-python-odbc-driver.md). I summarize the steps, below.  

These examples were created on a laptop computer running Ubuntu 22.04. I assume Python is already installed on your system. If not, follow the instructions at [www.python.org](https://www.python.org/).

Create a new Python virtual environment. In my case, I created the virtual environment in the new folder I created for this project.

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

This tutorial uses the [Microsoft AdventureWorks LT sample database](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure) running on Microsoft Azure. Follow my previous post about [creating a sample database on MZ Azure's free service tier]({filename}/articles/014-read-data-from-database-with-python/python-program-read-database-data.md) to create a similar sample database you can use to follow along with the steps in this post.

Then, install the [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver16) on your PC: 

```bash
(.venv) $ sudo su
(.venv) $ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
(.venv) $ curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
(.venv) $ exit
(.venv) $ sudo apt-get update
(.venv) $ sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

Install the [*pyodbc*](https://mkleehammer.github.io/pyodbc/) library in your Python virtual environment.

```bash
(.venv) $ pip install pyodbc
(.venv) $ sudo apt install unixodbc
```

Install the *[python-dotenv](https://pypi.org/project/python-dotenv/)* package:

```bash
(.venv) $ pip install python-dotenv
```

Install the *[tabulate](https://github.com/gregbanks/python-tabulate)* package so you may more easily format your output during this tutorial.

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
import os
import pyodbc
from dotenv import load_dotenv
from tabulate import tabulate

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

From reading the database documentation, or from exploring the database schema, you should already know the tables in the database and the columns in each table, and the data relationships defined by the primary and foreign key constraints. There is no official documentation for the AdventureWorks LT database, but the AdventureWorks LT database diagram is shown below [^1]:

[^1]: Diagram from *Microsoft Learning Transact-SQL Exercises and Demonstrations* website at [https://microsoftlearning.github.io/dp-080-Transact-SQL/](https://microsoftlearning.github.io/dp-080-Transact-SQL/)

![AdventureWorksLT database diagram]({attach}adventureworks-lt-diagram.png){width=99%}

## Using cursor methods

In this post, I show you how to use the *cursor* instance's *execute()* method to load SQL statements into the cursor so that they can be executed by the *fetchall()*, *fetchmany()*, *fetchone()*, or *fetchval()* method.

Other *cursor* instance methods, such as the methods used to discover the schema of a database, are not covered in this post. Those methods were already covered in the appendix of my previous blog post about [exploring SQL database schemas]({filename}/articles/014-read-data-from-database-with-python/python-program-read-database-data.md).

Also, since we are focusing on read-only actions, the methods related to writing data are not covered in this post. 

### SQL statements

To read data from an SQL database, you need to execute an SQL *SELECT* statement on the database server. The *pyodbc* driver requires that you create a string that contains the SQL statement and pass it as a parameter of the *execute()* method. You need to learn enough about the flavour of SQL supported by your server to select that data you need from one or more database tables.

Consult your database server's documentation for information about how to select data using SQL statements. Microsoft's SQL Server's version of SQL is called [Transact-SQL, or T-SQL](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql). I cover a few T-SQL examples below so I can demonstrate how to use the *cursor* instance's methods. You can create very powerful operations using SQL and you will learn more about it as your data extraction and transformation needs become more advanced. 

I cover some basic SQL examples later, in the *Examples* section. So I can demonstrate how the *cursor* instance's methods work I create an SQL statement below. I create a string that contains an SQL statement that reads all the rows from one of the views in the *AdventureWorks LT* database. I assign the string to a Python variable so I can use it later in the *execute()* method.


```python
statement = """
SELECT *
FROM SalesLT.vGetAllCategories
"""
```

The *vGetAllCategories* view will display the list of product categories in the database with their parent categories and sorts the results by parent catergory. If you want to see the SQL statement that created the view, read my previous post about [reading the database schema]({filename}/articles/013-read-database-python-odbc/read-db-python-odbc-driver.md).


### execute()

https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters

SQL statements

 

### Creating cursor with a contect manager

https://github.com/mkleehammer/pyodbc/wiki/Cursor#context-manager

test if cusrsor is still open after contect block

```python
with ...
    cursor.fetchone()
    ....

cursor.fetchone()
```

### fetchall()

https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchall

### fetchmany()

https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchmanysizecursorarraysize

### fetchone()

(example: find one random row)

https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchone

### fetchval()

https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchval

### description()

To get headers

https://github.com/mkleehammer/pyodbc/wiki/Cursor#description




## Examples

### Get all data in a table

```python
statement = """
SELECT *
FROM SalesLT.Product
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchall()
    print(tabulate(rows, headers=headers))
```

This outputs all the columns and rows in the table named *Product* in the schema named *SalesLT*. It outputs almost a hundred rows because you used the *fetchall()* method, which outputs all results available in the *cursor* instance. 

> **NOTE:** In Jupyter Notebook, the output may exceed the "IOPub data rate" and results in an error. If that happens, stop Jupyterlab and then restart it with an additional setting that sets the IOPub data rate to a higher level, as shown below:
>
>```
>(.venv) $ jupyter-lab --ServerApp.iopub_data_rate_limit 1000000000
>```

The data output is very large because there are so many columns and one of the columns contains an image file.

### Select columns

In the results returned in the example above, you see columns we don't need. For example, the *ThumbMailPhoto* column contains binary data. The *rowguid* or *ModifiedDate* columns are relevant to the database but not useful for data analysis. 

Change the T-SQL query statement to select only the columns you are interested in to see less cluttered results. Specify the columns you want to select. In the example below, you will select a subset of the available columns. You can rename columns in the results using the *AS* statement. See the example below:

```python
statement = """
SELECT
    ProductID,
    Name,
    ProductNumber AS ProdNum,
    ProductCategoryID AS CatID,
    ProductModelID AS ModID
FROM SalesLT.Product
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchall()
    print(tabulate(rows, headers=headers))
```

The output looks better but it still displays almost a hundred rows:

```
  ProductID  Name                              ProdNum       CatID    ModID
-----------  --------------------------------  ----------  -------  -------
        680  HL Road Frame - Black, 58         FR-R92B-58       18        6
        706  HL Road Frame - Red, 58           FR-R92R-58       18        6
        707  Sport-100 Helmet, Red             HL-U509-R        35       33
        708  Sport-100 Helmet, Black           HL-U509          35       33
        709  Mountain Bike Socks, M            SO-B909-M        27       18
        710  Mountain Bike Socks, L            SO-B909-L        27       18
        711  Sport-100 Helmet, Blue            HL-U509-B        35       33
        712  AWC Logo Cap                      CA-1098          23        2
        713  Long-Sleeve Logo Jersey, S        LJ-0192-S        25       11
        714  Long-Sleeve Logo Jersey, M        LJ-0192-M        25       11
...(many more rows)...        
```

### Limit the number of rows

You can limit the number of rows output by your program two different ways: you can use the *LIMIT* T-SQL statement to limit the number of rows that will be available in the *cursor*, or you can use the cursor's *fetchmany()* method, which will return a specified number of rows from the results available in the cursor.

#### The *TOP* statement

If you use the *TOP* statement and set the limit to four rows (most other SQL databases use the *LIMIT* statement), the cursor will return the first four rows of data in the table. 

```python
statement = """
SELECT TOP 4
    ProductID,
    Name,
    ProductNumber AS ProdNum,
    ProductCategoryID AS CatID,
    ProductModelID AS ModID
FROM SalesLT.Product
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchall()
    print(tabulate(rows, headers=headers))
```

In the output, you see that the *cursor* instance only contains the first four rows. You used the *fetchall()* method, which returns all rows selected by the T-SQL statement so you know there were only four rows found by the T-SQL query statement.

```
  ProductID  Name                       ProdNum       CatID    ModID
-----------  -------------------------  ----------  -------  -------
        680  HL Road Frame - Black, 58  FR-R92B-58       18        6
        706  HL Road Frame - Red, 58    FR-R92R-58       18        6
        707  Sport-100 Helmet, Red      HL-U509-R        35       33
        708  Sport-100 Helmet, Black    HL-U509          35       33
```

#### The *fetchmany()* method

If you do not limit the rows selected by the query statement and, instead, use the cursor's *fetchmany()* method and set its size to `4`, all rows in the database are made available in the *cursor* instance but you are choosing to read only the first four. 

```python
statement = """
SELECT
    ProductID,
    Name,
    ProductNumber AS ProdNum,
    ProductCategoryID AS CatID,
    ProductModelID AS ModID
FROM SalesLT.Product
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchmany(4)
    print(tabulate(rows, headers=headers))
```

The output looks the same as the case where we used the *TOP* statement but there is a key difference. If you run the *fetchmany()* instance again before you close the cursor, you will read the next four rows from the *cursor* instance. Essentially, you did not limit the total number of results available to you, but you process the results in batches. For example the code below runs the *fetchmany()* method twice on teh same *cursor* instance:

```python
with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchmany(4)
    print(tabulate(rows, headers=headers))
    print()
    rows_next = cursor.fetchmany(4)
    print(tabulate(rows_next, headers=headers))
```

The output shows two separate tables. the first table shows the first four rows in the table. The second table shows the next four rows.

```
  ProductID  Name                       ProdNum       CatID    ModID
-----------  -------------------------  ----------  -------  -------
        680  HL Road Frame - Black, 58  FR-R92B-58       18        6
        706  HL Road Frame - Red, 58    FR-R92R-58       18        6
        707  Sport-100 Helmet, Red      HL-U509-R        35       33
        708  Sport-100 Helmet, Black    HL-U509          35       33

  ProductID  Name                    ProdNum      CatID    ModID
-----------  ----------------------  ---------  -------  -------
        709  Mountain Bike Socks, M  SO-B909-M       27       18
        710  Mountain Bike Socks, L  SO-B909-L       27       18
        711  Sport-100 Helmet, Blue  HL-U509-B       35       33
        712  AWC Logo Cap            CA-1098         23        2
```

Note that each time you create a new *cursor* instance, it starts at the top of the table so if you want to read data from the table in chunks you need to keep the *cursor* instance open. In the example above, you would keep your code indented under the *with* statement block as long as you wanted to work with the same *cursor* instance.



## Combine data from other tables with *join* statements

Select only the rows you need

https://learnsql.com/blog/how-to-join-tables-sql/

https://learn.microsoft.com/en-us/sql/relational-databases/performance/joins

https://learnsql.com/blog/sql-joins-types-explained/

```python
statement = """
SELECT
    ProductID,
    Product.Name,
    ProductNumber AS ProdNum,
    ProductCategory.Name AS Category,
    ProductModel.Name AS Model
FROM SalesLT.Product
JOIN SalesLT.ProductCategory
    ON Product.ProductCategoryID=ProductCategory.ProductCategoryID
JOIN SalesLT.ProductModel
    ON Product.ProductModelID=ProductModel.ProductModelID
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchmany(4)
    print(tabulate(rows, headers=headers))
```

```
ProductID  Name                       ProdNum     Category     Model
---------  -------------------------  ----------  -----------  -------------
      680  HL Road Frame - Black, 58  FR-R92B-58  Road Frames  HL Road Frame
      706  HL Road Frame - Red, 58    FR-R92R-58  Road Frames  HL Road Frame
      707  Sport-100 Helmet, Red      HL-U509-R   Helmets      Sport-100
      708  Sport-100 Helmet, Black    HL-U509     Helmets      Sport-100
```

## Filtering database results

Filter database results using the *WHERE* statement

```python
statement = """
SELECT
    ProductID,
    Product.Name,
    ProductNumber AS ProdNum,
    ProductCategory.Name AS Category,
    ProductModel.Name AS Model
FROM SalesLT.Product
JOIN SalesLT.ProductCategory
    ON Product.ProductCategoryID=ProductCategory.ProductCategoryID
JOIN SalesLT.ProductModel
    ON Product.ProductModelID=ProductModel.ProductModelID
WHERE ProductCategory.Name = 'Tires and Tubes'
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchall()
    print(tabulate(rows, headers=headers))
```

```
  ProductID  Name                 ProdNum    Category         Model
-----------  -------------------  ---------  ---------------  ------------------
        873  Patch Kit/8 Patches  PK-7098    Tires and Tubes  Patch kit
        921  Mountain Tire Tube   TT-M928    Tires and Tubes  Mountain Tire Tube
        922  Road Tire Tube       TT-R982    Tires and Tubes  Road Tire Tube
        923  Touring Tire Tube    TT-T092    Tires and Tubes  Touring Tire Tube
        928  LL Mountain Tire     TI-M267    Tires and Tubes  LL Mountain Tire
        929  ML Mountain Tire     TI-M602    Tires and Tubes  ML Mountain Tire
        930  HL Mountain Tire     TI-M823    Tires and Tubes  HL Mountain Tire
        931  LL Road Tire         TI-R092    Tires and Tubes  LL Road Tire
        932  ML Road Tire         TI-R628    Tires and Tubes  ML Road Tire
        933  HL Road Tire         TI-R982    Tires and Tubes  HL Road Tire
        934  Touring Tire         TI-T723    Tires and Tubes  Touring Tire
```

```python
statement = """
SELECT
    ProductID,
    Product.Name,
    ProductNumber AS ProdNum,
    ProductCategory.Name AS Category,
    ProductModel.Name AS Model
FROM SalesLT.Product
JOIN SalesLT.ProductCategory
    ON Product.ProductCategoryID=ProductCategory.ProductCategoryID
JOIN SalesLT.ProductModel
    ON Product.ProductModelID=ProductModel.ProductModelID
WHERE ProductCategory.Name = 'Tires and Tubes'
    OR ProductCategory.Name = 'Forks'
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchall()
    print(tabulate(rows, headers=headers))
```

```
  ProductID  Name                 ProdNum    Category         Model
-----------  -------------------  ---------  ---------------  ------------------
        802  LL Fork              FK-1639    Forks            LL Fork
        803  ML Fork              FK-5136    Forks            ML Fork
        804  HL Fork              FK-9939    Forks            HL Fork
        873  Patch Kit/8 Patches  PK-7098    Tires and Tubes  Patch kit
        921  Mountain Tire Tube   TT-M928    Tires and Tubes  Mountain Tire Tube
        922  Road Tire Tube       TT-R982    Tires and Tubes  Road Tire Tube
        923  Touring Tire Tube    TT-T092    Tires and Tubes  Touring Tire Tube
        928  LL Mountain Tire     TI-M267    Tires and Tubes  LL Mountain Tire
        929  ML Mountain Tire     TI-M602    Tires and Tubes  ML Mountain Tire
        930  HL Mountain Tire     TI-M823    Tires and Tubes  HL Mountain Tire
        931  LL Road Tire         TI-R092    Tires and Tubes  LL Road Tire
        932  ML Road Tire         TI-R628    Tires and Tubes  ML Road Tire
        933  HL Road Tire         TI-R982    Tires and Tubes  HL Road Tire
        934  Touring Tire         TI-T723    Tires and Tubes  Touring Tire
```



## SQL functions

The SQL *func()* function has many methods that allow you to run [SQL functions](https://learn.microsoft.com/en-us/sql/t-sql/functions/functions?view=sql-server-ver16) on the SQL server. [^4] To select data from a random sample of five items, run the SQL Server's [*NEWID()* T-SQL function](https://learn.microsoft.com/en-us/sql/t-sql/functions/newid-transact-sql?view=sql-server-ver16#d-query-random-data-with-the-newid-function). Create a statement like the following:

[^4]: Each version of SQL support different functions. For example, to analyze data from a random sample of items, you use the *NEWID()* T-SQL function. But, other SQL database engines provide functions like *RANDOM()* or *RAND()* to do the same thing.

```python
statement = """
SELECT TOP 5
    ProductID,
    Product.Name,
    ProductNumber AS ProdNum,
    ProductCategory.Name AS Category,
    ProductModel.Name AS Model
FROM SalesLT.Product
JOIN SalesLT.ProductCategory
    ON Product.ProductCategoryID=ProductCategory.ProductCategoryID
JOIN SalesLT.ProductModel
    ON Product.ProductModelID=ProductModel.ProductModelID
ORDER BY NEWID()
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    headers = [h[0] for h in cursor.description]
    rows = cursor.fetchall()
    print(tabulate(rows, headers=headers))
```

```
ProductID  Name                       ProdNum     Category         Model
---------  -------------------------  ----------  ---------------  ------------------
      839  HL Road Frame - Black, 48  FR-R92B-48  Road Frames      HL Road Frame
      858  Half-Finger Gloves, S      GL-H102-S   Gloves           Half-Finger Gloves
      779  Mountain-200 Silver, 38    BK-M68S-38  Mountain Bikes   Mountain-200
      934  Touring Tire               TI-T723     Tires and Tubes  Touring Tire
      845  Mountain Pump              PU-M044     Pumps            Mountain Pump
```

Every time you execute the statement, you get a different set of data. 

In the following example, we call SQL Server's *COUNT()* function to count the number of rows in the table.  

```python
statement = """
SELECT COUNT(*)
FROM SalesLT.Product
"""

with conn.cursor() as cursor:
    cursor.execute(statement)
    result = cursor.fetchval()
    print(f'Rows in Product table:  {result}')
```

```
Rows in Product table:  295
```

## 