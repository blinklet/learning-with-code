Set environment variables for database login information

##### NO
##### Does not pass variable to virtual environment
##### Try Python .env file and 
##### https://analyzingalpha.com/jupyter-notebook-environment-variables-tutorial
#####








edit the */etc/environment* file:

```bash
$ sudo nano /etc/environment
```

Remember you saved your database information in another location, like a secure vault or a password manager. Add the lines containing the database information to the */etc/environment* file. The additional lines would look like below, with the values changed to your database information.

```
DB_UID="CloudSA18f60e2c"
DB_PWD="3ANq!vyhb9qA"
DB_SERVER="brian-dbserver.database.windows.net"
DB_NAME="data-science-test"
```

Then read the file:

```bash
$ source /etc/environment
```




```python
import os

if 'DB_UID' in os.environ:
    userid = os.environ.get('DB_UID')
else:
    raise exception('DB_UID environment variable is not set')

if 'DB_PWD' in os.environ:
    password = os.environ.get('DB_PWD')
else:
    raise exception('DB_PWD environment variable is not set')

if 'DB_SERVER' in os.environ:
    db_server_name = os.environ.get('DB_SERVER')
else:
    raise exception('DB_SERVER environment variable is not set')

if 'DB_NAME' in os.environ:
    db_name = os.environ.get('DB_NAME')
else:
    raise exception('DB_NAME environment variable is not set')
```

Then start notebook


```python
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};" +
    "Server=tcp:" + db_server_name + ",1433;" +
    "Database=" + db_name + ";" +
    "Uid=" + userid + ";" +
    "Pwd=" + password + ";" +
    "Encrypt=yes;" +
    "TrustServerCertificate=no;" +
    "Connection Timeout=30;"
)
```

```python
conn = pyodbc.connect(connection_string)
```

