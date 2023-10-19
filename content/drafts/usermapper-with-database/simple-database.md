In this post, I study how to use Python and the [*SQLAlchemy ORM*](https://medium.com/dataexplorations/sqlalchemy-orm-a-more-pythonic-way-of-interacting-with-your-database-935b57fd2d4d) to write data to a database and read it back. I will use the [*SQLAlchemy*](https://www.sqlalchemy.org/) library to define a database table, initialize a new database, and then write and read data.

## The fundamental topics

In some of my previous posts, I already described how to [use SQLAlchemy to read data]({filename}/articles/016-sqlalchemy-read-database/sqalchemy-read-database.md) from an existing relational database. If you have never used the SQLAlchemy ORM before, I suggest you read those posts, first.

To demonstrate this topic, I will create a simple database that contains just one table. The table will have the following columns: a user ID, which is a string and will serve as the table's primary key and must be unique in each row; a string containing user data, and a time stamp recorded in the standard *[datetime](https://docs.python.org/3/library/datetime.html)* format. I will use Python's built-in *[SQLite](https://www.sqlite.org/index.html)* database driver.

Then I will show how to add rows containing data to the database, how to read data from the database, and how to modify data in exsiting rows. As I work through these steps, I will discuss how SQLAlchemy and the database are handling data before and after a transaction is completed.

## Create the environment

As always, we need a Python virtual environment so we can install dependencies in an isolated environment. Create a project directory and a new Python virtual environment. Then, install SQLAlchemy in the virtual environment.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install sqlalchemy
```

You may, optionally, install and run [Jupyter Notebooks](https://docs.jupyter.org/en/latest/) so you can more easily follow this excercise. Or you may use the standard Python REPL. I will use a Jupyter Notebook.

```
(.venv) $ pip install jupyterlab
(.venv) $ jupyter-lab
```

The Jupyter Notebook will open in a browser window.


## Create a database

I will create and use an SQLite database because SQLite is already built into Python. You may use any database you wish. Just replace the database connection string in my examples below with your own database connection string.

### Create a connection

First, create a [connection](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#getting-a-connection) to a database. In most cases, the database must already exists but SQLite lets you start with no database.

SQLAlchemy's *create_engine()* function generates an instance of the [*Engine* class](https://docs.sqlalchemy.org/en/20/tutorial/engine.html), configured with the information in the connection string, which tells the Engine which database driver to use, the database location, and its authentication information. 

In the Jupyter Notebook cell (or the Python REPL), enter the following code:

```python
from sqlalchemy import create_engine

connection_string = "sqlite:///userdata.db"
engine = create_engine(connection_string, echo=True)
```

The Engine instance, which I named *engine*, does not immediately create a connection to the database. It will create a connection the first time it is asked to perform a database transaction. 

For example, after running the above code, the database file named *userdata.db* is not yet created in the project folder. 

### Declare database table information

There are two ways to create database metadata: [reflection](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html), or [declarative mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping). 

I covered reflection extensively in my previous post about [using SQLAlchemy to read data]({filename}/articles/016-sqlalchemy-read-database/sqalchemy-read-database.md) and, since we are starting with a new, empty database, reflection does not apply in this case so I will use [SQLAlchemy Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) to manually define SQL database tables as Python classes. 

The SQLAlchemy documentation recommends you use Declarative Mapping in all cases to manually [build SQLAlchemy ORM classes](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-metadata) that match the database structure that either exists or is to be defined. Declarative Mapping documents the database structure in your program and allows you to more easily handle changes to database structure in the future.

Use the SQLAlchemy ORM's [*DeclarativeBase* class](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) to perform declarative mapping. The standard practice is to first create a class called *Base* that is a subclass of the *DeclarativeBase* class. The new *Base* class has a metadata attribute that stores database table metadata [^2]. 

[^2]: Why create *Base* and not just subclass *DeclarativeBase* in my table classes, below? Because, in more advanced database applications, the *Base* class can be configured with custom metadata and other attributes that could be inherited by all other database subclasses. I don't add additional configuration to the *Base* class in this example so creating it now is just a "good practice".

Enter the following code and run it:

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```

Next, I create a class that defines a table. This new class is a subclass of the *Base* class I created earlier. I don't need to include an *__init__()* method in the class definition because SQLAlchemy creates a default *__init__()* method for subclasses of the *DeclarativeBase* class, which is good enough in this case.

I create a class named *Userdata* and define its *__tablename__* attribute. Then, I create three new attributes that map the table columns. Each attribute is generated using the *mapped_column()* function [^3], which takes parameters that define the column's data type and relationships. The attribute name defines the column name.

```python
from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

class Userdata(Base):
    __tablename__ = "userdata"
    user_id = mapped_column(String(32), primary_key=True, nullable=False)
    user_data = mapped_column(String(640))
    time_stamp = mapped_column(DateTime(timezone=True))
```

[^3]: In some other tutorials, you may have seen the attributes defined differently, using [Python type hints](https://peps.python.org/pep-0484/) and the [ORM's *Mapped* class](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html). I am not yet using type hints in my Python programs so I exclusively used the SQLAlchemy ORM *mapped_column()* function to define each column.

The *Userdata* class I defined is an *[ORM Mapped Class](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapped-class-overview)*. It, and any other ORM mapped classes I create, define the database. Every time I run this code in the future, this class sets up the Python objects that will interact with the table and columns in the database. 

When you create a new subclass, like *Userdata*, that is based on the *Base* class, information you defined in the subclass is also [registered](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) in the *Base* class's metadata collection. The SQLAlchemy developers used some advanced object-oriented programming techniques to accomplish this but users of SQLAlchemy don't need to worry about how this is done. Just know that you can get [table metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata) from the *Base.metadata.tables* attribute, even though that information is defined in other classes based on the *Base* class.

For example:

```python
print(Base.metadata.tables)
```

Produces the following output:

```
FacadeDict({'userdata': Table('userdata', MetaData(), Column('user_id', String(length=32), table=<userdata>, primary_key=True, nullable=False), Column('user_data', String(length=640), table=<userdata>), Column('time_stamp', DateTime(timezone=True), table=<userdata>), schema=None)})
```

### Connect to the database 

If you are running this program for the first time, you must create the database. All model classes that inherit from *Base* are registered in its metadata, so use the *Base* class to create all its associated tables [^1] in the database. The *Base* object's *metadata.create_all()* method will use the metadata I defined in the ORM mapped classes to create the database structure. 

Pass it the database *engine* instance as a parameter. 

[^1] From [StackOverflow answer #70402667](https://stackoverflow.com/questions/70402667/how-to-use-create-all-for-sqlalchemy-orm-objects-across-files)

```python
Base.metadata.create_all(engine)
```

At this point, SQLAlchemy will connect to the database defined by the *engine* instance and send SQL statements that create a table named *userdata*. Since I am using SQLite, a database file named *userdata.db* gets created in the project folder.

If the database already exists, SQLAlchemy detects it and does not alter the existing database. But, if the ORM Mapped Classes you created do not match the the existing database schema, SQLAlchemy will raise an exception. I do not cover how to modify existing database schema in this post. To learn more about that, read about [SQLAlchemy database migration](https://alembic.sqlalchemy.org/en/latest/).

### Start a session

Now, I want to write some data to the database, using the [unit-of-work pattern](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#updating-orm-objects-using-the-unit-of-work-pattern) recommended in the ORM documentation. To do this, I first create a [database session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-basics), which will manage the database transaction. One way to do that is to create an instance of the SQLAlcemy ORM's *Session* class and bind it to the *engine* instance I created earlier.

```python
from sqlalchemy.orm import Session

session = Session(engine)
```

There are may ways to [create and use sessions](https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session). The SQLAlchemy documentation describes multiple ways to [use sessions](https://docs.sqlalchemy.org/en/20/orm/session.html#module-sqlalchemy.orm.session) and many [blog posts](https://soshace.com/optimizing-database-interactions-in-python-sqlalchemy-best-practices/) are available that describe how to create efficient database transactions. I will cover a few methods in this post, starting with the simplest, shown above.


## Write some records

To add rows to the Userdata table in the database, add instances of the *Userdata* class to the SQLAlchemy session, and set the values of the attributes representing each column. For example, to add a row where the *user_id* is "Brad", and the *user_data* is "Brad's data", with a time stamp recording when the row was added, run the following code:

```python
from datetime import datetime
user = Userdata(user_id="Brad", user_data="Brad's data", time_stamp=datetime.now())
session.add(user)
```

You can add more records to the database using the same method: create a *Userdata* instance and add it to the *session* object.

```
user = Userdata(user_id="Larry", user_data="Data for Larry", time_stamp=datetime.now())
session.add(user)
user = Userdata(user_id="Jane", user_data="More data", time_stamp=datetime.now())
session.add(user)
```

If you look at the *SQLite Viewer Web App*, you see that the *userdata* table is still empty. We added data to the session but have not yet written it to persistent storage in the database table. However, you can still access the data added to the session in your program before it is written to the persistent database using the SQLAlchemy *select* function. 

To write data to the database, commit the changes:

```python
session.commit()
```

Commit sends one SQL INSERT command for each *Userdata* instance added to the session, followed by a COMMIT command.

> **NOTE:** I don't discuss the The SQLAlchemy session's [*flush()* method](https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit) in this post but you will need to know about it when you create more complex database relationships and transactions. For now, you should know that the *commit()* method runs the *flush()* method before it commits data. And, the *select()* method runs the *flush()* method before it builds a select statement unless you chain the `execution_options(autoflush=False)` method to it.


Look at teh 

The session's [*flush()* method](https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit)

https://docs.sqlalchemy.org/en/20/orm/session_basics.html#flushing
https://docs.sqlalchemy.org/en/20/orm/session_transaction.html

Look at SQL using Notebook

https://www.datacamp.com/tutorial/sql-interface-within-jupyterlab

```
session.commit()
```


See records in database: https://sqliteviewer.app/



Read function

```python
from sqlalchemy import select
stmt = select(Userdata).where(Userdata.user_id == id)
results = session.execute(stmt).scalar()
print(results)
```
```
<__main__.Userdata object at 0x000001F27489AFD0>
```
```
print(results.user_id, results.user_data, results.time_stamp)
```
```
Brian data 2023-10-12 19:58:35.491346
```




https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete

how to update a row using ORM instead of "query" class
https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-update-and-delete-with-custom-where-criteria

query class is deprecated
https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
"In the SQLAlchemy 2.x series, SQL SELECT statements for the ORM are constructed using the same select() construct as is used in Core, which is then invoked in terms of a Session using the Session.execute() method (as are the update() and delete() constructs now used for the ORM-Enabled INSERT, UPDATE, and DELETE statements feature). However, the legacy Query object, which performs these same steps as more of an “all-in-one” object, continues to remain available as a thin facade over this new system, to support applications that were built on the 1.x series without the need for wholesale replacement of all queries. For reference on this object, see the section Legacy Query API."
also see: https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#legacy-query-api

Update function

```python
def db_update(session, id, data):
    stmt = (update(Userdata)
            .where(Userdata.user_id == id)
            .values(user_data=data, time_stamp = datetime.now()))
    session.execute(stmt)
```

Delete function

```python
def db_delete(session, id):
    if db_id_exists(session, id):
        stmt = delete(Userdata).where(Userdata.user_id == id)
        session.execute(stmt)
    else:
        print(f"The user '{id}' does not exist.")
```

```
db_write(session, "tom", "this is test data")
db_read(session, "tom")
db_write(session, "jane", "more data")
db_read(session, "all")
db_update(session, "tom", "updated information")
db_read(session, "all")
db_delete(session, "jane")
db_read(session, "all")
```



After selecting and printing row objects, propose adding a new *__repr__* function to the class"

```python
class Userdata(Base):
    __tablename__ = "userdata"
    __table_args__ = {'extend_existing': True}
    user_id = mapped_column(String(32), primary_key=True, nullable=False)
    user_data = mapped_column(UnicodeText)
    time_stamp = mapped_column(DateTime(timezone=True))
    def __repr__(self):
        return f"user_id={self.user_id}, " \
               f"user_data={self.user_data}, " \
               f"time_stamp={self.time_stamp.strftime('%B %d %H:%M')}"
```

```python
stmt = select(Userdata).where(Userdata.user_id == "Brian")
results = session.execute(stmt).scalar()
print(results)
```
```
user_id=Brian, user_data=changed, time_stamp=October 12 19:58
```
```python
type(results)
```
```
<class '__main__.Userdata'>
```
```python
print(results.user_id)
```
```
Brian
```













Set up the database connection in the *connection.py* module:

**Explain why I use sessionmaker**

used sessionmaker to get automatic connection management
https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
use session.begin method

from:  https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
"When you write your application, the sessionmaker factory should be scoped the same as the Engine object created by create_engine(), which is typically at module-level or global scope. As these objects are both factories, they can be used by any number of functions and threads simultaneously."
where?
https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it


```python
# dbapp/database/connect.py
 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbapp import config


engine = create_engine(config.database_url)
Session = sessionmaker(engine)


if __name__ == "__main__":
    print(engine)
    with Session() as session:
        connection = session.connection()
        print(connection)
```



I used to have `server_default=func.now()` in the *time_stamp* column so that the [SQL server would create the datetime entry](https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime) when a new row was added but I chose to calculate datetime in my program because it is simpler to update the timestamp in an existing row. Another solution involves [creating a trigger](https://stackoverflow.com/questions/22594567/sql-server-on-update-set-current-timestamp) in the SQL database but, again, I thought it was better to run this logic in the Python program.


