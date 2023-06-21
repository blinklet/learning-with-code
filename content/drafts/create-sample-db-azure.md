title: Create a sample database on Azure cloud
slug: create-sample-db-azure
summary: Create your own personal database server on Microsoft's Azure cloud, populate it with sample data, and run the server on Azure's free service tier, which lasts for twelve months
date: 2022-05-14
modified: 2022-05-14
category: Databases
<!--status: published-->

[Data science](https://en.wikipedia.org/wiki/Data_science) has been a hot topic for more than a few years. There is a lot of information available online that will help you learn how to use Python to work with data. But I noticed one particular topic is often not covered in enough practical detail: how to use Python to access data from an SQL database.

Many data sets that are [available to the public](https://www.dropbase.io/post/top-11-open-and-public-data-sources) but very few of them run on database servers. If you want to learn how to analyze data stored in a database, you need readily-available sample data that can be loaded into the database and you need access to a database server. 

Microsoft offers solutions to both these challenges. They offer the multiple [sample databases](https://learn.microsoft.com/en-us/sql/samples/sql-samples-where-are?view=sql-server-ver16) and they make it easy to create a free [^1] database server that is [pre-loaded with the AdventureWorks sample database](https://learn.microsoft.com/en-ca/azure/azure-sql/database/free-sql-db-free-account-how-to-deploy?view=azuresql). 

[^1]: Microsoft Azure offers a [free service tier](https://azure.microsoft.com/free/) that, in addition to offering $200 in services for free for 30 days, allows you to run small configurations of certain service for 12 months at no cost.

This post will show you how to create your own personal database server on Microsoft's Azure cloud, populate it with the AdventureWorks sample database, and connect to the server. I will cover the details of exploring databases using various Python functions in future posts.

## Create a free SQL Server on Azure

Microsoft Azure allows many different methods to configure services. You may use [Azure Portal](https://learn.microsoft.com/en-us/azure/azure-portal/), [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest), [Azure Resource Manager](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview), [Terraform](https://learn.microsoft.com/en-us/azure/developer/terraform/overview), Microsoft's [Python API](https://learn.microsoft.com/en-us/python/api/overview/azure/resources?view=azure-python), and more.

Azure Portal is a web interface and is easy to use, but Azure CLI easiest to include in a blog post where the reader may want to copy and paste steps. I will show you how to quickly create a sample database using Azure CLI and then show you how to connect to it using Python libraries. I will show you how to use Azure Portal in an appendix at the end of this post. I'll write about suing the Azure Python API to create a server in a future post.

### Create an Azure account

If you do not already have an Azure account, [create one](https://learn.microsoft.com/en-us/dotnet/azure/create-azure-account). Go to [https://azure.com](https://azure.com) and click on the *Free account* button.

![Azure sign up page](../images/create-sample-db-azure/create-account-01.png)

In the next few pages that appear, you agree to terms and conditions and enter your user information such as your e-mail address and password.


### Install Azure CLI

Azure CLI can be installed on [all major operating systems](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli), including Linux. To install Azure CLI on Ubuntu, run the following command in your terminal window:

```bash
$ curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Or, if you don't like piping a third-party bash script through *sudo*, follow the [step-by-step install instructions](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt#option-2-step-by-step-installation-instructions) provided by Azure.

### Log into your Azure account

To login to your Azure account using Azure CLI, run the following command:

```bash
$ az login
```


### Create an Azure SQL Server

## Connect your Python program to the Azure SQL Server

### Authenticating your Python program

## Appendix A: Create Azure SQL Server using Azure Portal






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
$ python3 venv env
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






