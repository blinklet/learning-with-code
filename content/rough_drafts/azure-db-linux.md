Prepare the environment

https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-cli
https://learn.microsoft.com/en-ca/azure/azure-sql/database/free-sql-db-free-account-how-to-deploy?view=azuresql

Get US$200 free credits for one month
Also get a basic SQL database for 12 months for free

Do the sign up routine
Credit card, etc
Agree to rules

Create new DB
Create resource group in the form

Create new server
(goes to new screen)

Add AD admin
selected "Azure Portal" -- I hope it works

cleared the checkbox "Support only Azure Active Directory authentication for this server". 
click "Save"

The configure the server

Set up access:
https://learn.microsoft.com/en-ca/azure/azure-sql/database/network-access-controls-overview?view=azuresql




https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-python?view=azuresql

https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/tutorial-windows-vm-access-sql



Download the Microsoft [ODBC driver](https://github.com/mkleehammer/pyodbc/) from their [downloads page](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows)

Direct link to file
https://go.microsoft.com/fwlink/?linkid=2223270

Then run the following command in PowerShell or CMD console, or double-click the installer file:

https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline


```bash
$ sudo su
# curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
# exit
$ sudo apt update
$ sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
$ echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
$ source ~/.bashrc
```





Install the Client Components and the SDK

Then set up your Python virtual environment

```bash
$ mkdir project_dir
$ cd project_dir
$ python -Xfrozen_modules=off -m venv env
$ source env/bin/activate
(env) $ cc 
(env) $ pip install pandas
(env) $ pip install openpyxl xlsxwriter xlrd
(env) $ pip install jupyterlab
(env) $ pip install SQLAlchemy
(env) $ pip install azure-identity
```

Create and run a notebook

```bash
(env) $ jupyter-lab
```

Click on URL in terminal

Save-As "azure-db-python".

```python
import pyodbc
server = 'brian-dbserver.database.windows.net'
database = 'data-science-test'
username ='brian.e.linkletter@gmail.com'
Authentication='ActiveDirectoryInteractive'
driver= '{ODBC Driver 18 for SQL Server}'
conn = pyodbc.connect('DRIVER='+driver+
                      ';SERVER='+server+
                      ';PORT=1433;DATABASE='+database+
                      ';UID='+username+
                      ';AUTHENTICATION='+Authentication
                      )

print(conn)
```

from sqlalchemy import create_engine
engine = create_engine('mssql+pyodbc://bDriver={ODBC Driver 18 for SQL Server};Server=tcp:brian-dbserver.database.windows.net,1433;Database=data-science-test;Uid=brian.e.linkletter@gmail.com;Pwd=gpWQ%y3Xv29F;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryPassword')





import pyodbc
server = 'databaseserver.net'
database = 'db_name'
username ='brian.linkletter@test.com'
Authentication='ActiveDirectoryInteractive'
driver= '{ODBC Driver 18 for SQL Server}'
conn = pyodbc.connect('DRIVER='+driver+
                      ';SERVER='+server+
                      ';PORT=1433;DATABASE='+database+
                      ';UID='+username+
                      ';AUTHENTICATION='+Authentication
                      )

print(conn)




server_name = 'azure-db-test.database.windows.net'
database_name = 'azure-test'
username = 'brian@url.com'
password = 'XX**XX**XX**!'

connection_string = f"mssql+pymssql://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+18+for+SQL+Server"

engine = create_engine(connection_string)




engine = create_engine('mssql+pyodbc://username:brian.linkletter@test.com@database/db_name?driver=ODBC+Driver+18+for+SQL+Server')


from sqlalchemy import URL

url_object = URL.create(
    driver='{ODBC Driver 18 for SQL Server}',
    username='brian@url.com',
    authentication='ActiveDirectoryInteractive'
    server='azure-db-test.database.windows.net',
    database='azure-test',
)

engine = create_engine(url_object)

#engine = create_engine("mssql+pyodbc://scott:tiger@mydsn")




from sqlalchemy.engine import URL
credentials = {
    'username': 'brian@url.com',
    'password': 'XX**XX**XX**!',
    'host': 'azure-db-test.database.windows.net',
    'database': 'azure-test',
    'port': '1433'}
connect_url = URL.create(
    'mssql+pyodbc',
    username=credentials['username'],
    password=credentials['password'],
    host=credentials['host'],
    port=credentials['port'],
    database=credentials['database'],
    query=dict(driver='ODBC Driver 18 for SQL Server'))


jdbc:sqlserver://brian-dbserver.database.windows.net:1433;database=data-science-test;user={your_username_here};password={your_password_here};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;authentication=ActiveDirectoryPassword


from sqlalchemy.engine import URL
connection_string = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=dagger;DATABASE=test;UID=user;PWD=password"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

from sqlalchemy import create_engine
engine = create_engine(connection_url)

data-science-test




servername = 'azure-db-test.database.windows.net'
dbname = 'azure-test'
engine = create_engine('mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server')





```python
from sqlalchemy import create_engine
from azure.identity import InteractiveBrowserCredential
import pyodbc

server_name = 'brian-dbserver.database.windows.net'
database_name = 'data-science-test'

credential = InteractiveBrowserCredential()

# token fails "applications owned and operated by Microsoft must get approval from the API owner before requesting tokens for that API."
#token = credential.get_token('azure-db-test.database.windows.net')

token = credential.get_token(https://database.windows.net/)

connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server_name};Database={database_name};Authentication=ActiveDirectoryInteractive;UID='';PWD='';AccessToken={token.token}"

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
```




Base = automap_base()
Base.prepare(autoload_with=engine)





metadata = MetaData()

# list of tables...
tables = ['Snapshot P24 Last Close']
metadata.reflect(engine, only=tables)

Base = automap_base(metadata=metadata)
Base.prepare













```
from sqlalchemy import create_engine
engine = create_engine('mssql+pyodbc://bDriver={ODBC Driver 18 for SQL Server};Server=tcp:brian-dbserver.database.windows.net,1433;Database=data-science-test;Uid=brian.e.linkletter@gmail.com;Pwd=gpWQ%y3Xv29F;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryPassword')
```


Driver={ODBC Driver 18 for SQL Server};Server=tcp:brian-dbserver.database.windows.net,1433;Database=data-science-test;Uid=brian.e.linkletter@gmail.com;Pwd=gpWQ%y3Xv29F;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryPassword

