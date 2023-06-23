# Extra

Prepare the environment

Use Azure CLI to create a sample DB
https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-cli
https://learn.microsoft.com/en-us/azure/azure-sql/database/scripts/create-and-configure-database-cli?view=azuresql

Use Azure Portal
https://learn.microsoft.com/en-ca/azure/azure-sql/database/free-sql-db-free-account-how-to-deploy?view=azuresql
https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal


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
$ python3 -m venv env
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
from dotenv import load_dotenv, find_dotenv

print(find_dotenv('.env'))

load_dotenv(override=True)
```

```python
import os

db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_UID')
db_passwd = os.getenv('DB_PWD')

print(db_server, db_name, db_user, db_passwd)
```

```python
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"+
    "Server=tcp:"+db_server+",1433;"+
    "Database="+db_name+";"+
    "Uid="+db_user+";"+
    "Pwd="+db_passwd+";"+
    "Encrypt=yes;"+
    "TrustServerCertificate=no;"+
    "Connection Timeout=30;"
)

print(connection_string)
```

```python
import pyodbc
conn = pyodbc.connect(connection_string)
print(conn)
```