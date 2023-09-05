title: Add a database to a web app
slug: web-app-database-python
summary: Most web applications need to store data. Even if they do not store user data, they need to temporarily cache data so it can be passed between the application's routes or views. Many developers choose to use a database to solve this problem. This post shows how I added a database to my *usermapper-web* web app.
date: 2023-09-07
modified: 2023-09-07
category: Databases
<!-- status: Published -->


Flexibility:
- Can use any database service in the cloud when deploying -- just have to change some variables
- Or, can deploy using containers

Options:

Flask Session cookies
- store entire XML doc on user's browser?
https://sparkdatabox.com/tutorials/python-flask/flask-session

Flask Cache
https://flask-caching.readthedocs.io/en/latest/
   - can use filesystem cache, memory cache, https://stackoverflow.com/questions/18562006/efficient-session-variable-server-side-caching-with-pythonflask
   - use filesystem cache or memory cache with Gunicorn where works may be > 1 because: https://stackoverflow.com/questions/32149736/gunicorn-flask-caching/69903128#69903128

Use "Flask-Session" extension
https://flask-session.readthedocs.io/en/latest/
   - can use with database (better than using filesystem for complex apps. My app does not care)
   https://vegibit.com/how-to-use-sessions-in-python-flask/
   https://pythongeeks.org/flask-session/

Database
   - key off userid from session cookie?
   - allows your users to resume their transaction even if their browser crashes  (but only if I set up logins)


Idea:
1) flask session cookie with user's ID
2) ID is a key in table
3) save XML string in tables with key
4) When session ends, delete the row using the key
5) Upgrade to Flask-session


maybe use Redis, which can automatically timeout data?

json-ify the usermapper xml?

xml native in database???

How to return a file from DB??
https://stackoverflow.com/questions/60499958/what-is-the-best-way-to-store-an-xml-file-in-a-database-using-sqlalchemy-flask

https://realpython.com/flask-connexion-rest-api/
https://realpython.com/flask-connexion-rest-api-part-2/
https://realpython.com/flask-connexion-rest-api-part-3/

multiple-container apps
https://docs.docker.com/get-started/07_multi_container/



flask sessions
https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/


Use StringIO 
https://stackoverflow.com/questions/44672524/how-to-create-in-memory-file-object




future app ideas
- draw a diagram and create XML user-mapping file for it
     network diagram example: https://github.com/MJL85/natlas