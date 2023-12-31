title: Working with database views
slug: sqlalchemy-database-views
summary: Data scientists often read data from database views, in addition to database tables. Views offer a different challenge to developers working with SQLAlchemy because database views usually do not have primary key relationships defined.
date: 2023-10-07
modified: 2023-10-07
category: Databases
status: draft

<!--
This all comes from my "big database doc. It is mostly about using database views so use it with AdventureWorks LT on Azure and the view tables there
-->

Database Views are virtual tables that derive data dynamically, unlike static database tables [^1]. 

[^1]: From https://aristeksystems.com/blog/database-views-what-you-need-to-know/

Reasons for views:
- limit access to the data. Provide only what is needed by the user. This is often the way data scientists who work with sensitive data will work. This limits the risk that the data scientist's employer or client may incur if a data scientist mishandled other sensitive data from the database.
- being helpful by presenting results of queries, already prepared. For example, creating a view made up of selected columns from several different tables.


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


## View names

Use the Inspector instance's *get_view_names()* method to list views defined in the database.

```python
print(insp.get_view_names(schema='public'))
```

Since there are no views in the Chinook sample database, this method returns an empty list.

```
[]
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
[]
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
big_view = Base.metadata.tables['sample_schema.Sample View Name']
another_big_view = Base.metadata.tables['another_schema.Another View']
```

Now, you can get table data from the new table variable. For example:

```python
print(big_view.name)
print(another_big_view.name)
```

The above code lists the name of each table. So, we know the variable points to the correct table information in the *Base.metadata* object.

```
Sample View Name
Another View
```

You can access table column information from the table variable you just created. For example, you can get column names:

```python
print(big_view.columns.keys())
```

The *columns.key()* method listed the column names in the *Sample View Name* table. 

```
['Column Zero',  'Column One',  'Column Two',...]
```

It is possible to build select statements by indexing table columns. For example, the following *select()* statement, which we cover in the next chapter, selects five rows from three columns from the *Sample View Name* table:

```python
stmt = select(
    big_view.columns['Column One'], 
    big_view.columns['Column Two'],
    big_view.columns['Column Three']
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