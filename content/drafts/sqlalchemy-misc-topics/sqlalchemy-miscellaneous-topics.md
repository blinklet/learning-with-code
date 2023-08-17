title: unknown3
slug: unknown3
summary: tbd
date: 2023-08-07
modified: 2023-08-07
category: Databases
status: draft

## View the ORM classes

The reason programmers use the SQLAlchemy ORM is so that they can treat database tables like Python classes in their programs and work in the "Pythonic" way. Let's find out some more information about the SQLAlchemy classes that map the tables in the database.

List the SQLAlchemy classes mapped by the automap extension.

```python
print(*Base.classes.keys(), sep=", ")
```

You should see the output displayed below, showing the table names in the Chinook database.

```
Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, Track, MediaType, Playlist
```

If you compare the tables found using the *inspect* function and the *Base.metadata* object to the classes found in the *Base.classes* object, you will see that we have eleven tables but only ten ORM classes. This is because the *PlaylistTrack* table is an association table. SQLAlchemy ORM does not automatically create a class for an association table. It instead represents it as a table with foreign keys pointing to columns in the other tables.

## ORM Metadata

You can view more information about the tables declared in the ORM by parsing through the database class's metadata. You can learn the data types of each column. for example. To see a rough listing of all of the metadata for the *Album* table, run the following code:

```python
print(repr(Base.metadata.tables['Album']))
```

You see the following output:

```
Table('Album', MetaData(), Column('AlbumId', INTEGER(), table=<Album>, primary_key=True, nullable=False), Column('Title', NVARCHAR(length=160), table=<Album>, nullable=False), Column('ArtistId', INTEGER(), ForeignKey('Artist.ArtistId'), table=<Album>, nullable=False), schema=None)
```

If you wanted to see metadata for every table in the database schema, run the following code:

```python
meta = Base.metadata.tables.items()
for i in meta:
    print(i, end="\n\n")
```

You can find out any existing relationships between tables by looking at the columns defined as primary keys and secondary keys. The following code will print out table name, column names, primary keys, and foreign keys of any table in an easy-to-read format:

```python
from sqlalchemy.schema import ForeignKey
from tabulate import tabulate

def table_info(table_name):
    headers = [
        'Column Name',
        'Primary Key',
        'Foreign Key', 
        'Relationship'
    ]

    body = list()
    table = Base.metadata.tables[table_name]
    
    print(f"Table: {table_name}")
    
    for col in table.columns:
        line = dict.fromkeys(headers)
        line['Column Name'] = col.name
        
        if col.primary_key:
            line['Primary Key'] = "YES"
        
        if col.foreign_keys:
            line['Foreign Key'] = "YES"
            z = set(col.expression.foreign_keys)[.pop()]
            if isinstance(z, ForeignKey):
                line['Relationship'] = z.target_fullname
        
        body.append(line)
    
    rows =  [x.values() for x in body]
    return(
        tabulate(
            rows, 
            headers, 
            colalign=('left','center','center','left'), 
            tablefmt='psql'
        )
    )
```

Call the *table_info()* function, as shown below:

```python
print(table_info("PlaylistTrack"))
print("\n")
print(table_info("Track"))
```

You should see the two tables described, with each table's output looking like the below text:

```
Table: PlaylistTrack
+---------------+---------------+---------------+---------------------+
| Column Name   |  Primary Key  |  Foreign Key  | Relationship        |
|---------------+---------------+---------------+---------------------|
| PlaylistId    |      YES      |      YES      | Playlist.PlaylistId |
| TrackId       |      YES      |      YES      | Track.TrackId       |
+---------------+---------------+---------------+---------------------+


Table: Track
+---------------+---------------+---------------+-----------------------+
| Column Name   |  Primary Key  |  Foreign Key  | Relationship          |
|---------------+---------------+---------------+-----------------------|
| TrackId       |      YES      |               |                       |
| Name          |               |               |                       |
| AlbumId       |               |      YES      | Album.AlbumId         |
| MediaTypeId   |               |      YES      | MediaType.MediaTypeId |
| GenreId       |               |      YES      | Genre.GenreId         |
| Composer      |               |               |                       |
| Milliseconds  |               |               |                       |
| Bytes         |               |               |                       |
| UnitPrice     |               |               |                       |
+---------------+---------------+---------------+-----------------------+
```

In the listing above, you can [identify](https://condor.depaul.edu/gandrus/240IT/accesspages/relationships.htm) that the *PlaylistTrack* table is an [association table](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) that supports a [many-to-many relationships](https://medium.com/@BryanFajardo/how-to-use-associative-entities-in-relational-databases-4456a2c71cda) between two other tables. A typical association table has two columns and each of its columns are both Primary Keys and Foreign Keys. 

Association tables are declared differently in the ORM than normal tables in the SQLAlchemy ORM. They are not reflected as ORM classes so there will be no *PlaylistTrack* class in the ORM. The association table is defined only as a table object in the ORM.

After looking at all the information output, you should be able to draw a diagram showing the database tables and relationships, like the one below:

![Chinook database diagram showing relationships](./Images/chinook-diagram-03.png)

## Assign table classes

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







# SQLAlchemy query basics

Up until this point, we have been using Pandas to query the SQL database, using an SQLAlchemy ORM select statement that tells Pandas which data to pull from the database. This works well when you want to gather large data sets into Pandas for organization and analysis.

There may be times when you want to read data from an SQL database and receive the result directly, without loading it into a Pandas dataframe. You do this using the [SQLAlchemy's *Session* object]((https://docs.sqlalchemy.org/en/20/orm/session_basics.html)). 

Create a new database session named *session* by calling the *Session* class and passing it the *engine* object you created at the start of this document, using SQLAlchemy's *create_engine* method. 

For example, using the SQLAlchemy *select* below as the parameter to the *session.execute* method, get a Result object from the database:

```python
statement = (select(Album.Title.label("Album"),
            Artist.Name.label("Artist"),
            Track.Name.label("Track"),
            Track.Composer, 
            Track.Milliseconds.label("Length"))
     .join(Track)
     .join(Artist)
    )

with Session(engine) as session:
    print(type(session.execute(statement)))
    print(session.execute(statement))
```

You can see that the session.execute method returns a *Result* object, which is a proxy for the data queried from the database.

```
<class 'sqlalchemy.engine.result.ChunkedIteratorResult'>
<sqlalchemy.engine.result.ChunkedIteratorResult object at 0x00000173831B5550>
```

The Result object is connected to the database session and gives you access to all the rows returned by the execution of the *select* statement. It does not actually contain data but it sends you data from the database every time you iterate on it. You need to iterate through the result to get rows from the database.

To get rows from the database, use an iterator like a *for* loop or the *next* function. Each iteration returns a *Row* object

```python
with Session(engine) as session:
    result = session.execute(statement)

    print(next(result))
    print(next(result))
    print(type(result))
```
```
('For Those About To Rock We Salute You', 'AC/DC', 'For Those About To Rock (We Salute You)', 'Angus Young, Malcolm Young, Brian Johnson', 343719)
('Balls to the Wall', 'Accept', 'Balls to the Wall', None, 342562)
<class 'sqlalchemy.engine.result.ChunkedIteratorResult'>
```

Here is an example of iterating through the result using a *for* loop. In this case, I added some code to limit the output to four rows.

```python
with Session(engine) as session:
    limit = 4
    result = session.execute(statement)
    for index, item in enumerate(result, start=1):
        print(item)
        if index == limit:
            break
```
```
('For Those About To Rock We Salute You', 'AC/DC', 'For Those About To Rock (We Salute You)', 'Angus Young, Malcolm Young, Brian Johnson', 343719)
('Balls to the Wall', 'Accept', 'Balls to the Wall', None, 342562)
('Restless and Wild', 'Accept', 'Fast As a Shark', 'F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman', 230619)
('Restless and Wild', 'Accept', 'Restless and Wild', 'F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman', 252051)
```

When you print a *Row* object, it displays a tuple containing values from each column in that row. But, it is still a Row object so you can get data from any column in the row by addressing it by column name, as follows:

```python
with Session(engine) as session:
    result = session.execute(statement)

    x = next(result).Artist
    print(x)
    print(type(x))
```
```
AC/DC
<class 'str'>
```

You can get the column headers from the database and use them to identify table columns in your program. The *keys()* method returns a list of headers, as shown below:

```python
with Session(engine) as session:
    result = session.execute(statement)
    headers = result.keys()
    print(headers)
```
```
RMKeyView(['Playlist', 'Track', 'Album', 'Artist'])
```

Another way to get a number of rows from a table is to use the Result object's *fetchmany()* method, as shown below:

```python
with Session(engine) as session:
    result = session.execute(statement)
    headers = result.keys()
    table = result.fetchmany(4)

print(tuple(headers))
for row in table:
    print(row)
```
```
('Album', 'Artist', 'Track', 'Composer', 'Length')
('For Those About To Rock We Salute You', 'AC/DC', 'For Those About To Rock (We Salute You)', 'Angus Young, Malcolm Young, Brian Johnson', 343719)
('Balls to the Wall', 'Accept', 'Balls to the Wall', None, 342562)
('Restless and Wild', 'Accept', 'Fast As a Shark', 'F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman', 230619)
('Restless and Wild', 'Accept', 'Restless and Wild', 'F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman', 252051)
```

To explore what types are returned by the *session.execute.keys()*, *session.execute.fetchmany()* methods, run the following code:

```python
print(type(headers))
print(type(table))
for row in table:
    print(type(row))
```

We see the following output:

```
<class 'sqlalchemy.engine.result.RMKeyView'>
<class 'list'>
<class 'sqlalchemy.engine.row.Row'>
<class 'sqlalchemy.engine.row.Row'>
<class 'sqlalchemy.engine.row.Row'>
<class 'sqlalchemy.engine.row.Row'>
```

From this output, we see

* The *keys()* method returns a RMKeyView object, which can be converted to an interable, list, or tuple using the Python *iter()*, *list()*, or *tuple()* functions.
* The *fetchmany()* method returns a list that contains Row objects, which are similar to [Named Tuples](https://docs.python.org/3/library/collections.html#collections.namedtuple). But, when printed, they look like normal Tuples.









## Database metadata compared to ORM classes

Print the database table metadata using the following statement:

```python
print(*Base.metadata.tables, sep=", ")
```

You should see the output displayed below, showing the table names in the Chinook database.

```
Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, Track, MediaType, Playlist, PlaylistTrack
```

The reason programmers use the SQLAlchemy ORM is so that they can treat database tables like Python classes in their programs and work in the "Pythonic" way. Let's find out some more information about the SQLAlchemy classes that map the tables in the database.

List the SQLAlchemy classes mapped by the automap extension.

```python
print(*Base.classes.keys(), sep=", ")
```

You should see the output displayed below, showing the table names in the Chinook database.

```
Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, Track, MediaType, Playlist
```

If you compare the names found in *Base.metadata.tables* with the names returned by *Base.classes.keys()*, you will see that we have eleven table objects but only ten ORM classes. This is because the *PlaylistTrack* table is an association table. SQLAlchemy ORM does not automatically create a class for an association table. It instead represents it as a table with foreign keys pointing to columns in the other tables.









## More querying methods

The SQLAlchemy session object offers [several methods for querying](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying) rows or items from a database. You can use the *execute()* method to get a result containing database rows, the *scalars()* method to get results containing single items from each row, or the [*scalar()* method](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars) to get the actual value of a single item in a single row.

Below is an example of using the various methods, and chaining additional methods onto either the original statement object or onto the session object.

Given the following SQLAlchemy select statement:

```python
statement = (select(Album.Title.label("Album"),
            Artist.Name.label("Artist"),
            Track.Name.label("Track"),
            Track.Composer, 
            Track.Milliseconds.label("Length"))
     .join(Track)
     .join(Artist)
    )
```

The *session.execute()* method returns a SQLAlchemy ORM Result object.

```python
session = Session(engine)
print(session.execute(statement))
```
```
<sqlalchemy.engine.result.ChunkedIteratorResult object at 0x0000016E8881BBD0>
```

The *session.execute()* method's *first()* method returns the first row in the Result object.

```python
print(session.execute(statement).first())
```
```
('For Those About To Rock We Salute You', 'AC/DC', 'For Those About To Rock (We Salute You)', 'Angus Young, Malcolm Young, Brian Johnson', 343719)
```

The *fetchmany()* method returns the specified number rows and returns them in a list of Row objects.

```python
print(session.execute(statement).fetchmany(2))
```
```
[('For Those About To Rock We Salute You', 'AC/DC', 'For Those About To Rock (We Salute You)', 'Angus Young, Malcolm Young, Brian Johnson', 343719), ('Balls to the Wall', 'Accept', 'Balls to the Wall', None, 342562)]
```

The *fetchall()* method gets all rows in the Result object and returns them in a list of Row objects. In this case, adding the *limit()* method to the statement causes the Result object to have only two rows in it.

```python
print(session.execute(statement.limit(2)).fetchall())
```
```
[('For Those About To Rock We Salute You', 'AC/DC', 'For Those About To Rock (We Salute You)', 'Angus Young, Malcolm Young, Brian Johnson', 343719), ('Balls to the Wall', 'Accept', 'Balls to the Wall', None, 342562)]
```

The *session.scalars()* method returns a SQLAlchemy ORM Scalars object, which, when iterated, looks like a list containing a series of values that come from the first column of each row in results returned by executing the SQL statement.

```python
print(session.scalars(statement))
```
```
<sqlalchemy.engine.result.ScalarResult object at 0x0000016E8886F0D0>
```

The *session.scalars()* method's *first()* method returns the first value from the series.

```python
print(session.scalars(statement).first())
```
```
For Those About To Rock We Salute You
```

The *fetchmany()* method returns the specified number of items and returns them in a list of values.

```python
print(session.scalars(statement).fetchmany(2))
```
```
['For Those About To Rock We Salute You', 'Balls to the Wall']
```

The *session.scalar()* method returns one value from the SQL statement's results. It returns the value in the first column of the first row.

```python
print(session.scalar(statement))
session.close()
```
```
For Those About To Rock We Salute You
```

## Selecting rows

You can create an SQL statement that searches for rows that match a specified criteria, using the *where()* method. For example, below is a script that returns the rows where the artist is "Alice in Chains" 

```python
statement = (select(Album.Title.label("Album"),
            Artist.Name.label("Artist"),
            Track.Name.label("Track"),
            Track.Composer, 
            Track.Milliseconds.label("Length"))
     .join(Track)
     .join(Artist)
     .where(Artist.Name == 'Alice In Chains')
    )

with Session(engine) as session:
    result = session.execute(statement).fetchall()
```

The *result* object is a list of *Row* objects selected from the database based on the criteria in the *where()* method. Print the track name and track composer from each Row object in the list named *result*.

```python
for row in result:
    print(f"Track name: {row.Track:18} Composer: {row.Composer}")
```

The output is:

```
Track name: We Die Young       Composer: Jerry Cantrell
Track name: Man In The Box     Composer: Jerry Cantrell, Layne Staley
Track name: Sea Of Sorrow      Composer: Jerry Cantrell
Track name: Bleed The Freak    Composer: Jerry Cantrell
Track name: I Can't Remember   Composer: Jerry Cantrell, Layne Staley
Track name: Love, Hate, Love   Composer: Jerry Cantrell, Layne Staley
Track name: It Ain't Like That Composer: Jerry Cantrell, Michael Starr, Sean Kinney
Track name: Sunshine           Composer: Jerry Cantrell
Track name: Put You Down       Composer: Jerry Cantrell
Track name: Confusion          Composer: Jerry Cantrell, Michael Starr, Layne Staley
Track name: I Know Somethin (Bout You) Composer: Jerry Cantrell
Track name: Real Thing         Composer: Jerry Cantrell, Layne Staley
```









## Joining tables in SQLAlchemy

Another way to create the dataframe containing album and track information from the Chinook database is to perform the table joins in the SQLAlchemy ORM query so that Pandas receives the final dataframe in one step. This may be more desirable than using the *pd.merge* method because it simplifies your Pandas operations and may be more efficient. 

In a properly-designed database, the relationships between tables are already defined using primary and foreign keys, and association tables. SQLAlchemy objects can use these relationships to automatically join data in different tables together.

Using the *table_info* function you created earlier, look at the relationships between the tables named *Album*, *Track*, and *Artist*.

```python
print(table_info('Album'))
print(table_info('Track'))
print(table_info('Artist'))
```

This shows us the following relationships:

```
Table: Album
+---------------+---------------+---------------+-----------------+
| Column Name   |  Primary Key  |  Foreign Key  | Relationship    |
|---------------+---------------+---------------+-----------------|
| AlbumId       |      YES      |               |                 |
| Title         |               |               |                 |
| ArtistId      |               |      YES      | Artist.ArtistId |
+---------------+---------------+---------------+-----------------+
Table: Track
+---------------+---------------+---------------+-----------------------+
| Column Name   |  Primary Key  |  Foreign Key  | Relationship          |
|---------------+---------------+---------------+-----------------------|
| TrackId       |      YES      |               |                       |
| Name          |               |               |                       |
| AlbumId       |               |      YES      | Album.AlbumId         |
| MediaTypeId   |               |      YES      | MediaType.MediaTypeId |
| GenreId       |               |      YES      | Genre.GenreId         |
| Composer      |               |               |                       |
| Milliseconds  |               |               |                       |
| Bytes         |               |               |                       |
| UnitPrice     |               |               |                       |
+---------------+---------------+---------------+-----------------------+
Table: Artist
+---------------+---------------+---------------+----------------+
| Column Name   |  Primary Key  |  Foreign Key  | Relationship   |
|---------------+---------------+---------------+----------------|
| ArtistId      |      YES      |               |                |
| Name          |               |               |                |
+---------------+---------------+---------------+----------------+
```

We see that the Album table has a foreign key that points to the Artist table and that the Track table has a foreign key that points to the Album table.

Knowing that these relationships exist, we can simply join all the data from multiple tables together using the *select()* functions' *join()* method. Here we select data from the Album, Track, and Artist tables by joining the Track and Artist tables with the Album table.

```python
statement = (select(Album, Track, Artist)
     .join(Track)
     .join(Artist)
    )
```

Use the pandas *read_sql_query* method to get data selected by the statement and load it into a dataframe.

```python
df4 = pd.read_sql_query(sql=q.statement, con=engine)

print(df4.shape)
display(df4.head())
```

The resulting dataset will look like the following:

![stub](./Images/pandas008.png)


You can see the columns, and the column names assigned by SQLAlchemy the query result. To get only the specific columns you need, create a new statement that will select each column by name, starting with the *Album.Title* column. Then, [rename the columns](https://devsheet.com/code-snippet/column-name-as-alias-name-sqlalchemy/) in the select statement using the *label* method.

```python
statement = (select(Album.Title.label("Album"),
            Artist.Name.label("Artist"),
            Track.Name.label("Track"),
            Track.Composer, 
            Track.Milliseconds.label("Length"))
     .join(Track)
     .join(Artist)
    )
```

Load the selected data from the database into a pandas dataframe:

```python
dataframe = pd.read_sql_query(sql=statement, con=engine)

print(dataframe.shape)
display(dataframe.head().style.format(thousands=","))
```

The result is shown below:

![stub](./Images/pandas010.png)


You see that joining tables and selecting specific columns in an SQLAlchemy query can give you the data you need in one step. Reading that data into a Pandas dataframe makes it easy to analyze the results.

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

![stub](./Images/pandas015.png)


I used the *join_from()* method to make the left and right sides of each join clearer to the program. normally it can infer the correct relationships but sometimes you need to be more specific.

And, to use the association table, if you want to see all the tracks on all the playlists:

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

![stub](./Images/pandas016.png)

## Outer joins in SQLAlchemy

As we saw when merging dataframes with pandas, sometimes you need to perform an *outer join* to get all the data you want.

In SQLAlchemy, a normal (inner) join of the Employee and Customer tables would look like:

```python
statement = select(
    Employee.EmployeeId, 
    (Employee.FirstName + ' ' + Employee.LastName).label("Employee Name"), 
    Employee.Title,
    func.count(Customer.CustomerId)
).outerjoin(Customer).group_by(Employee.EmployeeId)

with Session(engine) as session:
    results_proxy = session.execute(statement)    
    results = results_proxy.fetchall()
    headers = results_proxy.keys()

print(tabulate(results, headers))
```
```
  EmployeeId  Employee Name    Title                  count
------------  ---------------  -------------------  -------
           3  Jane Peacock     Sales Support Agent       21
           4  Margaret Park    Sales Support Agent       20
           5  Steve Johnson    Sales Support Agent       18
```

But, if we perform an outer join by changing the statement to the following:

```
statement = select(
    Employee.EmployeeId, 
    (Employee.FirstName + ' ' + Employee.LastName).label("Employee Name"), 
    Employee.Title,
    func.count(Customer.CustomerId)
).outerjoin(Customer).group_by(Employee.EmployeeId)
```

We see we now get all employees in the result, even the ones who do not support customers.

```
 EmployeeId    Employee Name               Title  # Customers
          1     Andrew Adams     General Manager            0
          2    Nancy Edwards       Sales Manager            0
          3     Jane Peacock Sales Support Agent           21
          4    Margaret Park Sales Support Agent           20
          5    Steve Johnson Sales Support Agent           18
          6 Michael Mitchell          IT Manager            0
          7      Robert King            IT Staff            0
          8   Laura Callahan            IT Staff            0
```

Unlike the version of this example where we merged Pandas dataframes, we did not need to specify which columns to join on. SQLAlchemy knows the relationships between the Employee and Customer tables because it is defined in the database schema and is now reflected in the SQLAlchemy ORM.

### Merging with outer joins

The Pandas *merge()* function creates a new dataframe containing rows that match on the defined columns in each table and leaves out rows that do not match. As mentioned above, this is called an *inner join* and is the default operation.

Sometimes, you may want to include rows that do not match on the defined columns in each table. This is called at [*outer join*](https://www.freecodecamp.org/news/sql-join-types-inner-join-vs-outer-join-example/).

Consider the Employee and Customer tables in the Chinook database. Every customer row in the Customer table has a relationship with a Chinook employee. The SupportRepId column in the Customer table is a foreign key that points to the EmployeeId column in the Employee table to create a many-to-one relationship between teh Customer and Employee tables.

When you want to read data related to customers supported by each employee, you need to join the Employee table and the Customer table to get this data. However, the default inner join only returns rows from the joined tables if an employee is actually supporting customers so the returned dataframe is missing employees.

Work through the following example to see how this works.

First, see how many employees work for the Chinook company.

```python
employees = pd.read_sql_table(table_name='Employee', con=engine)
print(employees.shape)
print(employees)
```

The first part of the Employee table looks like the output below:

```
(8, 15)
   EmployeeId  LastName FirstName                Title  ReportsTo  BirthDate  \
0           1     Adams    Andrew      General Manager        NaN 1962-02-18   
1           2   Edwards     Nancy        Sales Manager        1.0 1958-12-08   
2           3   Peacock      Jane  Sales Support Agent        2.0 1973-08-29   
3           4      Park  Margaret  Sales Support Agent        2.0 1947-09-19   
4           5   Johnson     Steve  Sales Support Agent        2.0 1965-03-03   
5           6  Mitchell   Michael           IT Manager        1.0 1973-07-01   
6           7      King    Robert             IT Staff        6.0 1970-05-29   
7           8  Callahan     Laura             IT Staff        6.0 1968-01-09   
```

We see that the Chinook company has eight employees. 

Let's look at the dataframe created when we read the Customer table:

```python
customers = pd.read_sql_table(table_name='Customer', con=engine)
print(customers.shape)
print(customers.head(3))
```

The first three rows (truncated) of the customers dataframe looks like below:

```
(59, 13)
   CustomerId FirstName   LastName  \...  SupportRepId 
0           1      Luís  Gonçalves                   3
1           2    Leonie     Köhler                   5
2           3  François   Tremblay                   3
```

We see Chinook has fifty-nine customers. We can also check that every customer has a support representative assigned to them:

```python
test = customers.loc[customers['SupportRepId'].isnull()] 
print(len(test))
```
```
0
```

We see zero customers have a null, or "NaN", value in their *SupportRepId* column. 

Now we need to merge the *customers* and *employees* dataframes. But, we want to merge by matching each customer's *SupportRepId* with each employee's *EmployeeId*.

A default (inner join) merge would look like the following:

```python
dataframe = pd.merge(
    employees, 
    customers, 
    left_on='EmployeeId', 
    right_on='SupportRepId'
)
```

If we do some additional grouping and cleanup of the merged dataframe, and then print it:

```python
emp_info = ['EmployeeId','LastName_x', 'FirstName_x', 'Title']

dataframe2 = (dataframe
              .groupby(emp_info, 
                       as_index=False, 
                       dropna=False)['CustomerId'].count()
             )

dataframe2.rename(columns = {'CustomerId':'# Customers'}, inplace=True)

dataframe2['Employee Name'] = (dataframe2['FirstName_x'] 
                               + ' ' 
                               + dataframe2['LastName_x'])

dataframe2.drop(['FirstName_x', 'LastName_x'], 
                axis=1, 
                inplace=True)

dataframe2 = dataframe2[['EmployeeId',
                         'Employee Name',
                         'Title',
                         '# Customers']]

print(dataframe2.to_string(index=False))
```

We see the following output:

```
 EmployeeId Employee Name               Title  # Customers
          3  Jane Peacock Sales Support Agent           21
          4 Margaret Park Sales Support Agent           20
          5 Steve Johnson Sales Support Agent           18
```

This is nice, but we know we have eight employees. And, we wanted a report showing the customers supported by all eight employees. Apparently, five of our employees do not support customers so they were excluded from the inner join of the *employees* ad *customers* dataframes.

To ensure that we get all employees into the merged dataframe, even if their *EmployeeId* does not match with a customer's *SupportRepId*, we need to do an outer join. Specifically, a left outer join because we want to include unmatched rows from the left-side table (in the merge statement), but not from the right side. 

A merge statement that [executes a left outer join](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#brief-primer-on-merge-methods-relational-algebra) is shown below:

```python
dataframe = pd.merge(
    employees, 
    customers, 
    left_on='EmployeeId', 
    right_on='SupportRepId',
    how = 'left'
)
```

After you group and clean up the column headings, as previously shown above, you get the following output:

```
EmployeeId    Employee Name               Title  # Customers
          1     Andrew Adams     General Manager            0
          2    Nancy Edwards       Sales Manager            0
          3     Jane Peacock Sales Support Agent           21
          4    Margaret Park Sales Support Agent           20
          5    Steve Johnson Sales Support Agent           18
          6 Michael Mitchell          IT Manager            0
          7      Robert King            IT Staff            0
          8   Laura Callahan            IT Staff            0
```

Now all the employees records are in the dataframe that was grouped so we see that five employees supported no customers. This makes sense when you look at the employees' titles.

And, when you print the merged dataframe, you can see that there are five additional rows and each of those additional rows contains employee information but no customer information because no customers matched with that employee.










## Data analysis using SQLAlchemy queries

You may also analyze data using SQLAlchemy queries and functions. Many database engines support functions like maximum, minimum, and standard deviation. The functions supported may vary for each database engine. The SQLite database engine supports relatively few functions.

If you are writing an application that needs direct access to data from a database, you may want to see more examples of SQLAlchemy statements.

The following SQLAlchemy statements use [functions available in the SQLite database engine](https://www.techonthenet.com/sqlite/functions/index.php) and will display similar results to the Pandas dataframe work we did previously. 

First, write code that maps the structure of the database:

```python
from sqlalchemy import create_engine, select, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine(r"sqlite:///C:/Users/blinklet/Documents/chinook-database/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)

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

Then write the folloing SQLAlchemy queries, which use database functions, and some Python functions to analyze the data in the database.

```python
with Session(engine) as session:
    statement = select(func.max(Track.Milliseconds))
    length = session.scalar(statement)
    print(f"Longest track length: {length:,.0f}")

    statement = select(func.min(Track.Milliseconds))
    length = session.scalar(statement)
    print(f"Shortest track length: {length:,.0f}")
    
    statement = select(func.count(Track.TrackId)).where(Track.Composer == None)
    composer_rows = session.scalar(statement)
    print(f"How many blanks in Composer column?: {composer_rows:,.0f}")

    statement = select(func.avg(Track.Milliseconds))
    mean = session.scalar(statement)
    print(f"Track length mean: {mean:,.0f}")
    
    from statistics import median, stdev
    statement = select(Track.Milliseconds)
    list_of_lengths = list(session.scalars(statement))
    print(f"Track length median: {median(list_of_lengths):,.0f}")
    print(f"Track length standard deviation: {stdev(list_of_lengths):,.0f}")
    
    from statistics import correlation
    statement = select(Track.UnitPrice)
    list_of_prices = list(session.scalars(statement))
    l = [int(x) for x in list_of_lengths]
    p = [int(x) for x  in list_of_prices]
    print(f"Correlation between Length and UnitPrice {correlation(l,p):,.2f}")
    
    statement = (select(Artist.Name)
                 .join_from(Track, Album)
                 .join_from(Album, Artist)
                 .group_by(Artist.Name)
                 .order_by(func.count(Artist.Name).desc()))
    mode = session.scalar(statement)
    print(f"Artist mode: {mode}")
```

The output analysis looks like the following:

```
Longest track length: 5,286,953
Shortest track length: 1,071
How many blanks in Composer column?: 978
Track length mean: 393,599
Track length median: 255,634
Track length standard deviation: 535,005
Correlation between Length and UnitPrice 0.93
Artist mode: Iron Maiden
```

We had fewer options for analyzing data natively in the database.

You can see that performing simple calculations and transformations is easier with Pandas than with the SQLAlchemy ORM's *select* methods. It is still good to learn about how to build SQL queries using the SQLAlchemy ORM. 

You will want to use complex SQL queries when you need single values from the database for your application, or when you are building your initial data set from a larger database.











The statement `length = q[0]` is actually doing a lotmore than it looks like. The object, *q* returned by the query uses [lazy loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#lazy-loading) so it does not contain any data until you assign it to another object or cause it to iterate at least once. When the object does load data, it returns row data in a tuple. Since you queried only one row from the column, the tuple contains only one value. You [get that value by indexing](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#selecting-orm-entities-and-columns) the tuple.

I could also use the *iter()* function to cause the row object to return the tuple and then use the *next* functions to return the first item in the tuple. Then the statement would be `length = next(iter(q))`. 














# Visualizing data 

It is easy to display data visualizations when working in a Jupyter notebook. You create a dataframe containing the data you want to visualize and then use the [Pandas dataframe's *.plot()* method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html). If you want more functionality or prefer a certain style of charts, you can use one of many specialized Python visualization packages like [MatPlotLib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/), or [Plotly](https://plotly.com/python/).

We'll run a query that gets a lot of data from the database so we can perform analysis and visualization using Pandas. We'll get data that shows the purchase history of all the tracks in our inventory, including tracks that have not sold. This is a good example of using *outer joins* that include tracks that have not been sold, so do not have corresponding entries in the InvoiceLine table.

```python
statement = (
    select(
        Customer.CustomerId,
        Customer.FirstName.label("Customer Firstname"),
        Customer.LastName.label("Customer Lastname"),
        Customer.Country,
        Track.TrackId,
        Track.Name.label("Track"),
        Album.Title.label("Album"),
        Artist.Name.label("Artist"),
        Genre.Name.label("Genre"),
        MediaType.Name.label("Media"),
        InvoiceLine.Quantity,
        InvoiceLine.UnitPrice,
        Invoice.InvoiceDate,
        Employee.EmployeeId,
        Employee.FirstName.label("Employee Firstname"),
        Employee.LastName.label("Employee Lastname")
    )
    .join_from(Track, Album)
    .join_from(Track, Genre)
    .join_from(Track, MediaType)
    .join_from(Album, Artist)
    .outerjoin_from(Track, InvoiceLine)
    .outerjoin_from(InvoiceLine, Invoice)
    .outerjoin_from(Invoice, Customer)
    .outerjoin_from(Customer, Employee)
)

dataframe = pd.read_sql_query(statement, engine)

print(dataframe.shape)
display(dataframe.tail())
```

A sample of the data in the dataframe is shown below. You can see we have 3,759 rows and that some rows contain blank data where tracks have not sold.

![stub](./Images/pandas030.png)

Next, create a new dataframe that groups track sales by quarter and plot the results

```python
df = (dataframe[['InvoiceDate','Quantity','UnitPrice']]
       .dropna()
       .rename(columns = {'UnitPrice':'Revenue'})
       .groupby(pd.Grouper(key="InvoiceDate", freq='3M')).sum()
       .head(-1).tail(-1)    # drop first and last period
      )

display(df.plot())
```

You should see output like:

![stub](./Images/pandas040.png)


Next, analyze total revenue per country:

```python
df = (dataframe[['Country','UnitPrice']]
       .rename(columns = {'UnitPrice':'Revenue'})
       .groupby(pd.Grouper(key="Country")).sum()
       .sort_values(by = 'Revenue', ascending = False)
      )

display(df.plot(kind='bar'))
```

You should see an output like:

![stub](./Images/pandas041.png)

Finally, see how the total number of units sold in each genre correlates with the total number of units available in each genre:

```python
df = (dataframe[['Genre','Quantity']]
       .rename(columns = {'Quantity':'# Sold'})
       .groupby("Genre", as_index=False)['# Sold'].sum()
      )

df2 = (dataframe[['Genre','TrackId']]
       .rename(columns = {'TrackId':'# Tracks available'})
       .groupby("Genre", as_index=False)["# Tracks available"].count()
      )

df3 = pd.merge(df, df2)

display(df3.plot(kind='scatter', x='# Sold', y='# Tracks available'))
```

As you can see in the scatter plot below, there appears to be a strong correlation between the number if tracks sold and the number of tracks available in each category:

![stub](./Images/pandas042.png)




















## Convert an ORM result into a Pandas dataframe

You may wish to perform a query and get a result in the SQLAlchemy ORM and then convert the result into a Pandas dataframe. This allows you to separate your program's database logic from its business logic. 

Instead of building a select statement and running it as part of the Pandas *read_sql_query* method, get the ORM result object from the SQLAlchemy session. Then use the [Pandas *Dataframe*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) class to convert the received data into a dataframe. For example:

```python
statement = (
    select(
        Playlist.Name.label("Playlist"),
            Track.Name.label("Track"),
            Album.Title.label("Album"),
            Artist.Name.label("Artist")
    )
    .join_from(Playlist, playlisttrack)
    .join_from(playlisttrack, Track)
    .join_from(Track, Album)
    .join_from(Album, Artist)
)

with Session(engine) as session:
    results_proxy = session.execute(statement)
    
    headers = results_proxy.keys()
    results = results_proxy.fetchall()

dataframe = pd.DataFrame(results, columns=headers)

print(dataframe.sample(3).to_string(index=False))
```

The output should look like:

```
  Playlist               Track                   Album        Artist
     Music      No Bone Movies                 Tribute Ozzy Osbourne
90’s Music Upon A Golden Horse Walking Into Clarksdale  Page & Plant
90’s Music   The River (Remix)                Tangents The Tea Party
```