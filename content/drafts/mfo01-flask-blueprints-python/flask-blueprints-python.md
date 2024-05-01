title: Use blueprints to organize a Flask application
slug: flask-blueprints-python-templates
summary: This post demonstrates Flask blueprints and clearly describes the rules Flask follows when searching for template files in blueprint folders, and provides concrete examples.
date: 2024-04-01
modified: 2024-04-01
category: Flask
<!-- status: published -->


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

I am starting a large Flask project so I needed to define the project structure. After some research and testing, I decided I will organize application code and resources into [Flask Blueprints](https://flask.palletsprojects.com/en/3.0.x/blueprints/). 

I wrote this post to clearly describe the rules Flask follows when searching for template files, and to provide concrete examples. Flask searches for blueprint templates in all registered template folders. I hope this post helps readers better understand which template or static file will be rendered by each view function. I want to save readers from experiencing the same aggravation I encountered when I started developing the view functions and template files in a large Flask application.

## A small example

I start with a small "toy" application, similar to that which you may have seen in many other Flask tutorials. Then, I will add blueprints and additional functionality.

First, I created a project folder that contains a sub-folder with the application source code. The project folder also contains a *[dotenv](https://learningwithcode.com/use-environment-variables-python)* file that defines environment variable values used to configure the application, and a *requirements.txt* file.

```text
$ mkdir project
$ cd project
$ mkdir mfo
$ mkdir mfo/templates
$ touch mfo/templates/index.html
$ mkdir -p mfo/static/css
$ touch mfo/static/css/style.css
$ touch requirements.txt
$ touch .env
$ touch mfo/app.py
$ touch mfo/config.py
```

The initial project structure is shown below:

```text
project
├── mfo
│   ├── app.py
│   ├── config.py
│   ├── static
│   │   └── css
│   │       └── style.css
│   └── templates
│       └── index.html
├── .env
└── requirements.txt
```

The application is called *MFO* so the application folder is named *mfo*.

### The Flask application file

In this simple example, the Flask application file *app.py* creates the Flask app object, configures it, and defines a single view function. 

```text
$ nano mfo/app.py
```

The file is listed below:

```python
# mfo/app.py

import flask


def create_app():

    # Create app object
    app = flask.Flask(__name__)

    # Configure the app
    app.config.from_pyfile('config.py')

    # Define a view function
    @app.route('/')
    def index():
        return flask.render_template('/index.html')
        
    return app
```

### The configuration files

Two files work together to provide some initial configuration to the Flask application: the *config.py* file and the *dotenv* file.

#### config.py

The *config.py* file reads environment variable values and uses them to define the [application configuration values](https://flask.palletsprojects.com/en/3.0.x/config/#builtin-configuration-values).

```text
$ nano mfo/config.py
```

The *config.py* file contents are listed below:

```python
# mfo/config.py

import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
ENVIRONMENT = os.environ.get("FLASK_ENVIRONMENT")
DEBUG = os.environ.get("FLASK_DEBUG")
EXPLAIN_TEMPLATE_LOADING = os.environ.get("FLASK_EXPLAIN_TEMPLATE_LOADING")
```

By default, the *dotenv.load_dotenv()* method looks for the *dotenv* file in the current working directory or any parent directories and sets the shell's environment variables with the values found in that file. If environment variables are already set in the shell, the *load_dotenv()* method will not overwrite them.

#### .env

Create a *dotenv* file, named *.env*:

```text
$ nano .env
```

The *.env* file contents are listed below: 

```python
# .env

FLASK_APP = app
FLASK_SECRET_KEY = abcdFakeKey1234

FLASK_ENVIRONMENT = development
FLASK_DEBUG = True
FLASK_EXPLAIN_TEMPLATE_LOADING = True
```

Note that the *FLASK_EXPLAIN_TEMPLATE_LOADING* variable must be set to *True* so that Flask will display the template search paths on the terminal when it tries to render a template file. We will use this when debugging template problems later in this tutorial.

### The template file

Most Flask sites use a base template that defines the common look of the web site. Other templates will extend the base template to create specific web pages.

Create the base template, *mfo/templates/base.html*:

```text
$ nano mfo/templates/base.html
```

The base template is listed below:

```html
<!-- mfo/templates/base.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Example Website{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/styles.css" />
    {% block additional_css %}{% endblock %}
</head>

<body>
    <div class="content">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

Then, create an *index.html* template that contains the content to be displayed when the application calls the *index* view function.

```text
$ nano mfo/templates/index.html
```

```html
<!-- mfo/templates/index.html -->

{% extends "base.html" %}

{% block title %}Home page{% endblock %}

{% block content %}
    <h1>Home page</h1>
{% endblock %}
```


### The CSS file

Flask applications store CSS files in the *static* folder. To demonstrate how blueprints use their own *static* folders, I created a small bit of CSS styling for the base template. The base CSS file is named *styles.css* and is stored in the *mfo/static/css* directory:

```text
$ nano mfo/static/css/styles.css
```

The file contents are listed below:

```css
/*  mfo/static/css/styles.css  */

.content {
    padding: 20px;
}

h1 {
    font-weight: bold;
    color: rgb(0, 0, 0);
    font-size: 32px;
  }
```

## Testing the application

To test this simple example, install the required packages and run the Flask program.

First, create a *requirements.txt* file in the project folder:

```text
$ nano requirements.txt
```

The file contents are listed below:

```text
# requirements.txt

flask
python-dotenv
```

Then, create virtual environment in the project folder.

```text
$ python3 -m venv .venv
```

Finally, activate the virtual environment and install the requirements:

```text
$ source .venv/bin/activate
(venv) $ pip install -r requirements.txt
```

From the project folder, run the flask application:

```text
$ flask --app mfo.app run
```

Open a web browser and navigate to *http://localhost:5000*. You will see that the app serves up the base template and that its HTML code is styled as defined by the base CSS file:

![Home page]({attach}basic-page-01.png)

When you look at the terminal screen, you should see some output that shows how Flask searched for the *index.html* and *base.html* templates and the CSS file.

```text
[2024-04-30 12:31:18,140] INFO in debughelpers: Locating template '/index.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> found ('/home/brian/project/mfo/templates/index.html')
[2024-04-30 12:31:18,144] INFO in debughelpers: Locating template 'base.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> found ('/home/brian/project/mfo/templates/base.html')
127.0.0.1 - - [30/Apr/2024 12:31:18] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Apr/2024 12:31:18] "GET /static/css/styles.css HTTP/1.1" 200 -
```

No blueprints are defined yet so Flask has only one search path for template files. As you can see in the example above, the current search path is: *project/mfo/templates/*.

### Next steps

That was the basic scenario: Flask had only one folder in which it could look to find template files and one folder in which it could look to find static files like CSS files.

Next, we will move the view functions into Flask blueprint folders and register Flask blueprints. This will show how Flask finds template and static files in those folders.

## Create a Flask blueprint for the home page

Flask Blueprints are a powerful feature in Flask that allow you to organize your application into smaller, reusable components, which improves application maintainability and scalability. A Flask blueprint organizes a related group of views, templates, static files, and other code around a specific feature or sub-application. 

When you define a blueprint, you can specify folders for templates and static files that are local to that blueprint. This encapsulation makes it easier to manage resources that are specific to a component.

By default, Flask looks for templates in the templates folder at the root of your application. For blueprints, you can set a *template_folder* that points to a folder relative to the blueprint's Python file. This allows blueprints to have their own isolated set of templates.

Similar to templates, you can specify a *static_folder* for each blueprint to keep its static files, such as CSS, JavaScript, and images, organized and separate from those of other blueprints or the main application.

I will restructure the *home* page as a blueprint with its own view functions, templates, and static files.


### Create the blueprint folder

Create a new folder named *home* in the *mfo* folder. In it, create subfolders named *templates* and *static/css*:

```text
$ pwd
/home/brian/project/
$ mkdir mfo/home
$ mkdir mfo/home/templates
$ mkdir -p mfo/home/static/css
```

### Move the home page template to the *home* blueprint

Move the *index.html* template from the main application *templates* folder to the blueprint's *templates* folder:

```text
$ mv mfo/templates/index.html mfo/home/templates/
```

### Move view functions from app to blueprint

Create a file named *views.py* in the *home/* folder. 

```text
$ nano mfo/home/views.py
```

Move the *index* view function from the *app.py* file to this new *views.py* file and declare it as a blueprint view function. This way, the *app.py* file will exclusively contain application configuration code and all the application's actual functionality will be separated into easy-to-manage blueprints.

The *home* blueprint is a special case. It contains the view functions used by the application's home page so we want the URL prefix to be the application's root folder instead of the blueprint folder. So, we do not define the *url_prefix* attribute.

We did not need to create any template files for the home blueprint's *index.html* function because the blueprint's URL prefix is the application's root folder so the existing *index.html* template in the *mfo/templates* folder will be used.

```python
# mfo/home/views.py

import flask

bp = flask.Blueprint(
    'home',
    __name__,
    static_folder='static',
    template_folder='templates'
    )

@bp.route('/')
def index():
    return flask.render_template('index.html')
```

In this special case, the bluepint's *url_prefix* is the same as the main application's prefix, which is the root URL, "/". So, we do not need to define the blueprint's *template_folder* or *static_fol.

### Register the *home* blueprint

Then, change the *app.py* file. Remove the view function and replace it with the blueprint registration. Be sure to import the file containing the blueprint.

```text
$ nano mfo/app.py
```

The new *app.py* file looks like the following:

```python
# mfo/app.py

import flask
import mfo.home.views

def create_app():

    # Create app object
    app = flask.Flask(__name__)

    # Configure the app
    app.config.from_pyfile('config.py')

    # Register blueprints
    app.register_blueprint(mfo.home.views.bp)

    return app
```

When testing the application, now, it should appear to work the same as before. We re-organized the application but did not change or add any functionality. We moved the view function logic for the home page routes to the *home* blueprint.

You can see how the Flask program searched for the *index.html* template by looking at the terminal. See the output generated by Flask. It shows Flask looked in two places for the template file: the main application's *templates* folder and the *home* blueprint's *templates* folder. It found it in the *home* blueprint's *templates* folder.

```text
[2024-04-30 20:32:39,610] INFO in debughelpers: Locating template 'index.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> no match
    2: trying loader of blueprint 'home' (mfo.home.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/home/templates
       -> found ('/home/brian/project/mfo/home/templates/index.html')
[2024-04-30 20:32:39,614] INFO in debughelpers: Locating template 'base.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> found ('/home/brian/project/mfo/templates/base.html')
    2: trying loader of blueprint 'home' (mfo.home.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/home/templates
       -> no match
127.0.0.1 - - [30/Apr/2024 20:32:39] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Apr/2024 20:32:39] "GET /static/css/styles.css HTTP/1.1" 304 -
```

## Create the *account* blueprint

I want to create a new page for "accounts". It will eventually support functions like logging into a user account, displaying user information if the user is logged in, and registering new users. For now, it will just be a dummy page with two links to a "login" dummy page and a "register" dummy page. The URL for the account page will be */account*, and the same URL will be the prefix for all account management pages.

I will also implement this new page as a blueprint with its own view functions, templates, and static files.

In the *mfo* application folder, I created a new folder named *account*. In that folder, I also created new subfolders named *template* and *static*, which will contain the template files and CSS files that support the "accounts" page.

```text
$ mkdir mfo/account
$ mkdir mfo/account/templates
$ mkdir -p mfo/account/static/css
```

### Create the blueprint

In the *account* blueprint folder, I created a views file containing the blueprint definition and the routes supported by the blueprint. 

```text
$ nano mfo/account/views.py
```

Define the *account* blueprint. This time we will declare the template and static folder because we will have a unique URL prefix for this blueprint and we want it to have its own resources.

```python
# account/views.py

import flask

bp = flask.Blueprint(
    'account',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/account',
    )
```

Set the *url_prefix* to */account*. All URLs related to this blueprint will start with that prefix. For example, Flask will look for templates in the *mfo/account/templates* folder. 

Then, create the view functions that will render the *index.html* template associated with the *account* blueprint:


```python
@bp.route('/')
def index():
    return flask.render_template('index.html')
```

> **Note:** This is actually incorrect, but I am using it to illustrate the main thesis of this post.

### Register the blueprint

Modify the main Flask application file so it imports the *account* blueprint and registers it. 

```text
$ nano mfo/app.py
```

The new *app.py* file will look like below:

```python
# mfo/app.py

import flask
import mfo.home.views
import mfo.account.views

def create_app():

    # Create app object
    app = flask.Flask(__name__)

    # Configure the app
    app.config.from_pyfile('config.py')

    # Register blueprints
    app.register_blueprint(mfo.home.views.bp)
    app.register_blueprint(mfo.account.views.bp)

    return app
```

### The blueprint static folder

Create a CSS file named *styles.css* in the *account* template to demonstrate how the blueprint finds its own bundled static files. 

```text
$ nano mfo/account/static/css/styles.css
```

The main application's CSS file colored all *Heading1* tags black, along with other styles, but the CSS file in the *account* blueprint will change *Heading1* text to red. 

```css
/* mfo/account/static/css/styles.css */

h1 {
    color: rgb(255, 0, 0);
  }
```

Any template used by the *account* blueprint can add this additional CSS file and, in this example, the *login.html* template will add this CSS file. 

### The *account* blueprint's *index.html* template

Create an *index.html* template that will serve as the *account* main page. It will contain some information about a user's account.

```text
$ nano mfo/account/templates/index.html
```

The new template also points to the blueprint's CSS file using the Flask *url_for()* method. The blueprint's CSS file will extend the CSS from the Flask application's main CSS file. This demonstrates how the blueprint finds its own bundled static files.

```html
<!-- account/templates/index.html -->

{% extends "base.html" %}
{% block title %}User Information{% endblock %}

{% block content %}
    <div>
        <h1>Your user account</h1>

        <div>
            Welcome to your account!
        </div>
    </div>
{% endblock %}

{% block additional_css %}
    <link rel="stylesheet" href="{{ url_for('account.static', filename='css/styles.css') }}" >
{% endblock %}
```

### *url_for()* usage with blueprints

In Flask, the handling of static files and templates can vary significantly between the main application and blueprints, primarily due to how Flask's *url_for()* method resolves paths. For the main application, templates and static files are typically stored in default directories (templates and static, respectively). When referencing these files, *url_for()* simply requires the filename as its argument, since it automatically refers to these default directories. 

However, in the context of blueprints, each blueprint can have its own static and templates folders, which allows them to operate somewhat independently of the main application structure. When using *url_for()* to generate URLs for static files within a blueprint, you need to include the blueprint's name as a prefix. For example, *url_for('account.static', filename='css/styles.css')* tells Flask to look in the static folder of the *account* blueprint and to find the file *css/styles.css* in that static folder. 

This organization helps in keeping resources localized to the blueprint, enhancing modularity and maintainability of the application. Templates within blueprints are referenced similarly, which ensures that Flask renders the correct template even if multiple blueprints have templates with the same name by maintaining a unique namespace for each blueprint.

### Testing the *account* blueprint

Test the blueprint by running the flask application and entering the *account* blueprint's URl, *http://localhost:5000/account*, in the web browser. 

![Wrong template for *account* page]({attach}basic-page-02.png)

You expect to see the account template with red text and some information about the account page. Instead, you see the main application's home page again.

Look at the terminal and see how Flask searched for the template:

```text
[2024-04-30 20:48:59,963] INFO in debughelpers: Locating template 'index.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> no match
    2: trying loader of blueprint 'home' (mfo.home.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/home/templates
       -> found ('/home/brian/project/mfo/home/templates/index.html')
    3: trying loader of blueprint 'account' (mfo.account.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/account/templates
       -> found ('/home/brian/project/mfo/account/templates/index.html')
Warning: multiple loaders returned a match for the template.
  The template was looked up from an endpoint that belongs to the blueprint 'account'.
  Maybe you did not place a template in the right folder?
  See https://flask.palletsprojects.com/blueprints/#templates
[2024-04-30 20:48:59,967] INFO in debughelpers: Locating template 'base.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> found ('/home/brian/project/mfo/templates/base.html')
    2: trying loader of blueprint 'home' (mfo.home.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/home/templates
       -> no match
    3: trying loader of blueprint 'account' (mfo.account.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/account/templates
       -> no match
127.0.0.1 - - [30/Apr/2024 20:48:59] "GET /account/ HTTP/1.1" 200 -
127.0.0.1 - - [30/Apr/2024 20:49:00] "GET /static/css/styles.css HTTP/1.1" 304 -
```

The Flask *render_template()* method in the *account* blueprint's *index()* view function looked for it's template named *index.html*. However, it found multiple templates named *index.html* and chose to use the first one it found, which happened to be the one in teh *home* blueprint's templates folder.

The wrong template was used because the application is looking in all *templates* folders for a file named *index.html*. It uses the first *index.html* file it finds.

## Fix the template problem

To solve this problem, you must give every Flask template file a unique name. The [Flask documentation recommends creating a seemingly-redundant folder](https://flask.palletsprojects.com/en/3.0.x/blueprints/#templates) in the blueprint's *templates* directory that has the same name as the blueprint, and storing the template files there. This creates a unique "namespace" for each blueprint's template files. 

For example: all *account* template files will be stored in the folder: *mfo/account/templates/account* and will be referenced in the *render_template()* method with a name that includes the extra *account* folder as a prefix. For example, the *account* blueprint's index template would be referenced as *account/index.html*.

First, create the *account* subfolder and move the *account* blueprint's *index.html* template file to it:

```text
$ mkdir mfo/account/templates/account
$ mv mfo/account/templates/index.html mfo/account/templates/account/
```

Then, in the *account* blueprint's *views.py* file, change the file name used when you call Flask's *render_template* method from */index.html* to */account/index.html*:

```text
$ nano mfo/account/views.py
```

The new version of *views.py* will look like below:

```python
# account/views.py

import flask

bp = flask.Blueprint(
    'account',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/account',
    )

@bp.route('/')
def index():
    return flask.render_template('/account/index.html')
```

If we want to use the file name *index.html* for the "main" template associated with each blueprint, then we also need to ensure the home page template has its own unique namespace. 

To give the home page template its own namespace, move the *home* blueprint's *index.html* template to a new *home* subfolder its *templates* folder.

```text
$ mkdir mfo/home/templates/home
$ mv mfo/home/templates/index.html mfo/home/templates/home/
```

Finally, modify the *home* blueprint's *views.py* file so it will reference the new home template location:

```text
$ nano mfo/home/views.py
```

The changes will look like below:

```python
# mfo/home/views.py

import flask

bp = flask.Blueprint(
    'home',
    __name__,
    static_folder='static',
    template_folder='templates'
    )

@bp.route('/')
def index():
    return flask.render_template('home/index.html')
```
 
### Verify that the template namespaces work

When you run the Flask app again and go to the URL, *http://localhost:5000/account*, you see the page you expected, with red text in the header and displaying account options. 

![Account page template]({attach}blueprint-pages-01.png)

This proves that the Flask application is serving the *account* blueprint's *index.html* template and is incorporating the *account* blueprint's additioanl CSS styles, saved in the blueprint's *static* folder.

You can also verify Flask found the correct app by tracing the template search paths in the terminal:

```text
[2024-04-30 20:57:25,349] INFO in debughelpers: Locating template '/account/index.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> no match
    2: trying loader of blueprint 'home' (mfo.home.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/home/templates
       -> no match
    3: trying loader of blueprint 'account' (mfo.account.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/account/templates
       -> found ('/home/brian/project/mfo/account/templates/account/index.html')
[2024-04-30 20:57:25,355] INFO in debughelpers: Locating template 'base.html':
    1: trying loader of application 'mfo.app'
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/templates
       -> found ('/home/brian/project/mfo/templates/base.html')
    2: trying loader of blueprint 'home' (mfo.home.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/home/templates
       -> no match
    3: trying loader of blueprint 'account' (mfo.account.views)
       class: jinja2.loaders.FileSystemLoader
       encoding: 'utf-8'
       followlinks: False
       searchpath:
         - /home/brian/project/mfo/account/templates
       -> no match
127.0.0.1 - - [30/Apr/2024 20:57:25] "GET /account/ HTTP/1.1" 200 -
127.0.0.1 - - [30/Apr/2024 20:57:25] "GET /static/css/styles.css HTTP/1.1" 304 -
127.0.0.1 - - [30/Apr/2024 20:57:25] "GET /account/static/css/styles.css HTTP/1.1" 304 -

```

Here, you see the template */account/index.html* is found in only one place: the *mfo/account/templates/* folder. And you can see that the */css/styles.css* file is found in the *mfo/account/static/* folder.

### Explaining the template search path

The Flask developers wanted you to be able to "override" one template file with another of the same name if you wanted to. So, [Flask searches every *templates* folder](https://realpython.com/flask-blueprint/#including-templates) in your application for templates with the same name and chooses the folder that was registered first. 

This is why you need to use the naming convention we use with the seemingly unneccessary template folder structure. You need a unique string to identify the template if you are using generic filenames like *index.html*. So */account/index.html* is unique.

This behaviour can be useful when working with Flask extensions. For example, you could replace the Flask-Security *login* template with one of your own simply by creating a template named *security/login.html* and placing it in your main application's *templates* folder.

## Project review

After [learning the basics of Flask]([previous](https://learningwithcode.com/flask-web-app-tutorial)), I wanted to create a program structure that followed the generally-accepted practices of Flask application organization. So, I am using the [blueprint structure recommended in the Flask documentation](https://flask.palletsprojects.com/en/3.0.x/blueprints/), which keeps all code related to each blueprint in the its blueprint folder.

I decided that each page served by the application will have its own blueprint and each blueprint will be fully self-contained with its own resource files.

The application's high-level folder structure looks like below.

```text
mfo
├── account/
├── home/
│
├── static/
├── templates/
│
├── app.py
└── config.py
```

In the application's root folder, I have the main flask app named *app.py*, a config file named *config.py* and the standard Flask resource folders, *static* and *templates*. Then, I have two blueprint folders named *account* and *home*. 

The *account* and *home* blueprint folders each has its own view functions and its own *templates* and *static* sub-folders.

### Why this structure?

There are some alternative application structures one could consider. These organize the blueprint view files all in one folder and have common *templates* and *static* folders for the entire application. See the [DigitalOcean Flask blueprint tutorial](https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy) for an example. 

### The final structure

I show my complete project structure, below. This is a good base to start almost any Flask project from.

```text
project
├── mfo
│   │
│   ├── account
│   │   ├── static
│   │   │   └── css
│   │   │       └── styles.css
│   │   ├── templates
│   │   │   └── account
│   │   │       └── index.html
│   │   └── views.py
│   │
│   ├── home
│   │   ├── static
│   │   │   └── css
│   │   ├── templates
│   │   │   └── home
│   │   │       └── index.html
│   │   └── views.py
│   │
│   ├── static
│   │   └── css
│   │       └── styles.css
│   ├── templates
│   │   └── base.html
│   │
│   ├── app.py
│   └── config.py
│
├── .env
└── requirements.txt
```

## Conclusion

This post described a folder structure for a "real" Flask application and excercised using Flask blueprints to divide application functions into separate folders and files. This makes large Flask programs easier to maintain.
