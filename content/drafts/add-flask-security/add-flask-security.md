title: Add Flass-Security-Too to a Python web app
slug: flask-security-too-python
summary: After creating a basic web app that has several web pages, I need to add the ability to manage user access and permissions on the app. This post shows how I integrated the Flask-Security-Too extension into my existing web app. 
date: 2024-04-20
modified: 2024-04-20
category: Flask
status: Draft

# Look into Flask-AppBuilder extension


<!--
A bit of extra CSS code to centre all images in the post
-->
<style>
img
{
    display:block; 
    float:none; 
    margin-left:auto;
    margin-right:auto;
}
</style>



Default account routes used by Flask-Security-Too are /login and /register. So my old system using /account/login and /account/register will not work.

i could maybe configure settings like SECURITY_LOGIN_URL (https://flask-security-too.readthedocs.io/en/stable/configuration.html) so the routes appear where I want them but, let's keep things simple and let Flask-Security-Too do what it wants, for now. I will remove the *account* route from my program and use the routes provided by Flask-Security-Too

I changed the *home* blueprint so it has link that allow users to login and register.
Also, the /templates/shared_layout.html -- changed the nav links


To override the templates used by Flask-Security: https://flask-security-too.readthedocs.io/en/stable/customizing.html

1) Go to Flask-Security-Too Git repo
2) Copy the login template (https://github.com/Flask-Middleware/flask-security/blob/master/flask_security/templates/security/login_user.html)
3) Create a folder named security within my app's templates folder
4) Create a template with the same name for the template you wish to override
  a) In this case: /templates/security/login_user.html





First, add database config information to *config.py* and, if needed, *.env*

```python
# mfo/config.py

import os
import dotenv

app_dir = os.path.abspath(os.path.dirname(__file__))
project_dir, _unused = os.path.split(app_dir)

print(project_dir)

dotenv.load_dotenv()

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
ENVIRONMENT = os.environ.get("FLASK_ENVIRONMENT")
DEBUG = os.environ.get("FLASK_DEBUG")
EXPLAIN_TEMPLATE_LOADING = os.environ.get("FLASK_EXPLAIN_TEMPLATE_LOADING")

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")\
     or 'sqlite:///' + os.path.join(project_dir, 'app.db')
SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")


```

Since I want the database to be stored in the project directory, outside the application directory where *config.py* resides, I need to define the path to the project directory as shown above.


```python
# mfo/.env

FLASK_APP = app
FLASK_SECRET_KEY = abcd

FLASK_ENVIRONMENT = development
FLASK_DEBUG = True
FLASK_EXPLAIN_TEMPLATE_LOADING = True

SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Since I did not specify the SQLALCHEMY_DATABASE_URI environment variable, my program will use a default development database named *app.py*, stored in the project folder.

## database

Create a database folder and a *setup.py* file

```python
# mfo/database/setup.py
 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
```

# models

Then create a file containing user models

```python
# mfo/database/models/users.py


```

## app.py

Add `from mfo.database import db` and `db.base.init_app(app)` to the app file to configure flask-sqlalchemy using the Flask app configuration established in the *config.py* file. The add the`db.create_all()` statement to build the database tables, if they do not yet exist

```python
# mfo/app.py

import flask

from mfo.database.setup import db

from mfo.admin import admin
from mfo.home import home
from mfo.account import account


app = flask.Flask(__name__)
app.config.from_pyfile('config.py', silent=True)

# Configure Flask extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(home.bp)
app.register_blueprint(account.bp)
app.register_blueprint(admin.bp)


if __name__ == "__main__":
    app.run()
```



see:
https://flask-security-too.readthedocs.io/en/stable/quickstart.html#basic-sqlalchemy-application
https://github.com/hrishikeshrt/flask-bootstrap-anywhere/tree/master

https://blog.teclado.com/user-authentication-flask-security-too/
https://blog.teclado.com/customise-pages-emails-flask-security-too/