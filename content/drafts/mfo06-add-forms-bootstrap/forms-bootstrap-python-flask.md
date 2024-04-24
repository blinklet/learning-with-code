title: Add buttons and forms your Flask web site
slug: add-buttons-forms-python-flask-web-site
summary: Use Boostrap-Flask and Flask-WTF extensions to create interactive, attractive buttons and forms to your Flask web site
date: 2024-05-20
modified: 2024-05-20
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

Add interactive features to your web site

Buttons, by themselves, can act like a link that sends user to a new Flask route or a new web page. **Can they also activate functionality???**

Forms, usually with a *Submit* button, enable users to add control the web application or input data. Forms can be created easily using the *Flask-WTF* extension. However, if you want the forms to look attractive, **you need to take write more detailed templates...** 

## Basic setup

To create a simple example, let's start with a "toy" Flask application that uses an SQLite database and pre-populates it with some data. Then we'll add buttons and forms that manipulate data in the database.

```text
# requirements.txt

Flask
Flask-SQLAlchemy
Flask-WTF
Bootstrap-Flask
```


```python
# app.py


```
