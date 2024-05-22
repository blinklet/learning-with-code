title: Add a navigation bar to your Flask web app
slug: python-flask-navbar
summary: How to create a navigation bar that helps your web app's users understand if they are logged in and to which features they have access
date: 2024-04-30
modified: 2024-04-30
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
}
</style>

Using Flask-Nav3 to build navigation bars
Flask-Nav3 is a fork of Flask-Nav. Flask-Nav is a popular navigation menu package that is no longer maintained, so the developers of Flask-Nav3 forked it to continue its maintenance. At the time I write this post, the developers added Python 3.12 and Bootstrap5 support to Flask-Nav3, and it is at version 0.7.2, released March 12, 2024.

    nav = Nav()
    nav.init_app(app, bootstrap=True)



## My Flask-Nav journey

Flask-Nav3 simply points to [Flask-Nav's documentation](https://github.com/mbr/flask-nav). This is OK, because the functionality is mostly the same. But the docs are very lightweight and it would be greate to see some more examples of how to use Flask-Nav3.


Inspired by [my recent experience trying to use the Flask-Menu package](), I want to place the code for each blueprint's portion of the navbar in a blueprint. This will keep the code that implements navbar items related to the *admin* blueprint in the same folder as the *admin* blueprint's view functions, templates, and other files. I had to look for blogs and StackOverflow answers to figure out how to use Flask-Nav3 in Flask blueprints.

The Flask-Nav3 documentation would make you think you can render a navbar with a simple method call. This will render a simple menu as a bulleted list of links, but I found that I could not style the navigation menu in a way that I liked. I tried writing a custom renderer that would use Bootstrap5 classes to style the navigation menu but I could not make it work. 

In the end, I had to iterate through the navbar object and style each element using HTML in a Jinja2 template. It seems to me that most people who have used Flask-Nav or Flask-Nav3 do the same.

## Create navbar in an existing app

I used Flask-Nav3 to add a simple navigation menu to my current project, a [small Flask app that has two pages]({filename}/articles/030-mfo02-add-flask-security/add-flask-security.md). Follow along with that post to build the application or get the code directly from GitHub and run it, as shown below:

```text
$ wget https://github.com/blinklet/music-festival-organizer/archive/refs/tags/0.002.zip
$ unzip 0.002.zip
$ ls -1
0.002.zip
music-festival-organizer-0.002
$ cd music-festival-organizer-0.002
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ flask --app mfo.app database create
(.venv) $ sh ../tests/make-users.sh
(.venv) $ flask --app mfo.app run --debug
```

You will see that, if you log into the app as the admin user, `admin@testmail.com` with the password `abcd1234`, the app provides two routes: `https://localhost:5000/` and `https://localhost:5000/admin`, as shown below:

![App without a navigation menu]({attach}./images/old-app-01.png){ width=85% }

### Install Flask-Menu

To install Flask-Nav3, add it to the requirements.txt file as follows:

```python
# requirements.txt

flask
python-dotenv
Flask-Security-Too[fsqla,common]
Bootstrap-Flask
Flask-Nav3
```

Then, run the command:

```text
(.venv) $ pip install --force-reinstall -r requirements.txt
```

### Create the *nav* instance

Create a new module in the application folder named *nav.py*. In it, create an instance of the *Nav()* class, named *nav*. 

```python
# mfo/home/nav.py

from flask_nav3 import Nav


nav = Nav()
```

You only want one instance of the *Nav()* class in your program. Creating it in a separate module lets you import it into the main application or into a blueprint file. If you create the instance in your main application file, it can cause the problem of circular imports when you then try to import it into a blueprint file. So, create it in a separate module and import it where it is used.

### Register Flask-Nav3 with the app

Register the *nav* instance using its *init_app()* method. Import the *nav* module and then add the `nav.init_app(app)` method to the application, as shown below:

```python
# mfo/app.py

import flask
from flask_security import Security

import mfo.home.views
import mfo.admin.views
import mfo.database.users as users
import mfo.database.commands
import mfo.database.base as base
import mfo.nav


def create_app():

    # Create app object
    app = flask.Flask(__name__)

    # Configure the app
    app.config.from_pyfile('config.py')

    # Register Flask-SQLAlchemy
    base.db.init_app(app)

    # Register Flask-Security-Too
    app.security = Security(app, users.user_datastore)

    # Register navbars
    mfo.nav.nav.init_app(app)

    # Register blueprints
    app.register_blueprint(mfo.home.views.bp)
    app.register_blueprint(mfo.admin.views.bp)
    app.register_blueprint(mfo.database.commands.bp)

    return app
```

### Create navigation items in blueprints

The existing application already has two blueprint folders: *home* and *admin*. 

(Add login, register, and logout to navbar)


    record(func)

    Registers a function that is called when the blueprint is registered on the application. This function is called with the state as argument as returned by the make_setup_state() method.

    record_once(func)

    Works like record() but wraps the function in another function that will ensure the function is only called once. If the blueprint is registered a second time on the application, the function passed is not called.

    ...This avoids duplicating the navbar elements if the blueprint is registered more than once...

    "state" is an intance of BlueprintSetupState(blueprint, app, options, first_registration)

    A temporary holder object for registering a blueprint with the application. An instance of this class is created by the make_setup_state()

    The state object in the context of @blueprint.record_once is an instance of flask.blueprints.BlueprintSetupState. This object is used during the setup phase of a Flask application to hold the configuration and state needed to register the blueprint with the main application.

    When you use @blueprint.record_once, the function you define will be called with this state object as an argument. The state object contains references to the application and other relevant information needed to set up the blueprint.

    By accessing state.app.extensions['nav'], you retrieve the Nav instance that was registered with the Flask application, allowing you to register the navigation elements within the blueprint's setup phase.

Remember... 

    By ensuring that the Nav instance is initialized with the application before any blueprints are registered, the nav extension will be available when the blueprints' record_once functions are executed.

## Style with default render

## Style each item with bootstrap 

detect active
https://stackoverflow.com/questions/22173041/styling-active-element-menu-in-flask


## Customize Security-Flask-Too templates

...to include navbar

use app_context_manager

From: 
https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.context_processor

    Registers a template context processor function. These functions run before rendering a template. The keys of the returned dict are added as variables available in the template.

    This is available on both app and blueprint objects. When used on an app, this is called for every rendered template. When used on a blueprint, this is called for templates rendered from the blueprint’s views. To register with a blueprint and affect every template, use Blueprint.app_context_processor().

    Like context_processor(), but for templates rendered by every view, not only by the blueprint. Equivalent to Flask.context_processor().

because we need every navbar to be recalculated every time the user is redirected to a new view function, because the dynamic navbars from other blueprints may have changed due to the state of the application.

## Dynamic navbars in blueprints

Check out the @nav.navigation decorator
Would this work in a blueprint?
https://pythonhosted.org/flask-nav/advanced-topics.html#dynamic-construction




Flask-Nav with Blueprints
https://gist.github.com/thedod/eafad9458190755ce943e7aa58355934





## Conclusion

I showed how you can use the Flask-Nav3 library to build dynamic navigation bars for each blueprint in you project, and I showed how to style the menu items using a Jinja2 template.

I discovered that the process of building separate navigation menus for each blueprint could become confusing.

I found that the code required to divide up Flask-Nav3 navbar functionality into multiple blueprints was hard to read and could cause confusion for future developers. 

... not so different than using a navbar template. Would like a more modular approach based on blueprints



context manager
https://stackoverflow.com/questions/71834254/flask-nav-navigation-alternative-for-python-3-10
https://stackoverflow.com/questions/34487967/flask-nav-with-dynamic-secondary-navbar

detect active
https://stackoverflow.com/questions/22173041/styling-active-element-menu-in-flask


https://chat.openai.com/share/30cacaad-6625-4317-b329-c473f9a5901e




flask-nav
https://pythonhosted.org/flask-nav/
supported by flask-bootstrap (https://pythonhosted.org/Flask-Bootstrap/nav.html) but has not been updated in a long time

flask-nav3
https://github.com/wtfo-guru/flask-nav3
A "supported" fork of flask-nav but has only 2 stars
```
pip install flask-nav3
```



Bootstrap navbar class
https://getbootstrap.com/docs/5.2/components/navbar/




(use dictionary as a way to pass in navigation links for the user?)
https://education.launchcode.org/lchs/chapters/more-flask/page-navigation.html


In the main application template, named *base.html*, I added navigation links in a nav bar so we can navigate to the different application routes. The new *base.html* file looks like below:

```html
<!-- mfo/templates/base.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Music Festival Website{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/styles.css" />
    {% block additional_css %}{% endblock %}
</head>

<body>
    <nav>
        <a href="/">Home</a>
        <a href="{{ url_for('account.index') }}">Account</a>
        <a href="{{ url_for('admin.index') }}">Admin</a>
    </nav>

    <div class="content">
        {% block content %}
        <h1>This is a simple example page</h1>
        {% endblock %}
    </div>
</body>
</html>
```


## Dynamic templates based on roles

But, why show users links they can't use?

We modify templates so they show links based on user's roles. We can look at the *current_user.roles* context to evaluate if a user has the role required tio see a specific navbar link.


In the *shared_layout.html* template, add these checks around the *Admin* and *Account* links.


```python
<nav>
    <a href="{{ url_for('home.index') }}">Home</a>
    {% if "Admin" in current_user.roles %}
    <a href="{{ url_for('admin.index') }}">Admin</a>
    {% endif %}
    {% if ("User" in current_user.roles) or ("Admin" in current_user.roles) %}
    <a href="{{ url_for('account.index') }}">Account</a>
    {% endif %}
    {% if not _fs_is_user_authenticated(current_user) %}
    <a href="{{ url_for_security('login') }}">Login</a>
    <a href="{{ url_for_security('register') }}">Register</a>
    {% endif %}
    {% if _fs_is_user_authenticated(current_user) %}
    <a href="{{ url_for_security('logout') }}">Logout</a>
    {% endif %}
</nav>
```

This is a bit "clunky" and there is probably a better way to refactor this so I don't have to revisit the template every time a new role is added to the code. But, for now, this works in our simple navbar.

When you run the app again, you'll find that logged-in users who have the *Admin* role can see the *Admin* and *Account* links. Users who have the *User* role can see the *Account* link. Users who have no role assigned, which is all users who registered via teh *Register* page, will not see either the *Admin* nor the *Account* link in the navbar.

![User with no role assigned](./images/no_role.png)

> Maybe use Flask-Nav?  https://pythonhosted.org/flask-nav/
> This would require a major restructure of how the navbar works. Now, we need to [generate a list of navigation links allowed based on roles](https://stackoverflow.com/questions/33161507/how-can-i-hide-certain-links-in-jinja2-template-engine-using-flask-login-and-per) and pass that list into the template whenever it is rendered.




