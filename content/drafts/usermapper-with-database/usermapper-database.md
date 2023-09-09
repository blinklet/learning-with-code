title: Add a database to a web app
slug: web-app-database-python
summary: Most web applications need to store data. Even if they do not store user data, web apps need to temporarily cache data so it can be passed between the their routes or views. Many developers choose to use a database to solve this problem. This post shows how I added a database to my *usermapper-web* web app.
date: 2023-09-07
modified: 2023-09-07
category: Databases
<!-- status: Published -->

My [*usermapper-web* program](https://github.com/blinklet/usermapper-web) is a very simple web app that uploads a small configuration file and uses it to build a complex [XML file](https://guacamole.apache.org/doc/gug/configuring-guacamole.html#user-mapping-xml) for the [Apache Guacamole](https://guacamole.apache.org/) remote desktop gateway. The user may download the XML file and use it to prepare user accounts, using the Guacamole server's default authentication.

I used the [Flask framework](https://flask.palletsprojects.com/en/2.3.x/) to implement the program's web interface. To pass data created by the user between application routes, the program generated a randomly-named folder for each user and passed the folder name in a parameter when calling a new route. This works OK for a small app like *usermapper-web*, where I expect between zero and one users per week. But, this crude data-caching method requires filesystem services that may not be permitted on some web app platforms and it requires a separate data cleanup process to avoid filling the server's filesystem with user folders, over time.

The "standard" way to cache user data for a web app is to use a database server. In this post, I will create a local database instance and change my *usermapper-web* program so it uses the database to store user information.

## Why use a database

Flexibility:

- Can use any database service in the cloud when deploying -- just have to change some variables
- Or, can deploy using containers so the "state" is in the database
- Or, do both: test locally using containers and deploy using cloud services.


## Steps required

Changing the way *usermapper-web* stores user information requires the following steps:

1. Set up a database in a container running on your development PC, so you can test the changes you make to your program. Also, prepare the Python environment for your program. In my case, I run my *usermapper-web* application in a Python virtual environment.

1. Define and implement a way to identify each user. I prefer to avoid requiring users create a user ID and password so I want to create a temporary internal identifier for each user session. I plan assign a Flask [session](https://flask.palletsprojects.com/en/latest/quickstart/#sessions) to each user, and use it as the temporary user ID. I will use the [Flask-Session](https://flask-session.readthedocs.io/en/latest/) extension to make this easier.

1. Use the identifiers assigned to users as keys in the database table.

1. Save user data, which is meant to be downloaded as an XML file, as [XML data](https://www.postgresql.org/docs/current/datatype-xml.html) in the database table. 

1. Use [StringIO](https://docs.python.org/3/library/io.html) to serve the XML content as a [file download](https://www.geeksforgeeks.org/stringio-module-in-python/) to the user.

1. When the user session ends, delete the row that contained that session's data. The app does not need to save the user's data because they will have their config file on their local computer. Managing user accounts and data will be a feature that may be implemented in the future.

## Test the exiting *usermapper-web* application

Get the code for the *usermapper-web* application. If you want to follow along with this tutorial, start at the tag *v0.3*, as shown below:

```
$ git clone --branch v0.3 https://github.com/blinklet/usermapper-web.git
$ cd usermapper-web
$ ls -1
application.py
Dockerfile
dotenv.example
downloads
LICENSE
README.md
requirements.txt
templates
```

Prepare a Python virtual environment and the dotenv file for local development.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
$ cp dotenv.example .env
```

Run the application with the following command:

```
(.venv) $ flask run
```

To test the application, enter the application's URL in a browser window. Use the following URL:

```text
http://localhost:5000
```

The browser window should show the web app's first page, as shown in the screenshot below

![Usermapper Web App running on local PC in development mode]({attach}usermapper-01.png){width=90%}

For more information about the *usermapper-web* application and how to use it, either refer to the instructions on the web page or read [my web app tutorial post]({filename}/content/articles/003-flask-web-app-tutorial/flask-web-app-tutorial.md) that describes how I developed and use it.

After you finish testing the *usermapper-web* application, quit the Flask app by typing *CTRL-C* in the terminal window. 

## Generate a UUID

Use the Python Standard Library's [UUID module](https://docs.python.org/3/library/uuid.html) to generate a random ID that will be used to identify each user's session. The UUID module is very unlikely to produce a duplicate ID within your lifetime.

According to the UUID module's documentation, the *uuid4* function generates an instance of the UUID class that contains a random ID and its *int* attribute returns that ID as a 128-bit integer. So, I will use the statement, `uuid.uuid4().int` to generate a random integer that I will use to name the directory.

For example:

```python
(.venv) $ python3
>>> import uuid
>>> for i in range(4):
...     x = uuid.uuid4().int
...     print(x)
...
48373756605288068424419529448133529384
18514395524172778111336895815884387082
157990026457444853003560573840411066999
249080889110014159706537234532851223902
>>> quit()
(.venv) $ 
```

## Assign UUID to each user session

Use the [Flask-Session](https://flask-session.readthedocs.io/en/latest/) extension. This creates server-side user sessions for Flask but it also requires a "backend" to store the user data on the server. You can use the system memory, filesystem, or a database.

### Install Flask-Session

Install the extension in your Python virtual environment:

```bash
(.venv) $ pip install Flask-Session
```

And, add the line, `Flask-Session`, to your *requirements.txt* file.

### Create a session

(Flask-Session creates a cookie for the user called "session" that contains a UUID for that user)
Get the Flask-Session ID by looking for "session".

Near the top of the *application.py* file add the following import statements:

```python
from flask import request, session
from flask_session import Session
```

In the application configuration section, set the following configuration environment variables for the Session:

```python
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
```

In the "/" route function, change function so it uses the Flask Session instead of manually creating its own random directory

```python
@app.route("/", methods=('GET','POST'))
def index():
    form = MyForm()
    filename = None
    if form.validate_on_submit():

        f = form.filename.data
        basedir = os.path.join(
            os.path.relpath(os.path.dirname(__file__)), 
            'downloads')
        tempdir = tempfile.mkdtemp(dir=basedir)

        filename = os.path.join(tempdir,'user-mapping.xml')

        configuration = yaml.safe_load(f.read())
        structure = get_users(configuration)
        xmlwriter(structure,filename)

        temp_folder = os.path.split(tempdir)[1]
        return redirect (url_for('download_page', temp_folder=temp_folder))

    return render_template('index.html', form=form)
```




## 
The *application.py* file contains the Flask routes that create the randomly-named directories in the filesystem. Open the file and look at the 

```
newpath = r'C:\Program Files\arbitrary'
if not os.path.exists(newpath):
    os.makedirs(newpath)
```




































## Set up the database

Set up a Docker container that is running a PostgreSQL database. You may run the commands listed below and, if you wish, you may see more details about running a PostgreSQL database in a Docker container in my [previous post]({filename}/articles/018-postgresql-docker/postgresql-docker.md).

Get the official [PostgreSQL Docker image](https://hub.docker.com/_/postgres) from the *Docker Hub* container library. Open a terminal on your Linux PC and run the Docker *pull* command:

```bash
$ docker pull postgres
```

Create a new database container called *userdb* from the Postgres image. Set the admin password and define a user. Setting the user also creates a database with the same name as the user. Run the Docker *run* command:

```bash
$ docker run \
    --detach \
    --env POSTGRES_PASSWORD=abcd1234 \
    --env POSTGRES_USER=sessions \
    --publish 5432:5432 \
    --name userdb\
    postgres
```

Use the Docker *exec* command to run the *psql* utility on the container to check that the database server is running. Start it in interactive mode on the container. Use the username, *sessions*, which connects to the database, *sessions*:

```bash
$ docker exec -it userdb \
    psql --username sessions

sessions=#
```

Now you can be confident that the database is ready to use. Quit the *psql* utility:

```text
sessions=# \q
$ 
```





## x



Options:

Flask Session cookies
- store entire XML doc on user's browser?
https://sparkdatabox.com/tutorials/python-flask/flask-session

https://stackoverflow.com/questions/53899527/python-flask-how-to-remember-anonymous-users-via-cookie-session



Flask Cache
https://flask-caching.readthedocs.io/en/latest/
   - can use filesystem cache, memory cache, https://stackoverflow.com/questions/18562006/efficient-session-variable-server-side-caching-with-pythonflask
   - use filesystem cache or memory cache with Gunicorn where works may be > 1 because: https://stackoverflow.com/questions/32149736/gunicorn-flask-caching/69903128#69903128

Use "Flask-Session" extension
https://flask-session.readthedocs.io/en/latest/
   - can use with database (better than using filesystem for complex apps. My app does not care)
   https://vegibit.com/how-to-use-sessions-in-python-flask/
   https://pythongeeks.org/flask-session/

https://www.askpython.com/python-modules/flask/flask-user-authentication

Database
   - key off userid from session cookie?
   - allows your users to resume their transaction even if their browser crashes  (but only if I set up logins)





maybe use Redis, which can automatically timeout data?

json-ify the usermapper xml?

xml native in database???

How to return a file from DB??
https://stackoverflow.com/questions/60499958/what-is-the-best-way-to-store-an-xml-file-in-a-database-using-sqlalchemy-flask

https://realpython.com/flask-connexion-rest-api/
https://realpython.com/flask-connexion-rest-api-part-2/
https://realpython.com/flask-connexion-rest-api-part-3/

multiple-container apps
https://docs.docker.com/get-started/07_multi_container/



flask sessions
https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/


Use StringIO 
https://stackoverflow.com/questions/44672524/how-to-create-in-memory-file-object




future app ideas
- draw a diagram and create XML user-mapping file for it
     network diagram example: https://github.com/MJL85/natlas