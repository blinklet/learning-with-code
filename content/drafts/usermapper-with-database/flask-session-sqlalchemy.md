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
    return render_template('greeting.html', form=form)

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
app.config["PERMANENT_SESSION_LIFETIME"] = 30  # 1 hour
app.config["SESSION_FILE_THRESHOLD"] = 2
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


## Redis?

Try setting up a Redis server?








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



