https://mystery.knightlab.com/
The SQL Murder Mystery is designed to be both a self-directed lesson to learn SQL concepts and commands and a fun game for experienced SQL users to solve an intriguing crime.

https://www.db4free.net/
click on Signup
Enter DB name, your MySQL username and password, and e-mail (for verification email)
* datascience01
* greygrey1984
* LyJVCi#bS7
* vendors@brianlinkletter.ca
Check email confirmation email
The go to phpMyAdmin to add data to the database
https://www.mysqltutorial.org/mysql-sample-database.aspx
rename so extension is .sql.zip
Import file into myPHP admin. Click on import button at bottomn
(cannot import because probably someone else already used the "classicmodels" database name)



https://accessexperts.com/blog/2021/12/07/wide-world-importer-database-for-access/

https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/linq/downloading-sample-databases#northwind_access

https://pypi.org/project/sqlalchemy-access/



blinklet
testtset001



DSN=SQL-Northwind;APP=Microsoft Office 2003;WSID=DELLNOTEBOOK;DATABASE=Northwind;Network=DBMSSOCN;Address=LOCALHOST;Trusted_Connection=Yes

"Provider='SQLOLEDB';Server='MySqlServer';" & _ 
 "Database='Northwind';Integrated Security='SSPI';"
 

Docker container with Northwind database
https://github.com/pthom/northwind_psql

Try Podman Desktop because Docker Desktop has license issues
https://podman-desktop.io/






# Exploring the database structure

Create a new cell in the Jupyter notebook, enter the following code, and run it.

```python
print(inspector.get_schema_names())
```

The output shows there is one database schema, named *main*.

Create a new cell in the Jupyter notebook, enter the following code, and run it.

```python
print(inspector.get_schema_names(schema_name='main'))
```

This is similar to the code we used to verify our connection to the SQLite database was working. It prints out the database table names. This time, we passed in the schema name as a parameter but that is only necessary if you have multiple database schemas.

To see all the information about each column in all the database tables, run the following code:

```python
for tbl in inspector.get_table_names():
    print(inspector.get_columns(schema_name='main',table_name=tbl))
```

But, in this example, you only want the column names so create a new cell in the Jupyter notebook, enter the following code, and run it.

```python
for tbl in inspector.get_table_names():
    print(f"Table = {tbl}")
    for col in inspector.get_columns(schema_name="main",table_name=tbl):
        star = ""
        if col['primary_key'] == 1:
            star = "*"
        print(f"{star}{col['name']}{star}", end = ", ")
    print("\n")
```

The output shows all the tables, with a list of each table's column names. Primary key columns are highlighted by asterisks. The output looks like the output shown below:

```
Table = circuits
*circuitId*, circuitRef, name, location, country, lat, lng, alt, url, 

Table = constructor_results
*constructorResultsId*, raceId, constructorId, points, status, 

Table = constructor_standings
*constructorStandingsId*, raceId, constructorId, points, position, positionText, wins, , 

Table = constructors
constructorId, constructorRef, name, nationality, url, , 

Table = driver_standings
*driverStandingsId*, raceId, driverId, points, position, positionText, wins, 

Table = drivers
*driverId*, driverRef, number, code, forename, surname, dob, nationality, url, 

Table = laptimes
raceId, driverId, lap, position, time, milliseconds, 

Table = pitstops
raceId, driverId, stop, lap, time, duration, milliseconds, 

Table = qualifying
*qualifyId*, raceId, driverId, constructorId, number, position, q1, q2, q3, 

Table = races
*raceId*, year, round, circuitId, name, date, time, url, 

Table = results
resultId, raceId, driverId, constructorId, number, grid, position, positionText, positionOrder, points, laps, time, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId, 

Table = seasons
year, url, 

Table = status
*statusId*, status,
```
> PlaylistTrack is an *association table* so it is in the list of tables but not in the list of classes

Schema viewer
https://github.com/schemaspy/schemaspy



Examples of business analytics SQL queries on Chinook Database
https://m-soro.github.io/Business-Analytics/SQL-for-Data-Analysis/L4-Project-Query-Music-Store/

https://medium.com/analytics-vidhya/translating-sql-queries-to-sqlalchemy-orm-a8603085762b





The statement `length = q[0]` is actually doing a lotmore than it looks like. The object, *q* returned by the query uses [lazy loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#lazy-loading) so it does not contain any data until you assign it to another object or cause it to iterate at least once. When the object does load data, it returns row data in a tuple. Since you queried only one row from the column, the tuple contains only one value. You [get that value by indexing](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#selecting-orm-entities-and-columns) the tuple.

I could also use the *iter()* function to cause the row object to return the tuple and then use the *next* functions to return the first item in the tuple. Then the statement would be `length = next(iter(q))`. 








Knowing those relationships, we can directly access data from joined tables after querying the first table. For example, here we get the first record from the Album table, then access data in the the joined Artist and Track tables using the established relationships.

```python
from sqlalchemy import select

session = Session(engine)

statement = select(Album)
first_album = session.scalar(statement)

print(f"Album:  {first_album.Title}")
print(f"Artist: {first_album.artist.Name}")
print(f"Tracks:")
for t in first_album.track_collection:
    print(f"    {t.Name}")

session.close()
```
```
Album:  For Those About To Rock We Salute You
Artist: AC/DC
Tracks:
    For Those About To Rock (We Salute You)
    Put The Finger On You
    Let's Get It Up
    Inject The Venom
    Snowballed
    Evil Walks
    C.O.D.
    Breaking The Rules
    Night Of The Long Knives
    Spellbound
```







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









Programmers who are have already mastered the SQL language could simply use the appropriate driver that is compatible with the SQL database they are using, such as [psycopg](https://www.psycopg.org/) for PostgreSQL, or [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) for MySQL. Since we are using an SQLite database, we could use the [sqlite package](https://www.sqlite.org/index.html), which is part of the Python standard library. But, remember, you need to know the SQL query language when writing programs that use these Python database drivers.









You can remove the "ArtistId" column from the data frame because it is now redundant. Keep the *AlbumId* column because you will use it to join data from the Track table in the next step. 

```python
df1.drop('ArtistId', axis=1)
```

You can also rename the *Name* column to *Artist* so it is clearer.

```
df1.rename(columns = {'Name':'Artist'})
```

Also, you could have done everything in one statement when you merged the dataframes by chaining pandas methods together:

```python
df1 = (pd
     .merge(albums, artists)
     .drop('ArtistId', axis=1)
     .rename(columns = {'Name':'Artist'}))
```

Now get data from a third table and merge it with the dataframe *df1*. Get the data from the Track table and load it into a pandas dataframe named *tracks*:

```python
tracks = pd.read_sql_table(table_name='Track', con=engine)
```

If you print the first few rows of the *tracks* dataframe, you can see it has 3,503 rows and nine columns. You should expect that Pandas will use the *AlbumId* column in the dataframe *df1* to join on the AlbumId column in dataframe *tracks*.

```python
print(tracks.head())
print(tracks.shape)
```
```
   TrackId                                     Name  AlbumId  MediaTypeId  \
0        1  For Those About To Rock (We Salute You)        1            1   
1        2                        Balls to the Wall        2            2   
2        3                          Fast As a Shark        3            2   
3        4                        Restless and Wild        3            2   
4        5                     Princess of the Dawn        3            2   

   GenreId                                           Composer  Milliseconds  \
0        1          Angus Young, Malcolm Young, Brian Johnson        343719   
1        1                                               None        342562   
2        1  F. Baltes, S. Kaufman, U. Dirkscneider & W. Ho...        230619   
3        1  F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. D...        252051   
4        1                         Deaffy & R.A. Smith-Diesel        375418   

      Bytes  UnitPrice  
0  11170334       0.99  
1   5510424       0.99  
2   3990994       0.99  
3   4331779       0.99  
4   6290521       0.99  
(3503, 9)
```

You can see how Pandas displays the nine columns by spitting the displayed tables into three "rows". And you can see that we have 3,503 rows in the Tracks table.

Finally, merge the *tracks* dataframe with the *df1* dataframe and, at the same time, delete unneeded columns and rename other columns:

```python
df3 = (pd
     .merge(df1, tracks)
     .drop(['AlbumId','TrackId',
            'Bytes','UnitPrice',
            'MediaTypeId','GenreId'], axis=1)
     .rename(columns = {'Name':'Track', 
                        'Title':'Album',
                        'Milliseconds':'Length(ms)'}))

print(df3.shape)
display(df3.head().style.format(thousands=","))
```













# NaN and NULL and None


Check that every customer has a support representative assigned to them. 

```python
test = customers.loc[customers['SupportRepId'].isnull()] 
print(len(test))
```
```
0
```

We see zero customers have a null, or "NaN", value in their *SupportRepId* column. So, we can place the *customers* dataframe on the right side of the merge function and perform a *left outer join*.










## Available public databases

If you cannot get access to HRDP when you start experimenting with data science tools like Python and SQLAlchemy, use another available database for practice. There is lots of data [available to the public](https://www.dropbase.io/post/top-11-open-and-public-data-sources) that you may want to analyze as you learn more about data science. We want to learn how to analyze data stored in a database so we need data available in that format.

The best solution is to install an SQL database engine like [SQLite](https://www.sqlite.org/index.html) on your PC and download a database backup from a public repository. [Kaggle](https://www.kaggle.com/) offers many [database files that are suitable for learning data science](https://www.kaggle.com/datasets?search=SQL) but many databases offered by Kaggle are poorly designed and cause errors when SQLAlchemy performs database reflection. Experts may be able to work around these problems but they can frustrate beginners. Other, properly-designed databases like the [Northwind database](https://github.com/jpwhite3/northwind-SQLite3), or the [Chinook database](https://github.com/lerocha/chinook-database), may also be more suitable.






# MS Access
server like [Microsoft Access](https://www.microsoft.com/en-us/microsoft-365/access) on your laptop and then download a database backup from a public repository like the [Microsoft Northwind SQL Sample database](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/linq/downloading-sample-databases#northwind_access). I tried that but could not find good information about how to connect SQLAlchemy to the Access Database on a Windows laptop.

## Microsoft Access

You already have access to Microsoft Access via Nokia's Office 365 corporate license. Install Access if you do not already have it.

Start Microsoft Access. Then, get the [Northwind sample database for Microsoft Access](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/linq/downloading-sample-databases#northwind_access). 

Click on the *More templates* link on the Access screen. Search for *Northwind* in the *Search for Online Templates* field. The Northwind database should appear, as shown below:

![Find online Northwind database file](./Images/access001.png)

Select the Northwind database to download it. You will see an information screen like the one below. Change the filename to *Northwind* and select the folder to which it will be downloaded. The click the *Create* button.

![Download and save the database](./Images/access002.png)

Microsoft Access will display its view of the database with a welcome screen, as shown below. We are not interested in using the MS Access interface. We want to connect to this database using SQLAlchemy.

## SQLAlchemy Access dialect

SQLAlchemy needs a *dialect* installed so you can connect it to Microsoft Access. Install the [sqlalchemy-access](https://pypi.org/project/sqlalchemy-access/) python package into your virtual environment.

```powershell
(env) > pip install sqlalchemy-access
```

Python program:

```python
from sqlalchemy import create_engine, URL, inspect

engine = create_engine(r'access+pyodbc://@northwind')
inspector = inspect(engine)
print(inspector.get_table_names())
```






[split Access database](https://support.microsoft.com/en-us/office/split-an-access-database-3015ad18-a3a1-4e9c-a7f3-51b1d73498cc) creates a backend database and removes all the Access-only analysis tables to a front-end

```
import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\blinklet\Documents\Northwind.accdb;')
cursor = conn.cursor()
cursor.execute('select * from products')
for row in cursor.tables():
    print(row.table_name)
for row in cursor.fetchmany(2):
    print(row)
```


### Other sources

 

Another option is to create a database on the public SQL server at [db4free.net](https://www.db4free.net/). You will need to build a sample database from scratch, or from a backup file. The *db4free.net* service can only import very small database backups. While this service may be good for experimenting with databases, it is not that helpful for serving large datasets like those needed in data science.
