title: Using Flask-Session to manage user data in a web app
slug: flask-session-sqlalchemy-python
summary: An experiment to see if the Flask-Session extension can be used without Flask-Login to manage ephemeral user sessions. I also test using SQLAlchemy to provide sessions' backend database. 
date: 2023-09-29
modified: 2023-09-29
category: Flask
<!-- status: Published -->

Where is flask-session data stored in the filesystem?
https://stackoverflow.com/questions/32084646/flask-session-extension-vs-default-session
https://testdriven.io/blog/flask-server-side-sessions/
https://stackoverflow.com/questions/53841909/clean-server-side-session-files-flask-session-using-filesystem
https://dev.to/hackersandslackers/managing-session-data-with-flask-session-redis-360n


Use the [Flask-Session](https://flask-session.readthedocs.io/en/latest/) extension. This creates server-side user sessions for Flask but it also requires a "backend" to store the user data on the server. You can use the system memory, filesystem, or a database.

In this post, we will create a simple program that uses the filesystem backend and, after we have that working, we will test a database backend. The filesystem backend is suitable for development but most developers will plan to use the database backend in production.



## Set up Python environment

Prepare a Python virtual environment and the dotenv file for local development.

```bash
$ mkdir experiment
$ cd experiment
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $
```

```bash
(.venv) $ pip install flask
(.venv) $ pip install Flask-Session
```

## Create basic Flask templates

Let's have a base template and two page templates that display different pages: a greetings page that gathers some user data, and an action page that displays it back to the user.

I re-used code from my *[usermapper-web]({filename}/articles/003-flask-web-app-tutorial/flask-web-app-tutorial.md)* application to make these templates. I decided to keep the [Bootstrap](https://getbootstrap.com/) code because it makes the page look good.

Create a *templates* directory:

```bash
mkdir templates
```
### Base template

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

### Greeting template

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

### Action template

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

## Create a session

(Flask-Session creates a cookie for the user called "session" that contains a UUID for that user)
Get the Flask-Session ID by looking for "session".

Edit a file named *app.py*:

```nash
(.venv) $ nano app.py
```
At the top of the *app.py* file add the following import statements:

```python
from flask import Flask, request, redirect, url_for, render_template, session
from flask_session import Session
```

In the application configuration section, set the following configuration environment variables for the Flask app and for the sessions to be created:

```python
app = Flask(__name__)

app.config["SECRET_KEY"] = "xyzxyxyz"
app.config["FLASK_APP"] = "app"
app.config["FLASK_ENV"] = "Development"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
```

Create the Flask routes for the index page, which I call the *greeting* route, and the page that displays the file, which I call the *action* route. I am not checking for valid inputs or ensuring that the file is really a text file. I am keeping this code very simple so i can better demonstrate the way *Flask-Session* works.

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

@app.route("/action", methods=('GET','POST'))
def action():
    return render_template('action.html')
```

I used the Flask request *[files](https://flask.palletsprojects.com/en/2.3.x/api/#flask.Request.files)* property to get the objected named "textfile" when the form is submitted, which generates a *POST* request.

Flask uploads the file as a byte stream. The file's readlines() method outputs a list of rows but each row is a binary string. I need to convert each row in the list from bytes to UTF-8 character code points. The list comprehension in the *greeting* route, above, creates a new list named "lines" that contains the same rows but each row is now a UTF-8 string.

Save the file.

## Test the app

Test this first version of the app 

```bash
(.venv) flask run
```

Open a browser and enter in the URL where the Flask server is running:

```text
http://localhost:5000
```

The application will look like the following

![Flask app]({attach}session-001.png)

Create a dummy text file and save it. Add some dummy text to it.

Then upload the file using the web app and click the *Upload* button.

You should see output similar to the screenshot below:

![Flask app]({attach}session-002.png)

Now, look at the session information created on the filesystem. The session file should be saved in a directory, created by Flask-Session, named *flask_session*. It will be in the same location as the *app.py* file.

```bash
(.venv) $ ls flask_session
2029240f6d1128be89ddc32729463129  c4bf6e3ffacc6daeb6bfbfd9d5e54865
```

This shows two sessions on the server. There should also be two session cookies in your browser that correspond with the server-side sessions.

One was created when I first opened the URL in the web browser and the second was created when I uploaded a file and it contains the file contents for the current user. I don't know why the first session was not used to store the file. 

# answer: https://stackoverflow.com/questions/75858664/flask-session-filesystem-session-files-are-not-deleted-after-permanent-sessio

I did not configure encryption so you should be able to see the contents of the sessions:

```bash
(.venv) $ cat -A 2029240f6d1128be89ddc32729463129
^@^@^@^@M-^@^EK^B.(.venv) $
(.venv) $
(.venv) $ cat -A c4bf6e3ffacc6daeb6bfbfd9d5e54865
M-ZF#eM-^@^EM-^UM-^X^@^@^@^@^@^@^@}M-^TM-^L^Mfile_contentsM-^T]M-^T(M-^L^XThis is the first line^M$
M-^TM-^L^B^M$
M-^TM-^L^_    The next line is indented^M$
M-^TM-^L^B^M$
M-^TM-^L(Some special characters are %, &, <, >^M$
M-^TM-^L^KLast line^M$
M-^Tes.(.venv) $
(.venv) $
```

I configured the *SESSION_PERMANENT* environment variable as *False* so that sessions would be deleted when not used anymore. Flask-Session does not immediately delete unused sessions. It waits for some threshold to be reached before it deletes unused session. For example, if you set *SESSION_FILE_THRESHOLD* from its default value of `500` to a very low value, like `1`, you can see that Flask Session will delete older files when there are more than one in the *flask-session* folder, effectively limiting the app to one user at a time. New users overwrite the other user's session, causing them to lose their data.



"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" not configured
   - files remain in folder after session expires
     - SESSION_FILE_THRESHOLD has no affect
   - file names do not correspond to session UUIDs in session cookie (filename: 7ce5a9e059f23c82ec6ff3b9383eb4a5, session UUID in browser: session:"ae1fa662-088d-49a9-8f4a-e3183893cd45")
   - cookie expire time unknown (persists)
       - cookie is a *session* cookie and is handled by the browser. Some browsers do not delete session cookies.

"SESSION_PERMANENT" = false
"PERMANENT_SESSION_LIFETIME" = 30
   - files remain in folder after session expires
     - SESSION_FILE_THRESHOLD has no affect
   - cookie contents expire in 30 seconds but cookie remains (persists) so does not create a new file on system. Existing file name is reused for data for a new session so does not trigger directory cleanup.
       - cookie is a *session* cookie and is handled by the browser. Some browsers do not delete session cookies.

"SESSION_PERMANENT" = true (default)
"PERMANENT_SESSION_LIFETIME" not configured
   - files cleaned up after 5 minutes, which is the default value for PERMANENT_SESSION_LIFETIME, when a new session is added (when "Upload" button is clicked)
     - SESSION_FILE_THRESHOLD required for easy testing. Cleanup happens after limit reached (default is 500 so for texting need to set it lower)
   - cookie expire time = one month
    - cookie will be replaced by new cookie with new ID after 30 seconds, so triggers 

"SESSION_PERMANENT" = true (default)
"PERMANENT_SESSION_LIFETIME" = 30
   - files cleaned up after PERMANENT_SESSION_LIFETIME, when new session is added (when "Upload" button is clicked)
     - SESSION_FILE_THRESHOLD required for easy testing. Cleanup happens after limit reached (default is 500 so for texting need to set it lower)
     - **SESSION_FILE_THRESHOLD overrides PERMANENT_SESSION_LIFETIME. If there are more that x files, Flask-Session deletes files until the threshold is met, regardless of their lifetime.**
   - cookie expire time = 30 seconds
    - cookie will be replaced by new cookie with new ID after 30 seconds, so triggers 

9eb774d49bff1dc28b49c895aff742d2
fa9b99c03dec723a22b0b966f9e0b075

## Adding a database

Now, let's explore using a database as the backed.

Use SQLAlchemy

```bash
(.venv) $ pip install flask-sqlalchemy
(.venv) $ pip install psycopg2
```


### Set up the database

The easiest way to start a database server for testing is to use Docker. Set up a Docker container that is running a PostgreSQL database. You may run the commands listed below and, if you wish, you may see more details about running a PostgreSQL database in a Docker container in my [previous post]({filename}/articles/018-postgresql-docker/postgresql-docker.md).

Use the official [PostgreSQL Docker image](https://hub.docker.com/_/postgres) from the *Docker Hub* container library. Open a terminal on your Linux PC and run the Docker *run* command:

Create a new database container named *userdb* from the Postgres image. Set the admin password and define a user. Setting the user also creates a database with the same name as the user. In this case, I created a user named *userdata*. Run the Docker *run* command:

```bash
$ docker run \
    --detach \
    --env POSTGRES_PASSWORD=abcd1234 \
    --env POSTGRES_USER=userdata \
    --publish 5432:5432 \
    --name userdb\
    postgres
```

Use the Docker *exec* command to run the *psql* utility on the container to check that the database server is running. Start it in interactive mode on the container. Use the username, *userdata*, which connects to the database, *userdata*:

```bash
$ docker exec -it userdb \
    psql --username userdata

sessions=#
```

Now you can be confident that the database is ready to use. Quit the *psql* utility:

```text
sessions=# \q
$ 
```

### Set up the database in your program

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database


In *app.py*, add the following code under the existing import section to identify the database:

```python
uri = "postgresql://userdata:abcd1234@localhost:5432/userdata"
```

The change the app configuration. The *SESSION_PERMANENT* environment variable must be set to *True* or the database will generate type errors. To automatically clear old sessions, add the *PERMANENT_SESSION_LIFETIME* environment variable. 

```python
app = Flask(__name__)

app.config["SECRET_KEY"] = "xyzxyxyz"
app.config["FLASK_APP"] = "app"
app.config["FLASK_ENV"] = "Development"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config['SQLALCHEMY_DATABASE_URI'] = uri

Session(app)
```

Then add the following code to initialize the database.
This is a [workaround](https://stackoverflow.com/questions/45887266/flask-session-how-to-create-the-session-table) that is not well documented because the Flask-Session SQLAlchemy interface does not so it when you initialze the Session.

```python
Session(app)
with app.app_context():
    app.session_interface.db.create_all()
```

You need to use the *with app.app_context()* block to manually make the Flask app's [application context](https://flask.palletsprojects.com/en/2.3.x/appcontext/) available to the *app.session_interface.db.create_all()* function. Flask normally manages the application context for you but, in this case, we are manually initializing the database outside of a Flask route or view. 

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
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour
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

You can see how easy it was to change to a database backend. You could change the session type back to FileSystem just as easily.

However, Flask-Session does not seem to manage the sessions in the database well and leaves the data there for us to manage later.

**will not use Flask-Session for my usermapper web app because I plan to use an SQL database for it, because I get one for free on Azure**

```bash
userdata=# SELECT id, session_id, expiry FROM sessions;
 id |                  session_id                  |           expiry
----+----------------------------------------------+----------------------------
  1 | session:a84b86a7-579b-4213-9133-2676812b8759 | 2023-09-08 21:34:02.670951
  2 | session:58f4a217-1f5b-4a1a-a5ed-38dfa4b43def | 2023-09-08 22:13:32.22257
(2 rows)
```

```bash
userdata=# SELECT now();
              now
-------------------------------
 2023-09-11 17:30:39.633867+00
(1 row)
```

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


The following SQL code snippet [^1], from [The Art of Web Blog](https://www.the-art-of-web.com/sql/trigger-delete-old/), will configure postgres to clear old rows based on a trigger. In this case, the function us triggered when a new row is inserted into the *sessions* table.

[^1]: From [https://www.the-art-of-web.com/sql/trigger-delete-old/](https://www.the-art-of-web.com/sql/trigger-delete-old/). Accessed September, 2023

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



