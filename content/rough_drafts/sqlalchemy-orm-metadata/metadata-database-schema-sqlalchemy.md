title: View SQLAlchemy ORM metadata
slug: sqalchemy-database-schema-metadata
summary: View metadata that SQLAlchemy gathers via database reflection.
date: 2023-09-30
modified: 2023-09-30
category: Databases
status: Draft




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











sqlalchemy.schema.sort_tables_and_constraints()



You can also identify important details about the database. For example, you can [identify](https://condor.depaul.edu/gandrus/240IT/accesspages/relationships.htm) that the *PlaylistTrack* table is an [association table](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) that supports a [many-to-many relationships](https://medium.com/@BryanFajardo/how-to-use-associative-entities-in-relational-databases-4456a2c71cda) between two other tables. A typical association table has two columns and each of its columns are both Primary Keys and Foreign Keys. 

Association tables are declared differently in the ORM than normal tables in the SQLAlchemy ORM. They are not reflected as ORM classes so there will be no *PlaylistTrack* class in the ORM. The association table is defined only as a table object in the ORM.

After looking at all the information output, you should be able to draw a diagram showing the database tables and relationships, like the one below:

![Chinook database diagram showing relationships](./Images/chinook-diagram-03.png)