title: Flask Web App Tutorial
slug: flask-web-app-tutorial
summary: Use Python and the Flask framework to build a web app that re-uses code from an existing command-line application and enables users to run the application on a website, instead of installing and running it locally on their PC.
date: 2020-11-30
modified: 2020-12-16
category: Python
status: published

<!--
A bit of extra CSS code to make all images are centered in the post
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

Most network engineers don't need to create web sites but they may, like me, want to convert their existing Python command-line programs into web apps so others can use them more easily. This tutorial presents the minimum you need to know about Python, Flask, and the Bootstrap CSS framework to create a practical web app that looks professional.

This tutorial covers a different type of use-case than is usually demonstrated in Flask tutorials aimed at beginners. It shows you how to create a web app that "wraps up" another Python program's functionality.

![flask-120-1024p]({static}/images/flask-web-app-tutorial/flask-120-1024p.png)

I will show you how to use the Flask framework to build a web app that re-uses code from my [Usermapper program](https://github.com/blinklet/usermapper) and enables users to run it on a website, instead of installing and running it locally on their PC. You will create a "usermapper-as-a-service" application, served as a responsive web app that looks good on computer screens, tablets, and mobile phones.

I wrote this tutorial while I was learning Flask and developing my [*usermapper-web* Flask application](https://github.com/blinklet/usermapper-web). It was written by a beginner, for other beginners. It walks through topics in the order in which I learned them. I hope you find this approach to be readable and informative.

<!--more-->

### Flask overview

Flask is a Python framework, or code library, that makes it easier for developers to build web applications. 

I think it's helpful to think about Flask as a server that you may configure with Python statements and functions.  To use Flask, you write a Python program that configures the Flask server so that it "routes" users to "view functions" based on the address information in the URL the user entered in a web browser. The Flask server has a "user interface" that is managed by Python tools like *decorators*. 

#### Prerequisite learning

I previously wrote a blog post describing [*The Minimum You Need to Know About Python*]({filename}python-minimum-you-need-to-know.md) and created a [YouTube playlist about building *Usermapper*]({filename}python-learning-network-engineers.md), my first useful Python program.

Those efforts treated Python like a simple scripting language. They focused on Python syntax and basic logic, and built programs in a procedural way. To appreciate the Flask framework, you need to learn more about Python's object-oriented programming features and how they are used. In my case, I re-read the second half of the [*Learning Python* book](https://learning-python.com/) which covers both functional programming and object-oriented programming in Python, and covers Decorators.

#### Learning about Flask

Next, I watched a video tutorial about using Flask. There are many great videos on YouTube that introduce Flask. I looked at a few and I most enjoyed the [Web Programming video from the Harvard CS50 course](https://www.youtube.com/watch?v=zdgYw-3tzfI&list=PLWKjhJtqVAbmGw5fN5BQlwuug-8bDmabi&index=8&t=2108s). It covers Flask in a two-hour-long video and it gave me confidence I could get started. Later versions of this course have been expanded so, if you want more information about Flask and web programming, go to the [latest version of the CS50 course](https://cs50.harvard.edu).

Finally, I browsed through the [Flask documentation](https://flask.palletsprojects.com). I did not deep-dive into the docs. I browsed through them and learned just enough to get started.

#### Before you start Flask programming

Before you go further, you should review the object-oriented features in Python, read about decorators and how they are used in Python, and watch the *CS50 Flask video* mentioned above or a similar introduction-to-Flask video. You should have already created one or more simple command-line programs using Python and should be comfortable using the *Git* version control system. 

### No database (yet)

As you will see later, even a simple Flask app must store data somewhere so it can be used by the Flask "views" in the application. Most beginner Flask tutorials show you how to build a web app that [registers user names](https://flask.palletsprojects.com/en/1.1.x/tutorial/) or [stores objects like photos](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) in a database, but I disagree with forcing beginners to use databases in their first Flask applications.

I want to focus only on learning just enough Flask, Python, and Bootstrap to make a professional-looking web app. Databases are a separate subject that requires, in my opinion, more study than is usually provided in the database section of other Flask tutorials aimed at beginners. Those tutorials treat databases like some kind of "magic" and, while they show the commands required to set up a database that supports their example application, do not really teach the reader about databases. I will learn database technology later. 

Most network engineers who just want to "wrap" their command-line tools in a Flask app do not need to use a database because their command-line programs, like my *Usermapper* program, already use files for data storage instead of a database. So, this tutorial uses the host server's filesystem for data storage. 

Eventually, you will need to learn about databases. Using a database allows you to deploy your web app in a more flexible environment, as you will see later when you deploy this web app to a Python platform-as-a-service. If, at some point in the future, you find your web app is used by more than a few people, you should consider incorporating a database.

### Set up the programming environment

The first step in any programming project is to set up your environment. Create directories for source code, then create a Git repository, a remote Git repository, and a Python virtual environment.

#### Project directories

Create a directory in which you will build the Flask app and, eventually, in which you will clone the [Usermapper source code](https://github.com/blinklet/usermapper) so you can import its functions into your web app.

In my case, I will put all my code in a directory named "~/Projects"

```
$ mkdir ~/Projects
$ cd ~/Projects
```

Next, create a new folder for the Flask application in the ~/Projects directory. For example, I chose the directory name, *usermapper-web*.

```
$ mkdir usermapper-web
$ cd usermapper-web
```

In VScode, open the *usermapper-web* folder.

##### Git repository

Initialize a Git repository for the *usermapper-web* directory. 

```
$ git init
```

Create a *.gitignore* file for the project [^1]. Copy the standard *.gitignore* file for Flask projects found at: [https://github.com/pallets/flask/blob/master/.gitignore](https://github.com/pallets/flask/blob/master/.gitignore). Place the file in the usermapper-web directory.

[^1]: See many useful *.gitignore* files at: [https://github.com/github/gitignore](https://github.com/github/gitignore)

Commit the file to your local Git repository and push the change to GitHub.

```
$ git add .
$ git commit -m 'Added .gitignore file for Flask project'
```

Then change the branch name to *main*.

```
$ git branch -M main
```

##### Create a remote Git repository

Go to GitHub and create a new repository named *usermapper-web*. Get the URL of the repository and copy it to the clipboard. In my example, the GitHub URL is: [https://github.com/blinklet/usermapper-web.git](https://github.com/blinklet/usermapper-web.git).

Then, on the local machine, connect the local Git repository to the remote GitHub repository and push all the changes you made to the remote repository:

```
$ git remote add origin https://github.com/blinklet/usermapper-web.git
$ git push --set-upstream origin main
```

##### Python virtual environment

Create and start a Python virtual environment in the *usermapper-web* directory:

```
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install wheel
(env) $
```

Now, install Flask in the *usermapper-web* virtual environment:

```
(env) $ pip install flask
```

Now we're almost ready to get started.

### Flask "Hello, World!"

Test that Flask is working by pasting in the classic [Flask "Hello, World!" app](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) into a file and running it.

Create a file named *application.py* in the *usermapper-web* directory. Copy and paste the following code in the file, then save it.

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"
```

The code shown above configures the Flask server. It does not create all the logic that builds a web app; Flask does that.

In the first line, the program imports the Flask class from the flask package. The second line creates a instance of the Flask class which inherits the functions and classes in the application file (referenced by *\_\_name\_\_* variable). The third line is the Flask "route" decorator that "registers" a Flask "view" function with the address "/", the root level of the web app. The Flask app will run the view function registered with this URL address when a user enters it in their browser's search bar. The last two lines are the view function. The view function returns the text, "Hello, world!" to the Flask server. the Flask server (technically, the [WSGI server](https://www.fullstackpython.com/wsgi-servers.html) that supports the Flask server) presents the text to the user in their browser window.

Run the Flask app using the [Flask command-line interface](https://flask.palletsprojects.com/en/1.1.x/cli/). The *flask* command reads the [Flask environment variables](https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values) to learn the name of the application file and any other settings you may wish to set at run-time.

At a minimum, we need to tell Flask the application module name.

```
(env) $ export FLASK_APP=application
```

Then, run Flask:

```
(env) $ flask run
```

You should see some text appear in the terminal console that tells you the IP address and port from which the Flask app is being served. In my case, it is `127.0.0.1`, which is my PC's localhost address. In the browser, go to `localhost:5000` and see the text, "Hello, World!"

#### Flask templates, HTML & CSS

See the data rendered by the browser by using the developer tools. Enter the *CTRL-SHIFT-I* key combination to see the browser's Developer Tools or *CTRL-U* to see the source code on the page. In this example, the source code consists only of simple text with no [HTML markup](https://www.w3schools.com/html/html_intro.asp). 

Flask is not magic. You can't write a few lines of Python code and get a fully functioning web page. You need to create your own HTML pages and use the Flask `render_template` function to grab those HTML pages and serve them up to the browser. You may also use the built-in [Jinja template library](https://jinja.palletsprojects.com) to create placeholders in HTML pages that can be dynamically replaced during run-time.

By default, Flask expects to find Jinja templates in a directory named templates. Create a new folder named *templates*. Go to the new folder:

```
(env) $ mkdir templates
(env) $ cd templates
```

In the *templates* directory, create a new file named *index.html* with an `<H1>` tag, paragraph, and a form box. 

If you are using VScode, you can generate a simple HTML page snippet by pressing the *CTRL-space* key combination, then select "HTML".
Delete the CSS and JS links from the snippet because we do not need them, yet. Add the web page title between the *title* tags and the web page content between the *body* tags.

```
<!DOCTYPE html>
<html>
<head>
    <title>Hello World</title>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
</head>
    <body>
        <h1>Hello, World!</h1>
        <p>Hello, World!</p>
    </body>
</html>
```

Change the Flask application so it will render the HTML template you prepared, instead of just sending plain text to the browser. Go back to the *usermapper-web* directory and edit the *application.py* file. 

Import Flask's *render_template* function. Modify the first line of the *application.py* file as shown below:

```
from flask import Flask, render_template
```

Change the object returned by the *index* function. Change the last line of the *application.py* file as shown below

```
    return render_template("index.html")
```

Instead if returning a simple string, it will now return the results of the *render_template* function, which takes the *index.html* file as an argument. Then Flask will display the result, which is simply the contents of the *index.html* file, in the browser.

The *application.py* file should now look like the code listing below:

```
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
```

To make Flask read these changes, restart it. Enter `Ctrl-C` in the terminal, then `flask run`. Refresh the browser to see the rendered contents of the *index.html* page. 

Look at the web page's source code in the browser development tools: `CTRL-U` in the browser. You should see that the test displayed in the browser is formatted and you should see HTML code in the Browser's development tools. 

This example is not very interesting because it just serves up a web page named *index.html*, like any other web server. Soon, you will use Flask and Jinja templates to render web pages that includes data generated by the Flask program at run time, and allows the user to send data to the Flask application.

#### Flask development mode

To avoid restarting Flask when you modify your application code, set another environment variable to tell Flask to operate in a *development environment*. Flask will then automatically reload any changed code and will give you helpful error debug traces in the browser window, instead of in the console.

```
CTRL-C
(env) $ export FLASK_ENV=development
(env) $ flask run
```

### Get user input using Flask forms

Enough about the basics. Now, you may begin developing the real Flask application. The application used as an example in this tutorial needs to accept input from the user. HTML web pages use *forms* to gather and submit user input to the Flask application.

To create a basic form in HTML, modify the *index.html* template as shown below and add an [HTML form](https://www.w3schools.com/html/html_forms.asp). Also, change the header and add paragraph text in the page so it starts to looks a bit like the application you want to create. The listing below shows my first attempt at creating a form that accepts a text string: 

```
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width-device-width, initial-scale=1.0">
    <title>Guacamole User Mapper</title>
</head>
<body>
    <h1>Generate usermapping.xml</h1>
    <p>Upload your configuration file</p>
    <form>
        <label for="fname">upload file:</label><br>
        <input type="text" id="fname" name="fname"><br>
        <input type="submit" value="Submit">
    </form> 
</body>
</html>
```

In the browser, go to `localhost:5000`. Your web page should look similar to the screenshot below.

![screenshot]({static}/images/flask-web-app-tutorial/flask-001.png){width=90%}

The form looks OK but it does not do anything. You need to change the code so the form submits data to the Flask application.

#### Flask form extensions

As always, it's best to use tools others have created to make your programming easier. Use the [Python *WTForms* package](http://wtfforms.com/) and the [*Fask-WTF* Flask extension](https://flask-wtf.readthedocs.io/en/stable/) to handle forms in your application. Even with these helper libraries, you still need to know the basic HTML code for [HTML forms](https://www.w3schools.com/html/html_forms.asp).
    
Install *Flask-WTF*, which also installs *WTForms* for you: 

```
(env) $ pip install Flask-WTF
```

To get some experience with Flask forms, go to the [Flask-WTF Quickstart page](https://flask-wtf.readthedocs.io/en/stable/quickstart.html) and copy the example code. Replace the code in the *application.py* file with the sample code shown below:

```
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fix this later'

class MyForm(FlaskForm):
    filename = StringField('Filename: ')

@app.route("/", methods=('GET','POST'))
def index():
    form = MyForm()
    return render_template("index.html", form=form)
```

In the *application.py* file, above, you added the [app.secret key](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) so Flask extensions and features can use it when needed. Flask-WTF uses the secret key to support Cross Site Request Forgery (CSRF) protection. Normally, you would not include the secret key value in your source code, which is why it currently the value, "fix this later", to remind me you to clean this up before you deploy your application on a publicly-accessible web site.

You [defined a new class called *MyForm*](https://wtforms.readthedocs.io/en/2.3.x/forms/#defining-forms) that inherits all the attributes and functions from the FlaskForm class and adds an instance of the StringField class, called *filename*.

In the *index* view function, you created an instance of my *MyForm* class and named it *form*. Then you returned the template, *index.html*, and passed the *form* object instance into it as an argument.

Now, add the *form* object to the index.html template. Again, use the [example code from the Flask-WTF Quickstart Guide](https://flask-wtf.readthedocs.io/en/stable/quickstart.html). Modify the *templates/index.html* file as follows:

```
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width-device-width, initial-scale=1.0">
    <title>Guacamole User Mapper</title>
</head>
<body>
    <h1>Generate usermapping.xml</h1>
    <p>Upload your configuration file</p>
    <form method="POST">
        {{ form.csrf_token }}
        {{ form.filename.label }} {{ form.filename(size=20) }}
        <input type="submit" value="Upload">
    </form>
</body>
</html>
```

In the *index.html* template, above, you used Jinja template syntax to indicate where the *form* object should insert its HTML code. It places code generated by its *csrf_token* method and by its *filename* method into the Jinja placeholder text defined inside the HTML *form* tags.

Save the file and refresh the browser. Look at the page source code in the browser by pressing the *CTRL-U* key combination. You can see the HTML form code that Flask and WTForms created for you. It will be similar to the code snippet below:

```
<form method="POST">
    <input id="csrf_token" name="csrf_token" type="hidden" value="ImE5MmQ2YmE4YzIyYzIxM2NmNWYwODgyMTA2MzYwOTEyNWMzNWQyMDki.X9p5ow.Z_-HwhCD94kA1KR7Ui7BeHRiZYQ">
    <label for="filename">Filename: </label> <input id="filename" name="filename" size="20" type="text" value="">
    <input type="submit" value="Upload">
</form>
```

#### Adding input validation to Flask forms

Validate that the submitted form has data in it. Modify the application so it will show the text entered by the user after the form is submitted. 

In the *application.py* file, import the validator classes you need from the [validators module](https://wtforms.readthedocs.io/en/2.3.x/validators/#module-wtforms.validators) in the WTFforms library:

```
from wtforms.validators import DataRequired
```
    
Change the *form* object to use the validators:

```
class MyForm(FlaskForm):
    filename = StringField('Filename: ', validators=[DataRequired()])
```

Add the following validation check to the *index* function. If the validation passes, get the submitted form data, which is in the *filename.data* attribute of the *form* instance. Pass the submitted data to the *index.html* template by adding an extra argument when you call the *render_template* function.

```
@app.route('/', methods=('GET','POST'))
def index():
    data=None
    form = MyForm()
    if form.validate_on_submit():
        data = form.filename.data
    return render_template('index.html', form=form, data=data)
```

Then, modify the *templates/index.html* template so it will display the contents of the *data* variable after the form. Add the following after the *\<form\>\</form\>* stanza, before the closing *\</body\>* tag:

```
        <p>{{ data }}</p>
```

Refresh the browser to see the results. The browser should display "None". Check that the form will not let you submit it when the input field is empty. If you do enter some text, then you can submit the form and Flask will display the information you submitted in the form.

[Change the template](https://jinja.palletsprojects.com/en/2.10.x/templates/) so it does not show the 'None" when you use the application for the first time. It displays "None" because the *data* variable is empty until you submit data in the form. 

Jinja templates can include [conditional statements](https://pythonise.com/series/learning-flask/jinja-template-design#conditionals-comparison-operators). Replace the *data* variable with the following Jinja statement:

```
    {% if data != None %}
        <p>{{ data }}</p>
    {% endif %}
```

Save the file and refresh the browser. See how the page renders with no values below the form, then shows values when they are entered in the form.

### Uploading files

In *application.py*, import the *wtforms.SubmitField* class from the *flask_wtf* module. Import the *FileField*, *FileRequired*, and *FileAllowed* classes from the *flask-wtf.file* module. Also, import the *os* module so you can get system information like the Flask project directory when saving the file to the server. You no longer need the *StringField* and *DataRequired* classes from *wtforms* so you can delete those. 

The new import lines in the *application.py* file will be:

```
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import DataRequired
```

Modify the *MyForm* class to handle a file upload form. Add a *submit* field to the class so that *wtforms* will handle creating the correct HTML for the submit button. It's better to let the framework do the work for you, where possible. 

```
class MyForm(FlaskForm):
    filename = FileField('Filename: ', 
        validators=[FileRequired(), FileAllowed(['yaml'])])
    submit = SubmitField('Upload')
```

Notice how you are using the new validators and are only allowing files with the *.yaml* extension to be uploaded.

Change the *index* view function to save the file that is uploaded. 

```
@app.route("/", methods=('GET','POST'))
def index():
    form = MyForm()
    filename = None
    if form.validate_on_submit():
        f = form.filename.data
        basedir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 
            'uploads')
        filename = os.path.join(
            basedir, secure_filename(f.filename))
        f.save(filename)
    return render_template('index.html', form=form, data=filename)
```

The file contents are in the *form* object's *filename.data* attribute. We use the *os.path* module to get the directory in which the *application.py* file is located (since this may be different when we deploy to a server). We use the *secure_filename* function from the *werkzeug* module to ensure a user cannot enter a malicious file name.

The *form submit* input type in *templates/index.html* will not work for file uploads. replace it with the following Jinja template text so Flask-WTF can insert the submit tag syntax generated by the Jinja *form.submit* macro.

Replace the text in *templates/index.html*:

```
        <form method="POST">
            {{ form.csrf_token }}
            {{ form.filename.label }} {{ form.filename(size=20) }}
            <input type="submit" value="Go">
        </form>
```

with the following text:

```
        <form method="POST" enctype="multipart/form-data">
            {{ form.csrf_token }}
            {{ form.filename.label }} {{ form.filename(size=20) }}
            {{ form.submit }}
        </form>
```

Notice you added an encoding type to the form. Since you are now using the *FileField* class, you must change the form tag shown above so it tells the browser that the POST data will be [encoded as multipart data](https://flask-wtf.readthedocs.io/en/stable/form.html#module-flask_wtf.file).


If the form validation fails, you need to send an error message to the user. Insert the following code, which will display errors raised by the *form.filename* object, after the *{{ form.submit }}* Jinja placeholder:

```
    {% for error in form.filename.errors %}
        <p style="color: red;">{{ error }}</p>
    {% endfor %}
```

You must create an *uploads* directory in the application's folder because you hard-coded your *index* view function in *application.py* to save files in folder named "uploads".

```
(env) $ cd ~/Projects/usermapper-web
(env) $ mkdir uploads
```

Refresh the browser. Notice that the form looks different. Now, it contains a Browse button that will open the file explorer or your PC to find the file to upload. 

Now, you can upload a YAML file using its original filename in the relative directory, *./uploads*. When you upload a file, the Flask app saves it in the *uploads* directory and displays the file's path on the screen. The application screen should look like the screenshot below:

![screenshot]({static}/images/flask-web-app-tutorial/flask-010.png){width=90%}

#### Saving temporary files

Saving an uploaded file to a single location on disk could cause problems for web apps used by multiple users. Multiple users may overwrite each others' configuration files. 

Solve this problem by creating unique temporary files in randomly-named directories. Use the [*tempfile.mkdtemp* function](https://docs.python.org/3/library/tempfile.html) from the Python standard library to create a temporary directory that is unique for each user session. 

> **Note:** The temporary storage issue can also be solved by eventually incorporating a database and giving each user a unique id saved in their session variable -- but that's all for a later project.

In the *application.py* file, import the tempfile module:

```
import os, tempfile
```

Change the logic that defines the *filename* in the *index* view function. After the *basedir* variable is defined, add a line taht defines the *tempdir* variable and change the *filename* variable so it now incorporates the *tempdir* variable as part of its path:

```
        tempdir = tempfile.mkdtemp(dir=basedir)

        filename = os.path.join( 
            tempdir, secure_filename(f.filename))
```

Save the file and refresh the browser. Upload a config file. Check the filesystem for the temporary directory name, then go to it. You should see a random directory name containing the file you uploaded. For example:

```
(env) $ ls ./uploads/ 
test.yaml  tmpcrlrrmwa  tmppe646x2r
```

#### Limit the upload file size

As an additional check, limit the allowed size of the uploaded file. A malicious user could use up all your disk space or memory they submit a very large file.

I could not find a server-side function in Flask or Flask-WTF that lets you limit upload file size. You would need to do that on the client, using JavaScript (maybe as a future task).

Instead, implement a basic workaround using [Flask environment variables](https://flask.palletsprojects.com/en/1.1.x/config/#MAX_CONTENT_LENGTH). In the *application.py* file, under the secret key, under the application instance, add a new configuration that limits file upload sizes to 1 MB. 

```
app.config['SECRET_KEY'] = 'fix this later'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
```

Now, any file that exceeds one megabyte in size will fail to upload. According to the docs, Python will [raise an exception called *RequestEntityTooLarge*](https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#improving-uploads) so, if you want, you can [catch that exception](https://docs.python.org/3/tutorial/errors.html#handling-exceptions) and produce a nicer error announcement (also a future task).

#### Application files

The two files should now look like the two listings below:

##### application.py

```
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os, tempfile
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fix this later'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

class MyForm(FlaskForm):
    filename = FileField('Filename: ', 
        validators=[FileRequired(), FileAllowed(['yaml'])])
    submit = SubmitField('Upload')

@app.route("/", methods=('GET','POST'))
def index():
    form = MyForm()
    filename = None
    if form.validate_on_submit():
        f = form.filename.data
        basedir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 
            'uploads')
        tempdir = tempfile.mkdtemp(dir=basedir)
        filename = os.path.join( 
            tempdir,secure_filename(f.filename))
        f.save(filename)
    return render_template('index.html', form=form, data=filename)
```

##### templates/index.html

```
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width-device-width, initial-scale=1.0">
    <title>Guacamole User Mapper</title>
</head>
<body>
    <h1>Generate usermapping.xml</h1>
    <p>Upload your configuration file</p>
    <form method="POST" enctype="multipart/form-data">
        {{ form.csrf_token }}
        {{ form.filename.label }} {{ form.filename(size=20) }}
        {{ form.submit }}
        {% for error in form.filename.errors %}
        <p style="color: red;">{{ error }}</p>
        {% endfor %}
    </form>
    {% if data != None %}
        <p>{{ data }}</p>
    {% endif %}
</body>
</html>
```

### Downloading a file from a Flask app

You will eventually want users to be able to download the XML file generated by the Usermapper package. To experiment with this functionality, write some code that will download the file you recently uploaded.

Modify the *application.py* file. Import the *send_from_directory* and *url_for* modules from the Flask package:

```
from flask import Flask, render_template, send_from_directory, url_for
```

Modify the *index* view function to add a download link called *download_url*, which points to the temporary file created when you previously uploaded a file, and sends the *download_url* variable to the *index.html* template as another argument.

The *download_url* should contain the route address, *download/*, and the relative path of the file that had previously been uploaded.

Define the *download_url* variable near the start of the view function.

```
    download_url = ""
```

Replace the *return* statement at the end of the *index* view function with the following lines. The *download_url* creates a Dynamic URL comprised of the */download* route address, the name of the temporary folder that was created in the *uploads* folder in the filesystem, and the name of the file that was previously uploaded. Flask Dynamic URLs allow us to pass simple arguments from one view function to another view function.

```
        tempfolder = os.path.split(tempdir)[1]
        download_url = os.path.join(
            '/download', tempfolder, secure_filename(f.filename))

    return render_template(
        'index.html', form=form, 
        data=filename, download_url=download_url)
```

Create a new route and view function for [downloading the file from the temporary directory](https://flask.palletsprojects.com/en/1.1.x/api/#flask.send_from_directory). The route address, *"/download/\<tempfolder\>/\<filename\>"*, in the example below uses [Flask's Dynamic URL](https://pythonise.com/series/learning-flask/generating-dynamic-urls-with-flask) feature to send information encoded in the route URL to the view function.

```
@app.route("/download/<tempfolder>/<filename>", methods=('GET','POST'))
def download(tempfolder,filename):
    basedir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'uploads')
    temp_dir = os.path.join(basedir,tempfolder)
    return send_from_directory(
        temp_dir, filename, as_attachment=True)
```

Then, add a link to the *templates/index.html* template so the user can [download the file](https://pythonise.com/series/learning-flask/sending-files-with-flask). Display the download link in the browser only if the *data* variable is not empty, so it only appears if a file was previously uploaded. 

Replace the following text to *templates/index.html*, after the HTML form tags:

```
    {% if data != None %}
        <p>{{ data }}</p>
    {% endif %}
```

with the following text:

```
    {% if data != None %}
        <p></p>
        <p><a href="{{ download_url }}">Download the file you recently uploaded</a></p>
        <p></p>
        <h2>File path:</h2>
        <p></p>
        {{ data }}
    {% endif %}
```

Save the template file. Refresh the browser. 

Upload a file. Then, see the download link. Verify you can download the file when you click on the download link. After downloading the test file, your browser should look similar to the screenshot below:

![screenshot]({static}/images/flask-web-app-tutorial/flask-020.png){width=90%}

One issue is that the temporary folders do not get automatically cleaned up. That's a problem you will address later in this tutorial.

Now, a web app user can upload any file and then download the same file. By working through the previous steps, you have learned how to Flask and Jinja templates can create a functional web page that will display different options, depending on the values stored in program variables, and enables users to upload and download a file. You also learned how to pass simple bits of informtion from one view to another with Dynamic URLs.

You are ready to convert an existing Python command-line application to a Flask web app, or to build your own original Flask web app.

### Wrapping an existing program in a Flask web app

In this tutorial, you will create a Flask app that will upload and read the contents of a YAML configuration file so the Usermapper program I previously wrote can read the uploaded configuration file and generate the XML file. Then, the Flask application will allow the user to download the generated XML file.

To "wrap" my Usermapper command-line program in a Flask web app, you need to import functions from my Usermapper package and reuse them. To get access to these functions, you must install the Usermapper package in your Python virtual environment. 

#### Install the CLI package you plan to convert

Clone the Usermapper source code to the *~/Projects* folder.

```
(env) $ cd ~/Projects
(env) $ git clone https://github.com/blinklet/usermapper.git
```

This creates a folder named *usermapper* and downloads the package files into it.

Have a look at the source code. 

```
(env) $ tree usermapper
usermapper
├── config.yaml
├── example_config.yaml
├── example-xml.xml
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── test.py
└── usermapper
    ├── __init__.py
	├── __main__.py
    ├── mapperdata.py
    └── usermapper.py
``` 

The source code consists of some helper files and a package directory named *usermapper* that contains the modules *mapperdata.py* and *usermapper.py*. 

Install the *usermapper* package in the *usermapper-web* virtual environment in *editable* mode, so any changes we make to the source code in the *~/Projects/usermapper/usermapper* package directory will automatically be appied to the installed instance in the *usermapper-web* virtual environment:

```
(env) $ pip install --editable ~/Projects/usermapper
```

By re-using packaged code in this way, any changes I make to my original usermapper package will be available to users of the command-line usermapper application, as well as to users of the web app.

Keeping the code for the two applications separated like this enables developers to work individually on their projects, as long as the interfaces are agreed between projects. This avoids maintaining the same code in two different projects. 

#### Using Usermapper functions

Import the usermapper package's functions into the *application.py* Flask program. Also, import the *yaml* module from the Python standard library. The *application.py* file's imports should change as follows. 

Add *yaml* to the module imports line:

```
import os, tempfile, yaml
```

Add functions from the *usermapper* package:

```
from usermapper.usermapper import xmlwriter
from usermapper.mapperdata import get_users
```

I also removed the *werkzeug.utils* import line because we no longer need the *secure_filename* function.

Instead of saving the uploaded configuration file on the server's filesystem, process it immediately and save the generated XML file. The uploaded config file is stored in memory as the file objected named "f". Also, since you know the location you want to use for the temp folders, you will not put the entire relative path in the URL.

Delete the uploads directory and create a new directory named "downloads".

```
(env) $ rm -rf uploads
(env) $ mkdir downloads
```

In the *application.py* file, change the *index* view function to the following. Replace the following text near the end of the view function:

```
        f = form.filename.data
        basedir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'uploads')
        tempdir = tempfile.mkdtemp(dir=basedir)
        filename = os.path.join( 
            tempdir, secure_filename(f.filename))
        f.save(filename)
        tempfolder = os.path.split(tempdir)[1]
        download_url = os.path.join('
            /download', tempfolder, secure_filename(f.filename))
```

with the following new text:

```
        f = form.filename.data
        basedir = os.path.join(
            os.path.relpath(os.path.dirname(__file__)), 'downloads')
        tempdir = tempfile.mkdtemp(dir=basedir)

        filename = os.path.join(tempdir, 'user-mapping.xml')

        configuration = yaml.safe_load(f.read())
        structure = get_users(configuration)
        xmlwriter(structure,filename)

        tempfolder = os.path.split(tempdir)[1]
        download_url = os.path.join(
            '/download',tempfolder,'user-mapping.xml')
```

You made a lot of changes in the *index* view function. You built the *basedir* variable using the *os.path.relpath* function instead of *os.path.abspath* and pointed it to the new *downloads* directory. You changed the filename to a hard-coded value, *user-mapping.xml*. You no longer just save an uploaded file. You used the functions you imported from the Usermapping package to read the uploaded configuration file, process it and save the results to a temporary directory. Then, you set the *download_url* variable, which will create the download link in the Jinja template, to the file path of the saved *user-mapping.xml* file. You split statements into multiple lines to make the code a bit more readable.

Also, change the *basedir* variable in the *download* view function so it also points to the the new *downloads* folder:

```
@app.route("/download/<tempfolder>/<filename>", methods=('GET','POST'))
def download(tempfolder,filename):
    basedir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        'downloads')
    temp_dir = os.path.join(basedir,tempfolder)
    return send_from_directory(
        temp_dir,filename,as_attachment=True)
```

Reload the browser and upload the config file again. This time use a real configuration file. I suggest you use the file: *~/Projects/usermapper/example-config.yaml*.

See a new file named *user-mapping.xml* has been created in the a randomly-named directory in the *usermapper-web/downloads/* directory. 


#### Create a file preview in the web app

To provide some feedback to the user so they know the file generation worked, add some code that previews the contents of the XML file on the web page.

Modify the *index* view function. Change the section starting with *configuration = yaml.safe_load(f.read())* to:

```
        configuration = yaml.safe_load(f.read())
        structure = get_users(configuration)
        xmlwriter(structure,filename)

        preview = open(filename, 'r')
        data = preview.readlines()
        preview.close()

        temp_folder = os.path.split(tempdir)[1]
        download_url = os.path.join('/download',temp_folder)

    return render_template('index.html', 
        form=form, data=data, download_url=download_url)
```

This is a bit kludgey [^2]. You write the *user-mapping.xml* file to disk, then re-open and read it to get its contents to display on the web page. But, sometimes, "good enough" is good enough.

[^2]: In the future, I should re-write the *usermapper* package so it builds the *user-mapping.xml* file contents as a list in memory and returns that list to *application.py*. Then, the program can print the preview on the web page and save it to disk in application.py at the same time.

Next, fix the *templates/index.html* template. It currently displays the XML preview as a big blob of text all on one line. Fix this by changing the Jinja template.

Change the *templates/index.html* template so it uses a [Jinja For loop](https://jinja.palletsprojects.com/en/2.11.x/templates/#for) to iterate through the *data* object line by line. Use [minus signs to manually strip whitespace](https://jinja.palletsprojects.com/en/2.11.x/templates/#whitespace-control) from the HTML code that Jinja generates in the *for loop* block. Also, change some of the text in the download link generated by the *index.html* template. Change the following line:

In *templates/index.html*, change the *if* block from:

```
    {% if data != None %}
        <p></p>
        <p><a href="{{ download_url }}">Download the file you recently uploaded</a></p>
        <p></p>
        <h2>File path:</h2>
        <p></p>
        {{ data }}
    {% endif %}
```

to:

```
    {% if data != None %}
        <p></p>
        <p><a href="{{ download_url }}">Download the <em>user-mapping.xml</em> file</a></p>
        <p></p>
        <h2>File path:</h2>
        <p></p>
        <pre><code>
            {%- for item in data -%}
                {{ item }}
            {%- endfor %}
        </code></pre>
    {% endif %}
```

This displays the contents of *user-mapping.xml* in the browser. The file text needs to be formatted better and you can clean that up later with some CSS or Bootstrap classes.

It would also be helpful to add a button that will copy the text from the *user-mapping.xml* file. To do that, you would need to include some [JavaScript to enable a copy field](https://www.w3schools.com/howto/howto_js_copy_clipboard.asp). So, that's a topic for another tutorial.

#### Cleaning up temporary files

Delete temporary files after the user has downloaded them so they do not eventually fill up your disk with temporary files.

You should give the users at least a few minutes to download their files after they are generated. The temporary file should persist for, maybe, 20 minutes and then be deleted.

I think the easiest way is to run a [cron job that runs every twenty minutes](https://superuser.com/questions/430914/how-to-delete-directories-older-than-one-hour-cron-job) and deletes temporary files older than twenty minutes.

Create a crontab entry:

```
$ crontab -e
```

add the following line:

```
*/20 * * * * find /home/brian/Projects/usermapper-web/downloads/tmp* -maxdepth 0 -mmin +20 -exec rm -fr {} +;
```

Check if it is working (after twenty minutes):

```
$ grep CRON var/log/syslog
```

> **Note:** Hard-coding the temporary file location like this  is not ideal. You will eventually deploy this program to a remote server or to a serverless platform which may handle temporary files differently. As a future improvement, you may [define the temporary file location using an environment variable](https://stackoverflow.com/questions/2229825/where-can-i-set-environment-variables-that-crontab-will-use) so you can configure it to the appropriate value on any service or server where you deploy this app.

#### Create a separate download page

After uploading a config file and generating a user-mapping file, you will find that refreshing the browser generates a new temporary directory containing a new *user-mapping.xml* file. If you keep refreshing the browser, you generate more and more temporary files. Someone could create a minor denial of service attack and fill up your downloads directory with temporary files just my holding down the *CTRL-R* key combination in their browser!

This problem exists because the upload and download services are both on the same page. The browser sees the user is still on the same page so [the browser stores the state](https://www.semicolonworld.com/question/57791/clear-valid-form-after-it-is-submitted) [of the last request](https://stackoverflow.com/questions/31945329/clear-valid-form-after-it-is-submitted). If you refresh the page at this point [the browser will re-submit the cached form object](https://stackoverflow.com/questions/28184154/why-will-wtforms-submit-again-when-i-refresh-the-page), triggering the upload again and generating a nw user-mapping file in a new temporary directory.

The solution to the refresh problem is to create a new route and view function that returns a new template after successfully uploading a configuration file and saving the generated XML file. The new template will display the file preview and the XML file download link, and will include a link back to the index page.

Create a new template named: *templates/download.html*. Copy of the *index.html* template and paste it into the new template, with the form removed. Add in a link back to the *index* view. Change the displayed text so the instructions are clear. The *templates/download.html* template should look like the following:

```
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width-device-width, initial-scale=1.0">
    <title>Guacamole User Mapper</title>
</head>
<body>
    <h1>Download usermapping.xml</h1>
    <p>Download your configuration file</p>

    {% if data != None %}
        <p></p>
        <p><a href="{{ download_url }}">Download user-mapping.xml</a></p>
        <p></p>
        <p><a href="{{ url_for('index') }}">Create another user-mapping File</a></p>
        <p></p>
        <h2>File preview:</h2>
        <pre><code>
            {%- for item in data -%}
                {{ item }}
            {%- endfor %}
        </code></pre>
    {% endif %}
</body>
</html>
```

Then, change the *index.html* template and remove the download link and file preview, as shown below:

```
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width-device-width, initial-scale=1.0">
    <title>Guacamole User Mapper</title>
</head>
<body>
    <h1>Generate usermapping.xml</h1>
    <p>Upload your configuration file</p>
    <form method="POST" enctype="multipart/form-data">
        {{ form.csrf_token }}
        {{ form.filename.label }} {{ form.filename(size=20) }}
        {{ form.submit }}
        {% for error in form.filename.errors %}
            <p style="color: red;">{{ error }}</p>
        {% endfor %}
    </form>
</body>
</html>
```

Modify *application.py* to support the separate *index* and *download* templates. 

Add *redirect* to the list of imports from the Flask package, as shown below.
 
```
from flask import Flask, render_template, send_from_directory, url_for, redirect
```

The *index* view function now only needs to handle the configuration file upload and conversion to the XMP user mapping file. Add a redirect to a new route named *download_page* and move the logic that builds the *download_url* from the *index* view function to the *download_page* view function. Pass the xml file's temporary directory name to the new route, using the [Flask *url_for* function](https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for) to build a Dynamic URL. 

Delete the initial *download_url* definition statement in the *index* view function. Delete the following text:

```
    download_url = ""
```

Also, delete code that reads the generated user-mapping.xml file. Delete the following text:

```
        preview = open(filename, 'r')
        data = preview.readlines()
        preview.close()
```

Delete the second *download_url* definition statement at the end of the *if form.validate_on_submit():* block in the *index* view function:

```
        download_url = os.path.join('/download',temp_folder)
```

Add a redirect statement at the end of the *if form.validate_on_submit():* block in the *index* view function so that, when the form is submitted and the *user-mapping.xml* file is generated, the web app redirects to the download page:

```
        return redirect (url_for('download_page', temp_folder=temp_folder))
```

Change the *configuration* dictionary 
Delete the *data* and *download_url* variables from the index view function's return statement. The statement should now look like the line shown below:

```
    return render_template('index.html', form=form)
```

The *index* view function should now look like the source code below:

```
@app.route("/", methods=('GET','POST'))
def index():
    form = MyForm()
    filename = ""
    if form.validate_on_submit():
        f = form.filename.data
        basedir = os.path.join(
            os.path.relpath(os.path.dirname(__file__)), 
            'downloads'
        )
        tempdir = tempfile.mkdtemp(dir=basedir)
        filename = os.path.join(tempdir, 'user-mapping.xml')

        configuration = yaml.safe_load(f.read())
        structure = get_users(configuration)
        xml_web_download(structure, filename)

        temp_folder = os.path.split(tempdir)[1]
        return redirect (url_for('download_page', temp_folder=temp_folder))

    return render_template('index.html', form=form)
```

Create a new view function called *download_page*. It receives the temporary directory name in a dynamic URL. Add into it the preview file logic you deleted from the *index* view function. When adding back in the file preview code, change the file *open* statement to a *with* statement, which is more "Pythonic", results in fewer lines of code, and automatically closes the file when it is no longer needed.

```
@app.route('/download_page/<temp_folder>', methods=('GET','POST'))
def download_page(temp_folder):
    filename = os.path.join(
        os.path.relpath(os.path.dirname(__file__)), 
        'downloads',temp_folder,'user-mapping.xml')

    with open(filename) as preview:
       data = preview.readlines()
    
    download_url = url_for('download', 
        tempfolder=temp_folder, filename='user-mapping.xml')

    return render_template('download.html', 
        data=data, download_url=download_url)
```


Refresh the browser to test the application. After uploading a configuration file, you should end up with a screen that looks like the screenshot below.

![screenshot]({static}/images/flask-web-app-tutorial/flask-030.png){width=90%}

You should see that, after you upload a file, you are redirected to a page that previews the generated XML file and provides a link to download it. Refreshing the browser no longer regenerates the download file.

### Commit your code to Git, and record TO-DOs

Now your program is fully functional. Commit the new code to Git and push it to the remote repository.

```
(env) $ cd ~/Projects/usermapper-web
(env) $ git add .
(env) $ git commit -m 'First Flask program'
(env) $ git push
```

Next, make a record of any improvements you would like to make so, if you have time, you can implement those improvements in the future. 

Go to the GitHub repository on the GitHub web site. In my case, it is [https://github.com/blinklet/usermapper](https://github.com/blinklet/usermapper). Click on the *Issues* link and record any ideas you have for improving the code, so you do not forget about them.

There are a number of issues I want should record for later implementation in both the Usermapper command-line app repository and the Usermapper-web web app repository.

In the *Usermapper* project repository, I added the following Issues:

1. To improve efficiency, create the contents of the user-mapping.xml as a list in memory and return it to the flask app. The Flask app will save it to temporary storage. This decouples the *usermapper.mapperdata* module from the filesystem. 

2. Add more error checking code on the loaded configuration file (example: so we do not create crazy-large xml files if someone says there are one million students). Some ideas for config file restrictions:

  * Only two user type allowed (trainer and student)
    * Maybe three for flexibility
  * Up to 4 trainers allowed
  * up to 12 of any other type allowed
  * Up to 10 device types allowed
  * up to 10 devices per type

In the *Usermapper-web* project repository, I added the following issues:

1. Improve the user interface appearance with CSS and Bootstrap?

2. Add more input checking, such as for configuration file size, on the client side using JavaScript.

3. New user interface: Create a set of dynamic forms that allow the user to build the configuration in the browser and submit it -- instead of perparing a yaml configuration file in advance.

4. Use session cookies instead of passing variables between routes using dynamic urls. It is more secure and more flexible. See: Flask-Session.

### A quick break

Congratulations on making it this far through the tutorial. You successfully converted a Python command-line application into a web app using Flask and Flask extensions. At this point, you have a fully-functioning web app that runs in the development environment on your PC. If you only plan to use the application by yourself, you could stop here.

If you wish to share this application with others, continue reading. The next half of this tutorial shows you how to make the web app look more professional with the Bootstrap CSS library, and how to deploy the web app to a production environment running on a cloud service so everyone in the world can use it.

### Style your web app with Bootstrap

Currently, your web app works but it looks terrible. I imagine you want to make the web app look more professional but you don't want to spend an extra week learning CSS and JavaScript. You will achieve faster results if you use the [*Bootstrap* library](https://getbootstrap.com/), which provides a set of HTML classes you can use to style and structure a web page.

#### Bootstrap-Flask

To keep things simple, I will use the *[Bootstrap-Flask](https://bootstrap-flask.readthedocs.io/en/stable/)* helper library instead of manually importing Bootstrap and working with classes. Hopefully, the library developer will keep it up to date because Bootstrap 5 is coming out soon.

Install Bootstrap-Flask in your environment:

```
(env) $ pip install bootstrap-flask
```

Modify the *application.py* program to include Bootstrap-Flask. Import the Bootstrap class to the program, as shown below:

```
from flask_bootstrap import Bootstrap
```

Register The Bootstrap class with the application by creating an instance of the Bootstrap class, named *bootstrap*, that inherits all the functions and attributes of the original Flask application instance, named *app*:

```
app = Flask(__name__)
bootstrap = Bootstrap(app)
```

Bootstrap-Flask provides some Jinja macros that make developing templates a bit easier -- especially for more complex elements like tables and forms. I am using it as a quick way to style my web app forms without learning a lot about Bootstrap, itself. However, Bootstrap-Flask covers only a small amount of Bootstrap functionality so, if you need it, the normal Bootstrap 4 classes are all still available.

#### Jinja Template hierarchy and design

Now is a good time to start using the [block rendering features in Jinja templates](https://jinja.palletsprojects.com/en/master/templates/#base-template) because you will have a common elements, like a header or navigation bar, on each new page you create. To lean more about Jinja templates and template inheritance, see the following tutorials or videos from [Pythonise](https://pythonise.com/), listed below:

* Flask templates: [tutorial](https://pythonise.com/series/learning-flask/jinja-template-inheritance), [video](https://www.youtube.com/watch?v=pj1iLRljwxI&list=PLF2JzgCW6-YY_TZCmBrbOpgx5pSNBD0_L&index=5)
* Flask templates and Jinja: [tutorial](https://pythonise.com/series/learning-flask/jinja-template-design), [video](https://www.youtube.com/watch?v=mqrbF0qGSLI&list=PLF2JzgCW6-YY_TZCmBrbOpgx5pSNBD0_L&index=6)

Create a template file named *templates/base.html* and copy the [Bootstrap-Flask starter template from the Bootstrap-Flask web site](https://bootstrap-flask.readthedocs.io/en/stable/basic.html#starter-template) into the base template. Also, change the title to a block placeholder:

The *base.html* template will look like:

```
<!doctype html>
<html lang="en">
<head>
    {% block head %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    {% block styles %}
        <!-- Bootstrap CSS -->
        {{ bootstrap.load_css() }}
    {% endblock %}

    <title>{% block title %}Your page title{% endblock %}</title>
    {% endblock %}
</head>
<body>
    <!-- Your page content -->
    {% block content %}{% endblock %}

    {% block scripts %}
        <!-- Optional JavaScript -->
        {{ bootstrap.load_js() }}
    {% endblock %}
</body>
</html>
```

Then, change the *templates/index.html* and *templates/download.html* templates so they inherit the base template and each extends the *title*, *main*, and *script* blocks with unique data. 

The *index.html* template will look like:

```
{% extends "base.html" %}

{% block title %}Guacamole User Mapper{% endblock %}

{% block content %}
    <h1>Generate usermapping.xml</h1>
    <p>Upload your configuration file</p>
    <form method="POST" enctype="multipart/form-data">
        {{ form.csrf_token }}
        {{ form.filename.label }} {{ form.filename(size=20) }}
        {{ form.submit }}
        {% for error in form.filename.errors %}
            <p style="color: red;">{{ error }}</p>
        {% endfor %}
    </form>
{% endblock %}
```

The *download.html* template will look like:

```
{% extends "base.html" %}

{% block title %}Guacamole User Mapper{% endblock %}

{%block content %}

    <h1>Download usermapping.xml</h1>

    {% if data != None %}
    <p></p>
    <p><a href="{{ download_url }}">Download user-mapping.xml</a></p>
    <p></p>
    <p><a href="{{ url_for('index') }}">Create another user-mapping File</a></p>
    <p></p>
    <h2>File preview:</h2>
        <pre><code>
            {%- for item in data -%}
                {{ item }}
            {%- endfor %}
        </code></pre>
    {% endif %}

{% endblock %}
```

Reload the web page and see the fonts have changed. This gives us some indication tha Bootstrap is working properly. That's how simple it is to add Bootstrap to the page. 

#### Adding Bootstrap styles

Now we need to dig through the *[Bootstrap](https://getbootstrap.com/docs/4.1/getting-started/introduction/)* and *[Bootstrap-Flask](https://bootstrap-flask.readthedocs.io/en/stable/)* documentation. We'll be using *div* classes and other tag classes to style the elements on the web page. Because I do not have the time to become an expert in CSS, I'll use only the classes that *Bootstrap* and *Bootstrap-Flask* provide.

Add some [style to the form](https://bootstrap-flask.readthedocs.io/en/stable/macros.html#render-form) on the index page. 

Replace all the Jinja form placeholders with just one line, which uses the [*render_form* macro from Bootstrap-Flask](https://bootstrap-flask.readthedocs.io/en/stable/macros.html#render-form). 

You need to import the *render_form* macro into the template. Add the following line after the *extends* block at the top of the *index.html* file:

```
{% from 'bootstrap/form.html' import render_form, render_field %}
```

Delete the following text from *index.html*:

```
    <form method="POST" enctype="multipart/form-data">
        {{ form.csrf_token }}
        {{ form.filename.label }} {{ form.filename(size=20) }}
        {{ form.submit }}
        {% for error in form.filename.errors %}
            <p style="color: red;">{{ error }}</p>
        {% endfor %}
    </form>
```

and replace it with the following text:

```
        {{ render_form(form) }}
```

The *index.html* template now looks like:

```
{% extends "base.html" %}
{% from 'bootstrap/form.html' import render_form, render_field %}

{% block title %}Guacamole User Mapper{% endblock %}

{% block content %}
    <h1>Generate usermapping.xml</h1>
    <p>Upload your configuration file</p>

    {{ render_form(form) }}

{% endblock %}
```

This is a good example that shows how Flask extensions can make things simpler. Bootstrap-Flask's *render_form* macro takes the *form* object that was passed into the template from application.py's *index* view and renders all the form fields by in the *form* object.

Refresh the browser to see the changes. The form looks different because it is rendered by Bootstrap-Flask using CSS style classes provided by Bootstrap. Using Flask-Bootstrap macros makes development easier, but it forces you to lose some control over appearance.

To make things look a bit better, modify the *application.py* file and add a message in the *FileAllowed* validator and a description in the *FileField* object. Use the same text in both messages so it looks like the message turns red if the validation fails. 

The *MyForm* class in the *application.py* file should now look like:

```
class MyForm(FlaskForm):
    filename = FileField('Select configuration file: ', 
        validators=[FileRequired(), FileAllowed(['yaml'], 
        message='Only YAML files accepted')], 
        description="Only YAML files accepted")
    submit = SubmitField('Upload')
```

Save the file and refresh the browser. Your web page should now look similar to the below screenshot:

![screenshot]({static}/images/flask-web-app-tutorial/flask-040.png){width=90%}

#### Using the Bootstrap grid

Next, use [Bootstrap's grid system](https://getbootstrap.com/docs/4.0/layout/grid/) to arrange elements on the index web page. Create one row with two columns: one containing the form and another containing some information for the user.   

Add *div* tags with Bootstrap's *container*, *row*, and *column-size* classes to the *index.html* template. The content block in the *index.html* template should now look like:

```
{% block content %}

<div class='container'>
    <div class='row'>
        <div class='col-sm'>
            {{ render_form(form) }}
        </div>
        <div class='col-sm'>
            <h1>Generate usermapping.xml</h1>
            <p>Upload your configuration file</p>
        </div>
    </div>
</div>

{% endblock %}
```

Refresh the browser and see that the page is rendered in two columns and the layout is responsive. It should  look similar to the screenshot below:

![screenshot]({static}/images/flask-web-app-tutorial/flask-050.png){width=90%}

Similarly, add a grid layout to the *downloads.html* template. The content block in the *downloads.html* template should now look like:

```
{%block content %}

<div class = 'container'>
    <div class = 'row'>
        <div class='col'>
            <h1>Download user-mapping.xml</h1>

            {% if data != None %}
                <p></p>
                <p><a href="{{ download_url }}">Download user-mapping.xml</a></p>
                <p></p>
                <p><a href="{{ url_for('index') }}">Create another user-mapping File</a></p>
                <p></p>
                <h2>File preview:</h2>
                <pre><code>
                    {%- for item in data -%}
                        {{ item }}
                    {%- endfor %}
                </code></pre>
            {% endif %}

        </div>
    </div>
</div>

{% endblock %}
```

#### Jinja filters

Previously, in the *download.html* template, you used HTML preformatted text tags to present the *user-mapping.xml* file preview. This is OK, but could be better. You have limited style options in the preformatted text and the displayed lines are spaced a bit too far apart.

Now that you've learned more about Jinja templates, you can code a better solution using *[Jinja filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#filters)*.

In the *download.html* template, delete the preformatted text tags and use jinja filters to preserve the preview indenting. Replace the text:

```
            <pre><code>
                {%- for item in data -%}
                    {{ item }}
                {%- endfor %}
            </code></pre>
```

With the following text:

```
        <p style="font-size: small; line-height: 1.25; font-family: 'Courier New', Courier, monospace;">
            {% for item in data %}
                {{ item|replace(' ','&nbsp;'|safe )}}<br/>
            {% endfor %}
        </p>
```

Instead of the preformatted text tag, you now use a paragraph tag and specified the style that will be rendered in the browser. But, the blank spaces you use to indent the XML code will not be rendered by the browser. So you need to replace each space character with the HTML code for a space, * *.

As the for loop iterates through the *item* placeholder, the Jinja *replace* filter swaps spaces for HTML non-breaking-space codes and uses the *safe* filter to [prevent Jinja from automatically escaping](https://jinja.palletsprojects.com/en/2.11.x/templates/#working-with-automatic-escaping) the non-breaking-space HTML codes.

The final *download.html* template should look like:

```
{% extends "base.html" %}

{% block title %}Guacamole User Mapper{% endblock %}

{%block content %}

<div class = 'container'>
    <div class = 'row'>
        <div class='col'>
            <h1>Download user-mapping.xml</h1>

            {% if data != None %}
                <p></p>
                <p><a href="{{ download_url }}">Download user-mapping.xml</a></p>
                <p></p>
                <p><a href="{{ url_for('index') }}">Create another user-mapping File</a></p>
                <p></p>
                <h2>File preview:</h2>
                <p style="font-size: small; line-height: 1.25; font-family: 'Courier New', Courier, monospace;">
                    {% for item in data %}
                        {{ item|replace(' ','&nbsp;'|safe )}}<br/>
                    {% endfor %}
                </p>
            {% endif %}

        </div>
    </div>
</div>

{% endblock %}
```

Save the file and refresh the browser. After you upload a configuration file, the download page will look similar to the screenshot below:

![screenshot]({static}/images/flask-web-app-tutorial/flask-060.png){width=90%}

### More styling and content

Make more changes to the templates. At this point, you can use your personal taste to design your web page. To learn a bit more about Bootstrap classes, watch the [Bootstrap course on Scrimba](https://scrimba.com/learn/bootstrap4). The course consists of ten videos covering everything you need to know to produce a page similar to what I have created, below. Each video is only a few minutes long.

In the final templates, listed below, I spent more time refining the positioning of responsive elements in the [Bootstrap grid system](https://scrimba.com/learn/bootstrap4/responsive-grid-systems-in-bootstrap-4-cdm3asD) and I added a [Bootstrap navigation bar](https://scrimba.com/learn/bootstrap4/responsive-navbars-in-bootstrap-4-cPmpLhm) to the web site. 

I also added additional text that explains how to use the program. 

#### The base.html template

The final version of the *base.html* template is shown below:

```
<!doctype html>
<html lang="en">
<head>
    {% block head %}
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    {% block styles %}
        <!-- Bootstrap CSS -->
        {{ bootstrap.load_css() }}
    {% endblock %}
    <title>{% block title %}Your page title{% endblock %}</title>
    {% endblock %}
</head>
<body>
    <nav class="navbar navbar-light bg-light navbar-expand-sm">
        <a href="{{ url_for('index') }}" class="navbar-brand">UserMapper</a>
        <button class="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav ml-auto">
                <li class="navbar-item">
                    <a href="https://www.brianlinkletter.com" target="_blank" class="nav-link" rel="noopener">Network Simulation Blog</a>
                </li>
            </ul>
        </div>
    </nav>
    
    <div class="container-fluid mt-3">

    <!-- Your page content -->
    {% block content %}{% endblock %}

    </div>

    {% block scripts %}
        <!-- Optional JavaScript -->
        {{ bootstrap.load_js() }}
    {% endblock %}
</body>
</html>
```

#### The index.html template

The final version of the *index.html* template is shown below:

```
{% extends "base.html" %}
{% from 'bootstrap/form.html' import render_form, render_field, render_form_row %}

{% block title %}Guacamole User Mapper{% endblock %}

{% block content %}

    <div class='row'>

        <div class="col-md-5 bg-light ml-3">
            <form method='POST' enctype="multipart/form-data" class="p-3">
                {{ render_form(form, button_style="primary", form_type="basic") }}
            </form>
        </div>

        <div class="col-md-6 float-right">
            <div class="ml-3 mt-3">
                <p>UserMapper builds <a href="https://guacamole.apache.org/" target="_blank" rel="noopener">Apache Guacamole remote desktop gateway</a> basic authentication files (user-mapping.xml) for small network emulation labs used by one or more trainers and students. Each user will be given access to the same lab devices.</p>
            </div>
        </div>

    </div>
    <div class="row ml-1">
        
        <div class='col'>
            <hr />
            <h5>Instructions:</h5>
            <p>Upload a YAML configuration file. UserMapper will build a Guacamole basic authentication file based on your configuration. The file name must end with the ".yaml" extension.</p>
            <p>Create a file similar to the example configuration file listed below. You must have at least one user type and one device type. You may add more user types and device types as necessary. You may also add additional device parameters from the <a href="https://guacamole.apache.org/doc/gug/configuring-guacamole.html" target="_blank" rel="noopener">list of Guacamole configuration parameters</a>.</p>
            <p>The <em>username_suffix</em>, device <em>name_suffix</em>, and device <em>hostname_suffix</em> must be a number with or without leading zeros, enclosed in quotes. We generate names by combining the corresponding name prefix and a different name suffix with a length equal to the length of the suffix string and starting at the number specified in the suffix.</p>
            <p>If a user type's <em>password</em> is "random", each user will be assigned a unique random password. If you specify a specific user password, each user in the same user type will have the same password.</p>

            <h5>Example config.yaml file:</h5>

            <p style="font-size: small; line-height: 1.25; font-family: 'Courier New', Courier, monospace;">
            users:<br />
            {{('&nbsp;' * 4)|safe}}trainers:<br />
            {{('&nbsp;' * 8)|safe}}quantity: 2<br />
            {{('&nbsp;' * 8)|safe}}username_prefix: trainer<br />
            {{('&nbsp;' * 8)|safe}}username_suffix: '01'<br />
            {{('&nbsp;' * 8)|safe}}password: random<br /> 
            {{('&nbsp;' * 4)|safe}}students:<br />
            {{('&nbsp;' * 8)|safe}}quantity: 10<br />
            {{('&nbsp;' * 8)|safe}}username_prefix: student<br />
            {{('&nbsp;' * 8)|safe}}username_suffix: '01'<br />
            {{('&nbsp;' * 8)|safe}}password: random<br />
            devices:<br />
            {{('&nbsp;' * 4)|safe}}servers:<br />
            {{('&nbsp;' * 8)|safe}}quantity: 4<br />
            {{('&nbsp;' * 8)|safe}}name_prefix: PC<br />
            {{('&nbsp;' * 8)|safe}}name_suffix: '09'<br />
            {{('&nbsp;' * 8)|safe}}hostname_prefix: '10.0.10.'<br />
            {{('&nbsp;' * 8)|safe}}hostname_suffix: '109'<br />
            {{('&nbsp;' * 8)|safe}}parameters:<br />
            {{('&nbsp;' * 12)|safe}}protocol: rdp<br />
            {{('&nbsp;' * 12)|safe}}hostname: ~<br />
            {{('&nbsp;' * 12)|safe}}port: 3389<br />
            {{('&nbsp;' * 12)|safe}}username: root<br />
            {{('&nbsp;' * 12)|safe}}password: root<br />
            {{('&nbsp;' * 4)|safe}}routers:<br />
            {{('&nbsp;' * 8)|safe}}quantity: 4<br />
            {{('&nbsp;' * 8)|safe}}name_prefix: R<br />
            {{('&nbsp;' * 8)|safe}}name_suffix: '01'<br />
            {{('&nbsp;' * 8)|safe}}hostname_prefix: '10.0.10.'<br />
            {{('&nbsp;' * 8)|safe}}hostname_suffix: '1'<br />
            {{('&nbsp;' * 8)|safe}}parameters:<br />
            {{('&nbsp;' * 12)|safe}}protocol: ssh<br />
            {{('&nbsp;' * 12)|safe}}hostname: ~<br />
            {{('&nbsp;' * 12)|safe}}port: 22<br />
            {{('&nbsp;' * 12)|safe}}username: root<br />
            {{('&nbsp;' * 12)|safe}}password: root<br />
            </p>
        </div>
    </div>

{% endblock %}
```

Refresh the browser and see the results. The index page should look like the screenshot below:

![screenshot]({static}/images/flask-web-app-tutorial/flask-070.png){width=90%}

#### The download.html template

The final version of the *download.html* template is shown below:

```
{% extends "base.html" %}

{% block title %}Guacamole User Mapper{% endblock %}

{%block content %}

<div class = "row">
    <div class="col">
        <p>Thank you for using UserMapper. Your user-mapping.xml file is ready to download. You may check the file preview below to see if everything is correct. If needed, you may generate a new file from another, or updated, configuration file.</p>
    </div>
</div>

<div class = "row">
    <div class="col">
        <a href="{{ download_url }}" class="btn btn-primary col-md-5 mb-1">Download user-mapping.xml</a>
        <a href="{{ url_for('index') }}" class="btn btn-secondary col-md-6 float-right mb-1">Create a new user-mapping.xml file</a>
        <hr />
    </div>
</div>

<div class="row">
    <div class="col">
        <h5>File preview:</h5>
        <p style="font-size: small; line-height: 1.25; font-family: 'Courier New', Courier, monospace;">
        {% for item in data %}
        {{ item|replace(' ','&nbsp;'|safe )}}<br>
        {% endfor %}
        </p>
    </div>
</div>

{% endblock %}
```

Refresh the browser and see the results. After you upload a configuration file to the web site, the download page should look like the screenshot below:

![screenshot]({static}/images/flask-web-app-tutorial/flask-080.png){width=90%}

### Preparing to deploy your Flask application

Currently, you are running your Flask application on your local PC in a *development environment*. All your environment variables are either hard-coded in the source code, or manually configured in the Linux shell in which your application runs. Your application's secret key, which must be kept secret, is visible for all to see in GitHub because it is part of the source code in the *application.py* file.

Before you deploy your application to a public server, you must find a way to protect your application's configuration information from hackers who may scrape GitHub for application configuration information and secret keys. Of course, you could choose not to post your code in a public GitHub repository in order to protect your secret keys. However, you would then lose the benefits of collaborating with a community of open-source developers. In any case, tracking files that contain secret keys in any Git repository -- even a private one -- is bad practice.

In addition, the application configuration information may be different depending on where the application is running. For example, you must run your Flask application in a *production environment* on a public server. 

This section of the tutorial shows you how to set up a configuration file that [sets up environment variables for your development environment](https://hackingandslacking.com/configuring-your-flask-application-4e5341d7affb). You can then configure Git to ignore the configuration file. Depending on the platform you use to deploy your application to a public-facing web site, you may have a separate configuration file on the remote server.

#### Environment variables

You need to store your [environment variables in a separate file](https://flask.palletsprojects.com/en/1.1.x/cli/#environment-variables-from-dotenv) that we can set Git to ignore, so it will never be uploaded to your public GitHub repository. That file is typically named *.env* and is referred to as a "dot-env" file. 

You must especially protect the SECRET_KEY environment variable. Up until now, you've been using a dummy secret key. You need to [generate a secure secret key](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions). Use the following Python command to generate a secret key you can use.

```
$ python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
```

Copy the output to the clipboard so you can paste it into the *.env* file.

Create a new file named *.env* in the *usermapper-flask* directory. Define the following environment variables in the file:

```
FLASK_APP=application
FLASK_ENV=development
SECRET_KEY=b8rD0UJDkrr6MrdP8RQ1GpLPEA_SYsrrIfMuTjfw5AI
```

Many other environment variables affect both Flask and Bootstrap. You can modify the operation and appearance of your program, to some degree, just by defining additional environment variables in the *.env* file.

##### Add the *.env* file to *.gitignore*

To prevent yourself, from accidentally uploading the secret key to GitHub, add the *.env* file to *.gitignore*:

```
(env) $ cd ~/Projects/usermapper-web
(env) $ echo '.env' >> .gitignore
```

> **Note:** If you are using the [standard Flask *.gitignore* file from the Flask web site](https://github.com/pallets/flask/blob/master/.gitignore), you already have a line in the file that ignores the *.env* file.

Other programmers who clone your project's GitHub repository will be missing the *.env* file so the program will not work for them until they build their own *.env* file. They can infer which variables need to be defined in the file by looking at the source code in *application.py*. Most open-source Python projects have documentation for developers that tells them which environment files they need to define. That's another item for my to-do list.

##### Install *python-dotenv*

To enable Python programs to read the contents of the *.env* file, you must install the the [*python-dotenv* package](https://github.com/theskumar/python-dotenv#python-dotenv-----) in your Python virtual environment.

```
(env) $ pip install python-dotenv
```

##### Modify *application.py*

Edit the *application.py* file. Import the *load_dotenv* module from the *dotenv* package.

```
from dotenv import load_dotenv
```

Delete the secret key and content length configuration lines in *application.py*:

```
app.config['SECRET_KEY'] = 'fix this later'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
```

And replace them with the following configuration, which first finds the *.env* file and then configures the Flask app using the variables defines in the *.env* file:

```
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['FLASK_APP'] = os.environ.get('FLASK_APP')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
```

In the above code, you build the path to the *.env* file and to load the environment variables from that file. Then we get each environment variable and use it to configure the Flask app.

Save the file. Refresh the browser. Everything should work the same as before except that now, when we commit the changes and push them to Github, we have a secret key that remains on our local PC but does appear anywhere in the public GitHub repository.

#### Saving the requirements.txt file

To simplify installing the Flask application on a remote server, create a *requirements.txt* file for the Flask application. 

If you run the *pip freeze* command, you will see a lot of packages in the file, but you only need a few of them. Also, you need to configure the requirements file so the *Usermapper* package is installed from my GitHub repository.

Create a file named *requirements.txt* in the *usermapper-web* directory. You previously installed flask, Flask-WTF, python-dotenv, and bootstrap-flask so add them to the file. Add the wheel package because it is needed to install the others. Also, install the usermapper package from its Git repository. The Usermapper setup script installs pyyaml so you don't need to list pyyaml in your *requirements.txt* file. 

Add the following lines to the *requirements.txt* file.

```
wheel
flask
Flask-WTF
python-dotenv
bootstrap-flask
git+https://github.com/blinklet/usermapper.git@v0.3#egg=usermapper
```

Test the requirements.txt file by deactivating the current Python virtual environment and creating a new environment named *newenv* in the *usermapper-web* directory:

```
(env) $ deactivate
$ python3 -m venv newenv
$ source newenv/bin/activate
(newenv) $ pip install -r requirements.txt
(newenv) $ flask run
```

Refresh the browser. The app should work as expected.

Then delete the test environment and switch back to the original.

```
(env) $ deactivate
$ rm -rf newenv
$ source env/bin/activate
(env) $
```

#### *application.py* listing

The application.py source code should now look like the listing below:

```
from flask import Flask, render_template, send_from_directory, url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os, tempfile
import yaml
from usermapper.usermapper import xmlwriter
from usermapper.mapperdata import get_users
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv

app = Flask(__name__)
bootstrap = Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['FLASK_APP'] = os.environ.get('FLASK_APP')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

class MyForm(FlaskForm):
    filename = FileField('Select configuration file: ', 
        validators=[FileRequired(), FileAllowed(['yaml'], 
        message='Only YAML files accepted')], 
        description="Only YAML files accepted")
    submit = SubmitField('Upload')
    
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

@app.route('/download_page/<temp_folder>', methods=('GET','POST'))
def download_page(temp_folder):
    filename = os.path.join(
        os.path.relpath(os.path.dirname(__file__)), 
        'downloads',temp_folder,'user-mapping.xml')

    with open(filename) as preview:
       data = preview.readlines()
    
    download_url = url_for('download', tempfolder=temp_folder, filename='user-mapping.xml')

    return render_template('download.html', 
        data=data, download_url=download_url)

@app.route("/download/<tempfolder>/<filename>", methods=('GET','POST'))
def download(tempfolder,filename):
    basedir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        'downloads')
    temp_dir = os.path.join(basedir,tempfolder)
    return send_from_directory(
        temp_dir, filename, as_attachment=True)
```

#### Commit changes to Git

Commit these changes to git and push them to GitHub. 

```
(env) $ git add .
(env) $ git commit -m 'added envonment variables in env file'
(env) $ git push
(env) $
```

### Deploying a Flask application to Microsoft Azure

Now you are ready to deploy the web application to a remote server. You have two different ways to deploy the applications. 

You may purchase a remote server and install the application on it, in which case you will follow the same procedures you used to run the application on your local PC but you will need to install a production-grade WSGI server and do some extra work to ensure your server is secure. Many companies provide virtual private servers that you can configure and use according to your needs. Some companies I am familiar with are [Linode](https://www.linode.com), [DigitalOcean](https://www.digitalocean.com/), [Microsoft Azure Virtual Machines](https://azure.microsoft.com/en-us/services/virtual-machines/), [Amazon AWS EC2](https://aws.amazon.com/ec2/), and [Google Compute](https://cloud.google.com/compute/). 

Alternatively, you may deploy your Python program to a [Python web-app platform-as-a-service](https://www.fullstackpython.com/platform-as-a-service.html), in which case you do not need to create and secure a remote server, but you will need to learn the specific features and functions of the web-app service you choose and may not have access to all the functions you normally use on your own server. There are many Python web app services you may use, such as [Heroku Cloud Application Platform](https://www.heroku.com/), [Microsoft Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/overview), [Google App Engine](https://cloud.google.com/appengine/), [Amazon AWS CodeStar](https://aws.amazon.com/codestar/?nc=bc&pg=pr), [PythonAnywhere](https://www.pythonanywhere.com/), [Platform.sh](https://platform.sh/marketplace/python/), [DigitalOcean App Platform](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-app-using-gunicorn-to-app-platform), and more. To get started, look for one that offers a free tier of service for small applications with low usage.

In this tutorial, I chose to use a web app platform because I did not want to spend more time learning studying WSGI servers and web server security. The platform-as-a-service I choose will have dozens of engineers working to keep my application's environment secure. All I need to do is follow the service's instructions to deploy my app.

This tutorial uses the [Microsoft Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/overview) because Azure offers a permanently-free app-service tier.

#### Azure Portal 

If you do not already have an Azzure account, [create one](https://azure.microsoft.com/en-us/free/).  The Azure Portal web interface is available at: [https://portal/azure.com](https://portal/azure.com). 

Follow the Azure quickstart documentation about deploying a Python web app. The [Azure Web App Quick-Start Guide](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask), which uses the Azure CLI, is the easiest way to deploy your web-app to Azure.

#### Azure CLI 

Install the [Azure command-line interface (CLI)](https://docs.microsoft.com/en-us/cli/azure/) on your Linux PC. Run the following command:

```
(env) $ curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Login to your Azure account:

```
(env) $ az login
```

A browser window will open and prompt you to login. Follow the instructions in the browser. After you login, you may close the browser window or tab.

#### Deploy your web app using Git

You already have a *usermapper-web* Git repository on your PC. Use the Azure CLI to deploy your web app to an Azure Web App by following the steps outlined below. 

Deploy the *usermapper-web* web app with the command:

```
(env) $ cd ~/Projects/usermapper-web
(env) $ az webapp up --sku F1 --name usermapper 
```

The *F1* web app size is the free tier. 

Look at the output generated by the command, listed below. The Azure CLI automatically creates a lot of resources for you. 

```
The webapp 'usermapper' doesn't exist
Creating Resource group 'mail_rg_Linux_centralus' ...
Resource group creation complete
Creating AppServicePlan 'mail_asp_Linux_centralus_0' ...
Creating webapp 'usermapper' ...
Configuring default logging for the app, if not already enabled
Creating zip with contents of dir /home/brian/usermapper-web ...
Getting scm site credentials for zip deployment
Starting zip deployment. This operation can take a while to complete ...
Deployment endpoint responded with status code 202
You can launch the app at http://usermapper.azurewebsites.net
{
  "URL": "http://usermapper.azurewebsites.net",
  "appserviceplan": "mail_asp_Linux_centralus_0",
  "location": "centralus",
  "name": "usermapper",
  "os": "Linux",
  "resourcegroup": "mail_rg_Linux_centralus",
  "runtime_version": "python|3.7",
  "runtime_version_detected": "-",
  "sku": "FREE",
  "src_path": "//home//brian//usermapper-web"
}
```

See the web app information in the command's output. Go to the URL listed in the deployment response: http://usermapper.azurewebsites.net. You should see a server error. How do you debug this?

##### Check web app logs

To investigate the error, look at web app logs in the Azure portal. Or, run the following Azure CLI command:

```
(env) $ az webapp log tail --name usermapper
```

If you see a lot of logs, and no obvious errors, you may need to search for the "error" keyword:

```
(env) $ az webapp log tail --name usermapper | grep -i error
2020-12-11T21:26:52.422108240Z     raise RuntimeError(message)
2020-12-11T21:26:52.422113040Z RuntimeError: A secret key is required to use CSRF.
```

It looks like you do not have a secret key configured. This is because you did not configure the environment variables for the web app. The remote web app's environment is a production environment, so the FLASK_ENV variable must be set to *production*. The SECRET_KEY variable also needs to be configured in the remote web app's environment and it can either be the same as, or different from, the secret key you configured in your local *.env* file.

Quit the command with CTRL-C.

##### Configure web app environment variables

The Azure Portal offers an intuitive user interface for changing the [Azure web application configuration settings](https://docs.microsoft.com/en-us/azure/app-service/configure-common) but it's easier to show the command-line-interface in a blog post like this so [use the Azure CLI to configure the web app](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python). In your Linux PC's terminal window, enter the Azure CLI command shown below, except your resource group name and web app name will be different:

```
(env) $ az webapp config appsettings set \
        --name usermapper \
        --resource-group mail_rg_Linux_centralus \
        --settings FLASK_ENV="production" \
        FLASK_APP="application" \
        SECRET_KEY="b8rD0UJDkrr6MrdP8RQ1GpLPEA_SYsrrIfMuTjfw5AI"
```

You configured the environment variables for the FLASK_APP, FLASK_ENV, and SECRET_KEY environment variables. Now go to the web app URL: [http://usermapper.azurewebsites.net](http://usermapper.azurewebsites.net).

The application looks like it works. Upload a config file. Then download the *user-mapping.xml* file. It seems to work OK.

#### The web app's filesystem

Remember that the usermapper program saves downloaded files in temporary directories. Have a look at the web app's filesystem and see those files on the remote web app service. 

Azure offers an SSH console connection to the container running the web app. Log into the Azure web app container by doing the following:

* Go to "App Services" in the Azure portal
* Click on the "usermapper" web app
* Click on "SSH"

![screenshot]({static}/images/flask-web-app-tutorial/flask-090.png){width=90%}

Finally, click on the "go" link in the SSH Panel. A new browser tab will open runnning an SSH session connected to the web app's container. 

In the browser's SSH tab, run the following commands:

```
# cd downloads
# ls 
tmphqspiosn  tmpnwjs1vmj
```

![screenshot]({static}/images/flask-web-app-tutorial/flask-100.png){width=90%}

See one or more temporary directories have already been created. Each one should contain a *user-mapping.xml* file.

##### Problems cleaning up files on a web app

Unfortunately, you cannot delete these temporary files on a scheduled basis using the same method you used when you were developing the web app.

On your local PC, you used a cron job to delete temporary files every 20 minutes. I tried installing *cron* in the web app container and editing the crontab file, the same way I did when I was testing on my local PC. Installation and configuration worked OK. However, the web app container pauses itself when it is not being actively used so, given that it is very rarely used right now, it is almost always paused. Unless the container is actively running when its system clock ticks past a 20-minute mark on its clock, the cron service will not delete any temporary files.

This is a case where using a database would solve the problem because a managed database service can be configured to delete old data. 

For now, because you want to use the free service provided by Microsoft Azure, you need to occasionally log into the web app's SSH console and manually delete old temporary files so your web app's disk space does not fill up. 

Azure offers a platform service called *WebJobs* that runs a script on a scheduled basis, which could clean up files for you. Regretably, the [WebJobs service](https://docs.microsoft.com/en-us/azure/app-service/webjobs-create#CreateScheduledCRON) is not available for Python apps. Maybe it will be available for Python apps in the future.

#### Custom domain name

Currently, your web app is a subdomain in the *azurewebsites.net* domain. 

If you want to [map a custom domain name to your new web app](https://docs.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-custom-domain), you must upgrade to a paid Azure Web Services tier. I chose not to upgrade to a paid service tier at this time.

#### Paid options for web app deployment

If you already paid for a custom domain name registration, then you are probably willing to spend some money on hosting your web app. If that is the case, you could upgrade to a Basic Azure App Service tier, which costs at least $14 per month. Then, you could refactor your application to use a database and use one of Microsoft Azure's managed database services to your web app. For a small application like this, the database cost would be very low. The Azure App Service already includes value-added services like load balancers and content delivery networks (CDNs).

If you want to keep costs low, purchase a cheap virtual private server (VPS) from any cloud infrastructure provider, including Azure, for around $5 per month. You take on more system administration responsibilities when you [deploy a web app on remote VPS](https://www.linode.com/docs/guides/flask-and-gunicorn-on-ubuntu/). However, you gain more control over the system so you could use cron or any other method you prefer to clean up old files. You can also configure a custom domain to point to a VPS for free, after paying for the domain, and use SSL encryption for free.

### Conclusion

This tutorial showed you how to convert an existing Python command-line program into a web app so users can more easily access it. You learned how to use Flask to upload and download files, how to get user input using HTML forms, and how to use Bootstrap to make your application look professional while learning just the minimum you need to know about HTML and CSS. You also learned how to deploy a web app to a Python platform-as-a-service that costs nothing.

While working on this tutorial, I found a [web app that helps developers create cron expressions](https://www.freeformatter.com/cron-expression-generator-quartz.html), based on information they enter in the user interface. This is both a great tool and a good example of how the tools you develop may be made available to others.