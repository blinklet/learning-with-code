% SQLAlchemy and Pandas: The minimum you need to know

In my previous document, "Reading database tables into pandas dataframes", I showed show you how to use simple SQL queries to read data from a database and load it into Pandas dataframes. To integrate Pandas with larger, more complex databases, you need to master the [SQL language](https://en.wikipedia.org/wiki/SQL) or use a Python library like SQLAlchemy to create SQL query statements.

SQLAlchemy can seem like it has a large learning curve but you only need to learn a little bit about it if all you want to do is use it to create SQL queries. Many SQLAlchemy books and blog posts are written for web application developers so they show how to create a new database, how to build Python objects that map to new database tables using [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html), and then how to manage SQLAlchemy sessions that write data to the tables. They cover all these topics before they show you how to use SQLAlchemy to read from a database.

This document covers the minimum you need to know about SQLAlchemy to gather information about an existing database's schema and to build complex, powerful SQL queries that you can use with the Pandas *read_sql_query()* function.

# SQLAlchemy

[SQLAlchemy](https://www.sqlalchemy.org/SQLAlchemy) is an [Object Relational Mapper (ORM)](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) tool that translates Python classes to tables on relational databases and automatically converts function calls to SQL statements. SQLAlchemy provides a standard interface that allows developers to create database-agnostic code that communicates with a wide variety of database engines. [^1]

[^1]: From https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/ on March 23, 2023

## Why use SQLAlchemy to generate query statements?

The SQL language is relatively simple to use for simple database table queries. So, why would a Python progammer want to use SQLAlchemy ORM to build the SQL statements used by the Pandas *read_sql_query* function?

When working with large and complex databases, users must ensure their SQL statements are optimized. Un-optimized queries can produce the same data as optimized queries but may use up significantly more resources. The SQLAlchemy ORM will output query statements using industry standard optimizations.

Different SQL servers support variations on the SQL language so an SQL statement that works on SQLite might not work on Microsoft SQL Server. Programmers can configure the SQLAlchemy ORM to create different SQL statements for different SQL databases. The Python programmer may invest her time learning SQLAlchemy instead of [multiple SQL language dialects](https://towardsdatascience.com/how-to-find-your-way-through-the-different-types-of-sql-26e3d3c20aab).

Finally, Python programmers may prefer to use SQLAlchemy to create query statements because it allows them to use Python code to express database queries and, if they want to explore more advanced uses of SQLAlchemy, the database schema.

## The minimum you need to know about SQLAlchemy

If you analyze data, all you need to know is how to read data from an existing database. This is a small sub-set of SQLAlchemy functionality and it easy to learn by working through a few practical examples. This document covers the following topics with step-by-step tutorials:

* How to install SQLAlchemy
* How to connect SQLAlchemy to an existing database
* How to make SQLAlchemy read the database schema and automatically convert it into mapped Python objects
* Learn the SQLAlchemy functions that create SQL queries
* Integrate the SQLAlchemy queries into Pandas functions to get data from the database

## Prerequisite knowledge

Before you get started using SQLAlchemy, you need to know a little bit about each of the following topics:

* The basics of Python. If you do not already have some basic Python skills, I suggest you read my document, "Python: the Minimum You Need to Know", or a similar tutorial.
* The basics of relational databases. You need to understand the principles upon which [relational databases](https://www.oracle.com/ca-en/database/what-is-a-relational-database/) like SQL databases are based.
* The basics of working with data in Pandas. I covered this in my previous document, "Reading database tables into pandas dataframes"


# Install SQLAlchemy and other packages

Install SQLAlchemy in the same virtual environment in which you already installed Pandas. If you have not already created a Python virtual environment, run the folloing commands to create one in the same folder in which you will save your Jupyter notebook files:

```powershell
> cd data-science-folder
> python -m venv env
> .\env\Scripts\activate
(env) > 
```

Then, install SQLAchemy with the following command.

```powershell
(env) > pip install SQLAlchemy
```

## Database drivers

If you are using a database driver other than [SQLite](https://www.sqlite.org/index.html), which is built into Python, you will have to install it. Other database drivers include [psycopg](https://www.psycopg.org/) for PostgreSQL, or [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) for MySQL.

## Pandas and Jupyter Notebooks

If you did not already install Pandas and Jupyter when you followed the tutorials in the "Reading database tables into pandas dataframes" document, install them now:

```powershell
(env) > pip install pandas
(env) > pip install openpyxl xlsxwriter xlrd
(env) > pip install jupyterlab
```

This document uses a [Jupyter notebook](https://jupyter.org/) as an advanced [REPL](https://codewith.mu/en/tutorials/1.0/repl) that makes it easier to demonstrate the Python code used to access data from a database and display the results. Create a new Jupyter notebook and start it using the commands below:

```powershell
(env) > create-notebook my_notebook
(env) > jupyter notebook my_notebook.ipynb
```

If you prefer to use a simple text editor or another REPL, you can still follow along with this tutorial.


# Database and documentation

You need a database that is usable for practice. Use the [SQLite](https://www.sqlite.org/index.html) version of the *[Chinook database](https://github.com/lerocha/chinook-database)*, which is a public database that tries to emulate a media store's database. It contains customer names and addresses, sales data, and inventory data.

[Download the *Chinook_Sqlite.sqlite* file](https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite) from the Chinook Database project's [downloads folder](https://github.com/lerocha/chinook-database/tree/master/ChinookDatabase/DataSources) and save it to a folder your computer.

You need information about the database schema, specifically the relationships between tables. Read the database documentation or analyze the database with an SQL discovery tool like [*SchemaSpy*](https://schemaspy.org/), [*SchemaCrawler*](https://www.schemacrawler.com/), [*SQLite Browser*](https://github.com/sqlitebrowser/sqlitebrowser), or [ Community Edition](https://dbeaver.io/). Another way is to use the [SQLAlchemy *inspection* module](https://docs.sqlalchemy.org/en/20/core/inspection.html#module-sqlalchemy.inspection) to gather information and use it to draw your own diagram. The *inspection* module is described in *Appendix A*.

>**NOTE:** You can also use the metadata stored in SQLAlchemy ORM classes to derive the database schema information. This is a good exercise because it will help you learn about the information stored in the SQLAlchemy ORM objects. This is a more advanced topic and is not covered here.

The Chinook database diagram, created by SchemaSpy, is shown below:

![Chinook database diagram showing table relationships](./Images/chinook-diagram-03.png){width=14cm}

The diagram shows the database tables, the columns in each table, each table's primary key, and the columns that are foreign keys that create relationships between tables.

# Create a database connection

Create the [database URL](https://dev.to/chrisgreening/connecting-to-a-relational-database-using-sqlalchemy-and-python-1619#deconstructing-the-database-url) that tells SQLAlchemy which database driver to use, the location of the database, and how to authenticate access to it. The URL may be as simple as the string shown below, which simply contains the name of the SQLite driver, *sqlite*, and the path to the SQLite file on my computer disk. Or, it may involve an internet address and access credentials.

Enter the following Python code into a Jupyter notebook cell or text editor and run it:

```
url = r"sqlite:///C:/Users/blinklet/Documents/Chinook_Sqlite.sqlite"
```

Next, import the *create_engine()* function from SQLAlchemy and use it to create an [engine](https://docs.sqlalchemy.org/en/20/core/engines_connections.html) object which includes a connection to the database specified in the URL passed to the *create_engine* function.

```python
from sqlalchemy import create_engine

engine = create_engine(url)
```

You are now ready to get information from the database connection. You will use the *engine* object in your program when you need to specify the connection.

# Build an SQLAlchemy model

The SQLAlchemy ORM defines database tables as classes. The process of automatically building new classes based on an existing database's schema is called [reflection](https://betterprogramming.pub/reflecting-postgresql-databases-using-python-and-sqlalchemy-48b50870d40f). If you start with a properly designed database, you can automatically map classes and relationships with the [SQLAlchemy Automap extension](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html). Database reflection is useful when writing simple, single-use scripts like the ones in this document.

> **NOTE:** Instead of using reflection, The SQLAlchemy documentation recommends you use [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) to manually build SQLAlchemy ORM classes as Python classes. The code you write that describes these classes enables other program maintainers to see the database information expressed in Python code. It also makes a program more robust, because you will be better able to predict the impact that changes in the database schema will have on your program. 
>
> When working with an existing database you may us the *[sqlacodegen](https://github.com/agronholm/sqlacodegen)* tool to read the structure of an existing database and generate Python code describing SQLAlchemy declarative mapping classes. We leave Declarative Mapping for your future consideration. 

## Automap the ORM

To automatically generate an object model from the Chinook database, run the following code:

```python
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()
Base.prepare(autoload_with=engine)
```

You used SQLAlchemy's *automap_base* function to create a [declarative base class instance](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#basic-use) named *Base* and then used its *prepare* method to automatically map, or *reflect*, the database schema metadata. 

## Assign table classes

The *automap_base* function returns class instances that were mapped to database tables in the *Base.classes* instance and also stores tables in the *Base.metadata*. It's important to know this because [association tables](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) that support [many-to-many relationships](https://medium.com/@BryanFajardo/how-to-use-associative-entities-in-relational-databases-4456a2c71cda) between other tables do not get mapped to classes and are only available as table objects in the ORM.

For example, in the Chinook database diagram above, you can [identify](https://condor.depaul.edu/gandrus/240IT/accesspages/relationships.htm) that the *PlaylistTrack* table is an association table because it has only two columns and each of its columns are both Primary Keys and Foreign Keys. 

So that you can more easily use the reflected tables, assign each SQLAlchemy ORM class to a variable so it is easier to work with. Run the following code:

```python
Album = Base.classes.Album
Artist = Base.classes.Artist
Customer = Base.classes.Customer
Employee = Base.classes.Employee
Genre = Base.classes.Genre
Invoice = Base.classes.Invoice
InvoiceLine = Base.classes.InvoiceLine
MediaType = Base.classes.MediaType
Playlist = Base.classes.Playlist
Track = Base.classes.Track
playlisttrack = Base.metadata.tables['PlaylistTrack']
```

Notice that we assigned the *playlisttrack* variable name to the *PlaylistTrack* table in the *Base.metadata.tables* class, instead of to a class instance like the other table objects. Now that you've created variable names that represent each table mapped in the ORM, you don't need to worry about whether a table is an association table, or not.


# Generating SQL statements in SQLAlchemy

SQLAlchemy has functions that support interacting with a database. Since we are only interested in reading data from the, we will cover some examples using the *select()* function and the methods.


## Reading data with the *select()* function

Use the SQLAlchemy [*select()* function](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) to create SQL SELECT statements and that read rows from tables in the database. The *select()* function returns an instance of the SQLAlchemy Select class that offers methods that can be chained together to provider all the information the Select object needs to output a query when requested by Pandas, or when executed as part of other functions like Python's *print()* function.

This section covers some common uses of the *select()* function and its methods. Use the SQLAlchemy guides, [*Using Select Statements*](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) and [*ORM Querying Guide*](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html) as references when you need to look up additional methods to build the SQL queries you need.

The following code builds an SQL query that selects all rows in the Chinook database's *Album* table. 

```python
from sqlalchemy import select

statement = (select(Artist))
```

The statement variable name is assigned to the SQLAlchemy Select object returned by the *Select()* function. You can view the SQL statement by printing the *statement* object or by converting it to a string. Either of those operations cause the *statement* object to return a string containing the SQL Query.

```
print(statement)
```

Running the previous code produces the following output:

```
SELECT "Artist"."ArtistId", "Artist"."Name" 
FROM "Artist"
```

You can use the *statement* object directly in the *pandas_sql_query()* function to read the rows returned by the SQL query into a Pandas data frame.

```
import pandas as pd

artists = pd.read_sql_query(sql=statement, con=engine)
```

>**NOTE:** Some other documents show that you can use the database URL in the Pandas *read_sql_query()* function instead of the *engine* object. That would work for SQLite, but you need to define the engine to manage a more complex connection to a server that requires authentication. So, we use the engine object to manage the database connection even in a simple example like this.

Show the Pandas dataframe shape and print the first five rows.

```
print(artists.shape)
print(artists.head(5))
```

The output below shows all 275 rows from the *Artist* database table are in the *artists* dataframe.

```
(275, 2)
   ArtistId               Name
0         1              AC/DC
1         2             Accept
2         3          Aerosmith
3         4  Alanis Morissette
4         5    Alice In Chains
```

## Filtering with the *where* method

If you want to get only data about the artist named "Alice in Chains", add the *where()* method to the instance returned by the *Select()* function. 

```python
statement = select(Artist).where(Artist.Name=='Alice In Chains')
print(statement)
```

The generate SQL statement is:

```
SELECT "Artist"."ArtistId", "Artist"."Name" 
FROM "Artist" 
WHERE "Artist"."Name" = :Name_1
```

The Select object that returned the above SQL statement knows that the ":Name_1" variable's value is "Alice in Chains". When you pass the *statement* variable into the Pandas *read_sql_query* function, it creates the correct query for the SQL dialect used by the database.

Use this new *statement* object with Pandas to read the data you requested into a dataframe:

```python
dataframe = pd.read_sql_query(sql=statement, con=engine)

print(dataframe.shape)
print(dataframe.head(5))
```

This returned only one row: the row containing the artist named "Alice In Chains"

```
(1, 2)
   ArtistId             Name
0         5  Alice In Chains
```

If you have very large data sets, you can imagine how useful it can be to filter data before it is loaded into a pandas dataframe.

## Chaining *select()* function methods

You can use other methods to perform more complex queries and you can chain instance methods together similar to the way you can chain methods in Pandas.

For example, if you want to sort the names in the Artist table in alphabetical order and then read the first five rows into a Pandas dataframe, use the *order_by()* and *limit()* methods. Run the following code:

```python
statement = (
    select(Artist)
    .order_by(Artist.Name)
    .limit(5)
    )

alpha_artists = pd.read_sql_query(sql=statement, con=engine)
print(alpha_artists.shape)
print(alpha_artists.head(5))
```

You can see below that only five rows were returned and the rows were sorted alphabetically.

```
(5, 2)
   ArtistId                                               Name
0        43                                       A Cor Do Som
1         1                                              AC/DC
2       230          Aaron Copland & London Symphony Orchestra
3       202                                     Aaron Goldberg
4       214  Academy of St. Martin in the Fields & Sir Nevi...
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




# Appendix A: Exploring the database schema using the *inspection* module

One way to learn about the structure of an existing database is to use the [SQLAlchemy *inspect* module](https://docs.sqlalchemy.org/en/20/core/inspection.html#module-sqlalchemy.inspection). It provides a simple interface to read database schema information via a Python API. This appendix provides inspection examples that are relevant to users who read data into Pandas dataframes and who need to understand the [relationships](https://blog.devart.com/types-of-relationships-in-sql-server-database.html#self-referencing-relationships) within a database. Inspecting SQLAlchemy [relationship constraints](https://www.digitalocean.com/community/conceptual-articles/understanding-sql-constraints) may be more complex, but constraints are relevant only to users who want to update or delete information in a database so we will not inspect them in this document. See the [SQLAlchemy Inspect documentation](https://docs.sqlalchemy.org/en/20/core/reflection.html#fine-grained-reflection-with-inspector) for more ways to use the *inspect()* module.

## Create an Inspector object

After establishing a connection to the database and generating an *engine* object, as shown earlier in this document, create an [Inspector object](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) using SQLAlchemy's *inspect()* function. 

```python
from sqlalchemy import inspect

inspector = inspect(engine)
```

You created a new Inspector object, named *inspector*, that contains all the information you need about the database structure. 

## Table names

Use the Inspector object's *get_table_names()* method to list the tables in the database.

```python
print(inspector.get_table_names())
```

You should see the output displayed as a list containing the table names in the Chinook database.

```
['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
```

## Column details

When the Inspector object instance's methods return iterables, you can use Python's "pretty print" module, *pprint*, to display inspection in a manner that is easier to read. To see details about a table's columns and primary key, enter the following code: 


```python
from pprint import pprint

pprint(inspector.get_columns("Album"))
```

When you run the code, you see that the *get_columns()* method returns a list. Each item in the list is a dictionary that contains information about a column in the *Album* table. 

```python
[{'autoincrement': 'auto',
  'default': None,
  'name': 'AlbumId',
  'nullable': False,
  'primary_key': 1,
  'type': INTEGER()},
 {'autoincrement': 'auto',
  'default': None,
  'name': 'Title',
  'nullable': False,
  'primary_key': 0,
  'type': NVARCHAR(length=160)},
 {'autoincrement': 'auto',
  'default': None,
  'name': 'ArtistId',
  'nullable': False,
  'primary_key': 0,
  'type': INTEGER()}]
```

You can see which column is the primary key column by looking at the *primary_key* item in each column dictionary. If the number is larger than zero, the column is a private key. Remember that association tables have two or more primary keys so, if there are two private keys, one private key value will be "1" and the second will be "2".

## Private keys

To see only the private key of a table, use the *get_pk_constraint()* method:

```python
print(inspector.get_pk_constraint("Album"))
```

You see the *get_pk_constraint()* method returns a dictionary containing a list of the table's primary keys.

```python
{'constrained_columns': ['AlbumId'], 'name': None}
```

## Foreign keys

To see which columns in a table are foreign keys, use the *get_foreign_keys()* method:

```python
pprint(inspector.get_foreign_keys("Album"))
```

You can see in the output below that the *Album* table's *ArtistId* column is a foreign key that points to the *ArtistId* column in the *Artist* table:

```python
[{'constrained_columns': ['ArtistId'],
  'name': None,
  'options': {},
  'referred_columns': ['ArtistId'],
  'referred_schema': None,
  'referred_table': 'Artist'}]
```

## Gathering table relationship information

To gather all the information you need about table relationships to build a database diagram, write a Python function named *inspect_relationships()* that read a table's columns and relationships by iterating through the *inspection* object's attributes. Enter the code shown below:

```python
def inspect_relationships(table_name):
    tbl_out = f"Table = {table_name}\n"
    
    col_out = "Columns = "
    cols_list = inspector.get_columns(table_name)
    for i, c in enumerate(cols_list, 1):
        if i < len(cols_list):
            col_out += (c['name'] + ", ")
        else:
            col_out += c['name'] + "\n"
    
    pk_out = "Primary Keys = "
    pk = inspector.get_pk_constraint(table_name)
    pk_list = pk["constrained_columns"]
    for i, c in enumerate(pk_list):
        if i < len(pk_list) - 1:
            pk_out += (c + ", ")
        else:
            pk_out += (c + "\n")  
    
    fk_out = ""
    fk_list = inspector.get_foreign_keys(table_name)
    if fk_list:
        fk_out = "Foreign Keys:\n"
        fk_name_list = []
        fk_reftbl_list = []
        fk_refcol_list = []
        
        for fk in fk_list:
            fk_name_list.append(*fk['constrained_columns'])
            fk_reftbl_list.append(fk['referred_table'])
            fk_refcol_list.append(*fk['referred_columns'])
            
        fk_info = zip(fk_name_list, fk_reftbl_list, fk_refcol_list)
        
        for n, t, c in fk_info:
            fk_out += f"    {n} ---> {t}:{c}\n"
    
    return("".join([tbl_out, col_out, pk_out, fk_out]))
```

Use the *inspect_relationships()* function to print table relationship information by passing it a table name. The function returns the table information as a long string.

You can get information about one table by passing it a table name, as shown below:

```python
print(inspect_relationships("Album"))
```

The function returns the table information as a long string:

```
Table = Album
Columns = Title, ArtistId, AlbumId
Primary Keys = AlbumId
Foreign Keys:
    ArtistId ---> Artist:ArtistId
```

you can see all tables in a database by iterating through the list returned by the *inspector* object's *get_table_names()* method, as shown below. 

```python
for tbl in inspector.get_table_names():
    print(inspect_relationships(tbl))
```

The output is a long list showing information about each table. 

```
Table = Album
Columns = Title, ArtistId, AlbumId
Primary Keys = AlbumId
Foreign Keys:
    ArtistId ---> Artist:ArtistId

Table = Artist
Columns = Name, ArtistId
Primary Keys = ArtistId

Table = Customer
Columns = FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId, CustomerId
Primary Keys = CustomerId
Foreign Keys:
    SupportRepId ---> Employee:EmployeeId

Table = Employee
Columns = LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email, EmployeeId
Primary Keys = EmployeeId
Foreign Keys:
    ReportsTo ---> Employee:EmployeeId

Table = Genre
Columns = Name, GenreId
Primary Keys = GenreId

Table = Invoice
Columns = CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total, InvoiceId
Primary Keys = InvoiceId
Foreign Keys:
    CustomerId ---> Customer:CustomerId

Table = InvoiceLine
Columns = InvoiceId, TrackId, UnitPrice, Quantity, InvoiceLineId
Primary Keys = InvoiceLineId
Foreign Keys:
    TrackId ---> Track:TrackId
    InvoiceId ---> Invoice:InvoiceId

Table = MediaType
Columns = Name, MediaTypeId
Primary Keys = MediaTypeId

Table = Playlist
Columns = Name, PlaylistId
Primary Keys = PlaylistId

Table = PlaylistTrack
Columns = PlaylistId, TrackId
Primary Keys = PlaylistId, TrackId
Foreign Keys:
    TrackId ---> Track:TrackId
    PlaylistId ---> Playlist:PlaylistId

Table = Track
Columns = Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice, TrackId
Primary Keys = TrackId
Foreign Keys:
    MediaTypeId ---> MediaType:MediaTypeId
    GenreId ---> Genre:GenreId
    AlbumId ---> Album:AlbumId
```

You can use the information gathered about each table's relationships to draft a database diagram similar to the diagram shown earlier in this document. 