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









# Set up your Python environment

Before you start working through this tutorial, install Python on your laptop. Then, start a Python virtual environment and install the required Python packages in it.

## Install Python on your Windows laptop

Start by installing Python on your laptop, if it is not already installed. Go to the [Python web page](https://www.python.org/) for the most up-to-date information about installing python on your operating system.

On a Windows laptop, it is easiest to install Python from the Windows Store. Choose the latest version. When this document was written, the current version of Python was 3.11.

>**NOTE:** At the time this document was written, Python 3.11 code could crash when run in Jupyter notebooks because it enables frozen modules, which seem to cause problems with the current version of Jupyter notebook. Work around this problem by installing Python 3.10 or by  turning off frozen modules when you create your Python virtual environment using the *-Xfrozen_modules=off* option.



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



## Next steps

Now, you are ready to start working through the tutorials in this document. You may start with using raw T-SQL statements with the Python ODBC driver or you may skip ahead to the SQLAlchemy topic.



### Alternative to connection strings (on Windows)

Another way to create a connection string is to [create a Data Source  (DSN)](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows) using the *ODBC Data Sources* app. This is a Windows-only feature and it lets you avoid entering database information in your code. 

It's probably better to enter the information as a connection string in your code or to use [environment variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.3) if you do not want to hard-code database and use information in your code. 

Just to be complete, we record the procedure for creating and using a DSN in *Appendix A: Data Source Names*.



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











