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

I used the following shell commands to create the *database* sub-package:

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

The module defines the *engine* object and creates the [*Session* object](https://docs.sqlalchemy.org/en/20/orm/session_basics.html) that will be used in the other modules to create database sessions.

I chose to use SQLAlchemy's [*sessionmaker()*](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker) function so that the Session object created would include automatic [connection management](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html) when other modules use it as a context manager.

To test the module, I ran it as a module. Because the *connect.py* module imports the *config.py* module from the *dbapp* package, I needed to run this module from the *dbproject/src* directory:

```bash
(.venv) $ cd ../..
(.venv) $ python -m dbapp.database.connect
```

The [*session.connection()* function](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) in the test code forces the session to start a transaction, which makes it try to immediately connect to the database. If the SQLAlchemy session failed to connect to the database, it would have raised an exception. The output shown below shows that the database connection was successful.

```
Engine(postgresql+psycopg2://userdata:***@localhost:5432/userdata)
<sqlalchemy.engine.base.Connection object at 0x7fd4c9015f00>
```

Then, I went back to the *database* sub-package directory so I can continue adding modules there.

```bash
(.venv) $ cd dbapp/database
```

## Create database models

To define the database tables, I used ORM mapped classes that are usually called [models](https://en.wikipedia.org/wiki/Database_model). In the *models.py* module, I created three tables that have relationships between them:

* The *users* table contains user information. Each user may have many data items so this table has a *one to many* relationship with the *data* table.
* The *labels* table contains valid data label names. Each data label may be associated with many data entries so this forms a *one to many* relationship with the *data* table.
* The *storage* table contains data for each user and label. Each data item is associated with only one user and each user may have more than one data item in the table. Each data item has a label that identifies its type or purpose.

I found it was very helpful to create a diagram of the tables that shows the columns and relationships. I used the database modeling web application at [https://dbdiagram.io/](https://dbdiagram.io/) to create the diagram, below:

![*userdata* database diagram]({attach}dbproject-light-3.png)

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
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass
```

### The *users* and *labels* tables

In a [star schema](https://en.wikipedia.org/wiki/Star_schema) like the one I am using for this application, tables like the *users* and *labels* tables are called *dimension* tables. They contain details about the characteristics of the data in the *fact* table.

The *users* table has three columns:

  * The *id* column that will serve as its primary key. Each User ID will be an integer.
  * The *name* column contains a string meant to contain a user's name.  It also sets its *nullable* attribute to *False* because the user must have a name and its name cannot have a value of *None* or *NULL*.
  * The *info* column contains a user's information. It is here just as a demonstration and is not critical to the program. In a more realistic scenario, I can imagine that a *users* table might contain many columns that describe the different attributes of each user.

The *Users* class defines the *users* table as shown below:

```python
class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(64), unique=True, nullable=False)
    info = mapped_column(UnicodeText)
```

The *labels* table has two columns:

* The *id* column identifies the label and is the table's primary key
* The *label* column is the name of the label. It also sets its *nullable* attribute to *False* because the label must have a name and cannot have a value of *None* or *NULL*.


```python
class Label(Base):
    __tablename__ = "labels"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(32), unique=True, nullable=False)
```

### The *storage* table

In this schema, the *storage* table acts as the *fact* table. It contains the data we are interested in and refers to the *dimension* tables for additional details. The *storage* table has five columns:

* The *data_id* column uniquely identifies the data item and serves as the *data* table's primary key.
* The *user_id* column identifies the user associated with this data and has a [foreign key relationship](https://en.wikipedia.org/wiki/Foreign_key) with the *id* column in the *users* table. It creates a [one-to-many relationship](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many) with the *user* table. It also sets its *nullable* attribute to *False* because every row must be related to a user via the *user_id*. If I make a mistake in my program that allows a value of *None* in this field, SQLAlchemy will raise an error.
* The *label_id* column identifies the label associated with this data and has a foreign key relationship with the *id* column in the *labels* table. It creates a one-to-many relationship with the *labels* table. It also sets its *nullable* attribute to *False* because every row must be related to a label via the *label_id*.
* The *data_item* column contains the user's data. In this simple example, it will be a unicode text field that may contain any size of unicode data. It could be any readable text, from a short message to a novel.
* The *time_stamp* column shows when the data was created, or when it was last updated. This column [runs an SQL function](https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime) on the database server to generate the time stamps. 

```python
class Storage(Base):
    __tablename__ = "storage"
    # columns
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    label_id = mapped_column(ForeignKey("labels.id"), nullable=False)
    data_item = mapped_column(UnicodeText)
    time_stamp = mapped_column(DateTime(), default=func.now(), onupdate=func.now())
```

### The *db_setup()* function

The *db_setup()* function creates the database if it does not yet exist on the connected database server. If the database already exists, it makes no changes to it, so it is safe to run every time the program runs.

### Test code

The test code, which runs when this module is executed as a script, simply tries to create the database using the *Base* object's metadata that was created by each ORM mapped class in the *models.py* file. It will echo the SQL commands generated by SQLAlchemy onto the terminal screen.

If I had made any syntax errors in the table definitions of relationships, or declared something that SQLAlchemy does not allow, the test code will raise an exception.

```python
if __name__ == "__main__":
    from dbapp.database.connect import engine
    engine.echo = True
    db_setup(engine)
```

The `engine.echo` attribute will print out on the console the SQL commands 

### The *models.py* file, complete

After entering all the above code into the *models.py* module, I saved the file. 

I ran the module from the *dbroject/src* directory to see if any errors were raised. It appeared that all worked correctly.

```bash
(.venv) $ cd ../..
(.venv) $ python -m dbapp.database.models
```

There was a lot of output, that I do not show, caused by the SQL database checking for existing tables and setting up the schema. Then,the database [prints the SQL commands](https://docs.sqlalchemy.org/en/20/core/connections.html) used to create the new tables to the console:

```sql
2023-11-04 23:27:51,160 INFO sqlalchemy.engine.Engine 
CREATE TABLE users (
        id SERIAL NOT NULL, 
        name VARCHAR(64) NOT NULL, 
        info TEXT, 
        PRIMARY KEY (id), 
        UNIQUE (name)
)

2023-11-04 23:27:51,161 INFO sqlalchemy.engine.Engine [no key 0.00054s] {}
2023-11-04 23:27:51,194 INFO sqlalchemy.engine.Engine 
CREATE TABLE labels (
        id SERIAL NOT NULL, 
        name VARCHAR(32) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
)

2023-11-04 23:27:51,194 INFO sqlalchemy.engine.Engine [no key 0.00025s] {}
2023-11-04 23:27:51,206 INFO sqlalchemy.engine.Engine 
CREATE TABLE storage (
        id SERIAL NOT NULL, 
        user_id INTEGER NOT NULL, 
        label_id INTEGER NOT NULL, 
        data_item TEXT, 
        time_stamp TIMESTAMP WITHOUT TIME ZONE, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES users (id), 
        FOREIGN KEY(label_id) REFERENCES labels (id)
)


2023-11-04 23:27:51,206 INFO sqlalchemy.engine.Engine [no key 0.00017s] {}
2023-11-04 23:27:51,220 INFO sqlalchemy.engine.Engine COMMIT
```

## Create database functions

I decided to create a module that contains all the functions that operate on the database. My plan was to import functions from this module when other modules need to add data to a database session, read data from the database, and delete data.

All these functions will interact with the SQLAchemy ORM session. So, at this point, I needed to decide where in the program I should create the database session, or if I should create multiple sessions. 

The SQLAlchemy ORM documentation [recommends that CLI utilities create one session for the entire program](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it), and import it into any other modules that use it. So, the functions in the *database/functions.py* module will accept the *session* object as a parameter and the module in which they are used will import the *session* object from the *\_\_main\_\_.py* module in the *dbapp* package directory.

I create the *functions.py* module in the *dbproject/scr/dbapp/database* directory:

```bash
(.venv) $ cd dbapp/database
(.venv) $ nano modules.py
```

First, I imported the functions I need from the Python standard library and from SQLAlchemy. Then, I imported the database models I created in *models.py*.

```python
# dbproject/src/dbapp/database/functions.py

from sqlalchemy import select, delete, func

from dbapp.database.models import Storage, User, Label
```

### The *data_write()* function

The *data_write* function writes user data to the database. If the user does not already exist in the *users* table, the function will add the user name in the *users* table and then add the data in the *data* table. The same happens for the label: if the label does not already exist in the *labels* table, the function adds it there before adding the data.

```python
def data_write(session, user_name, label_name, data_item):

    # if user exists, get user from database
    user = session.scalar(select(User).where(User.name == user_name))
    # if user does not exist, create new user in database
    if user == None:
        user = User(name=user_name)
        session.add(user)
        session.flush()  # create user.id
    
    # if label exists, get label from database
    label = session.scalar(select(Label).where(Label.name == label_name))
    # if label does not exist, create new label in database
    if label == None:
        label = Label(name=label_name)
        session.add(label)
        session.flush()  # create label.id

    # Add data item
    data = Storage(label_id=label.id, user_id=user.id, data_item=data_item)
    session.add(data) 

    print(f"User '{user.name}' added data labeled '{label.name}'.")
```

In the function's first stanza, I check to see if the contents of the *user_name* parameter matches the name of any user in the *users* table. If so, I get that *User* instance from the database. If not, I create a new *User* instance, which will add a new row to the *users* table when added to the session. In that case, I also [flush the session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing) so that the database will automatically populate the table's *id* column with a valid key and return that key to the session so it can be used later in the function.

In the function's second stanze, I do the same with the *label_name* parameter.

And, finally, I create a *Storage* instance and add it to the session. This will result in a new row in the *storage* table that has the user ID, label ID, and the data. The timestamp column and the storage ID column will get automatically populated by the database when the session is committed.

### The *data_read()* function

The *data_read()* function reads user data from the database. the function needs both a *user_name* and a *Label_name* to find the one or more rows that have the matching user ID and label ID.

If the *user_name* and *label_name* exist in the database, the function selects joins the information in the *users* and *labels* tables with the *storage* table and returns all rows where both the *user_id* and *label_id* columns from the *storage* table matches the user ID and label ID associated with the *user_name* and *label_name*. 

If no results are returned, even though the *user_name* and *label_name* were valid, then that means that the user is not using that label for any of their data. 

The *data_read()* function is shown below:

```python
def data_read(session, user_name, label_name):

    user = session.scalar(select(User).where(User.name == user_name))
    if user == None:
        print(f"User '{user_name}' does not exist.")
        return
    
    label = session.scalar(select(Label).where(Label.name == label_name))
    if label == None:
        print(f"Label '{label_name}' does not exist.")
        return

    stmt = (
        select(Storage.data_item.label("data"), 
            User.name.label("user_name"), 
            Label.name.label("label_name"))
        .join(Label)
        .join(User)
        .where(Label.id==label.id)
        .where(User.id==user.id)
    )
    result = session.execute(stmt).fetchall()
    if len(result) > 0:
        for row in result:
            print(
                f"User: {row.user_name},  "
                f"Label: {row.label_name},  "
                f"Data: {row.data},  "
                f"Time: {row.time_stamp}"
                )
    else:
        print(f"User '{user_name}' does not use label '{label_name}.")
```

#### Why use the *select()* function?

Many SQLAlchemy blog posts and tutorials use the SQLAlchemy ORM's *query()* function to read data from a database. However, since version 2.0 of SQLAlchemy, the *query()* function is considered to be a [legacy tool](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#legacy-query-api). It still works, for now, but has been replaced by a new recommended function: the *select()* function.

I am using the [*select()* function](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html) because it is the recommended way to get data from the SQLAlchemy ORM and I want to focus on using SQLAlchemy in the most "modern" way.

### The *data_delete()* function

The *data_delete()* function deletes user data from the database. After deleting the rows that match both the *user_name* and *label_name*, teh function checks if the label and/or the user are still have data associated with them in the *storage* table. If not, the leftover label or user is deleted from the *labels* or *users* table.

This function uses the new SQLAlchemy ORM *delete()* function to perform a bulk-delete of *storage* table rows that match both the user ID and the label ID.

```python
def data_delete(session, user_name, label_name):

    # Get user record, or quit if user does not exist in "users" table
    user = session.scalar(select(User).where(User.name == user_name))
    if user == None:
        print(f"User '{user_name}' does not exist.")
        return
    
    # Get label record, or quit if label does not exist in "labels" table
    label = session.scalar(select(Label).where(Label.name == label_name))
    if label == None:
        print(f"Label '{label_name}' does not exist.")
        return

    # Check if any records match both the user ID and the label ID
    stmt = (
        select(func.count())
        .select_from(Storage)
        .join(Label)
        .join(User)
        .where(Label.id == label.id)
        .where(User.id == user.id)
    )
    number_matched = session.execute(stmt).scalar()
    if number_matched == 0:
        print(f"User '{user_name}' does not use Label '{label_name}'.")
        return

    # Bulk delete all records that match both the user ID and the label ID
    stmt = (
        delete(Storage)
        .where(Storage.user_id == user.id)
        .where(Storage.label_id == label.id)
    )
    session.execute(stmt)
    print(f"Deleted {number_matched} rows.")

    # If label is no longer used in the "storage" table, 
    # then also delete it from the "labels" table
    stmt = select(Storage.id).where(Storage.label_id == label.id).limit(1)
    label_exists = session.scalar(stmt)
    if label_exists == None:
        session.delete(label)

    # If user is no longer used in the "storage" table, 
    # then also delete them from the "users" table
    stmt = select(Storage.id).where(Storage.user_id == user.id).limit(1)
    user_exists = session.scalar(stmt)
    if user_exists == None:
        session.delete(user)
```

### The *user_read()* function

The *user_read()* function simply lists all user names in the *users* table. 

```python
def user_read(session):
    stmt = (select(User.name))
    user_list = session.scalars(stmt).all()
    for x in user_list:
        print(x)
```

### The *label_read()* function

The *label_read()* function lists all labels used by a particular user. This helps find data items one may want to read, using the *data_read()* function.

```python
def label_read(session, user_name):
    user = session.scalar(select(User).where(User.name == user_name))
    if user == None:
        print(f"User '{user_name}' does not exist!")
    else:
        stmt = (select(Label.name).distinct()
                .join(Storage)
                .join(User)
                .where(User.id == user.id)
        )
        label_list = session.scalars(stmt).all()
        for x in label_list:
            print(x)
```

### The test code

At the end of the *functions.py* module, I created some test code which will create an empty database, then add, read, and delete information.

```python
if __name__ == "__main__":

    from dbapp.database.connect import Session
    from dbapp.database.connect import engine
    from dbapp.database.models import Base
    from sqlalchemy import select

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    data_write(session, user_name="Bill",label_name="Notes",data_item="makes some notes")
    data_write(session, user_name="Jane",label_name="reports",data_item="I would like to report that...")
    data_write(session, user_name="Bill",label_name="directions",data_item="Go west")
    data_write(session, user_name="Jane",label_name="directions",data_item="Go north then east")
    data_write(session, user_name="Jane",label_name="description",data_item="tall and dark")
    data_write(session, user_name="Jane",label_name="reports",data_item="more reports data")
    data_write(session, user_name="Brian",label_name="reports",data_item="Brian reports...")
    data_write(session, user_name="Walter",label_name="www",data_item="Walter web data...")
    session.commit()
    print()
    data_read(session, user_name="Jane", label_name="zed")
    data_read(session, user_name="Noone", label_name="reports")
    data_read(session, user_name="Jane", label_name="www")
    data_read(session, user_name="Jane", label_name="reports")
    print()
    user_read(session)
    print()
    label_read(session, user_name="Jane")
    session.commit()
    print()
    data_delete(session, user_name="Bill", label_name="reports")
    data_delete(session, user_name="Brian", label_name="reports")
    data_delete(session, user_name="Jane", label_name="reports")
    session.commit()

    session.close()
```

To test my code, I run the *functions.py* module as a script:

```text
(.venv) $ cd ../..
(.venv) $ python -m dbapp.database.functions
```

I will get the following output:

```text
User 'Bill' added data labeled 'Notes'.
User 'Jane' added data labeled 'reports'.
User 'Bill' added data labeled 'directions'.
User 'Jane' added data labeled 'directions'.
User 'Jane' added data labeled 'description'.
User 'Jane' added data labeled 'reports'.
User 'Brian' added data labeled 'reports'.
User 'Walter' added data labeled 'www'.

Label 'zed' does not exist.
User 'Noone' does not exist.
User 'Jane' does not use label 'www.
User: Jane,  Label: reports,  Data: I would like to report that...,  Time: 2023-11-06 14:02:12.044012
User: Jane,  Label: reports,  Data: more reports data,  Time: 2023-11-06 14:02:12.044012

Bill
Jane
Brian
Walter

description
directions
reports

User 'Bill' does not use Label 'reports'.
Deleted 1 rows.
Deleted 2 rows.
```

I used the *psql* program on the *postgres* database container to see the results of the database commands. First I execute the command on the container:

```bash
(.venv) $ docker exec -it postgres_db psql --username userdata --dbname userdata
```

Then I read the data in the three tables:

```text
userdata=# select * from users;
 id |  name  | info 
----+--------+------
  1 | Bill   | 
  2 | Jane   | 
  4 | Walter | 
(3 rows)

userdata=# select * from labels;
 id |    name     
----+-------------
  1 | Notes
  3 | directions
  4 | description
  5 | www
(4 rows)

userdata=# select * from storage;
 id | user_id | label_id |     data_item      |         time_stamp         
----+---------+----------+--------------------+----------------------------
  1 |       1 |        1 | makes some notes   | 2023-11-06 00:00:33.389959
  3 |       1 |        3 | Go west            | 2023-11-06 00:00:33.389959
  4 |       2 |        3 | Go north then east | 2023-11-06 00:00:33.389959
  5 |       2 |        4 | tall and dark      | 2023-11-06 00:00:33.389959
  8 |       4 |        5 | Walter web data... | 2023-11-06 00:00:33.389959
(5 rows)

userdata=# quit
$
```



## The user interface

At this point I have defined a database and created a set of functions that can manipulate data in the database. Now, I need to create a user interface so the program can be used.

I decided to create a command-line interface. I chose to use the Python Standard Library's *[argparse](https://docs.python.org/3/library/argparse.html)* module because it is the "standard" CLI module for Python and I wanted to learn the basics before I tried other Python CLI libraries. Other popular libraries that help programmers build command-line interfaces are: *[Click](https://click.palletsprojects.com)*, *[DocOpt](http://docopt.org/)*, and *[Typer](https://typer.tiangolo.com/)*. 

In the *interface* sub-package, I created the *cli.py* module:

```text
(.venv) $ cd dbapp/interface
(.venv) $ nano cli.py
```

The interface is simple. I each database function I created in the *database/functions.py* module will correspond with a CLI sub-command. For example, the *dbapp.database.functions.data_read()* function will correspond to a command like `dbapp read <user> <label>`. 

### Define CLI interface

The first section in the *cli.py* module imports the *argparse* and *dbapp.database.functions* modules and documents the user interface. I found it useful to write a docstring that would be similar to what should be output by the command when the user requests help. This helped me understand the sub-commands I would create and the parameters required by each sub-command.

```python
# dbapp/interface/cli.py

import argparse

import dbapp.database.functions as f

"""Database Application.

Usage: 
  dbapp.py write USER LABEL DATA
  dbapp.py delete USER LABEL
  dbapp.py read USER LABEL
  dbapp.py read_users
  dbapp.py read_labels USER
  dbapp.py -h | --help
  dbapp.py -v | --version

Options:
  -h --help         Show this help message and exit
  --version         Show program version and exit
"""
```


### The *create_parser()* function

The *create_parser()* function builds the scafolding for the CLI and returns the *argparse* parser object to the program.

The [*argparse* documentation](https://docs.python.org/3/library/argparse.html) and [tutorial](https://docs.python.org/3/howto/argparse.html#argparse-tutorial) are well-written so I won't re-create an explanation of how to create an *argparse* parser in this post.

Basically, I created a parser for each "command" and a sub-parser for each "sub-command". Then I added help text to each command or sub-command and define arguments expected. This all helps that *argparse* library to manage the CLI and to print out context-appropriate help messages when requested.


```python
def create_parser():
    parser = argparse.ArgumentParser(
        description="Database Application"
        )
    subparsers = parser.add_subparsers(
        title='subcommands', 
        dest='subparser_name'
        )

    read_parser = subparsers.add_parser(
        'read', 
        aliases=['r'], 
        help="Display rows that match name and label."
        )
    read_parser.add_argument('user_id')
    read_parser.add_argument('label_id')

    read_users_parser = subparsers.add_parser(
        'read_users', 
        aliases=['u'], 
        help="Display all users in the database."
        )

    read_labels_parser = subparsers.add_parser(
        'read_labels', 
        aliases=['l'], 
        help="Display labels used by a user."
        )
    read_labels_parser.add_argument('user_id')

    write_parser = subparsers.add_parser(
        'write', 
        aliases=['w'], 
        help="Add new data. Enter user name, label, and data.")
    write_parser.add_argument('user_id')
    write_parser.add_argument('label_id')
    write_parser.add_argument('user_data')

    delete_parser = subparsers.add_parser(
        'delete', 
        aliases=['d', 'del'], 
        help="Delete rows that matche name and label.")
    delete_parser.add_argument('user_id')
    delete_parser.add_argument('label_id')

    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version='dbapp 0.1')
    
    return parser
```

I liked using *argparse*. It let me design the CLI one command, or sub-command, at a time. Looking through the code in the *create_parser()* function, I can see how each command is expected to work.

### The *get_cli_arguments()* function

The *get_cli_arguments()* function just runs the parser's *parse_args()* method which returns the CLI arguments. 

```python
def get_cli_arguments(parser):
    args = parser.parse_args()
    return args
```

### The *main()* function

The *main()* function checks which sub-parser is in use, or which sub-command has been entered by the user. Then it gets the arguments associated with that sub-command and calls the appriopriate database function.

```python
def main(session, args):
    match args.subparser_name:
        case 'read' | 'r': 
            f.data_read(session, args.user_id, args.label_id)
        case 'read_users' | 'u': 
            f.user_read(session)
        case 'read_labels' | 'l': 
            f.label_read(session, args.user_id)
        case 'write' | 'w': 
            f.data_write(session, args.user_id, args.label_id, args.user_data)
        case 'delete' | 'del' | 'd': 
            f.data_delete(session, args.user_id, args.label_id)
        case None if not args.interactive:
            parser.print_help()
```

### The test code

The test code for the *cli.py* module creates the parsers, gets the arguments that have been entered at the command-line interface, and runs the *main()* function. 

```python
if __name__ == "__main__":
    from dbapp.database.models import db_setup
    from dbapp.database.connect import engine, Session
    db_setup(engine)

    parser = create_parser()
    args = get_cli_arguments(parser)
    with Session.begin() as session:
        main(session, args)
```

### The *cli.py* module complete

I saved the *cli.py* module. I can test it by calling the module as follows:

```text
(.venv) $ cd ../..
(.venv) $ python -m dbapp.interface.cli --help
```

The above command should display the help text generated by the *argparse* library, as shown below:

```text
usage: cli.py [-h] [-v] {read,r,read_users,u,read_labels,l,write,w,delete,d,del} ...

Database Application

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

subcommands:
  {read,r,read_users,u,read_labels,l,write,w,delete,d,del}
    read (r)            Display rows that match name and label.
    read_users (u)      Display all users in the database.
    read_labels (l)     Display labels used by a user.
    write (w)           Add new data. Enter user name, label, and data.
    delete (d, del)     Delete rows that matche name and label.
```

I can also use the sub-commands, as shown below:

```text
(.venv) $ python -m dbapp.interface.cli read_users
Bill
Jane
Walter

(.venv) $ python -m dbapp.interface.cli read_labels Bill
Notes
directions

(.venv) $ python -m dbapp.interface.cli read Bill Notes
User: Bill,  Label: Notes,  Data: makes some notes,  Time: 2023-11-06 14:02:12.044012
```

## The *\_\_main\_\_.py* program

So that the package runs when the *dbapp* package is called, I need to create a module named *\_\_main\_\_.py* in the *dbapp* package directory, which will run when the package is run.

```text
(.venv) $ cd dbapp
(.venv) $ nano __main__.py
```

The *\_\_main\_\_.py* is the entry point to the program. It calls the *dbapp.database.models.db_setup()* function, which creates the database tables if they do not already exist, then it creates a database session in a context manager, which automatically commits changes to the database when the context manager code block ends. The *dbapp.interface.cli.main()* function parses the command arguments and performs the appropriate database function.

The *\_\_main\_\_.py* module is shown below:

```python
from dbapp.interface import cli
from dbapp.database.models import db_setup
from dbapp.database.connect import Session

def main():
    db_setup(engine)

    parser = cli.create_parser()
    args = cli.get_cli_arguments(parser)
    with Session.begin() as session:
        cli.main(session, args)


if __name__ == "__main__":
    main()
```

There is no test code in the *\_\_main\_\_.py* module since it is the main program starting point. To test it, run the package in the Python intepreter. For example:

```bash
(.venv) $ cd ..
(.venv) $ python -m dbapp write user1 label100 "test data 1"
User 'user1' added data labeled 'label100'.
(.venv) $ python -m dbapp write user2 label200 "more test data"
User 'user2' added data labeled 'label200'.
(.venv) $ python -m dbapp read_users
Bill
Jane
Walter
user1
user2
(.venv) $ python -m dbapp read_labels user1
label100
```

## Packaging the application

To make it easy for others to use this program I will package it as a *wheel*. I do not intend to publish a "toy" program like this to PyPI so I will perform a simpler packaging procedure than would normally be required.

### The *pyproject.toml* file

```text
$ cd ..
$ nano pyproject.toml
```


```text
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "dbapp"
version = "0.1"
requires-python = ">=3.10"
dependencies = ["SQLAlchemy","psycopg2","python-dotenv"]

[tool.setuptools.packages.find]
where = ["src"]
include = ["dbapp*"]
exclude = ["tests", "docs"]

[project.scripts]
dbapp = "dbapp:main"
```


```text
$ python3 -m venv .bld
$ source .bld/bin/activate
(.bld) $ pip install wheel
(.bld) $ pip install build
(.bld) $ python -m build

(.bld) $ ls dist
dbapp-0.1-py3-none-any.whl  dbapp-0.1.tar.gz
```




```text
$ (.bld) deactivate
$ python3 -m venv .venv2
$ source .venv2/bin/activate
(.venv2) $ pip install dist/dbapp-0.1-py3-none-any.whl
(.venv2) $ set -a; source src/dbapp/.env; set +a
```
