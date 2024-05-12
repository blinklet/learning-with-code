title: Add a navigation bar to your Flask web app
slug: python-flask-navbar
summary: How to create a nav-bar that helps users understand if they are logged in and what web app features they have access to.
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
    width:80%;
}
</style>




flask-nav
https://pythonhosted.org/flask-nav/
supported by flask-bootstrap (https://pythonhosted.org/Flask-Bootstrap/nav.html) but has not been updated in a long time

flask-nav3
https://github.com/wtfo-guru/flask-nav3
A "supported" fork of flask-nav but has only 2 stars



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




