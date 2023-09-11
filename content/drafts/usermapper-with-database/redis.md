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
app.config["PERMANENT_SESSION_LIFETIME"] = 30

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

action.html

```
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

base.html

```
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

greeting.html

```
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

