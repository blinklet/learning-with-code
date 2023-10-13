In this post, I show how to create a simple application that writes and reads data to a database. I will use the [SQLAlchemy](https://www.sqlalchemy.org/) library to define a database table, initialize a new database, and then write and read data. I will use the [SQLAlchemy ORM](https://medium.com/dataexplorations/sqlalchemy-orm-a-more-pythonic-way-of-interacting-with-your-database-935b57fd2d4d) for all operations so that my program is as "Pythonic" as possible.

## The fundamental topics

I already describe how to use SQLAlchemy to read data from an existing relational database in some of my previous posts. If you have never used the SQLAlchemy ORM, I suggest you read those posts, first.

In this post, I will describe a Python program that creates a single, simple table in a database and how I added, retrieved, and deleted data from that table. The program must, neccessarily, include functions that interact with the database and with the user. But, before I create a project structure and write all the Python modules that contain those functions, I will preview the main points in the Python REPL.  

When creating 
After connecting to a database engine, SQLAchemy will check if 

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install sqlalchemy
(.venv) $ python
>>>
```

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
engine = create_engine("sqlite:///userdata.db")
```


There are two ways to create database metadata: reflection or declarative mapping. 

I covered reflection extensively in my previous post about [using SQLAlchemy to read data]({filename}/articles/016-sqlalchemy-read-database/sqalchemy-read-database.md).

In this case, I am creating a new database so I will use [SQLAlchemy Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) to manually build SQLAlchemy ORM classes as Python classes. 

The SQLAlchemy documentation recommends you use Declarative Mapping in all cases to manually build SQLAlchemy ORM classes that match the database structure that either exists or is to be defined. Declarative Mapping documents the database structure in your program and allows you to more easily handle changes to database structure in the future.



https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase

Compatible with new [Python type hints](https://peps.python.org/pep-0484/), which I am not using in my programs, yet.

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```

Base class has a metadata attribute that contains table information. Why create Base and not just subclass Declartive base in my table classes, below? Because Base can be configured with custom metadata and other attributes that could be inherited by all other database subclasses in more advanced database applications. This is just a good practice, for now.

```python
from sqlalchemy import String, UnicodeText, DateTime
from sqlalchemy.orm import mapped_column
```

https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-orm-table-metadata

I am not yet using type hints in my Python programs so I will exclusively use the SQLAlchemy ORM *mapped_column()* function to define each columns instead of also using the [ORM's *Mapped* class](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html).

```python
class Userdata(Base):
    __tablename__ = "userdata"
    user_id = mapped_column(String(32), primary_key=True, nullable=False)
    user_data = mapped_column(UnicodeText)
    time_stamp = mapped_column(DateTime(timezone=True))
```

Create the database. May run even if database already exists. 

```python
Base.metadata.create_all(engine)
```

Now, we want to write some data to the database, using the unit-of-work model recommended in the ORM documentation.

```python
session = Session(engine)
```

https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete

https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#updating-orm-objects-using-the-unit-of-work-pattern


```python
from datetime import datetime

from sqlalchemy import select, update, delete

from dbapp.database.models import Userdata


def db_write(session, id, data):
    userdata = Userdata(
        user_id = id,
        user_data = data,
        time_stamp = datetime.now()
    )
    session.add(userdata)
```

Read function

```python
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
    user_id = mapped_column(String(32), primary_key=True, nullable=False)
    user_data = mapped_column(UnicodeText)
    time_stamp = mapped_column(DateTime(timezone=True))
    def __repr__(self):
        return f"user_id = {self.user_id}, " \
               f"user_data = {self.user_data}, " \
               f"time_stamp = {self.time_stamp.strftime('%B %d %H:%M')}"
```


















## Project files and folders

I want the application name to be *dbapp*. So, the application modules and sub-packages will all be in a directory named *bdapp*. The project metadata, used when installing dependencies, is stored in the *requirements.txt* file in the same project folder as the *dbapp* package.

The *dbapp* package contains two sub-packages, *database* and *interface*, a configuration module, a dotenv file for safely storing sensitive database connection strings and other configurations, and a file named *__main__.py*, which Python runs automatically when a user runs the `python -m dbapp` command when in the *dbproject* directory.

The *database* package contains three modules:

  * *connect.py* sets up the database connection
  * *functions.py* creates functions that read, write, and delete database information
  * *models.py* contains the SQLAlchemy code that defines the database

The *interface* package contains just one module, for now.

  * *cli.py* runs the program's command-line interface
  * more user interfaces, such as an interactive user interface, could be added later

The project structure will look like below:

```
project/
   ├── .gitignore
   ├── requirements.txt
   ├── README.md
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

The *.gitignore* file
use Python file from GitHub
ensure *.env* file is included in *.gitignore* file

The *__init__.py* file in each package directory is just a blank file that indicates that the directory is to be treated as a [regular Python package](https://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html).

The *__main__.py* file in the top-level package directory will be executed when the package is called using the `python -m` command. https://realpython.com/pypi-publish-python-package/#call-the-reader
https://docs.python.org/3/library/__main__.html#main-py-in-python-packages


You can see that the project is in three folders named *src*, *docs*, and *tests*. 

The *docs* folder contains a *dotenv_example.txt* file because the real [*dotenv** file]({filename}/articles/011-use-environment-variables/use-environment-variables.md) is excluded from source control, using the *.gitignore* file, so I like to document an example for anyone who clones one of my projects from [GitHub](https://github.com/blinklet).

## Create a database container

Create a new database container called *ps_userdata*. In this case, I will start a [new container running *PostgreSQL*]({filename}/articles/018-postgresql-docker/postgresql-docker.md). Run the following command:

```bash
$ docker run \
    --detach \
    --env POSTGRES_PASSWORD=abcd1234 \
    --env POSTGRES_USER=userdata \
    --publish 5432:5432 \
    --name userdata\
    postgres:alpine
```

## Configuration files

The *requirements.txt* file looks like the one below. 

```python
# requirements.txt
SQLAlchemy 
psycopg2
python-dotenv
```

I saved the *requirements.txt* file.


## Install dependencies

I created a Python virtual environment and used the *requirements.txt* file to install the project dependencies.

```
$ cd project
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

## Application configuration

Configuration file, *config.py* defines the database connection string:

```python
import os

from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

_database_server = os.getenv('DB_SERVER')
_database_port = os.getenv('DB_PORT')
_database_name = os.getenv('DB_NAME')
_database_userid = os.getenv('DB_UID')
_database_password = os.getenv('DB_PWD')

database_url = URL.create(
    drivername='postgresql+psycopg2',
    username=_database_userid,
    password=_database_password,
    host=_database_server,
    port=_database_port,
    database=_database_name
    )

# SQLite3 database
# database_url = "sqlite:////home/brian/db/userdata.db"

if __name__ == "__main__":
    print(f"Database URL = {database_url}")
```

To test the module, run it as a script:

```bash
(.venv) $ cd src
(.venv) $ python -m dbapp.config
Database URL = postgresql+psycopg2://userdata:***@localhost:5432/userdata
```

## Database code

### Database 

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

To test the module, run it as a script:

```bash
(.venv) $ python -m dbapp.database.connect
Engine(postgresql+psycopg2://userdata:***@localhost:5432/userdata)
<sqlalchemy.engine.base.Connection object at 0x7fd4c9015f00>
```

## Create database tables


[declarative mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping)

https://www.youtube.com/watch?v=XWtj4zLl_tg

Create the *models.py file:

```
# dbapp/database/models/py

from sqlalchemy import Integer, String, UnicodeText, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column

from dbapp.database.connect import engine


Base = declarative_base()


class Userdata(Base):
    __tablename__ = "userdata"

    user_id = mapped_column(String(32), primary_key=True, nullable=False)
    user_data = mapped_column(UnicodeText)
    time_stamp = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f"ID = {self.user_id:10}  " \
               f"DATA = {self.user_data:20}  " \
               f"TIME = {self.time_stamp.strftime('%B %d %H:%M')}"


def db_setup():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    db_setup()
```

I used to have `server_default=func.now()` in the *time_stamp* column so that the [SQL server would create the datetime entry](https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime) when a new row was added but I chose to calculate datetime in my program because it is simpler to update the timestamp in an existing row. Another solution involves [creating a trigger](https://stackoverflow.com/questions/22594567/sql-server-on-update-set-current-timestamp) in the SQL database but, again, I thought it was better to run this logic in the Python program.



## Create database functions

where to create session?
"outside" functions that use it
see: 



```python
from datetime import datetime

from sqlalchemy import select, update, delete

from dbapp.database.models import Userdata


def db_write(session, id, data):
    userdata = Userdata(
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


## The *__main__.py* program

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


Save the *__main__.py* program.

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

