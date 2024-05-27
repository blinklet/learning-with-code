
## Dynamic navbars in blueprints

Check out the @nav.navigation decorator
Would this work in a blueprint?
https://pythonhosted.org/flask-nav/advanced-topics.html#dynamic-construction




Flask-Nav with Blueprints
https://gist.github.com/thedod/eafad9458190755ce943e7aa58355934


When you run the app again, you'll find that logged-in users who have the *Admin* role can see the *Admin* and *Account* links. Users who have the *User* role can see the *Account* link. Users who have no role assigned, which is all users who registered via teh *Register* page, will not see either the *Admin* nor the *Account* link in the navbar.


## Make a dynamic navbar

The application navbar currently displays the same links to every user, regardless of whether they have permission to visit those links. 

To demonstrate this, logout of the application my entering the URL, `http://localhost:5000/logout` into the browser search bar. Then, login as userid `user1@testmail.com` with password `password`. 

Now, if you click on the *Admin* link, you will see a message indicating you do not have access to the page:

![User cannot access Admin page](./images/navbar-07-admin-forbidden.png)

I want to make the navbar dynamic, so it only shows the elements that the user is allowed to access.

### When a navbar is created

In the previous version of this application, we create the navbar object when the application registers its blueprints. This only happens when the application starts. 

When the application starts, no users are logged in so it is impossible to build a global navbar that responds to users' permissions.

You can solve this problem two ways:

* Create a [Flask signal](https://flask.palletsprojects.com/en/3.0.x/signals/) that runs a function when a user logs in. This will build a new global navbar whenever a new user logs in. This is good if the navbar will never change after the user logs in.
  * Use either the *[flask_login.user_logged_in.connect_via()](https://flask-login.readthedocs.io/en/latest/#signals)* decorator or *flask_security.signals.user_authenticated.connect_via()* decorator  on a navbar-building function in the main app file.
  * Unfortunately, you cannot use these decorators in the blueprints' views.py modules because the signal will only be handled when the sender is the main app or in the blueprint. If the login action doesn't happen in a route belonging to the blueprint, the signal won't be triggered. The login action takes place in Flask-Security-Too blueprint, and we can't include this function there. So, this solution will not work for our use-case.
* Create a function that will run every time a template is rendered. This is good if the navbar changes depending on other application states, in addition to depending on which user is logged in.
  * Use the *[Blueprint.app_context_processor()](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.context_processor)* decorator on the navbar-building function in each blueprint.


Now, I want to change my application so that the navigation bar 

use app_context_manager

From: 
https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.context_processor

    Registers a template context processor function. These functions run before rendering a template. The keys of the returned dict are added as variables available in the template.

    This is available on both app and blueprint objects. When used on an app, this is called for every rendered template. When used on a blueprint, this is called for templates rendered from the blueprint’s views. To register with a blueprint and affect every template, use Blueprint.app_context_processor().

    Like context_processor(), but for templates rendered by every view, not only by the blueprint. Equivalent to Flask.context_processor().

because we need every navbar to be recalculated every time the user is redirected to a new view function, because the dynamic navbars from other blueprints may have changed due to the state of the application.












context manager
https://stackoverflow.com/questions/71834254/flask-nav-navigation-alternative-for-python-3-10
https://stackoverflow.com/questions/34487967/flask-nav-with-dynamic-secondary-navbar



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


