title: Use signals and events in your Flask app
slug: flask-sqlalchemy-signals-events
summary: Create functions that automatically execute when your Flask app performs some other action, like creating a new user.
date: 2024-06-30
modified: 2024-06-30
category: Flask
status: Draft

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
    width:80%;
}
</style>


* [Write a *Flask-Security-Too* event handler](https://stackoverflow.com/questions/76892576/assign-user-role-on-signup-flask-security-too) to assign a default role every time it sees the [signal](https://flask-security-too.readthedocs.io/en/stable/api.html#signals) that a new user is registered.



## Automatically assigning roles for new users

The above example raised the issue of how to we set a default role for all new users. I think it is OK if we must set the *Admin* role manually using the Flask CLI, but all new users who register should be assigned the *User* role.

This can be done using [Flask-Security-Too *signals*](https://flask-security-too.readthedocs.io/en/stable/api.html#signals). 

At first, this seems a bit hard to understand. But, once you realize that you are writing a function to *configure the Flask application*, instead of to call in a some other part of your program, you will see how setting up signals frees you to manage other functionality while relying on Flask to do the right thing every time the conditions for the signal are triggered.

Flask-Security-Too provides signals ready to use. In the main application, *app.py*, just import the *user_registered* signla from the *signal* module:

```python
from flask_security.signals import user_registered
```

Then, near the end of the program, after the app and Flask-Security-Too have been set up, [create the signal handler](https://stackoverflow.com/questions/76892576/assign-user-role-on-signup-flask-security-too):

```python
# Assign "User" role to all newly-registered users
@user_registered.connect_via(app)
def user_registered_sighandler(sender, user, **extra):
    role = "User"
    user_datastore.add_role_to_user(user, role)
```

Ideally, I would have likes to create the signal handler in a blueprint so I keep the main application file clean and simple. However, I could not figure out how to manage the *app* context in another module so I left the signal handler here, for now.

The full *app.py* file now looks like the following:

```python
# mfo/app.py

import flask
from flask_security import Security
from mfo.database.setup import db, create_database
from mfo.database.models.users import user_datastore
from flask_security.signals import user_registered


app = flask.Flask(__name__)
app.config.from_pyfile('config.py', silent=True)

# Register Flask-SQLAlchemy
db.init_app(app)

# Register Flask-Security-Too
app.security = Security(app, user_datastore)

# Register blueprints
from mfo.admin import admin
from mfo.home import home
from mfo.account import account
app.register_blueprint(home.bp)
app.register_blueprint(account.bp)
app.register_blueprint(admin.bp)

# Create application database, if one does not exist
with app.app_context():
    create_database()

# Assign "User" role to all newly-registered users
@user_registered.connect_via(app)
def user_registered_sighandler(sender, user, **extra):
    default_role = app.security.datastore.find_or_create_role(
        name="User", permissions=["user_read", "user_write"]
    )
    user_datastore.add_role_to_user(user, default_role)


if __name__ == "__main__":
    app.run()
```


