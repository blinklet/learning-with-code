title: A command-line utility that updates a database
slug: sqlalchemy-database-cli-program
summary: How to use Python and the SQLAlchemy ORM to create a table in a database, write data to it, and read it back.
date: 2023-10-25
modified: 2023-10-25
category: Python
<!--status: Published-->

I created a simple command-line-interface utilty that modifies data in a database. It can add, update, or delete data. I created the program to practice working with databases in Python programs. While doing this I also learned how to use Python libraries to build CLI programs.

My goals were to:

* Write a "real program" using the [packaging concepts I learned]({filename}/articles/022-modern-packaging/modern-packaging.md) over the past few months
* Excercise more relational database concepts, like relationships between tables
* Learn to manage SQLAlchemy sessions in different types of programs
* Learn one of the Python CLI libraries

This post assumes the reader is familiar with SQLAlchemy basics. If you are new to the topic of SQLAlchemy, I suggest you review some of my previous posts about the [basic features of SQLAlchemy]({filename}/articles/016-sqlalchemy-read-database/sqalchemy-read-database.md), how [SQLAlchemy represents data]({filename}/articles/019-inspect-database-schema-sqlalchemy/inspect-database-schema-sqlalchemy.md) in a Python program, and how to [declare SQLAlchemy ORM mapped classes]({filename}/articles/023-simple-db-write/simple-database-write.md).

## Project files and folders

First, I created a project folder that contains the project's metadata, the program source code, test code, and documentation. A good project structure supports packaging the program for distribution and makes testing the program more realistic.

I created the project directory structure shown below:

```text
dbproject/
   ├── .gitignore
   ├── requirements.txt
   ├── README.md
   ├── LICENCE.txt
   ├── src
   │   └── dbapp/
   │       ├── database/
   │       │   ├── connect.py
   │       │   ├── functions.py
   │       │   ├── models.py
   │       │   └── __init__.py
   │       ├── interface/
   │       │   ├── cli.py
   │       │   ├── functions.py
   │       │   └── __init__.py
   │       ├── config.py
   │       ├── .env
   │       ├── __init__.py
   │       └── __main__.py
   ├── docs/
   │   └── dotenv_example.txt
   └── tests/
       └── test.py
```

### The project folder

Everything is in a directory named *dbproject*. I could have chosen any name for the project directory because the actual name used to run the program is set in the program's package sub-directory, not the project directory. 

When using source control, I prefer the project directory name to be the same as the source control remote repository name. If I were to publish this on [GitHub](https://github.com/blinklet), I would call the repository "dbproject". 

The project metadata is in the root level of the *dbproject* directory. I created all the files necessary for packaging, which includes a *README.md* file, a license file, Git files (if using source control), and a *requirements.txt* file[^2]. I organized the rest of the project into three sub-directories named *src*, *docs*, and *tests*. 

[^2]: I do not intend to publish this package to the Python Package Index so I do not need a *pyproject.toml* file.

### The *docs* directory

The *docs* directory contains a *dotenv_example.txt* file because the real [*dotenv* file]({filename}/articles/011-use-environment-variables/use-environment-variables.md) must be excluded from source control, using the *.gitignore* file, so I like to document an example for anyone who clones one of my projects from [GitHub](https://github.com/blinklet).

### The *tests* directory

The *tests* directory contains one program named *test.py*. I am not proficient in writing real tests yet so it is just a simple script. In the future, I will write more complex test modules and store them in this directory.

### The *src* directory

The *src* directory contains the program's source code. Using a directory like *src* instead of just starting with the application package directory is [recommended](https://packaging.python.org/en/latest/tutorials/packaging-projects/) by the [Python Packaging Authority](https://www.pypa.io/en/latest/) and others[^1]. 

[^1]: See also the following blog posts: *[Packaging a python library](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)*, and *[Testing & Packaging](https://hynek.me/articles/testing-packaging/)*

#### The *dbapp* package

The program I wrote is called *dbapp*. So, I organized the application source code in the *src* directory in a package directory named *dbapp*. The *dbapp* package contains the following:

* A file named *\_\_init\_\_.py*. The presence of this file tells Python that its directory is a [package directory](https://docs.python.org/3/tutorial/modules.html#packages) and is to be treated as a [regular Python package](https://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html). It is often left blank but any code in it will run when a Python module imports the package.
* A file named *\_\_main\_\_.py*, which is the [program entry point](https://docs.python.org/3/library/__main__.html#main-py-in-python-packages). Python [automatically runs](https://realpython.com/pypi-publish-python-package/#call-the-reader) *\_\_main\_\_.py* when a user runs the `python -m dbapp` command while in the *dbproject/src* directory.
* A configuration module named *config.py*
* A dotenv file named *.env* for [safely storing]({filename}/articles/011-use-environment-variables/use-environment-variables.md) sensitive database connection strings and other secrets. It must be excluded from source control.
* Two sub-packages named *database* and *interface*, that contain the program's other modules

#### The *database* sub-package

The *database* sub-package contains four modules:

* *\_\_init\_\_.py*, which is blank
* *connect.py* sets up the database connection
* *models.py* contains the SQLAlchemy code that defines the database. An abstract representation of a database table is called a [model](https://en.wikipedia.org/wiki/Database_model) so many developers call the module that contains database table classes *models.py*.
* *functions.py* creates functions that read, write, and delete database information

#### The *interface* sub-package

The *interface* sub-package contains three modules:

* *\_\_init\_\_.py*, which is blank
* *cli.py* runs the program's command-line interface
* *functions.py* creates functions that support interacting with the user

## Set up the environment

Before I started writing code, I set up my programming environment. I created a Python virtual environment so I could install the dependencies and test my code. I also created a database server so I could test my database code.

### Python virtual environment

As usual, I created a Python virtual environment and activated it:

```
$ mkdir dbproject
$ cd dbproject
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ 
```

### Install dependencies

In the *requirements.txt* file, I recorded the libraries that need to be installed so my program will work: 

```python
# dbproject/requirements.txt
SQLAlchemy 
psycopg2
python-dotenv
```

Then, I used the *requirements.txt* file to install the project dependencies.

```
(.venv) $ pip install -r requirements.txt
```

### Define database variables

I set up a PostgreSQL database server so I could test my program. In production, a database administrator would usually assign a database server and provide to a developer its userid and password. During development, I created my own local server so I am in control of its configuration.

I decided that my database information would be as follows:

* Database name = userdata
* Admin user = userdata
* Admin password = abcd1234
* TCP port: 5432

Since the database server will run on a Docker container on my local machine, its connection information will be:

* Server address: localhost

#### Create the dotenv file

I created a dotenv file named *.env* that was used to load these configurations into variables in the *config.py* module. Some of these variables will also be used by the Docker *run* command[^3] when I create my database container.

I created the file in the *src/dbapp* directory (the current working directory is *dbproject*). 

```bash
(.venv) $ mkir -p src/dbapp
(.venv) $ cd src/dbapp
(.venv) $ nano .env 
```

I entered the following variables in the file and then saved it:

```python
# dbproject/src/dbapp/.env
DB_SERVER_ADDRESS=localhost
DB_SERVER_TCP_PORT=5432
POSTGRES_DB=userdata
POSTGRES_USER=userdata
POSTGRES_PASSWORD=abcd1234
```

[^3]: Alternatively, one can export environment variables from the dotenv file to the shell environment. Then, set each of the container's environment variables using the shell variables. I that case, I would [load the environment variables in my dotenv file into my Bash shell](https://andrew.red/posts/how-to-load-dotenv-file-from-shell), then run my Docker command. I could have used the Bash shell's [*set* builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) to temporarily modify my Bash shell so each variable sourced from the dotenv file is given the export attribute and marked for export to the shell environment. Then, I would run the command: `set -a; source .env; set +a`


### Create the database server

I used Docker to create a new database container called *ps_userdata*. I started a [container running *PostgreSQL*]({filename}/articles/018-postgresql-docker/postgresql-docker.md) using the official PostgreSQL docker image from Docker Hub.

I ran the following command to start the server (the current working directory is *dbproject/src/dbapp*):

```bash
(.venv) $ docker run \
    --detach \
    --env-file ./.env \
    --publish 5432:5432 \
    --name postgres_db\
    postgres:alpine
```

I tested that the server was running by logging into it:

```bash
(.venv) $ docker exec -it postgres_db psql \
    --username userdata \
    --dbname userdata \
    --password
```

After entering the password, I saw the *psql* prompt and checked that the database was empty. Then, I quit the *psql* application:

```text
userdata=# \d
Did not find any relations.
userdata=# quit
(.venv) $
```

### Ready to start

Now the development environment is ready. I have a Python virtual environment with my dependencies installed, and a database server ready to use. I also have a dotenv file from which my Python configuration module can can get the database connection information.

## Program configuration

It is good practice to place all configuration code in one module (or, if multiple configurations are needed, then place them all in one package)[^5] and then import information from that module when needed. 

There are [multiple ways](https://climbtheladder.com/10-python-config-file-best-practices/) to store configuration settings. I am using one of the simpler schemes.

[^5]: From StackOverflow [answer #49643793](https://stackoverflow.com/questions/49643793/what-is-the-best-method-for-setting-up-a-config-file-in-python): "What is the best method for setting up a config file in Python?"

### The configuration file

I created a module called *config.py* in the *dbapp* package directory. It builds the database configuration string from environment variables that are expected to be configured on the system where the application is installed, or made available in a *dotenv* file in the package directory.

```python
# dbproject/src/dbapp/config.py
import os

from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()  # get environment variables from system or from dotenv file

_database_server = os.getenv('DB_SERVER_ADDRESS')
_database_port = os.getenv('DB_SERVER_TCP_PORT')
_database_name = os.getenv('POSTGRES_DB')
_database_userid = os.getenv('POSTGRES_USER')
_database_password = os.getenv('POSTGRES_PASSWORD')

database_url = URL.create(
    drivername='postgresql+psycopg2',
    username=_database_userid,
    password=_database_password,
    host=_database_server,
    port=_database_port,
    database=_database_name
    )

if __name__ == "__main__":
    print(f"Database URL = {database_url}")
```

To test the module, run it as a module:

```bash
(.venv) $ python -m config
Database URL = postgresql+psycopg2://userdata:***@localhost:5432/userdata
```

## Database code

Before I write the *\_\_main\_\_.py* module in the *dbapp* package, I will write all the program modules and test them one by one. Then, I will write the *\_\_main\_\_.py* module, which will simply import and run the other modules.

First, I will write the modules that interface with the database.

### Database sub-package

I created the *database* sub-package with the following shell commands:

```bash
(.venv) $ mkdir database
(.venv) $ cd database
(.venv) $ touch __init__.py
```

Then, I created the database modules, *connect.py*, *models.py*, and *functions.py*.

### Database connection module

I set up the database connection in the *connect.py* module, as shown below.

```python
# dbproject/src/dbapp/database/connect.py
 
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

The module defines the *engine* object and creates the [*Session* object](https://docs.sqlalchemy.org/en/20/orm/session_basics.html) that will be used in the other modules.

I chose to use SQLAlchemy's [*sessionmaker()*](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker) function so that the Session object created would include automatic [connection management](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html) when other modules use it as a context manager. Based on the recommendations for CLI apps in the SQLAlchemy documentation, I will import the Session object into the *dpapp* package's \_\_main\_\_.py* module so [it has a global scope](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it)

To test the module, I ran it as a module. Because the *connect.py* module imports the *config.py* module from the *dbapp* package, I needed to run this module from the *dbproject/src* directory:

```bash
(.venv) $ cd ../..
(.venv) $ 

```

The [*session.connection()* function](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) in the test code forces the session to start a transaction, which makes it try to immediately connect to the database. If the SQLAlchemy session failed to connect to the database, it would have raised an exception. The output shown below shows that the database connection was successful.

```
Engine(postgresql+psycopg2://userdata:***@localhost:5432/userdata)
<sqlalchemy.engine.base.Connection object at 0x7fd4c9015f00>
```

Then, I went back to the *database* sub-package directory.

```bash
(.venv) $ cd dbapp/database
```

## Create database models

I defined the code that defines the database tables. These code abstractions are usually called [models](https://en.wikipedia.org/wiki/Database_model). In the *models.py* module, I created three tables that have relationships between them:

* The *users* table contains user information. Each user may have many data items so this table has a *one to many* relationship with the *data* table.
* The *data* table contains data for each user. Each data item is associated with only one user and each user may have more than one data item in the table. Each data item has a label that identifies its type or purpose.
* The *labels* table contains valid data label names. Each data label may be associated with many data entries so this forms a *one to many* relationship with the *data* table.

I found it was very helpful to create a diagram of the tables that shows the columns and relationships. I used the database modeling web application at [https://dbdiagram.io/](https://dbdiagram.io/) to create the diagram, below:

![*userdata* database diagram]({attach}dbproject-light.png)

### The declarative base

I used the SQLAlchemy [declarative mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping) method to define the tables and [relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html).

I walk through each section of the *models.py* module, in order, below.

First, I imported the necessary SQLAlchemy classes and functions and created the *Base* class that support the declarative mapping of database tables to classes.

```python
# dbproject/src/dbapp/database/models.py

from sqlalchemy import Integer, String, UnicodeText, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship


class Base(DeclarativeBase):
    pass
```

### The *data* table

I created an ORM mapped class named *Data* that describes the *data* table. It has five columns:

* The *data_id* column uniquely identifies the data item and serves as the *data* table's primary key.
* The *user_id* column identifies the user associated with this data and has a foreign key relationship with the *id* column in the *users* table. It creates a [one-to-many relationship](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many)) with the *user* table.
* The *label_id* column identifies the label associated with this data has a foreign key relationship with the *id* column in the *labels* table. It creates a [one-to-many relationship](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many)) with the *labels* table. It also sets it *nullable* attribute to *False* so the dabase server will not allow the field to have the value *None*. Effectively, this [prevents data being deleted](https://stackoverflow.com/questions/42978090/prevent-deletion-of-parent-row-if-its-child-will-be-orphaned-in-sqlalchemy) if a label is deleted from the *labels* table while any data in the *data* table still uses that label.
* The *data* column contains the user's data. In this simple example, it will be a unicode text field that may contain any size of unicode data. It could be any readable text, from a short message to a novel.
* The *time_stamp* column shows when the data was created or when it was last updated. This column [runs an SQL function](https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime) on the database server to generate the time stamps.

```python
class Data(Base):
    __tablename__ = "data"
    # columns
    id = mapped_column(Integer, primary_key=True, nullable=False)
    user_id = mapped_column(ForeignKey("users.user_id"))
    label_id = mapped_column(ForeignKey("labels.label_id"), nullable=False) # nullable=False prevents label deletion if any labels in use
    data = mapped_column(UnicodeText)
    time_stamp = mapped_column(DateTime(), default=func.now(), onupdate=func.now())
```

### The *users* table

The *users* table has three columns and a relationship:

  * The *id* column that will serve as its primary key. Each User ID will be an integer.
  * The *name* column contains a string meant to contain a user's name.
  * The *info* column contains a user's information. It is here just as a demonstration and is not critical to the program. In a more realistic scenario, I can imagine that a *users* table might contain many columns that describe the different attributes of each user.
  * The *user_data* relationship has two purposes:
    * It provides access to user data in the *data* table from the *Users* class
    * It tells SQLAlchemy to cascade delete operations to all rows in the *data* table when a user is deleted from the *user* table. When a user is deleted, SQLAlchemy (and the database server) will automatically delete all the user's data records. So, I do not need to write that logic into my program.

```python
class Users(Base):
    __tablename__ = "users"
    # columns
    id = mapped_column(Integer, primary_key=True, nullable=False)
    name = mapped_column(String(64))
    info = mapped_column(UnicodeText)
    # relationships
    user_data = relationship("Data", cascade="all, delete, delete-orphan") 
```

### The *labels* table

The *labels* table has two columns and a relationship:

* The *id* column identifies the label and is the table's primary key
* The *label* column is the name of the label.
* The *labeled_data* relationship has two purposes, similar to the *user_data* relationship in the *users* table described above, but with one difference:
  * It provides access to the rows in the *data* table that have a *label_id* that is the same as the *id* in the *labels* table.
  * It tells SQLAlchemy to cascade delete operations to all rows in the *data* table when a label is deleted from the *labels* table. However, because I previously defines the *label_id* column in the *labels* table to be non-nullable, SQLAlchemy will raise an exception if I try to delete a label that is still in use in the *data* table. This will prevent unintentional deletion of data.

```python
class Labels(Base):
    __tablename__ = "labels"
    # columns
    id = mapped_column(Integer, primary_key=True, nullable=False)
    label = mapped_column(String(32))
    # relationships
    labeled_data = relationship("Data", cascade="all, delete") 
```

### Test code

The test code, which runs when this module is executed as a script, simply tries to create the database using the *Base* object's metadata that was created by each ORM mapped class in the *models.py* file. It will echo the SQL commands generated by SQLAlchemy onto the terminal screen.

If I had made any syntax errors in the table definitions of relationships, or declared something that SQLAlchemy does not allow, the test code will raise an exception.

```python
if __name__ == "__main__":
    from dbapp.database.connect import engine
    engine.echo = True
    Base.metadata.create_all(engine)
```

### The *models.py* file, complete

After entering all the above code into the *models.py* module, I saved the file. 

I ran the module from the *dbroject/src* directory to see if any errors were raised. It appeared that all worked correctly.

```bash
(.venv) $ cd ../..
(.venv) $ python -m dbapp.database.models
```

There was a lot of output I did understand, but the section I could read showed that the tables were being created:

```sql
CREATE TABLE users (
        id SERIAL NOT NULL, 
        name VARCHAR(64), 
        PRIMARY KEY (id)
)

CREATE TABLE labels (
        id SERIAL NOT NULL, 
        label VARCHAR(32), 
        PRIMARY KEY (id)
)

CREATE TABLE data (
        id SERIAL NOT NULL, 
        user_id INTEGER, 
        label_id INTEGER NOT NULL, 
        data TEXT, 
        time_stamp TIMESTAMP WITHOUT TIME ZONE, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES users (id), 
        FOREIGN KEY(label_id) REFERENCES labels (id)
)
```



## Create database functions

I decided to create a module that contains all the functions that operate on the database. My plan was to abstract away the details of adding data to a database session, selecting data from the database, updating data, and deleting data.

All these functions will interact with the SQLAchemy ORM session. So, I needed to decide where in the program should I create the session, or if I should create multiple sessions. The SQLAlchemy ORM documentation [recommends that CLI utilities create one session for the entire program](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it), and import it into any other modules that use it. So, the functions in the *database/functions.py* module will accept the *session* object as a parameter and the module in which they are used will import the *session* object from the *\_\_main\_\_.py* module in the *dbapp* package directory.

I create the *functions.py* module in the *dbproject/scr/dbapp/database* directory:

```bash
(.venv) $ cd dbapp/database
(.venv) $ nano modules.py
```

First, I imported the functions I need from the Python standard library and from SQLAlchemy. Then, I imported the database models I created in *models.py*.

```python
# dbproject/src/dbapp/database/functions.py

from datetime import datetime

from sqlalchemy import select, update, delete

from dbapp.database.models import Data, Users, Labels
```

The *bd_write* function creates user data in the database. If the user does not already exist in the *users* table, the function will add the user name in the *users* table and then add the data in the *data* table. The same happens for the label: if the label does not already exist in the *labels* table, the function adds it there before adding the data.

```python
def db_write(session, id, data):
    userdata = User(
        user_id = id,
        user_data = data,
        time_stamp = datetime.now()
    )
    session.add(userdata)
```

Read function

```python
def db_id_exists(session, id):
    stmt = (select(Userdata.user_id).where(Userdata.user_id == id))
    result = session.scalar(stmt)
    if result == None:
        return False
    else:
        return result
```
```python
def db_read(session, id):
    if id == "all":
        stmt = select(Userdata)
    else:
        stmt = select(Userdata).where(Userdata.user_id == id)
    results = session.execute(stmt)
    return results
```

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

Save the *functions.py* module.


























## The user interface

```python
# dbapp/interface/cli.py

import argparse

from dbapp.interface.functions import read, write, update, delete

def main(session):

    parser = argparse.ArgumentParser(description="Database Application")
    subparsers = parser.add_subparsers(title='subcommands', dest='subparser_name')

    read_parser = subparsers.add_parser('read')
    read_parser.add_argument('user_id_list', nargs='+')

    write_parser = subparsers.add_parser('write')
    write_parser.add_argument('user_id')
    write_parser.add_argument('user_data')

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('user_id')
    update_parser.add_argument('user_data')

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('user_id_list', nargs='+')

    args = parser.parse_args()

    match args.subparser_name:
        case 'read': 
            read(session, args.user_id_list)
        case'write': 
            write(session, args.user_id, args.user_data)
        case'update': 
            update(session, args.user_id, args.user_data)
        case'delete': 
            delete(session, args.user_id_list)
        case None:
            parser.print_help()
```

Save the *cli.py* module.


## The *\_\_main\_\_.py* program

So that the package runs 

```python
from dbapp.interface import cli
from dbapp.database.models import db_setup
from dbapp.database.connect import Session

db_setup()

with Session.begin() as session:
    session.expire_on_commit = False
    cli.main(session)
```



Why use just one session? https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-frequently-asked-questions


Save the *\_\_main\_\_.py* program.

Test

```bash
(.venv) $ cd project/src
(.venv) $ python -m dbapp write user1 "test data 1"
(.venv) $ python -m dbapp write user2 "more test data"
(.venv) $ python -m dbapp read all
```

The output is:

```
ID = user1       DATA = test data 1           TIME = October 09 22:21
ID = user2       DATA = more test data        TIME = October 09 22:22
```








Python package structure recommendation

https://docs.python-guide.org/writing/structure/
https://kennethreitz.org/essays/2013/01/27/repository-structure-and-python

Good post on importing
import submodules in \_\_init\_\_.py to make them importable from other packages (See Numpy example in:)
https://note.nkmk.me/en/python-import-usage/#packages

another good post on importing
https://fortierq.github.io/python-import
sys.path seems a clunky solution... may be useful when writing tests, though
relative paths
do you intend to build/install or run as script?

see also
https://blog.finxter.com/python-how-to-import-modules-from-another-folder/
https://ioflood.com/blog/python-import-from-another-directory/

"namespace packages" are the new tech, but may create confusion and seem best for advanced cases where sub-packages are distributed across different directories in teh filesystem and will be "re assembled" at run time

https://peps.python.org/pep-0420/

with relative imports and packages with blank \_\_init\_\_.py files, "python -m dbapp" works but "python dbapp/\_\_main\_\_.py" fails due to " ImportError: attempted relative import with no known parent package "


From chatgpt:

Whether you should use namespace packages or regular packages in your Python project depends on your project's specific requirements and goals. Both namespace packages and regular packages have their use cases, and understanding the differences between them can help you make an informed decision.

1. Regular Packages:
   - Regular packages are the most common type of packages in Python.
   - They are used when you want to organize your code into hierarchical directories and create a clear package structure.
   - Regular packages are self-contained and can include modules (Python files) and sub-packages (nested directories with an `__init__.py` file).
   - They provide strong encapsulation, meaning that each regular package is its own namespace, and names within the package do not collide with names in other packages.

   Example:
   ```
   mypackage/
       __init__.py
       module1.py
       module2.py
       subpackage/
           __init__.py
           module3.py
   ```

2. Namespace Packages:
   - Namespace packages are used when you want to split a package across multiple directories or when you want to extend an existing package without modifying its source code.
   - They are more suitable for scenarios where you have multiple packages that share a common namespace and you want to merge them dynamically.
   - Namespace packages do not contain any actual code or `__init__.py` files. They are created by declaring a shared namespace in one or more distribution packages.
   - Names within a namespace package can be spread across multiple locations, and they are merged at runtime.

   Example (project structure with namespace packages):
   ```
   mynamespacepackage/
       subpackage1/
           module1.py
       subpackage2/
           module2.py
   ```

In summary, if you are building a self-contained package with a clear structure and want strong encapsulation, regular packages are a good choice. On the other hand, if you need to extend or split a package dynamically across multiple directories or collaborate on a shared namespace with other packages, namespace packages might be more appropriate.

Consider your project's specific needs and whether you anticipate collaborating with other packages or distributing your code as part of a larger ecosystem when deciding whether to use regular packages or namespace packages.



# Python scripts

* Modules in one directory; no sub-directories
* No \_\_init\_\_.py file
* One file contains the main logic, other modules contain functions

```
project1
├── functions.py
└── program.py
```

functions.py:

```
def func1(message)
    return message + " by func1"
```

program.py

```
import functions

def main():
    print(functions.func1("test"))

if __name__ == "__main__":
    main()
```

Run from project directory:

```
$ cd project1
$ python3 -m program
test by func1
```

```
$ python3 program.py
test by func1
```

Run from another directory

```
$ cd ..
$ python3 -m project1.program
Traceback (most recent call last):
...
  File "/home/brian/Projects/learning/python/imports/project1/program.py", line 1, in <module>
    import functions
ModuleNotFoundError: No module named 'functions'
```

```
$ python3 project1/program.py
test by func1
```

## Python package (normal)

Add an empty file named *\_\_init\_\_.py* and the project directory becomes a *package*. Changes the way imports work. Now you need "relative" or "absolute" imports.

```
project2
├── functions.py
├── __init__.py
└── program.py
```

```
$ cd project2
$ python3 -m program.py
test by func1
```
```
$ python3 program.py
test by func1
```
```
$ cd ..
$ python3 -m project2.program
Traceback (most recent call last):
...
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    import functions
ModuleNotFoundError: No module named 'functions'
```
```
$ python3 project2/program.py
test by func1
```

Seems to work the same as normal script modules.

### Relative imports

To make the case of `python3 -m project2.program` work, you need to use relative imports. *\_\_init\_\_.py* tells python that relative imports are allowed. Also the `python -m` flag tells Python that relative imports are allowed. Relative imports will not wotk when running as a script with `python program.py`

Change *program.py* to:

```
from . import functions

def main():
    print(functions.func1("test"))

if __name__ == "__main__":
    main()
```

The import line was changed to `from . import functions`.

Now, the following works:

```
$ python3 -m project2.program
test by func1
```

The directory *project2* is now a *package* and Python searches for modules starting from the directory containing the *project* package directory, not from the *project2* directory, itself.
???

But the program can no longer be run as a Python script. It must be run as a module with the `-m` flag and it must be run as a package: identified as `project2`:

```
$ python3 project2/program.py
Traceback (most recent call last):
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    from . import functions
ImportError: attempted relative import with no known parent package
```
```
$ cd project2
$ python3 program.py
Traceback (most recent call last):
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    from . import functions
ImportError: attempted relative import with no known parent package
```
```
$ python3 -m program
Traceback (most recent call last):
  File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    from . import functions
ImportError: attempted relative import with no known parent package
```

## Namespace package

You need to keep in mind how you will distribute the program. If you intend to "package" it using something like *setuptools*, then you may need to be careful about the metatdata you generate for the packaging process.
adding some code to the \_\_init\_\_.py file to initialize the Python search path to include the package directory

*\_\_init\_\_.py* would contain:

```
from pathlib import Path
import  sys

print(Path(__file__).parents[0])
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))
print(sys.path)
```

Now all types of launches run 

```
$ cd project2
$ python3 -m program.py
test by func1
```
```
$ python3 program.py
test by func1
```
```
$ cd ..
$ python -m project2.program
C:\Users\blinklet\Documents\learning\python\imports\project2
test by func1
```

**(Note, the above call to the *project2.program* module caused the */_/_init.py/_/_* code to ruin. None of the other launches started the init file.)**

```
$ python3 project2/program.py
test by func1
```

So, that's one way to make package module imports work for all cases






Running a Python program using "python x.py" and "python -m x" can yield different results because they use different ways to execute Python code and have different implications for how modules and packages are treated. Here's an explanation of the differences:

1. "python x.py":
   - When you run "python x.py," you are executing the Python script "x.py" directly as a standalone script.
   - The Python interpreter treats "x.py" as the main program and starts executing code from the top of the file.
   - Any code within "x.py" that is not encapsulated in functions or classes will be executed immediately when you run the script.
   - This method is suitable for standalone scripts and simple programs.

2. "python -m x":
   - When you run "python -m x," you are telling Python to run the module named "x" as a script.
   - In this case, "x" should be a Python package or a module that can be imported.
   - Python will search for the "x" module/package in its module search path, including the current directory.
   - It treats "x" as a package or module and executes the code in the "\_\_main\_\_.py" file inside the "x" package (if it exists), or it runs the module "x" directly if there is no "\_\_main\_\_.py" file.
   - This method is often used for running packages or modules within a larger Python project.

Key Differences:
- The "python -m x" method is typically used for structured Python projects where you want to utilize packages and modules, while "python x.py" is often used for standalone scripts.
- Using "python -m x" allows you to avoid issues related to naming conflicts with other scripts or modules in the same directory or on the Python path.
- When using "python -m x," the "\_\_name\_\_" attribute of the script/module will be "\_\_main\_\_," just like when running a standalone script, so you can still use conditional logic based on "\_\_name\_\_" to control script behavior.

In summary, the choice between "python x.py" and "python -m x" depends on the structure and purpose of your Python code. If it's a simple standalone script, "python x.py" is sufficient. If you're working with modules and packages in a more complex project, "python -m x" is a better choice for running your code as a module.







The error message you're encountering, "ImportError: attempted relative import with no known parent package," is related to the way you are running your Python script and the use of relative imports.

In Python, relative imports are used within packages (directories containing an `__init__.py` file) to reference other modules or sub-packages within the same package. However, when you run a script directly with "python3 .\dbapp\interface\cli.py," Python treats it as a standalone script, not as part of a package, which is why relative imports fail.

To resolve this issue, you have a few options:

1. Run the script as a module with the `-m` flag:

   ```
   python3 -m dbapp.interface.cli
   ```

   This method treats the script as a module within the `dbapp` package and allows you to use relative imports correctly.

2. Change your project structure:

   If you intend to use relative imports within your script, consider organizing your project structure as a package. To do this:

   - Ensure that the top-level directory (`dbproject` in your case) contains an `__init__.py` file. This makes it a Python package.
   - Move your script (`cli.py`) to the appropriate location within the package. For example, if `dbapp` is your package and `cli.py` is a module within it, your directory structure might look like this:

     ```
     dbproject/
     ├── dbapp/
     │   ├── __init__.py
     │   ├── interface/
     │   │   ├── __init__.py
     │   │   └── cli.py
     ├── ...
     ```

   With this structure, you can run your script as a module with relative imports:

   ```
   python3 -m dbapp.interface.cli
   ```

3. Use absolute imports:

   Instead of relying on relative imports, you can use absolute imports by specifying the full path to the module you want to import. For example:

   ```python
   from dbapp.interface import db
   ```

   This approach works both when running the script as a standalone file and when using it as a module.

Choose the approach that best fits your project structure and requirements. If you intend to work with packages and modules within your project, I recommend organizing your project as a package to leverage the benefits of relative imports and better code organization.



References??

Certainly! Here are some reference links that provide more information on the topics discussed:

1. **Python Official Documentation**:
   - [Python Modules](https://docs.python.org/3/tutorial/modules.html)
   - [Packages](https://docs.python.org/3/tutorial/modules.html#packages)
   - [Command line and environment](https://docs.python.org/3/using/cmdline.html)

2. **PEP 328 - Imports: Multi-Line and Absolute/Relative**:
   - [PEP 328](https://www.python.org/dev/peps/pep-0328/) explains the rationale behind relative imports and their usage.

3. **Python Module vs. Script**:
   - [Python Module vs. Script](https://realpython.com/run-python-scripts/) - An article explaining the differences between running Python modules and scripts.

4. **Structuring Your Project**:
   - [Structuring Your Project](https://docs.python-guide.org/writing/structure/) - A guide on structuring Python projects, including the use of packages and modules.

5. **Absolute vs. Relative Imports in Python**:
   - [Absolute vs. Relative Imports in Python](https://realpython.com/absolute-vs-relative-python-imports/) - A Real Python article that delves into the details of absolute and relative imports in Python.

6. **Python's -m Switch**:
   - [Python's -m Switch](https://docs.python.org/3/using/cmdline.html#cmdoption-m) - Python documentation on the `-m` switch for running modules as scripts.

These resources should provide you with a deeper understanding of Python modules, packages, and the differences between running scripts and modules, as well as how to handle imports effectively.




Example: in *dbproject/dbapp/dbsetup/models.py*
    Change:
        from dbapp.dbsetup import database
    To:
        from . import database


