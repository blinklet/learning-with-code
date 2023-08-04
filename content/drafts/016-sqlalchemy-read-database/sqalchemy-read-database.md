title: SQLAlchemy queries: The minimum you need to know
slug: sqalchemy-read-database
summary: The minimum you need to know about SQLAlchemy to build complex, powerful SQL queries that you can use with the Pandas *read_sql_query()* function, without having to learn SQL.
date: 2023-08-07
modified: 2023-08-07
category: Databases
<!--status: Published-->

In my previous post about [reading database tables into pandas dataframes]({filename}/articles/015-pandas-and-database/Pandas-data-from-database.md), I showed show you how to use simple SQL queries to read data from a database and load it into Pandas dataframes. To integrate Pandas with larger, more complex databases, you need to master the [SQL language](https://en.wikipedia.org/wiki/SQL) or use a Python library like SQLAlchemy to create SQL query statements.

SQLAlchemy can seem like it has a large learning curve but you only need to learn a little bit about it if all you want to do is use it to create SQL queries. This document covers the minimum you need to know about SQLAlchemy to gather information about an existing database's schema and to build complex, powerful SQL queries that you can use with the Pandas *read_sql_query()* function.

## SQLAlchemy

[SQLAlchemy](https://www.sqlalchemy.org/SQLAlchemy) is an [Object Relational Mapper (ORM)](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) tool that translates Python classes to tables in relational databases, and automatically converts function calls to SQL statements. SQLAlchemy provides a standard interface that allows developers to create database-agnostic code that communicates with a wide variety of database engines. [^1]

[^1]: From https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/ on March 23, 2023

### Why use SQLAlchemy to generate query statements?

The SQL language is relatively simple to use for database table queries. So, why would a Python programmer want to use the SQLAlchemy ORM to build the SQL statements used by the Pandas *read_sql_query* function instead of writing actual SQL statements? The main reasons are:

* Automatic SQL statement optimization
* Support for multiple SQL language variations
* Philosophical focus on writing "Pythonic" code and avoiding embedding SQL code in Python programs
* Declarative mapping of database tables to Python classes documents the database schema

When working with large and complex databases, users must ensure their SQL statements are optimized. Un-optimized queries can produce the same data as optimized queries but may use up significantly more resources. The SQLAlchemy ORM will output query statements using industry-standard optimizations.

Different SQL servers support variations of the SQL language. For example, an SQL statement that works on SQLite might not work on Microsoft SQL Server. Programmers can configure the SQLAlchemy ORM to create different SQL statements for different SQL databases without changing the functions that build the queries. The Python programmer may invest her time learning SQLAlchemy instead of [multiple SQL language dialects](https://towardsdatascience.com/how-to-find-your-way-through-the-different-types-of-sql-26e3d3c20aab).

Python programmers may prefer to use SQLAlchemy to create query statements because it allows them to use Python code to express database queries and 

While we do not cover it in this post, programmers may use [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) to manually build SQLAlchemy ORM classes as Python classes. The code you write documents the database and its relationships in Python classes, which help other program maintainers. It also makes a program more robust, because you will be better able to predict the impact that changes in the database schema will have on your program.

### The minimum you need to know about SQLAlchemy

To select data from a database, you only need to know a small sub-set of SQLAlchemy functionality and it easy to learn by working through a few practical examples. This document covers the following topics with step-by-step tutorials:

* How to make SQLAlchemy read the database schema and automatically convert it into mapped Python objects
* Learn the SQLAlchemy functions that create SQL queries
* Integrate the SQLAlchemy queries into Pandas functions to get data from the database

### Prerequisite knowledge

Before you get started using SQLAlchemy, you need to know a little bit about each of the following topics:

* The basics of Python. If you do not already have some basic Python skills, I suggest you read my post, *[Python: the Minimum You Need to Know]({filename}/articles/001-python-minimum-you-need-to-know/python-minimum-you-need-to-know.md)*, or a similar tutorial.
* The basics of relational databases. You need to understand the principles upon which [relational databases](https://www.oracle.com/ca-en/database/what-is-a-relational-database/) like SQL databases are based.
* The basics of working with data in Pandas. I covered this in my previous post, *[Python, pandas, and databases]({filename}/articles/015-pandas-and-database/Pandas-data-from-database.md)*


## Basic setup

The examples in this document were created on a system running Ubuntu Linux 22.04. You may follow the same procedures using Windows or Mac OS, with minor changes.

### Database

You must have access to a database. Either you followed the instructions in my previous post about [setting up a sample database on Azure SQL Server]({filename}/articles/012-create-sample-db-azure/create-sample-db-azure.md) and got the connection string from your Azure database server, or you already have a valid connection string to an existing database. 

In this post, you will use a [*sqlservercentral.com* public SQL Server database](https://www.sqlservercentral.com/articles/sqlservercentral-hosts-adventureworks-on-azure) that serves an instance of the AdventureWorks LT sample database. So, you need to install the Microsoft SQL Server driver on your PC and get the [database and user information](https://www.sqlservercentral.com/articles/connecting-to-adventureworks-on-azure) provided on the *sqlservercentral.com* web site.  

### Install drivers and other software

I have already covered the process for installing the correct drivers on Ubuntu Linux and creating a Python virtual environment in my previous posts, so I will just list the required commands here, without explanation.

```bash
$ sudo su
$ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
$ curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
$ exit
$ sudo apt-get update
$ sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
$
$ mkdir data-science
$ cd data-science
$ python -m venv .venv
$ source ./.venv/bin/activate
(.venv) $ pip install jupyterlab
(.venv) $ pip install python-dotenv
(.venv) $ pip install pyodbc
(.venv) $ sudo apt install unixodbc
(.venv) $ pip install pandas
(.venv) $ pip install openpyxl xlsxwriter xlrd
```

### Install SQLAlchemy

Install [SQLAlchemy](https://www.sqlalchemy.org/):

```bash
(.venv) $ pip install sqlalchemy
```

### Start a notebook

This post uses a [Jupyter notebook](https://jupyter.org/) as an advanced [REPL](https://codewith.mu/en/tutorials/1.0/repl) that makes it easier to demonstrate the Python code used to access data from a database and display the results. Start a new Jupyter Notebook. 

```bash
(.venv) $ jupyter-lab
```

When following along with the code examples in this document, open a new notebook cell for each example, enter the code, and run it. The results of code run in previous cells is held in memory and is available to subsequent cells. For example, a dataframe created in one cell can be used in a later cell.

If you prefer to use a simple text editor or the Python REPL, you can still follow along with this tutorial.

### Database documentation

You need information about the database schema, specifically the relationships between tables. Read the database documentation or analyze the database with an SQL discovery tool like [*SchemaSpy*](https://schemaspy.org/), [*SchemaCrawler*](https://www.schemacrawler.com/), [*SQLite Browser*](https://github.com/sqlitebrowser/sqlitebrowser), or [ Community Edition](https://dbeaver.io/). Another way is to use the [SQLAlchemy *inspection* module](https://docs.sqlalchemy.org/en/20/core/inspection.html#module-sqlalchemy.inspection) to gather information and use it to draw your own diagram. I will describe how to use the *inspection* module in a future post.

>**NOTE:** You can also use the metadata stored in SQLAlchemy ORM classes to derive the database schema information. This is a good exercise because it will help you learn about the information stored in the SQLAlchemy ORM objects. This is a more advanced topic and is not covered in this post.

The database diagram is shown below [^1]:

[^1]: Diagram from *Microsoft Learning Transact-SQL Exercises and Demonstrations* website at [https://microsoftlearning.github.io/dp-080-Transact-SQL/](https://microsoftlearning.github.io/dp-080-Transact-SQL/)

![AdventureWorksLT database diagram]({attach}adventureworks-lt-diagram.png){width=99%}

The diagram shows the database tables, the columns in each table, each table's primary key, and the columns that are foreign keys that create relationships between tables.

## Create a database connection

To connect to the database, first define an environment variables that contain the database authentication information. In this case, use the [database and user information](https://www.sqlservercentral.com/articles/connecting-to-adventureworks-on-azure) provided on the *sqlservercentral.com* web site, which is:

* Server: sqlservercentralpublic.database.windows.net
* Database: AdventureWorks
* User: sqlfamily
* Password: sqlf@m1ly

It's good practice to [store your authentication information separately from the program code]({filename}/articles/011-use-environment-variables/use-environment-variables.md) in a file that is not tracked by source control. In this example, you will create a *dotenv* file name *.env*. 

In your terminal window, run the following command to create the *dotenv* file the contains the correct database authentication information:

```bash
(.venv) $ echo DB_SERVER=sqlservercentralpublic.database.windows.net > .env
(.venv) $ echo DB_NAME=AdventureWorks >> .env
(.venv) $ echo DB_USER=sqlfamily >> .env
(.venv) $ echo DB_PASSWD=sqlf@m1ly >> .env
```

In your Python program, convert the database information into a [database URL](https://dev.to/chrisgreening/connecting-to-a-relational-database-using-sqlalchemy-and-python-1619#deconstructing-the-database-url) that tells SQLAlchemy which database driver to use, the location of the database, and how to authenticate access to it. In this example, the URL will contain an internet address and access credentials.

Enter the following Python code into a Jupyter notebook cell or text editor, and run it. This code imports the [sqlalchemy.engine.URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) class and uses its *create()* method to build a database URL. In addition to the database authentication information you got from the database administrator, you also specify the drive names you will use and the TCP port. Also, because you are using Microsoft SQL Server, you need to add an additional [query parameter](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.query) the contains the name of the SQL Server driver installed on your PC. 

```python
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv('.env2', override=True)

url_object = URL.create(
    drivername='mssql+pyodbc',
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWD'),
    host=os.getenv('DB_SERVER'),
    port='1433',
    database=os.getenv('DB_NAME'),
    query=dict(driver='ODBC Driver 18 for SQL Server')
)
```

Next, import the *create_engine()* function from SQLAlchemy and use it to create an [engine](https://docs.sqlalchemy.org/en/20/core/engines_connections.html) object which includes a connection to the database specified in the URL passed to the *create_engine* function.

```python
from sqlalchemy import create_engine

engine = create_engine(url)
```

You are now ready to get information from the database engine, which represents the connection to the database. You will pass the *engine* object to the Pandas *read_sql_query()* function when you want to select data from the database and load it into Pandas.

## Build an SQLAlchemy model

The SQLAlchemy ORM defines database tables as classes. The process of automatically building new classes based on an existing database's schema is called [reflection](https://betterprogramming.pub/reflecting-postgresql-databases-using-python-and-sqlalchemy-48b50870d40f). If you start with a properly designed database, you can automatically map classes and relationships with the [SQLAlchemy Automap extension](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html). Database reflection is useful when writing simple, single-use scripts like the ones in this document.

> **NOTE:** Instead of using reflection, The SQLAlchemy documentation recommends you use [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) to manually build SQLAlchemy ORM classes as Python classes. We ignore that recommendation in this post because it goes beyond the minimum you need to know.
>
> If you do not know the schema of an existing database, and if you want to use declarative mapping, you may use the *[sqlacodegen](https://github.com/agronholm/sqlacodegen)* tool to read the structure of an existing database and generate Python code describing SQLAlchemy declarative mapping classes. 
>
> We leave Declarative Mapping to your future studies. 

### Automap the ORM

To automatically generate an object model from the public AdventureWorks LT database, run the following code. If the database has many tables, this code may take a while to return a result. Note that you already need to know the name of the database schema you will reflect, which is *SalesLT* in this example.

```python
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(autoload_with=engine, schema='SalesLT')
```

You used SQLAlchemy's *automap_base* function to create a [declarative base class instance](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#basic-use) named *Base* and then used its *prepare* method to automatically map, or *reflect*, the database schema metadata as a collection of classes. 

### Assign table classes

The *automap_base* function returns class instances that were mapped to database tables in the *Base.classes* instance and also stores tables in the *Base.metadata* [^1]. You should already know the table names from reading the database diagram, but if you want to list them for your own convenience, run the following code:

[^1]: It's important to know this because [association tables](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) that support [many-to-many relationships](https://medium.com/@BryanFajardo/how-to-use-associative-entities-in-relational-databases-4456a2c71cda) between other tables do not get mapped to classes and are only available as table objects in the ORM. But, there are no association tables in the AdventureWorks LT database so we won't explore this complication at this time.

```python
print(Base.classes.keys())
```

Which outputs a list containing all the table names, as shown below:

```python
['Address', 'Customer', 'CustomerAddress', 'Product', 'ProductCategory', 'ProductModel', 'ProductDescription', 'ProductModelProductDescription', 'SalesOrderDetail', 'SalesOrderHeader']
```

So that you can more easily use the reflected tables, assign each SQLAlchemy ORM class to a variable. Run the following code:

```python
Address = Base.classes.Address
Customer = Base.classes.Customer
CustomerAddress = Base.classes.CustomerAddress
Product = Base.classes.Product
ProductCategory = Base.classes.ProductCategory
ProductDescription = Base.classes.ProductDescription
ProductModel = Base.classes.ProductModel
ProductModelProductDescription = Base.classes.ProductModelProductDescription
SalesOrderDetail = Base.classes.SalesOrderDetail
SalesOrderHeader = Base.classes.SalesOrderHeader
```

Now you've created variable names that represent each table mapped in the ORM.

Remember, you got this far because you already had a database diagram or documentation. You need to know the schema names in the database and you should also know the table names, column names, primary keys, and foreign key relationships in the database. If you do not have this information, either from documentaion of by discovering it yourself using the SQLAlchemy *inspection* module or by examining the *Base* object's metadata, then using reflection by itself to read data will be less effective. 


## Generating SQL statements in SQLAlchemy

SQLAlchemy has functions that support interacting with a database. Since we are only interested in reading data from the database, we will cover some examples using the *select()* construct and its methods.


### Reading table data with the *select()* construct

Use the SQLAlchemy [*select()* construct](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) to create SQL SELECT statements and that select rows from tables in the database. The *select()* construct returns an instance of the SQLAlchemy Select class that offers methods that can be chained together to provider all the information the Select object needs to output a query when requested by Pandas, or when executed as part of other functions like Python's *print()* function.

This section covers some common uses of the *select()* construct and its methods. Use the SQLAlchemy guides, [*Using Select Statements*](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) and [*ORM Querying Guide*](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html) as references when you need to look up additional methods to build the SQL queries you need.

The following code builds an SQL query that selects all rows in the AdventureWorks LT database's *Product* table. 

```python
from sqlalchemy import select

statement = (select(ProductDescription))
```

The statement variable name is assigned to the SQLAlchemy Select object returned by the *Select()* function. You can view the SQL statement by printing the *statement* object or by converting it to a string. Either of those operations cause the *statement* object to return a string containing the SQL Query.

```
print(statement)
```

Running the previous code produces the following output:

```sql
SELECT "SalesLT"."ProductDescription"."ProductDescriptionID", "SalesLT"."ProductDescription"."Description", "SalesLT"."ProductDescription".rowguid, "SalesLT"."ProductDescription"."ModifiedDate" 
FROM "SalesLT"."ProductDescription"
```

You can use the *statement* object directly in the *pandas_sql_query()* function to read the rows returned by the SQL query into a Pandas data frame.

```python
import pandas as pd

artists = pd.read_sql_query(sql=statement, con=engine)
```

>**NOTE:** Some other documents show that you can use the database URL in the Pandas *read_sql_query()* function instead of the *engine* object. That would work for SQLite, but you need to define the engine to manage a more complex connection to a server that requires authentication. So, we use the engine object to manage the database connection even in a simple example like this.

Show the Pandas dataframe shape and print the first five rows.

```python
print(descriptions.shape)
print(descriptions.head())
```

The output below shows all 762 rows from the *ProductDescription* database table are in the *descriptions* dataframe.

```
(762, 4)
   ProductDescriptionID                                        Description  \
0                     3                                    Chromoly steel.   
1                     4       Aluminum alloy cups; large diameter spindle.   
2                     5             Aluminum alloy cups and a hollow axle.   
3                     8  Suitable for any type of riding, on or off-roa...   
4                    64  This bike delivers a high-level of performance...   

                                rowguid ModifiedDate  
0  301EED3A-1A82-4855-99CB-2AFE8290D641   2007-06-01  
1  DFEBA528-DA11-4650-9D86-CAFDA7294EB0   2007-06-01  
2  F7178DA7-1A7E-4997-8470-06737181305E   2007-06-01  
3  8E6746E5-AD97-46E2-BD24-FCEA075C3B52   2007-06-01  
4  7B1C4E90-85E2-4792-B47B-E0C424E2EC94   2007-06-01  
```

### Selecting columns

You can select specific columns from a table by specifying each column as a parameter in the *select()* construct. For example, to select only the *ProductDescriptionID* and *Description* columns in the *ProductDescription* table, run the following code:

```python
statement = (select(ProductDescription.ProductDescriptionID, 
                    ProductDescription.Description))
descriptions = (pd.read_sql_query(sql=statement, con=engine))
print(descriptions.shape)
print(descriptions.head())
```

You can see that only the columns you selected were loaded into the dataframe, which is still 762 rows but now only 2 columns:

```bash
(762, 2)
   ProductDescriptionID                                        Description
0                     3                                    Chromoly steel.
1                     4       Aluminum alloy cups; large diameter spindle.
2                     5             Aluminum alloy cups and a hollow axle.
3                     8  Suitable for any type of riding, on or off-roa...
4                    64  This bike delivers a high-level of performance...
```

### Limiting output with the *limit()* method

In cases where you want to limit output to a specific number of rows, use the *limit()* method. For example, to load only the first three rows into the dataframe, run the following code:

```python
statement = (select(ProductDescription.ProductDescriptionID, 
                    ProductDescription.Description)).limit(3)

descriptions = (pd.read_sql_query(sql=statement, con=engine))
print(descriptions.shape)
print(descriptions)
```

The output shows only three rows in the dataframe:

```bash
(3, 2)
   ProductDescriptionID                                   Description
0                     3                               Chromoly steel.
1                     4  Aluminum alloy cups; large diameter spindle.
2                     5        Aluminum alloy cups and a hollow axle.
```

### Filtering with the *where()* method

If you want to get only data about the descriptions of "Chromoly steel", add the *where()* method to the instance returned by the *Select()* construct. 

```python
statement2 = (select(ProductDescription.ProductDescriptionID, 
                    ProductDescription.Description))
             .where(ProductDescription.Description=='Chromoly steel.'))
print(statement2)
```

The generate SQL statement is:

```sql
SELECT "SalesLT"."ProductDescription"."ProductDescriptionID", "SalesLT"."ProductDescription"."Description" 
FROM "SalesLT"."ProductDescription" 
WHERE "SalesLT"."ProductDescription"."Description" = :Description_1
```

The Select object that returned the above SQL statement knows that the ":Description_1" variable's value is "Chromoly steel.". When you pass the *statement* variable into the Pandas *read_sql_query* function, it creates the correct query for the SQL dialect used by the database.

Use this new *statement2* object with Pandas to read the data you requested into a dataframe:

```python
descriptions2 = pd.read_sql_query(sql=statement, con=engine)

print(descriptions2.shape)
print(descriptions2.head())
```

This returned only one row: the row containing the description "Chromoly steel."

```
(1, 2)
   ProductDescriptionID      Description
0                     3  Chromoly steel.   
```

If you have very large data sets, you can imagine how useful it can be to filter data before it is loaded into a pandas dataframe.

#### Filtering columns containing text

You can also select text within a column using that column's *like()* method. For example, if you want to select all rows where the *Description* column contains the word "Aluminum" anywhere in the string, run the following code:

```python
statement3 = (select(ProductDescription.ProductDescriptionID, 
                    ProductDescription.Description)
             .where(ProductDescription.Description.like("%Aluminum%")))

print(statement3)
```

Which creates the following SQL query:

```sql
SELECT "SalesLT"."ProductDescription"."ProductDescriptionID", "SalesLT"."ProductDescription"."Description" 
FROM "SalesLT"."ProductDescription" 
WHERE "SalesLT"."ProductDescription"."Description" LIKE :Description_1
```

Pass the SQLAlchemy select statement into the Pandas *read_sql_query()* method, as shown below:

```python
descriptions3 = (pd.read_sql_query(sql=statement3, con=engine))

print(descriptions3.shape)
print(descriptions3.head())
```

This will select only twenty-seven of the rows in the *ProductDescriptions* table. Each row loaded into the Pandas dataframe has the word "aluminum" in the *Description* column, as seen below.

```bash
(27, 4)
   ProductDescriptionID                                        Description
0                     4       Aluminum alloy cups; large diameter spindle.   
1                     5             Aluminum alloy cups and a hollow axle.   
2                   457  This bike is ridden by race winners. Developed...   
3                   594  Travel in style and comfort. Designed for maxi...   
4                   634  Composite road fork with an aluminum steerer t...   
```

### Chaining *select()* methods

You can use other methods to perform more complex queries and you can chain the *select()* construct's methods together similar to the way you can chain methods in Pandas.

For example, if you want to sort the returned results by the *ProductDescriptionID* column, and then select a specific range of rows, chain the *order_by()*, *offset()* and *limit()* methods together [^2]. To skip over the first three rows and then load the next two rows into the dataframe, run the following code:

[^2]: The *offset()* method requires the *order_by()* method or an error will occur. See: [https://docs.sqlalchemy.org/en/20/dialects/mssql.html#limit-offset-support](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#limit-offset-support)

```python
statement = (
    select(ProductDescription.ProductDescriptionID, 
           ProductDescription.Description)
    .order_by(ProductDescription.ProductDescriptionID)
    .offset(3)
    .limit(2)
)

descriptions = (pd.read_sql_query(sql=statement, con=engine))
print(descriptions.shape)
print(descriptions)
```

The output shows only two rows in the dataframe:

```bash
(2, 2)
   ProductDescriptionID                                        Description
0                     8  Suitable for any type of riding, on or off-roa...
1                    64  This bike delivers a high-level of performance...
```


































## SQL Functions using the *func()* method

The SQAlchemy *func()* function has many methods that provide standard SQL functions. 

For example, if you wanted to analyze data from a random sample of five artists, and you wanted to filter the data before loading it into a pandas dataframe, you could change the statement to the following:

```python
statement = (
    select(Artist)
    .order_by(func.random())
    .limit(5))

rand_artists = pd.read_sql_query(sql=statement, con=engine)
print(rand_artists.shape)
print(rand_artists)
```

The output shows five rows were read at random from the database and loaded into the *rand_artists* dataframe.

```
(5, 2)
   ArtistId                                               Name
0       225  Herbert Von Karajan, Mirella Freni & Wiener Ph...
1       191                                        Nação Zumbi
2        18                        Chico Science & Nação Zumbi
3       197                                          Aisha Duo
4       232                  Sergei Prokofiev & Yuri Temirkano
```

## Joining tables using *join()* methods

To create a dataframe containing album and track information from the Chinook database, use the *select()* function's *join()* or *join_from()* methods to join the *Album* and *Track* tables.

In a well-designed database like the Chinook database, the relationships between tables are already defined by primary and foreign keys, and association tables. SQLAlchemy objects can use these relationships to automatically join data in different tables together even if the column that form the relationship have different names.

In the Chinook database diagram above, look at the relationships between the tables named *Album*, *Track*, and *Artist*. The *Album* table has a foreign key that points to the *Artist* table and the *Track* table has a foreign key that points to the *Album* table.

Knowing that these relationships exist, we can simply join all the data from multiple tables together using the *select()* function's *join()* method. 

The code below creates an SQL statement that selects all the columns from the *Album*, *Track*, and *Artist* tables by joining the *Track* and *Artist* tables with the Album table.

```python
statement = (select(Album, Track, Artist)
     .join(Track)
     .join(Artist)
    )
print(statement)
```

The SQL query looks like the following :

```
SELECT "Album"."AlbumId", 
       "Album"."Title", 
       "Album"."ArtistId", 
       "Track"."TrackId", 
       "Track"."Name", 
       "Track"."AlbumId" AS "AlbumId_1", 
       "Track"."MediaTypeId", 
       "Track"."GenreId", 
       "Track"."Composer", 
       "Track"."Milliseconds", 
       "Track"."Bytes", 
       "Track"."UnitPrice", 
       "Artist"."ArtistId" AS "ArtistId_1", 
       "Artist"."Name" AS "Name_1" 
FROM "Album" 
JOIN "Track" ON "Album"."AlbumId" = "Track"."AlbumId" 
JOIN "Artist" ON "Artist"."ArtistId" = "Album"."ArtistId"
```

Use the pandas *read_sql_query* method to get data selected by the statement and load it into a dataframe.

```python
df4 = pd.read_sql_query(sql=q.statement, con=engine)
print(df4.shape)
display(df4.head())
```

The resulting dataset will look like the following:

![Joined tables loaded into Pandas dataframe](./Images/pandas008.png)

You can see the columns, and the column names assigned by SQLAlchemy where column names overlapped, in the query result. 

To get only the specific columns you need, create a new statement that will select each column by name, starting with the *Album.Title* column. Then, [rename the columns](https://devsheet.com/code-snippet/column-name-as-alias-name-sqlalchemy/) in the select statement using the *label()* method.

```python
statement = (select(Album.Title.label("Album"),
            Artist.Name.label("Artist"),
            Track.Name.label("Track"),
            Track.Composer, 
            Track.Milliseconds.label("Length"))
     .join(Track)
     .join(Artist)
    )
print(statement)
```

The resulting SQL statement looks like the following:

```
SELECT "Album"."Title" AS "Album", 
       "Artist"."Name" AS "Artist", 
       "Track"."Name" AS "Track", 
       "Track"."Composer", 
       "Track"."Milliseconds" AS "Length(ms)" 
FROM "Album" 
JOIN "Track" ON "Album"."AlbumId" = "Track"."AlbumId" 
JOIN "Artist" ON "Artist"."ArtistId" = "Album"."ArtistId"
```

Use the statement to load the selected data from the database into a pandas dataframe:

```python
dataframe = pd.read_sql_query(sql=statement, con=engine)
print(dataframe.shape)
display(dataframe.head().style.format(thousands=","))
```

The result is shown below:

![Selected columns from joined tables](./Images/pandas010.png)


You see that joining tables and selecting specific columns in an SQLAlchemy query can give you the data you need in one step. Reading that data into a Pandas dataframe makes it easy to analyze the results.

### Using *join_from()* methods

You can create very large datasets by joining many tables together. As you create more complex queries, SQLAlchemy may not be able to automatically choose how tables will join. You can assist SQLAlchemy in determining relationships between tables by using the *join_from* method, which will specify which tables are on the left and right side of a join. 

For example, if you want to know the names of all the tracks purchased by each customer, create the following SQLAlchemy select statement:

```python
statement = (select(Customer.FirstName,
                    Customer.LastName,
                    Customer.Country,
                    Track.Name.label("Track"),
                    Album.Title.label("Album"),
                    Artist.Name.label("Artist"),
                    InvoiceLine.Quantity,
                    InvoiceLine.UnitPrice
                    )
                .join_from(InvoiceLine, Invoice)
                .join_from(Invoice, Customer)
                .join_from(InvoiceLine, Track)
                .join_from(Track, Album)
                .join_from(Album, Artist))
```

Read the data selected by the statement into a pandas dataframe:

```python
dataframe = pd.read_sql_query(sql=statement, con=engine)
print(dataframe.shape)
display(dataframe.head(5).style.format(thousands=","))
```

See that the output looks like that below:

![Selected columns from many tables](./Images/pandas015.png)


You used the *join_from()* method to make the left and right sides of each join clearer to the program. normally it can infer the correct relationships but sometimes you need to be more specific.

As another example, if you want to see all the tracks on all the playlists, which have a many-to-many relationship:

```python
statement = (select(Playlist.Name.label("Playlist"),
                    Track.Name.label("Track"),
                    Album.Title.label("Album"),
                    Artist.Name.label("Artist")
                    )
                .join_from(Playlist, playlisttrack)
                .join_from(playlisttrack, Track)
                .join_from(Track, Album)
                .join_from(Album, Artist))

dataframe = pd.read_sql_query(sql=statement, con=engine)

print(dataframe.shape)
display(dataframe.head(5))
```

The result was a dataframe with 4 columns and 8,715 rows.

![Joining tables with many-to-many relationship](./Images/pandas016.png){width=12cm}

### Outer joins using the *select()* function

Sometimes you need to perform an *outer join* to get all the data you want.

In SQLAlchemy, a normal (inner) join of the Employee and Customer tables would look like:

```python
statement = select(
    Employee.EmployeeId, 
    Employee.FirstName.label("Emp_First_Name"),
    Employee.LastName.label("Emp_Last_Name"), 
    Employee.Title,
    Customer.FirstName.label("Cust_First_Name"),
    Customer.LastName.label("Cust_Last_Name"),
    Customer.Company.label("Cust_Company"),   
).join(Customer)

dataframe = pd.read_sql_query(sql=statement, con=engine)
print(dataframe.shape)
display(dataframe.style.hide(axis="index"))
```

Which gives you 59 rows showing the employee names and the customers each employee supports. 

![Inner join of Employee and Customer table](./Images/sqlalchemy010.png)

We know we have eight employees but only three employee names appear in the output. You can assume that the missing five employees do not support customers but if you want to see them in the report, anyway, you need to perform an outer join.

An outer join simply uses the *select()* function's *outerjoin()* method:

```python
statement = select(
    Employee.EmployeeId, 
    Employee.FirstName.label("Emp_First_Name"),
    Employee.LastName.label("Emp_Last_Name"), 
    Employee.Title,
    Customer.FirstName.label("Cust_First_Name"),
    Customer.LastName.label("Cust_Last_Name"),
    Customer.Company.label("Cust_Company"),   
).outerjoin(Customer)

dataframe = pd.read_sql_query(sql=statement, con=engine)
print(dataframe.shape)
display(dataframe.style.hide(axis="index"))
```

Which gives you 64 rows because it now includes the five employees who do not support customers. You can see that the customer information contains null values in the rows where the employee's *EmployeeId* column does not match any customers' *SupportRepId* column.

![Outer join of Employee and Customer table](./Images/sqlalchemy011.png)

## Grouping results using the *group_by()* method

You can use SQL queries to group results before reading them into a Pandas dataframe. For example, group employees based on how many customers each supports, similar to an example we described in the "Reading database tables into pandas dataframes" document. Run the following code:

```
statement = (
    select(
        Employee.EmployeeId, 
        (Employee.FirstName + ' ' + Employee.LastName).label("Employee Name"), 
        Employee.Title,
        func.count(Customer.CustomerId).label("Num_Customers")
    )
    .outerjoin(Customer)
    .group_by(Employee.EmployeeId)
)

dataframe = pd.read_sql_query(sql=statement, con=engine)
print(dataframe.to_string(index=False))
```

You also performed an outer join so you get all employees grouped in the dataframe, even the ones who do not support customers.

```
 EmployeeId    Employee Name               Title  Num_Customers
          1     Andrew Adams     General Manager              0
          2    Nancy Edwards       Sales Manager              0
          3     Jane Peacock Sales Support Agent             21
          4    Margaret Park Sales Support Agent             20
          5    Steve Johnson Sales Support Agent             18
          6 Michael Mitchell          IT Manager              0
          7      Robert King            IT Staff              0
          8   Laura Callahan            IT Staff              0
```

Unlike when merging Pandas dataframes where one contained information from the Employee table and the other contained information from the Customer table, we did not need to specify which columns to join on. SQLAlchemy knows the relationships between the Employee and Customer tables, even if the matching columns have different names, because it is defined in the database schema and is now reflected in the SQLAlchemy ORM.

# Conclusion

This document showed you the simple ways you can use SQLAlchemy to build SQL queries using Python code, and use those queries to load database information into a Pandas dataframe. You only need to know a little bit about SQLAlchemy to get started. Eventually, you should learn to use SQLAlchemy functions to Declaratively Map your database schema and use database reflection only when doing single-use scripts where performance is not an issue.