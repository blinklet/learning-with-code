title: Exploring relational database schema using SQLAlchemy's inspection module
slug: sqalchemy-database-schema-explore-inspect
summary: Use the SQLAlchemy *inspect* module to read SQL database schema information via a Python API. This post provides inspection examples that are relevant to users who read data from existing databases and who need to understand the data relationships within a database.
date: 2023-08-31
modified: 2023-08-31
category: Databases
<!--status: Published-->


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