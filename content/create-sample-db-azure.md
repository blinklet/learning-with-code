title: Create a sample database on Azure cloud
slug: create-sample-db-azure
summary: For the purpose of practicing data analytics programming, create your own personal database server on Microsoft's Azure cloud, populate it with sample data, and run the server on Azure's free service tier
date: 2023-05-30
modified: 2023-05-30
category: Databases
status: published

<!--
A bit of extra CSS code to center all images in the post
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

The best way to start learning [Data science](https://en.wikipedia.org/wiki/Data_science) is to work on practical projects. You can find a lot of information available online that will help you learn how to use Python to work with data and there are many [data sets available to the public](https://www.dropbase.io/post/top-11-open-and-public-data-sources) for practicing data analytics. Almost all public data sets are made available as [CSV files](https://fileinfo.com/extension/csv) or from an [API](https://www.ibm.com/topics/api).

After reviewing data science books, courses, and online resources, I noticed one particular topic is not covered in enough practical detail: how to use Python to access data from an SQL database. If you do not have access to an existing database, and want to learn how to analyze data stored in a database, you have to create your own sample database, preferably pre-loaded with a [sample data set](https://learn.microsoft.com/en-us/sql/samples/sql-samples-where-are?view=sql-server-ver16).

This post will show you how to [create your own free database server](https://learn.microsoft.com/en-ca/azure/azure-sql/database/free-sql-db-free-account-how-to-deploy?view=azuresql) [^1] on Microsoft's Azure cloud, populate it with the [AdventureWorks sample database](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms), and connect to the server. I will cover the details of exploring databases using various Python functions in future posts.

[^1]: Microsoft Azure offers a [free service tier](https://azure.microsoft.com/free/) that, in addition to offering $200 in services for free for 30 days, allows you to run small configurations of certain services, like a small SQL Server, for 12 months at no cost.

## How to configure services in Azure's free service tier

Microsoft Azure allows many different interfaces for configuring services. You may use [Azure Portal](https://learn.microsoft.com/en-us/azure/azure-portal/), [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest), [Azure Resource Manager](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview), [Terraform](https://learn.microsoft.com/en-us/azure/developer/terraform/overview), Microsoft's [Python API](https://learn.microsoft.com/en-us/python/api/overview/azure/resources?view=azure-python) [^2], and more.

[^2]: I cover Azure's Python API in my post about [creating the *azruntime* program]({filename}manage-azure-infrastructure-python.md).

Azure CLI is easiest interface to include in a blog post where the reader may want to copy and paste steps. I will show you how to quickly create a sample database using Azure CLI and then show you how to connect to it using Python libraries. 

If, instead, you want to use Azure Portal to create your sample database, follow the [instructions in Microsoft's Azure documentation](https://learn.microsoft.com/en-ca/azure/azure-sql/database/free-sql-db-free-account-how-to-deploy?view=azuresql) and then skip down to the [rest of this post](#connect-your-python-program-to-the-azure-sql-server-database) to learn how to connect a Python program to the sample database.

### Create an Azure account

If you do not already have an Azure account, [create one](https://learn.microsoft.com/en-us/dotnet/azure/create-azure-account). Go to [https://azure.com](https://azure.com) and click on the *Free account* button.

![Azure sign up page]({static}/images/create-sample-db-azure/create-account-01.png){width=90%}

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

This starts login with interactive mode. A browser window will open up and ask you for your Azure account userid and password

![Azure login window]({static}/images/create-sample-db-azure/az_login-001.png){width=90%}

Enter your Azure userid. Then, enter your password at the next screen. You should see a notification in the browser window indicating you successfully logged it and you should see your account information printed in the terminal window.

#### Solving login problems

If you have trouble logging in with the interactive method, check the [Azure CLI login instructions](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli) for other login methods. Azure has multiple ways to login with Azure CLI, depending on your account settings. 

For example, since I use multi-factor authentication on my Azure account, I had to use the following command to login:

```bash
$ az login --use-device-code
```

## Create an SQL Server on Azure

If you want to create a database that you can experiment with, you need to act like a database administrator and set up a database server and a database. 

This section describes how to set up a free sample database for practice purposes and to gather the information you need to connect to it. I do not cover other SQL database administration topics like adding new database users, setting up user roles, and permissions.

### Free service tier restrictions

Microsoft provides some good examples of [using Azure CLI to set up an SQL Server database](https://learn.microsoft.com/en-us/azure/azure-sql/database/scripts/create-and-configure-database-cli?view=azuresql). The largest SQL server configuration supported on the free tier is:

* 1 S0 database
* 10 database transaction units
* 256 GB storage

Fortunately, these seem to be the default values for Azure SQL servers so you only need to specify a few configurations to [set up a server](https://learn.microsoft.com/en-us/azure/azure-sql/database/free-sql-db-free-account-how-to-deploy?view=azuresq) that fits within the free tier.

### Create a *dotenv* file

Choose your database configuration information. You need to know the Azure location where you will deploy your services; pick one located close to you. Next, you need to decide what names you will assign to your resource group, server, and database. You will also have to choose your SQL database userid and password. 

Assign your database server configuration information to environment variables that you can use in your Azure CLI commands and in your Python programs. The best way to do this is to create a file named *.env*, also known as a *dotenv file* [^3]. I wrote about [environment variables and dotenv files]({filename}use-environment-variables.md) in a previous post.

[^3]: [Sourcing](https://www.techrepublic.com/article/linux-101-what-does-sourcing-a-file-mean-in-linux/) the *.env* file only works on Linux and Mac OS. To load environment variables defined in the *.env* file in a Windows Powershell terminal, use the Powershell script described in [Stackoverflow answer #48607302](https://stackoverflow.com/questions/48607302/using-env-files-to-set-environment-variables-in-windows).

First, create a directory for your project and navigate to it. You may name your project folder anything you wish. I named mine *data-science-folder*.

```bash
$ mkdir data-science-folder
$ cd data-science-folder
```

Open a new file in your favorite text editor and enter the environment variables you need. Look at the example values below. You should use the same variable names but assign your own values to them. You are choosing the [Azure location](https://azure.microsoft.com/en-us/explore/global-infrastructure/geographies/#overview) where your server will be deployed. Then, you pick the names for your Azure resource group, SQL server, and SQL database. Finally, you pick your database userid and password.

```bash
location="eastus"
resource_group="new-resource-group-name"
server="my-sql-server-name"
database="my-sql-database-name"
login="sqldb_userid"
password="sqldb_passwd"
```

Save the file as *.env* in your project directory.

Activate your environment variables using the dotenv file:

```bash
$ source .env
```

Now, the environment variables are available in your terminal's shell and also will be available to your Python program.

### Create a resource group 

Use the Azure CLI to create a new resource group in which you will allocate your SQL Server and database.

```bash
$ az group create \
    --name $resource_group \
    --location $location
```

### Create an SQL Server

Create an SQL Server instance that will run in the free service tier.

```bash
$ az sql server create \
    --name $server \
    --resource-group $resource_group \
    --location $location \
    --admin-user $login \
    --admin-password $password
```

The server name needs to be unique to the Azure location. The command will take a few minutes to complete. 

### Create an SQL database instance

Create an SQL database instance that will run on your server and fit within the free service tier. Populate it with Microsoft's *AdventureWorks* sample data set.

```bash
$ az sql db create \
    --resource-group $resource_group \
    --server $server \
    --name $database \
    --sample-name AdventureWorksLT \
    --edition Standard \
    --service-level-objective S0 \
    --zone-redundant false
```

After the command completes, it displays the database information in JSON format. It lists a lot of information. In the JSON output, you can see that the configured database fits within the free tier because the *capacity* is `10`, the *edition* is `standard`, the *service objective* is `S0`, and the *maxSizeBytes* disk size is `268435456000` or 256 GigaBytes.

### Enable access through database firewall

Azure automatically blocks your database server from Internet access. To allow programs running on your development PC to connect to the database, set up a [new firewall rule on the SQL server](https://learn.microsoft.com/en-ca/azure/azure-sql/database/network-access-controls-overview?view=azuresql).

You need to know the correct IP address to allow. You can get your public IP address, which may be different than the IP address configured on your PC, by opening *https://google.com* in your web browser and searching for: "What is my IP address?". This will give you the IP address that external services see when they receive traffic from your PC.

Make a note of the address and then use it to create a firewall rule that allows connections from that IP address. For example, if that IP address was `203.0.113.23`:

```bash
$ az sql server firewall-rule create \
    --resource-group $resource_group \
    --server $server \
    --name MyHomeIPaddress \
    --start-ip-address 203.0.113.23 \
    --end-ip-address 203.0.113.23
```

Only users on the same address as your PC can access the server, and they still need to know all the server information and passwords to connect to it. This server is only for experimentation and you will delete it when you are done, so you do not need to learn the more advanced Azure database security options.

Your database server is set up and ready to experiment with. If you recently started your free trial on Azure, you can use it for twelve months for free.

## Connect your Python program to the Azure SQL Server Database

To connect to an SQL Server running on Azure, use the *[Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver16)* which works with the *pyodbc* library to authenticate your Python program's access to the Azure database. 

### Install Microsoft ODBC driver for SQL Server

Install the [Microsoft ODBC Driver for SQL Server on Linux](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Cubuntu17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline) using the following procedure:

Add the Microsoft repository to your [sources list](https://itsfoss.com/sources-list-ubuntu/):

```bash
$ sudo su
$ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
$ curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
$ exit
```

Install the *msodbcsql18* package:

```bash
$ sudo apt-get update
$ sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

You may need to logout and login again to ensure everything works well. 

### Set up a Python virtual environment

To create a Python virtual environment, navigate to your project folder and run the following commands. In this example, I named my project folder *data-science-folder*.

```bash
$ cd data-science-folder
$ python3 -m venv env
```

Then, activate the virtual environment.

```bash
$ source .\env\bin\activate
(env) $ 
```

Install the *[python-dotenv](https://pypi.org/project/python-dotenv/)* package in your Python project's [virtual environment](https://realpython.com/python-virtual-environments-a-primer/). You will use it later.

```bash
(env) $ pip install python-dotenv
```


### Install the *pyodbc* library

Next, install [*pyodbc*](https://mkleehammer.github.io/pyodbc/), the open-source Python ODBC driver for SQL Server. This provides the Python interface to the Windows ODBC driver. 

```bash
(env) $ pip install pyodbc
(env) $ sudo apt install unixodbc
```

### Get the connection string

You need to know the connection string that you must pass into the *pyodbc* function in your program. Normally, you might ask your database administrator for a valid connection string but, since you create this database yourself, you need to get the connection string from Azure.

Use Azure CLI to get the connection string for your ODBC driver.

```bash
(env) $ az sql db show-connection-string \
          --client odbc \
          --name $database \
          --server $server
```

You should get an output similar to the following:

```bash
"Driver={ODBC Driver 13 for SQL Server};Server=tcp:my-sql-server-name.database.windows.net,1433;Database=my-sql-database-name;Uid=<username>@my-sql-server-name;Pwd=<password>;Encrypt=yes;TrustServerCertificate=no;"
```

You will need to update the driver version from "13" to "18". Use the rest of the string as building blocks for a Python statement that creates a valid connection string.

Open a new file in your favorite text editor and enter the following Python code:

```python
import os
from dotenv import load_dotenv
load_dotenv()

server =  'tcp:' + os.getenv('server') + '.database.windows.net,1433'
database = os.getenv('database')
username = os.getenv('login') + '@' + os.getenv('server')
password = os.getenv('password')

connection_string = (
  'Driver={ODBC Driver 18 for SQL Server}' +
  ';Server=' + server +
  ';Database=' + database +
  ';Uid=' + username +
  ';Pwd=' + password +
  ';Encrypt=yes' +
  ';TrustServerCertificate=no;'
)

print(connection_string)
```

Save the file and run it. I saved it as *test1.py*:

```
(env) $ python test1.py
```

It should print out the connection string, incorporating the environment variable values you defined earlier in the *dotenv* file:

```bash
Driver={ODBC Driver 18 for SQL Server};Server=tcp:my-sql-server-name.database.windows.net,1433;Database=my-sql-database-name;Uid=sqldb_userid@my-sql-server-name;Pwd=sqldb_passwd;Encrypt=yes;TrustServerCertificate=no;
```

This is the same as the connection string provided by Azure, but with the driver version updated and your userid and password added. 

### Create a database connection

Once you have the connection string, [connect to the Azure SQL Server database](https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16), using the [*pyodbc* library](https://github.com/mkleehammer/pyodbc/wiki/Getting-started#connect-to-a-database). Add the following code to the end of your Python program and run it again:

```python
import pyodbc
conn = pyodbc.connect(connection_string)
print(conn)
```

The [database connection](https://github.com/mkleehammer/pyodbc/wiki/Connection) will be managed by the object instance returned by the *pyodbc.connect()* function call. You assigned that object to the variable name, *conn*.

Save and run the program. You should see output similar to the following:

```
<pyodbc.Connection object at 0x7f0a8cbf7380>>
```

This indicates that you have successfully established a connection to the database server. If you did not successfully connect, you will see an error message that should help you debug the problem.

In my experience, the most common problem was that my public IP address had changed. In those cases, checked my public IP address and used the Azure CLI to create a new firewall rule with the new public IP address.

### Reading data

To read data from the database connection, create a database cursor object, or pointer, using the *conn* object's [*cursor()* method](https://www.mssqltips.com/sqlservertip/7293/pyodbc-open-source-access-odbc-databases/). 

Execute an SQL statement using the cursor object's *execute()* method. It populates the cursor with database rows returned by the query. If you want to read just one row, use the cursor instance's *fetchone()* method. 

For example, to read the SQL Server software version, add the following code to the end of your program:

```python
statement = "SELECT @@version;"

cursor = conn.cursor()
cursor.execute(statement) 
print(cursor.fetchone())
cursor.close()
```

Save and run the program. You should see output similar to the following:

```
('Microsoft SQL Azure (RTM) - 12.0.2000.8 \n\tMay 22 2023 22:22:02 \n\tCopyright (C) 2022 Microsoft Corporation\n',)
```

To read the database schemas available in the database, add the following code to the end of your program:

```python
statement = """
SELECT DISTINCT
  TABLE_SCHEMA
FROM INFORMATION_SCHEMA.VIEWS
ORDER BY TABLE_SCHEMA
"""

cursor = conn.cursor()
cursor.execute(statement) 
print(cursor.fetchall())
cursor.close()
```

Since you expect more than one row in the result, use the [*fethchall()* method](https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/), which will return all rows in a list.

The returned list shows the database schemas that you have permission to read.

```
[('dbo',), ('SalesLT',), ('sys',)]
```

This proves you have successfully created a database containing sample data.

## Delete Azure resources

The database you created may be left running at no cost for twelve months so you do not need to delete it immediately. However, if you want to clean up the resources you created, the easiest way is to delete the resource group with the following command:

```bash
$ az group delete --name $resource_group
```

## Conclusion

After you create your Azure free trial account and install Azure CLI, you can create a sample database with just a few Azure CLI commands. You can get the connection information from Azure and connect your Python programs to the database using the *pydobc* Python library and the *Microsoft ODBC Driver for SQL Server*.

Once you have a connection established, you can start practicing using Python to explore the database tables and to read and analyze the data. I will cover various ways to explore the database schema and to read and transform data in future posts. 















