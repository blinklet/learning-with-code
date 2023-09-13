title: Flask-Session deep dive
slug: flask-session-sqlalchemy-redis-python
summary: An in-depth review of the Flask-Session extension for the Flask Python web application framework. I review how well it can be used to manage ephemeral, anonymous user sessions. I test using the local file system, SQLAlchemy with a PostgeSQL database, and a Redis database to provide the sessions' backend data storage. 
date: 2023-09-29
modified: 2023-09-29
category: Flask
<!-- status: Published -->

The *[Flask-Session](https://flask-session.readthedocs.io/en/latest/)* extension manages user sessions for your *[Flask](https://flask.palletsprojects.com/en)* web app and can use a variety of "backends" to store the user data on the server, enabling you to store large amounts of user data per session. The "backend" can be the server's system memory, file system, or a database. 

In this post, I test Flask-Session to see if it is suitable for an application I am developing. I want to use an SQL database to manage user data associated with each user's session. I want users to remain anonymous so I do not implement *Login* and *Logout* buttons in my application. Instead, I want to automatically delete the user data after an anonymous user leaves the application. 

While working with Flask-Session in my sample program, I solved some frustrating issues that I think some readers who are writing similar programs will want to know about. Flask-Session can be made to work in my application by setting configuration variables and adding some initialization code.

## Shortcut to the conclusion

This is a long post so I will preview my conclusion here. At the end of this post, I conclude that I will not use Flask-Session for the program on which I am currently working. 

Flask-Session has problems initializing an SQL database that required me to add SQLAlchemy code. If I have to use *[SQLAlchemy](https://www.sqlalchemy.org/)* into my program, anyway, I may as well write my own SQLAlchemy mappings and use them to manage the SQL database backend.

Flask-Session's documentation assumes that the programmer will manually clean up sessions when a user logs out. It does not clearly explain how to use its configuration options to make it automatically delete backend data from non-permanent sessions. I document these points later in this post but, if I am no longer using Flask-Session to manage the database, it is clearer to use Flask's native *[session](https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions)* objects in my application.

However, there are many cases where Flask-Session will work, especially in more classic applications that manage users via the *[Flask-Login](https://pypi.org/project/Flask-Login/)* extension. Flask-Session works well for anonymous users if you use the *[Redis](https://redis.io/)* database backend. I assume most bloggers have come to the same conclusion because it seems every other blogger who writes about Flask-Session uses only Redis in their examples.

## Create a simple program that uses Flask-Session

To evaluate how Flask-Session works, create a simple Flask application that uses the Flask-Session extension with the *FileSystemSessionInterface* backend. This backend caches session data on your PC's file system and is useful for local testing.

The application will consist of a single application file, named *app.py*, and several Jinja template files that create the application's HTML web pages.

### Set up Python environment

Prepare a Python virtual environment for this project. I will place my application and the virtual environment in a directory named *experiment*.

```bash
$ mkdir experiment
$ cd experiment
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $
```

Install Flask and Flask-Session.

```bash
(.venv) $ pip install flask
(.venv) $ pip install Flask-Session
```

### Create basic Flask templates

Create a base template and two page templates that display different pages: a greetings page that gathers some user data, and an action page that displays that data back to the user.

Create a *templates* directory for the templates:

```bash
(.venv) $ mkdir templates
(.venv) $ cd templates
```
#### Base template

Create a file named *base.html*:

```bash
(.venv) $ nano templates/base.html
```

Enter the following text

```html
<!doctype html>
<html lang="en">
    <head>
    {% block head %}
        <meta charset="utf-8">
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <title>{% block title %}Experiment{% endblock %}</title>
    {% endblock %}
    </head>
    <body>
        {% block content %}{% endblock %}
    </body>
</html>
```

Save the file.

#### Greeting template

Create a file named *greeting.html*:

```bash
(.venv) $ nano templates/greeting.html
```

Enter the following text

```html
{% extends "base.html" %}
{% block title %}Experimental Greeting{% endblock %}
{% block content %}
    <h1>Upload text file</h1>
    <form method='POST' enctype="multipart/form-data">
        <input type='file' name='textfile'>
        <input type='submit' value='Upload'>
    </form>
    {% if session.file_contents %}
        <p>Thank you for uploading a file. See the contents of your previous upload <a href="{{ url_for('action') }}">here</a> or upload a new file.</p>
    {% else %}
        <p>This is an experiment. Upload the text file whose contents you want displayed. Or, go to the <a href="{{ url_for('action') }}">Action page</a></p> to see what happens.
    {% endif %}
{% endblock %}
```

#### Action template

Create a file named *action.html*:

```bash
(.venv) $ nano templates/action.html
```

Enter the following text

```html
{% extends "base.html" %}
{% block title %}This is what you asked for!{% endblock %}
{% block content %}
    <h2>Go back to the <a href="{{ url_for('greeting') }}">upload page</a>.</h2>
    <br>
    <h3>The file contents are:</h3>
    <br>
    {% if session.file_contents %}
        {% for item in session.file_contents %}
            {{ item|replace(' ','&nbsp;'|safe) }}<br>
        {% endfor %}
    {% else %}
        <p>You have not yet uploaded a file</p>
    {% endif %}
{% endblock %}
```

### Create the Flask application

Edit a file named *app.py*:

```nash
(.venv) $ nano app.py
```

At the top of the *app.py* file, import the following classes and functions from Flask and Flask-Session:

```python
from flask import Flask, request, redirect, url_for, render_template, session
from flask_session import Session
```

[Instantiate](https://flask.palletsprojects.com/en/2.0.x/design/) the Flask application object. In this case, we will follow convention and call it *app*.

```python
app = Flask(__name__)
```

To configure the Flask application, set the usual Flask environment variables, *SECRET_KEY*, *FLASK_APP*, and *FLASK_ENV*. 

 for the Flask app and for the sessions to be created:

```python
app.config["SECRET_KEY"] = "xyzxyxyz"
app.config["FLASK_APP"] = "app"
app.config["FLASK_ENV"] = "Development"
```

Then set the Flask-Session environment variables. Set the *SESSION_TYPE* to *filesystem* because it is the simplest backend to set up and so it is a good backend with which to start experimenting. 

Flask-Session will start cleaning up old files from the directory after more than 500 files are stored there. You can change this threshold by setting the *SESSION_FILE_THRESHOLD* variable. I set it to a small value to make testing easier. 

```python
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_THRESHOLD"] = 5
```

Call Flask-Session's *Session* class and pass the Flask application object into it. This adds configurations to the application's [*session* object](https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions). 

```
Session(app)
```

Create the Flask route for the index page that contains the file upload form, which I call the *greeting* route.

```python
@app.route("/", methods=('GET','POST'))
def greeting():
    if request.method == 'POST':
        file = request.files['textfile']
        if file:
            lines = [x.decode('UTF-8') for x in file.readlines()]
            session['file_contents'] = lines
            return redirect (url_for('action'))
    return render_template('greeting.html')
```

I used the Flask *[request.files](https://flask.palletsprojects.com/en/2.3.x/api/#flask.Request.files)* property to get the objected named "textfile" (whose name was defined in the Jinja template *greeting.html*) when the form is submitted, which generates a *POST* request.

Flask uploads the file as a byte stream. The file's *readlines()* method outputs a list of rows but each row is a binary string. I need to convert each row in the list from bytes to UTF-8 character code points. The list comprehension in the *greeting* route, above, creates a new list named "lines" that contains the same rows but each row is now a UTF-8 string.

Create the Flask route for the page that displays the uploaded file, which I call the *action* route. 

```python
@app.route("/action", methods=('GET','POST'))
def action():
    return render_template('action.html')
```

This simply renders the *action.html* Jinja2 template, which contains the code that checks if there is any user data in the *session['file_contents']* object and, if so, prints it on the page.

Save the file.

Note that I am not checking for valid inputs or ensuring that the file is really a text file. I am keeping this code very simple so I can quickly demonstrate the way *Flask-Session* works. So, when testing, use small text files.

### Test the application

Test that the application will request a text file and then display the contents of the file in the Browser. Run the app: 

```bash
(.venv) $ flask run
```

Open a browser and enter in the URL where the Flask server is running:

```text
http://localhost:5000
```

The index, or *greeting*, page of the application will look like the following:

![Flask app]({attach}session-001.png)

Create a dummy text file, add some dummy text to it, and save it. Select the file using the web app and click the *Upload* button. The *action* page should look similar to the screenshot below:

![Flask app]({attach}session-002.png)

You should expect that the program will create a new directory and store user data as files in that directory.  The session file should be saved in a directory, created by Flask-Session, named *flask_session*. It will be in the same location as the *app.py* file. If you want, you can define another directory by setting the *SESSION_FILE_DIR* variable.

```bash
(.venv) $ ls flask_session
2029240f6d1128be89ddc32729463129
```

This shows a session saved on the server. There should also be a session cookie in your browser that corresponds with the server-side session file. The file names are created by encrypting the Session UUID so you can't easily match which cache file is associated with which browser session. 

If you delete the session cookie using your browser's development tools, and then try to upload a text file again, you will see that the new session creates a new file in the *flask_session* directory. For example:

```bash
(.venv) $ ls -1 flask_session
2029240f6d1128be89ddc32729463129
394ee48c85cd86a3e1391102c3ce25d3
```




### FileSystem session configuration variables

I found the Flask-Session documentation did not describe how its configuration variables affect your program's operation. I describe in more detail the variables that interact with each other to affect how many sessions are cached and for how long. Other variables set the default storage directory, cookies and session names, and are described well enough in the [Flask-Session configuration](https://flask-session.readthedocs.io/en/latest/config.html) documentation.

#### SESSION_FILE_THRESHOLD

The *SESSION_FILE_THRESHOLD* variable controls the number of session data files cached in the *flask_session* directory. The default is value is 500. Depending on your application you may need more or less. For testing, I usually set a small number like five. No files, even files older than the *PERMANENT_SESSION_LIFETIME* are deleted until the configured threshold is met. When the threshold is met, all files older than the *PERMANENT_SESSION_LIFETIME* are deleted, even if that makes the number of files in the directory much lower than *SESSION_FILE_THRESHOLD*.

If many files are generated quickly so that the threshold is reached before any file is older than *PERMANENT_SESSION_LIFETIME*, Flask-Session will still maintain the threshold and delete session files until there are only *SESSION_FILE_THRESHOLD* remaining.

#### PERMANENT_SESSION_LIFETIME

The *PERMANENT_SESSION_LIFETIME* variable controls the length of time a session will last before Flask-Session deletes it. It has a default value of 2,592,000 seconds or 30 days. You may set it to a smaller or larger number of seconds. It is used to calculate the session expiry in cookies and is used to select which session files on the server will be deleted when the number of files exceeds *SESSION_FILE_THRESHOLD*. It can be used even if you are creating non-permanent sessions, as described below.

#### SESSION_PERMANENT

The *SESSION_PERMANENT* variable controls the type of cookie created in the browser and has only an indirect affect on how files are stored on the server, because of the way Flask-Session reacts to cookies in the browser. 

If *SESSION_PERMANENT* is true, the cookie sets its *Expires/Max-Age* to its default value of the current time plus 30 days or to the current time plus *PERMANENT_SESSION_LIFETIME* variable, if it was also configured. When you use the web app again to upload a new file after *PERMANENT_SESSION_LIFETIME*, you create a new cookie with a new session UUID and a new cache file in the *flask_session* directory.

If *SESSION_PERMANENT* is false, the cookie sets its *Expires/Max-Age* to the string, "session". In theory this is a temporary cookie that should be deleted when the session ends but many browsers keep session cookies indefinitely. However, the *PERMANENT_SESSION_LIFETIME* variable still has an impact on sessions even if *SESSION_PERMANENT* is false. Flask-Session stops using the session after *PERMANENT_SESSION_LIFETIME* even though the session cookie still exists. When you use the app again to upload a file, it "re-initializes" the session and, since the session cookie still exists, it re-uses its Session UUID so it overwrites the corresponding session file on the server. The result is that is seems as though no new session file was added.

## Using the Flask-Session SQLAlchemy backend 

The FileSystemSessionInterface backend is useful for for trying Flask-Session for the first time and may be good for local testing but you need to use a database if you intend to deploy your application as a web app. Flask-Session has an SQL database backend called *SqlAlchemySessionInterface*, which requires the Flask-SQLAlchemy extension.

Install Flask-SQLAlchemy and the Postgres Python driver in your Python virtual environment.

```bash
(.venv) $ pip install flask-sqlalchemy
(.venv) $ pip install psycopg2
```

### Set up the database

The easiest way to start a database server for testing is to use Docker. In this example, I will create a Docker container that is running a *PostgreSQL* database. You may run the commands listed below and, if you wish, you may see more details about running a PostgreSQL database in a Docker container in my [previous post]({filename}/articles/018-postgresql-docker/postgresql-docker.md).

Use the official [PostgreSQL Docker image](https://hub.docker.com/_/postgres) from the *Docker Hub* container library. Create a new database container named *userdb* from the Postgres image. Set the admin password and define a user. Setting the user also creates a database with the same name as the user. In this case, I created a user named *userdata*. Run the Docker *run* command:

```bash
(.venv) $ docker run \
    --detach \
    --env POSTGRES_PASSWORD=abcd1234 \
    --env POSTGRES_USER=userdata \
    --publish 5432:5432 \
    --name userdb\
    postgres
```

Use the Docker *exec* command to run the *psql* utility on the container to check that the database server is running. Start it in interactive mode on the container. Use the username, *userdata*, which connects to the database, *userdata*:

```bash
(.venv) $ docker exec -it userdb \
    psql --username userdata

sessions=#
```

Now you can be confident that the database is ready to use. Quit the *psql* utility:

```text
sessions=# \q
(.venv) $ 
```

You also know the database information that is required to create the database connection string in your Flask application. The database is running on TCP port 5432 at your PC's loopback address, which can be expressed either as *127.0.0.1* or *localhost*. You know the username and password and the database name.

### Modify your program to use the SQL database

Edit the *app.py* program so it uses a database backend instead of the local filesystem. Open the file in your favorite text editor and add the following code under the existing import section to assign the [database connection string](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) to a variable named *uri*:

```python
uri = "postgresql://userdata:abcd1234@localhost:5432/userdata"
```

Change the Flask-Session configuration variables. Assign the string "sqlalchemy* to the *SESSION_TYPE* variable. You *must* set the *SESSION_PERMANENT* variable to be *True* or the database will generate type errors. You don't need to set the *PERMANENT_SESSION_LIFETIME* variable because Flask-Session will not delete old rows in the after their *PERMANENT_SESSION_LIFETIME* expires. However, I will create an SQL function that is triggered by a new row, that deletes rows who *expiry* column contains an old-enough timestamp. So, configure *PERMANENT_SESSION_LIFETIME* to a low value like 60 seconds for testing purposes. Finally, assign the connection string from the *uri* variable to the *SQLALCHEMY_DATABASE_URI* variable.

```python
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["PERMANENT_SESSION_LIFETIME"] = 60  # 1 minute
```

Then, add the following code after you initialize the *Session* class. This code is a [workaround](https://stackoverflow.com/questions/45887266/flask-session-how-to-create-the-session-table) that is not well documented. The Flask-Session *SqlAlchemySessionInterface* does not create the database when you initialze the Session. I consider this to be a bug in Flask-Session.

```python
Session(app)
with app.app_context():
    app.session_interface.db.create_all()
```

In the code above, you need to use the *with app.app_context()* block to manually make the Flask app's [application context](https://flask.palletsprojects.com/en/2.3.x/appcontext/) available to the *app.session_interface.db.create_all()* function. Flask normally manages the application context for you but, in this case, we are manually initializing the database outside of a Flask route or view. 

In the end, the entire *app.py* program will look like below:

```python
$ cat app.py
from flask import Flask, redirect, url_for, render_template, session, request
from flask_session import Session

uri = "postgresql://userdata:abcd1234@localhost:5432/userdata"

app = Flask(__name__)
app.config["SECRET_KEY"] = "xyzxyxyz"
app.config["FLASK_APP"] = "app"
app.config["FLASK_ENV"] = "Development"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 60  # 1 minute
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config['SQLALCHEMY_DATABASE_URI'] = uri

Session(app)
with app.app_context():
    app.session_interface.db.create_all()

@app.route("/", methods=('GET','POST'))
def greeting():
    if request.method == 'POST':
        file = request.files['textfile']
        if file:
            lines = [x.decode('UTF-8') for x in file.readlines()]
            session['file_contents'] = lines
            return redirect (url_for('action'))
    return render_template('greeting.html')

@app.route("/action", methods=('GET','POST'))
def action():
    return render_template('action.html')
```

You can see how easy it was to change to a database backend. Except for the workaround required to create the database, we just changed a few variables. You could change the session type back to *filesystem* just as easily.

### Test the program

To test the modified program, run it with the `flask run` command and then open a browser to the URL: `http://localhost:5000`. The application looks and works the same as it did when we used the filesystem backend. Only, now, it is using a database to cache session data. 

Using your browser's development tools, delete the session cookie (or wait one minute), and upload the text file again. Now you should have two rows in the database. Check the contents of the database by starting *psql* in the database container:

```bash
(.venv) $ docker exec -it userdb \
    psql --username userdata

sessions=#
```

Read rows in the *sessions* table in the database. By default, Flask-Sessions creates the table named *sessions* to store the session data. You may select your own table name if you configure the *SESSION_SQLALCHEMY_TABLE* variable in the program.


```text
userdata=# SELECT id, session_id, expiry FROM sessions;
 id |                  session_id                  |           expiry           
----+----------------------------------------------+----------------------------
  1 | session:84c64ee0-69e8-4e05-a6b4-ed18a9ef3719 | 2023-09-13 02:18:12.278563
  2 | session:24c8b4a0-52b1-4e53-b5ae-e44daf4629f5 | 2023-09-13 02:18:28.17735
(2 rows)
```

You can see that the expiry time is set 60 seconds in the future. Check the database time using the *now()* SQL function:


```text
userdata=# SELECT now();
              now              
-------------------------------
 2023-09-13 02:17:35.826363+00
(1 row)
```

However, the database rows will not be cleaned up after their expiry time passes. Flask-Session expects you to manually remove user data when the session ends. The only way for your program to know that is if a user clicks on a *Logout* button or something similar. Your Flask program cannot detect when a user just closes their browser. So, a lot of rows could potentially build up as people use your application. In my case, I do not try to detect when a user leaves their session so every time their session expires, as defined by the *PERMANENT_SESSION_LIFETIME* variable, the data related to it remains in the SQL database.

### Solving the data cleanup problem

In my opinion, Flask-Session should take care of cleaning up old rows in the database. However, it does not.

There are two ways you can solve the data cleanup problem. You can create an SQL function that is triggered every time you insert a new row in the database. The function would check the *expiry* column in each row against the current time and delete any rows where the current time is later than the datetime in the row's *expiry* column. See [The Art of Web Blog](https://www.the-art-of-web.com/sql/trigger-delete-old/) for a good description of this solution. 

Another solution, and the one I prefer, is to add some more workaround code to the *app.py* program. The code will run when a new file is uploaded and check all the rows in the database. If the datetime in the *expiry* column in any row is later than the database's current time, it deletes the row. I integrated the code from a [stackoverflow answer](https://stackoverflow.com/questions/38455893/flask-session-cleanup-of-expired-sessions) into my *greeting* route.

```python
import datetime
```

```python
@app.route("/", methods=('GET','POST'))
def greeting():
    if request.method == 'POST':
        file = request.files['textfile']
        if file:
            lines = [x.decode('UTF-8') for x in file.readlines()]
            session['file_contents'] = lines
            expired_sessions=(
                app.
                session_interface.
                sql_session_model.
                query.filter(
                    app.
                    session_interface.
                    sql_session_model.
                    expiry <= datetime.utcnow()
                )
            )
            for es in expired_sessions:
                app.session_interface.db.session.delete(es)
                app.session_interface.db.session.commit()
            return redirect (url_for('action'))
    return render_template('greeting.html')
```






## Redis?

Try setting up a Redis server?
https://testdriven.io/blog/flask-server-side-sessions/


```bash
(.venv) $ pip install redis
```

app.py 

```python
from flask import Flask, request, redirect, url_for, render_template, session
from flask_session import Session
import redis

app = Flask(__name__)

app.config["SECRET_KEY"] = "xyzxyxyz"
app.config["FLASK_APP"] = "app"
app.config["FLASK_ENV"] = "Development"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.Redis()

Session(app)

@app.route("/", methods=('GET','POST'))
def greeting():
    if request.method == 'POST':
        file = request.files['textfile']
        if file:
            lines = [x.decode('UTF-8') for x in file.readlines()]
            session['file_contents'] = lines
            return redirect (url_for('action'))
    return render_template('greeting.html')

@app.route("/action", methods=('GET','POST'))
def action():
    return render_template('action.html')
```

Start Redis container

```bash
(.venv) $ docker run --name some-redis -d -p 6379:6379 redis
```
redis driver:
https://redis-py.readthedocs.io/en/stable/


Try `r = redis.Redis()` for the connection string
It uses the defaults

```bash
(.venv) $  docker exec -it some-redis redis-cli
127.0.0.1:6379> KEYS *
1) "session:29aadd11-8831-4b2b-8453-0ca323c9f12b"
127.0.0.1:6379> 
127.0.0.1:6379> EXPIRETIME session:29aadd11-8831-4b2b-8453-0ca323c9f12b
(integer) 1696906209
127.0.0.1:6379> QUIT
(.venv) $ 
```

https://unixtime.org/
https://www.epochconverter.com/
1696906209
Mon Oct 09 2023 22:50:09 GMT-0400 (Eastern Daylight Time)

```bash
(.venv) $ date -d @1696906209
Mon Oct  9 10:50:09 PM EDT 2023
```


variable effects

"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" not configured
   - database timeout = 1 month
   - cookie expire time unknown (persists)
       - cookie is a *session* cookie and is handled by the browser. Some browsers do not delete session cookies.

"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" = 30
   - database expires in 30 seconds
   - cookie expire time unknown (persists)
       - cookie is a *session* cookie and is handled by the browser. Some browsers do not delete session cookies.

"SESSION_PERMANENT" = true
"PERMANENT_SESSION_LIFETIME" not configured
   - database timeout = 1 month (default)
   - cookie expire time = 1 month (default)

"SESSION_PERMANENT" = true
"PERMANENT_SESSION_LIFETIME" = 30
   - database expires in 30 seconds
   - cookie expire time = 30 seconds
   - cookie will be replaced by new cookie with new ID after 30 seconds

So, recommended settings are:

```python
app = Flask(__name__)

app.config["SECRET_KEY"] = "xyzxyxyz"
app.config["FLASK_APP"] = "app"
app.config["FLASK_ENV"] = "Development"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.Redis()
app.config["PERMANENT_SESSION_LIFETIME"] = 30

Session(app)
```



NOTE: clearning session only works on the active session, and only for the browser cookies. For example, if you set the *PERMANENT_SESSION_LIFETIME* variable to 30 seconds, then the cookie is deleted after 30 seconds but the user data remains in stuck in the database. 
Also, if you are testing, and clear your browser cache before the timeout occurs, you lose the association with the server-side session so it just stays in the database forever. 
Add more program logic to periodically clean up the database.

https://stackoverflow.com/questions/38455893/flask-session-cleanup-of-expired-sessions


Get current time on db server

```sql
userdata=# select current_time;
```

get database contents:

```sql
userdata=# select * from sessions;
```

```sql
userdata=# select session_id, expiry from sessions;
```




























SQL session

"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" not configured
   - Error

"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" = 30
   - Error

"SESSION_PERMANENT" = true
"PERMANENT_SESSION_LIFETIME" not configured
   - database timeout = 1 month (default)
   - cookie expire time = 1 month (default)

"SESSION_PERMANENT" = true
"PERMANENT_SESSION_LIFETIME" = 30
   - database sets expiry to a timestamp 30 seconds from now, in the row
     - no rows deleted from DB
   - cookie expire time = 30 seconds
       - cookie will be replaced by new cookie with new ID after 30 seconds
   - new DB record for each new cookie, so not good to have short expiry time (for data sizes)

































FileSystem

"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" not configured
   - SESSION_FILE_THRESHOLD seems to have strong effect. It does not matter how new or old a cache file is. As soon as SESSION_FILE_THRESHOLD is exceeded, Flask-Session deletes cache files until number of remaining files are SESSION_FILE_THRESHOLD.
   - files older than PERMANENT_SESSION_LIFETIME will *probably* be deleted even if it brings the total files below SESSION_FILE_THRESHOLD but it is hard to test because the default value is 30 days.
   - Browser cookie sets *Expires/Max-Age* to the value, "session". The cookie's contents expire in PERMANENT_SESSION_LIFETIME seconds but the cookie UUID remains (persists) so Flask-Session sees the same session ID. So, when you upload a new file after PERMANENT_SESSION_LIFETIME seconds, you do not create a new file on the filesystem. You get the same file name because the session ID is still the same. If you want to build up a lot of cache files during testing, you need to manually delete the session cookie using the Browser's developer tools.

"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" = 30
   - SESSION_FILE_THRESHOLD seems to have strong effect. It does not matter how new or old a cache file is. As soon as SESSION_FILE_THRESHOLD is exceeded, Flask-Session deletes cache files until number of remaining files are SESSION_FILE_THRESHOLD.
   - files older than PERMANENT_SESSION_LIFETIME are deleted even if it brings the total files below SESSION_FILE_THRESHOLD
   - Browser cookie sets *Expires/Max-Age* to the value, "session". The cookie's contents expire in PERMANENT_SESSION_LIFETIME seconds but the cookie UUID remains (persists) so Flask-Session sees the same session ID. So, when you upload a new file after PERMANENT_SESSION_LIFETIME seconds, you do not create a new file on the filesystem. You get the same file name because the session ID is still the same. If you want to build up a lot of cache files during testing, you need to manually delete the session cookie using the Browser's developer tools.

"SESSION_PERMANENT" = true (default)
"PERMANENT_SESSION_LIFETIME" not configured
   - SESSION_FILE_THRESHOLD seems to have strong effect. It does not matter how new or old a cache file is. As soon as SESSION_FILE_THRESHOLD is exceeded, Flask-Session deletes cache files until number of remaining files are SESSION_FILE_THRESHOLD.
   - files older than PERMANENT_SESSION_LIFETIME will probably be deleted even if it brings the total files below SESSION_FILE_THRESHOLD but it is hard to test because the default value is 15 minutes.
   - Cookie cookie sets *Expires/Max-Age* to 30 days older than time cookie was created. After cookie expires, it will be replaced by a new cookie with a new UUID, causing a new backend file to be created with a new filename.

"SESSION_PERMANENT" = true (default)
"PERMANENT_SESSION_LIFETIME" = 30
   - SESSION_FILE_THRESHOLD seems to have strong effect. It does not matter how new or old a cache file is. As soon as SESSION_FILE_THRESHOLD is exceeded, Flask-Session deletes cache files until number of remaining files are SESSION_FILE_THRESHOLD.
   - files older than PERMANENT_SESSION_LIFETIME are deleted even if it brings the total files below SESSION_FILE_THRESHOLD
   - Cookie cookie sets *Expires/Max-Age* to a value PERMANENT_SESSION_LIFETIME older than time cookie was created. After cookie expires, it will be replaced by a new cookie with a new UUID, causing a new backend file to be created with a new filename.








[^1]: From [https://www.the-art-of-web.com/sql/trigger-delete-old/](https://www.the-art-of-web.com/sql/trigger-delete-old/). Accessed September, 2023

(maybe change language to sql?)

```sql
CREATE FUNCTION delete_old_rows2() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM sessions WHERE expiry < CURRENT_TIMESTAMP - INTERVAL '30 seconds';
  RETURN NULL;
END;
$$;


CREATE TRIGGER trigger_delete_old_rows
    AFTER INSERT ON sessions
    EXECUTE PROCEDURE delete_old_rows2();
```


or try and event:

```sql
CREATE EVENT `purge_table` ON SCHEDULE
        EVERY 1 DAY
    ON COMPLETION NOT PRESERVE
    ENABLE
    COMMENT ''
    DO BEGIN
DELETE FROM sessions WHERE expiry <= now() - INTERVAL '1 DAY'
END
```

Now, when cookie expires on browser so new session id is created, the new record triggers old records to be deleted

This is OK, but requires I set this up in Postgres outside my Flask app.

I could define this using SQLAlchemy [^2] in my app. But that defeats the original purpose for using Flask-Session, which is to abstract away the management of browser sessions and the back-end storage of user data.

[^2]: For example, after creating an SQLAlchemy engine object, run the following statement: 
```
engine.execute("""
CREATE TRIGGER trigger_delete_old_rows
    AFTER INSERT ON sessions
    EXECUTE PROCEDURE delete_old_rows2();
""")
```

https://stackoverflow.com/questions/27367886/user-defined-function-creation-in-sqlalchemy