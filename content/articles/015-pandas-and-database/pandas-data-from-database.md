title: Python, pandas, and databases
slug: python-pandas-databases
summary: Use the Pandas data analysis framework to read data from an SQL database. In this post, I show you how to use two methods: you can read entire database tables and process them exclusively in Pandas, or you can use SQL queries to pre-process only selected database data to reduce the memory used by Pandas when analyzing the data.
date: 2023-07-14
modified: 2023-07-14
category: Databases
status: Published

[Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) is a Python package that makes working with relational or labeled data both easy and intuitive. It aims to be the fundamental high-level building block for doing practical, real-world data analysis in Python [^2]. Data scientists commonly load data from databases into Pandas dataframes. However, when you are learning to use Pandas, it is hard to find a public database with which you can practice meaningful data operations. 

[^2]: From the [Pandas package overview documentation](https://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html), accessed on March 17, 2023

This post shows you how to Pandas to read data from a database that contains enough data to be interesting and how to perform basic data preparation. The examples in this tutorial will use the Microsoft *AdventureWorks LT* sample database. You may [create your own version of this database]({filename}/articles/012-create-sample-db-azure/create-sample-db-azure.md) or you may use the [public AdventureWorks SQL Server](https://www.sqlservercentral.com/articles/sqlservercentral-hosts-adventureworks-on-azure). In this post, you will use the public server so that you can immediately get started with the examples.

## The short answer

Once you are connected to a database, Pandas makes it easy to load data from it. 

If you read my previous posts about [reading databases schema information]({filename}/articles/013-read-database-python-odbc/read-db-python-odbc-driver.md) or [using Python programs to read data from a database]({filename}/articles/014-read-data-from-database-with-python/python-program-read-database-data.md), you have already learned how to connect to a database. 

Programmers can use the Pandas *read_sql_table()* method to read entire SQL database tables into Pandas dataframes by passing in the table name as a parameter. Then, they can use Pandas to join, transform, and filter those dataframes until they create the dataset that they need.

Python programmers who are proficient in writing [SQL queries](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select/) may pass a string containing an SQL query in the Pandas *read_sql_query()* method to extract and transform a dataset before loading it into a Pandas dataframe. 


## Set up your environment

Before you start working through this tutorial, create a Python virtual environment and install the packages you need in it. Then, start a Jupyter Notebook so you can follow along with this tutorial. You may use the Python REPL instead, if you do not want to use Jupyter.

### Basic configuration

I have already covered the virtual environment setup process in my previous posts so I will just list the required commands here, without explanation.

```bash
$ sudo su
$ curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
$ curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
$ exit
$ sudo apt-get update
$ sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
$
$ mkdir data-science
$ cd data-science
$ python -m venv .venv
$ source ./.venv/bin/activate
(.venv) $ pip install jupyterlab
(.venv) $ pip install python-dotenv
(.venv) $ pip install pyodbc
(.venv) $ sudo apt install unixodbc
```

### Install Pandas

Install Pandas. When Pandas is installed, [NumPy](https://numpy.org/) will also be installed. NumPy (Numerical Python) is an open source Python library that’s used for working with arrays of numerical data in Python. Also install some Excel packages that help Pandas write dataframes to local storage as Excel spreadsheets.

```bash
(.venv) $ pip install pandas
(.venv) $ pip install openpyxl xlsxwriter xlrd
```

### Install SQLAlchemy

Install [SQLAlchemy](https://www.sqlalchemy.org/). Pandas methods use SQLAlchemy functions when they read SQL database tables. [Pandas does not support *pyodbc* connection objects](https://stackoverflow.com/questions/71082494/getting-a-warning-when-using-a-pyodbc-connection-object-with-pandas). It only supports *SQLAlchemy* connections, *sqlite* connections, or a *database string URI*. Even when using just the database string URI, Pandas still uses SQLAlcehmy functions to connect to and read from an SQL database. 


```bash
(.venv) $ pip install sqlalchemy
```

We don't use it explicitly in this tutorial, but SQLAlchemy is a very interesting library. It can be used with Pandas to define programmers' access to databases, to  manage connections, and to build database queries using only Python code. I will cover more about using SQLAlchemy in future posts.

### Start a notebook

Start a new Jupyter Notebook. 

```bash
(.venv) $ jupyter-lab
```

When following along with the code examples in this document, open a new notebook cell for each example, enter the code, and run it. The results of code run in previous cells is held in memory and is available to subsequent cells. For example, a dataframe created in one cell can be used in a later cell.

## The database

Use the [public SQL server](https://www.sqlservercentral.com/articles/sqlservercentral-hosts-adventureworks-on-azure) that is supported by the team that runs the *[sqlservercentral.com](https://www.sqlservercentral.com/about)* web site. It contains most of the AdventureWorks LT sample database. As far as I know, this is the only public SQL server that contains interesting data and is available to use for free [^3]. 

[^3]: Many data sets that are [available to the public](https://www.dropbase.io/post/top-11-open-and-public-data-sources) but very few of them run on database servers.

If this public server is not available when you read this post, you can [create your own AdventureWorks LT database]({filename}/articles/012-create-sample-db-azure/create-sample-db-azure.md) on a free server in Microsoft Azure. Or, you can run a version of the same database locally on your PC with [SQLite](https://database.guide/2-sample-databases-sqlite/) or [Docker](https://github.com/pthom/northwind_psql). 

### Prepare to connect to the database

To connect to the database, first define an environment variable that contains the connection string. If you are working with a database on Microsoft Azure, you will get the string from the Azure Portal or from the database administrator. In this case, the connection string is based on the [database and user information](https://www.sqlservercentral.com/articles/connecting-to-adventureworks-on-azure) provided on the *sqlservercentral.com* web site. 

In your terminal window, run the following command to create a *dotenv* file the contains the correct connection string:

```bash
(.venv) $ echo 'CONN_PUBLIC="Driver={ODBC Driver 18 for SQL Server};'\
'Server=tcp:sqlservercentralpublic.database.windows.net,1433;'\
'Database=AdventureWorks;Uid=sqlfamily;Pwd=sqlf@m1ly;Encrypt=yes;'\
'TrustServerCertificate=no;"' > .env
```

Then switch to your Jupyter Notebook (or REPL). In the first Jupyter Notebook cell, get the connection string environment variable and assign it to the variable named *connection_string*:

```python
import os
from dotenv import load_dotenv

load_dotenv('.env', override=True)
connection_string = os.getenv('CONN_PUBLIC')
```

Pandas does not directly support *pyodbc* connection objects. Pandas uses SQLAlchemy, which uses the *pyodbc* library and the Microsoft ODBC driver, to manage database connections, based on the information you provide in the database string URI. Convert the connection string you stored in the *dotenv* file into the format required so it can be used as a database URI.

The code below will perform the conversion. The [*quote_plus()* function](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote_plus) replaces spaces and special characters with escape codes so, if you have a password in your connection string and if that password contains special characters, Pandas can still use it. Then, append a prefix that identifies the drivers SQLAlchemy and Pandas will use. Run the code below to set up the database URI:

```python
from urllib.parse import quote_plus

url_string = quote_plus(connection_string)
uri = f'mssql+pyodbc:///?odbc_connect={url_string}'
```

You are not yet connected to the database. You have created a database string URI in the right format so Pandas and SQLAlchemy can use it to create and manage connections to the database. Now, you are ready to use Pandas to read data from the database.

### Database schema

To read data from the database, you need to know the schema information. Ideally, the database administrator would provide you with documentation that describes the schemas, tables, and data relationships. You can read more information about the AdventureWorks LT database in my previous posts. For this example, you just need to know the schema and table names.

The only schema available to you, other than system schemas, is the *SalesLT* schema. It contains the following tables:

* Address
* Customer
* CustomerAddress
* Product
* ProductCategory
* ProductDescription 
* ProductModel 
* ProductModelProductDescription
* SalesOrderDetail
* SalesOrderHeader


### Read database tables into Pandas dataframes

Developers who want to use Pandas to read entire tables from the SQL database into Pandas dataframes may use the Pandas [*read_sql_table()* method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql_table.html). Simply pass it the name of the table in the database, the database URI, and the schema name.

Pandas does the work of creating a connection to the database, reading all the columns in the table, exporting them into a Pandas dataframe, and returning the dataframe. For example, we will read the contents of the *ProductCategories* table and print the first few lines.

```python
import pandas as pd

categories = pd.read_sql_table('ProductCategory', uri, 'SalesLT')
print(categories.head(7))
```

The printed dataframe looks like the following output:

```
   ProductCategoryID  ParentProductCategoryID            Name  \
0                  1                      NaN           Bikes   
1                  2                      NaN      Components   
2                  3                      NaN        Clothing   
3                  4                      NaN     Accessories   
4                  5                      1.0  Mountain Bikes   
5                  6                      1.0      Road Bikes   
6                  7                      1.0   Touring Bikes   

                                rowguid ModifiedDate  
0  CFBDA25C-DF71-47A7-B81B-64EE161AA37C   2002-06-01  
1  C657828D-D808-4ABA-91A3-AF2CE02300E9   2002-06-01  
2  10A7C342-CA82-48D4-8A38-46A2EB089B74   2002-06-01  
3  2BE3BE36-D9A2-4EEE-B593-ED895D97C2A6   2002-06-01  
4  2D364ADE-264A-433C-B092-4FCBF3804E01   2002-06-01  
5  000310C0-BCC8-42C4-B0C3-45AE611AF06B   2002-06-01  
6  02C5061D-ECDC-4274-B5F1-E91D76BC3F37   2002-06-01  
```

You can read multiple tables into different dataframes to build up a set of data to analyze. Get the contents of the *Product* and *ProductModel* tables:

```python
products = pd.read_sql_table('Product', uri, 'SalesLT')
models = pd.read_sql_table('ProductModel', uri, 'SalesLT')
```

## Merging dataframes in Pandas

To get more interesting data sets, we need to [join database tables](https://learnsql.com/blog/how-to-join-tables-sql/). For now, because we are using the Pandas *read_sql_table()* method, we will accomplish this by reading different tables into Pandas dataframes and [merging the dataframes](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html). 

It is easier to merge dataframes if you already understand the relationships between them. If you imported entire tables into dataframes, look at the database documentation and find the primary keys and foreign keys that define relationships. 

Print the output of each dataframe's *columns* attribute:

```python
print(products.columns)
print(categories.columns)
print(models.columns)
```

the output shows the columns names in each dataframe

```bash
Index(['ProductID', 'Name', 'ProductNumber', 'Color', 'StandardCost',
       'ListPrice', 'Size', 'Weight', 'ProductCategoryID', 'ProductModelID',
       'SellStartDate', 'SellEndDate', 'DiscontinuedDate', 'ThumbNailPhoto',
       'ThumbnailPhotoFileName', 'rowguid', 'ModifiedDate'],
      dtype='object')
Index(['ProductCategoryID', 'ParentProductCategoryID', 'Name', 'rowguid',
       'ModifiedDate'],
      dtype='object')
Index(['ProductModelID', 'Name', 'CatalogDescription', 'rowguid',
       'ModifiedDate'],
      dtype='object')
```

You see that the *ProductCategoryID* column in the *products* dataframe matches with the *ParentProductCategoryID* column in the *categories* dataframe. It's not obvious, but the *ParentProductCategoryID* in the *categories* dataframe has a foreign-key relationship with the *ProductCategoryID* in the same table (which is why you need to document your database schema). The *ProductModelID* column in the *products* dataframe matches with the *ProductModelID* column in the *models* dataframe.

### Merging two dataframes

Create a dataframe that lists selected product information, including the product name, model, category. [Merge](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#database-style-dataframe-or-named-series-joining-merging) the dataframe *products* and the dataframe *models* into a new dataframe named *df1*. By default, the [pandas merge method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge.html) operates like an [*inner join*](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#database-style-dataframe-or-named-series-joining-merging) operation so it returns merged rows that match between the left and right side of the join.

You can join two dataframes together using the Pandas *merge()* function, or you can join any number of dataframes together using each dataframe's *merge()* method. Pandas does not know about the relationships between the tables in the database. In simple cases Pandas will perform the inner join by matching columns with the same name from each dataframe. But, you have to be careful if you have multiple columns that have the same name, as you get in this case. Pandas will return only the rows that match in all columns with same names. To avoid this problem, specify the column that each merge should match on.

For example, to merge the albums and artists dataframes, use the following code:

```python
df1 = pd.merge(left=products, right=categories, on='ProductCategoryID')
print(df1.shape)
print(df1.head())
```

Use the Pandas dataframe's *shape* attribute to check the number of rows and columns in the dataframe, since you are only printing the first two rows.

```bash
(295, 21)
   ProductID                     Name_x ProductNumber  Color  StandardCost  \
0        680  HL Road Frame - Black, 58    FR-R92B-58  Black       1059.31   
1        706    HL Road Frame - Red, 58    FR-R92R-58    Red       1059.31   

   ListPrice Size   Weight  ProductCategoryID  ProductModelID  ...  \
0     1431.5   58  1016.04                 18               6  ...   
1     1431.5   58  1016.04                 18               6  ...   

  SellEndDate DiscontinuedDate  \
0         NaT              NaT   
1         NaT              NaT   

                                      ThumbNailPhoto  \
0  b'GIF89aP\x001\x00\xf7\x00\x00\x00\x00\x00\x80...   
1  b'GIF89aP\x001\x00\xf7\x00\x00\x00\x00\x00\x80...   

         ThumbnailPhotoFileName                             rowguid_x  \
0  no_image_available_small.gif  43DD68D6-14A4-461F-9069-55309D90EA7E   
1  no_image_available_small.gif  9540FF17-2712-4C90-A3D1-8CE5568B2462   

           ModifiedDate_x ParentProductCategoryID       Name_y  \
0 2008-03-11 10:01:36.827                     2.0  Road Frames   
1 2008-03-11 10:01:36.827                     2.0  Road Frames   

                              rowguid_y ModifiedDate_y  
0  5515F857-075B-4F9A-87B7-43B4997077B3     2002-06-01  
1  5515F857-075B-4F9A-87B7-43B4997077B3     2002-06-01  

[2 rows x 21 columns]
```

You can see that Pandas uses the "_x" and "_y" suffixes to rename merged columns with the same name. 

If you want to use other suffixes, you can specify them as parameters when you call the *merge()* method. For example, the output would be clearer if you wrote the following code, instead:

```python
df1 = pd.merge(
    left=products, 
    right=categories, 
    on='ProductCategoryID',
    suffixes=['_product','_category']
)

print(df1.shape)
print(df1.head(2))
```

Now, after the merge, the columns from each table that had the same name are called "Name_product" and "Name_category"


### Merging multiple dataframes

Pandas dataframes have a [*merge()* method](https://www.w3schools.com/python/pandas/ref_df_merge.asp) that works the same as the Pandas *merge()* function with the calling data frame being considered the left side in the join.

Perform the same merge as you performed above with the Pandas *merge()* function, but use the dataframe's *merge()* method:

```python
df2 = products.merge(categories, on='ProductCategoryID', suffixes=['_product','_category'])

print(df2.shape)
display(df2.head(2))
```

You get the same output as was displayed when you used the Pandas *Merge()* function.

You can chain multiple *merge()* methods together to join multiple dataframes in one statement. 

```python
df3 = (
    products
        .merge(categories, 
               on='ProductCategoryID', 
               suffixes=['_product','_category'])
        .merge(models)
        .merge(categories,
              left_on='ParentProductCategoryID',
              right_on='ProductCategoryID',
              suffixes=['_child','_parent'])
)
print(df3.shape)
print(df3.head(2))
```

The output has 30 columns and the columns names are confusing, with duplicate data in columns. 

```bash
(295, 30)
   ProductID                     Name_x ProductNumber  Color  StandardCost  \
0        680  HL Road Frame - Black, 58    FR-R92B-58  Black       1059.31   
1        706    HL Road Frame - Red, 58    FR-R92R-58    Red       1059.31   

   ListPrice Size   Weight  ProductCategoryID_child  ProductModelID  ...  \
0     1431.5   58  1016.04                       18               6  ...   
1     1431.5   58  1016.04                       18               6  ...   

  ModifiedDate_y     Name_child CatalogDescription  \
0     2002-06-01  HL Road Frame               None   
1     2002-06-01  HL Road Frame               None   

                          rowguid_child ModifiedDate_child  \
0  4d332ecc-48b3-4e04-b7e7-227f3ac2a7ec         2002-05-02   
1  4d332ecc-48b3-4e04-b7e7-227f3ac2a7ec         2002-05-02   

  ProductCategoryID_parent ParentProductCategoryID_parent  Name_parent  \
0                        2                            NaN   Components   
1                        2                            NaN   Components   

                         rowguid_parent ModifiedDate_parent  
0  c657828d-d808-4aba-91a3-af2ce02300e9          2002-06-01  
1  c657828d-d808-4aba-91a3-af2ce02300e9          2002-06-01  

[2 rows x 30 columns]
```

You can make the resulting dataframe more useful by choosing only the columns you want from each dataframe and renaming columns as needed.

You can keep chaining Pandas dataframe methods to create complex operations that merge more dataframes, rename and delete columns, filter results, and more. The [Pandas documentation](https://pandas.pydata.org/docs/) is a good resource for learning more about other Pandas [method](https://practicaldatascience.co.uk/data-science/how-to-use-method-chaining-in-pandas) [chaining](https://towardsdatascience.com/using-pandas-method-chaining-to-improve-code-readability-d8517c5626ac), and [Pandas dataframe methods](https://tomaugspurger.net/posts/modern-1-intro/).

## Select data from the database using SQL queries

When working with large amounts of data, you may prefer to perform most of your data joins, grouping, and filter operations on the database server instead of locally on your PC. The Pandas *read_sql_query* enables you to send an SQL query to the database and then load the selected data into a dataframe.

### The *read_sql_query* function

To select data from the SQL database, you need to create an SQL query statement using the [SQL language](https://en.wikipedia.org/wiki/SQL). For example, see the SQL statement below that selects all the columns in a table:

```sql
SELECT * FROM SalesLT.Product
```

To use that statement with Pandas, run the following code:

```python
statement = "SELECT * FROM SalesLT.Product"

products = pd.read_sql_query(statement, uri)
print(products.shape)
print(products.sample(2))

```

The output shows a random sample of two rows from the *products* dataframe, which contains the entire contents, 295 rows with 17 columns, of the *Product* table.

```bash
(295, 17)
     ProductID                    Name ProductNumber Color  StandardCost  \
104        809  ML Mountain Handlebars       HB-M763  None       27.4925   
47         752        Road-150 Red, 52    BK-R93R-52   Red     2171.2942   

     ListPrice  Size   Weight  ProductCategoryID  ProductModelID  \
104      61.92  None      NaN                  8              54   
47     3578.27    52  6540.77                  6              25   

    SellStartDate SellEndDate DiscontinuedDate  \
104    2006-07-01         NaT             None   
47     2005-07-01  2006-06-30             None   

                                        ThumbNailPhoto  \
104  b'GIF89aP\x001\x00\xf7\x00\x00\x00\x00\x00\x80...   
47   b'GIF89aP\x001\x00\xf7\x00\x00\x92\x04\x07\xc6...   

           ThumbnailPhotoFileName                               rowguid  \
104  no_image_available_small.gif  AE6020DF-D9C9-4D34-9795-1F80E6BBF5A5   
47       superlight_red_small.gif  5E085BA0-3CD5-487F-85BB-79ED1C701F23   

               ModifiedDate  
104 2008-03-11 10:01:36.827  
47  2008-03-11 10:01:36.827
```

### Joining tables into one dataframe

Another benefit of SQL is that, when working with large databases, you can join tables and filter data more efficiently on the SQL server because it is optimized for these kinds of operations.

SQL query statements can select specific columns from tables, filter returned rows based on your criteria, join tables, rename columns, and more. For example, the query below is similar to the previous Pandas *merge* example, above. It joins the *Product*, *ProductCategory*, and *ProductModel* tables. 

```python
statement = """
SELECT *
FROM SalesLT.Product AS P
JOIN SalesLT.ProductCategory AS PC1 ON ( P.ProductCategoryID = PC1.ProductCategoryID )
JOIN SalesLT.ProductModel AS PM ON ( P.ProductModelID = PM.ProductModelID )
JOIN SalesLT.ProductCategory AS PC2 ON ( PC2.ProductCategoryID = PC1.ParentProductCategoryID )
"""

df = pd.read_sql_query(statement, uri)
print(df.shape)
print(df.sample(2))
```

The *df* dataframe contains thirty-two rows and has duplicat columns names. Similar to the example above, where you merged multiple dataframes, the information presented is confusing.

```bash
(295, 32)
     ProductID                     Name ProductNumber  Color  StandardCost  \
204        909  ML Mountain Seat/Saddle       SE-M798   None       17.3782   
82         787   Mountain-300 Black, 44    BK-M47B-44  Black      598.4354   

     ListPrice  Size    Weight ProductCategoryID ProductModelID  ...  \
204      39.14  None       NaN                19             80  ...   
82     1079.99    44  11852.31                 5             21  ...   

    ProductModelID                       Name CatalogDescription  \
204             80  ML Mountain Seat/Saddle 2               None   
82              21               Mountain-300               None   

                                  rowguid ModifiedDate ProductCategoryID  \
204  5CEFBB6E-3B7E-414F-AC1B-8F6DF741FB21   2007-06-01                 2   
82   ECDDD0D7-2DB2-464D-B2DA-89BFFC6276AA   2006-06-01                 1   

    ParentProductCategoryID        Name                               rowguid  \
204                    None  Components  C657828D-D808-4ABA-91A3-AF2CE02300E9   
82                     None       Bikes  CFBDA25C-DF71-47A7-B81B-64EE161AA37C   

    ModifiedDate  
204   2002-06-01  
82    2002-06-01  

[2 rows x 32 columns]
```

### Filtering data

When you use SQL queries in Pandas, you can select a smaller subset of data to read into your dataframe. This is more efficient than reading in all the data from a table and then using Pandas to remove data you don't need.

For example, if you only need a list four random products from the database with the product name, model, category, and parent category run the following code:

```python
statement = """
SELECT TOP 5
  P.Name AS 'Product', 
  M.Name AS 'Model', 
  C.Name AS 'Category', 
  PC.Name AS 'Parent'
FROM SalesLT.Product AS P
JOIN SalesLT.ProductCategory AS C ON ( P.ProductCategoryID = C.ProductCategoryID )
JOIN SalesLT.ProductModel AS M ON ( P.ProductModelID = M.ProductModelID )
JOIN SalesLT.ProductCategory AS PC ON ( PC.ProductCategoryID = C.ParentProductCategoryID )
ORDER BY NEWID()
"""

df = pd.read_sql_query(statement, uri)
print(df.shape)
print(df)
```

The output shows that the *df* dataframe now contains only four rows of product information with four columns, not including the index column, in each row. You do not need to perform any additional Pandas operations to reduce the data to only what we need.

```bash
(5, 4)
                 Product         Model       Category      Parent
0            Rear Brakes   Rear Brakes         Brakes  Components
1                HL Fork       HL Fork          Forks  Components
2       Road-250 Red, 52      Road-250     Road Bikes       Bikes
3  Touring-3000 Blue, 58  Touring-3000  Touring Bikes       Bikes
4     Road-750 Black, 58      Road-750     Road Bikes       Bikes
```

You can see that this procedure would be better if you have large database tables and are only interested in specific columns or in rows that meet a certain criteria. Then you do not need to put pressure on the network and on computer memory to move entire tables to your computer when, instead, you can select the data you need on the SQL server and send only what you selected to your computer.

## Saving pandas dataframes

Pandas works in your computer's memory. The pandas workflow does not require that you save work to disk and then read it back later. If you are re-starting a data analysis project, you would normally go back to the original data source, read in the data again and apply the Pandas functions you wish to apply. If you are [handing the dataframe off to another program](https://sparkbyexamples.com/pandas/convert-pandas-to-pyspark-dataframe/), you would normally do that in memory.

One case where you might want to save a dataframe to disk is when you wish to output the results to a spreadsheet for an end user, who may have asked for a spreadsheet version of the results. To [save a dataframe to an Excel spreadsheet](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_pickle.html), execute the following statement:

```python
df1.to_excel("product_info.xlsx", index=False)  
```

You can [add style methods](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.io.formats.style.Styler.to_excel.html#pandas.io.formats.style.Styler.to_excel) to make the Excel spreadsheet look nice for your stakeholder. You can also output [complex spreadsheets with multiple worksheets](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html).

Another case might be where you want to convert the Pandas dataframe into a CSV file for use by Power BI. This is not the best way to integrate Pandas and Power BI; it is better to [use pandas *in* Power BI](https://realpython.com/power-bi-python/). But, sometimes you have to work the way others with whom you collaborate are working. To save a Pandas dataframe as a CSV file, execute the following statement:

```python
df1.to_csv("product_info.csv", index=False)
```

You will not normally need to save your Pandas dataframe to disk for your own use. You should avoid saving data to disk when you work with sensitive data. However, if you want to save your Pandas dataframe to disk so you can use it later, the best option is to [*pickle*](https://realpython.com/python-pickle-module/) the dataframe. This saves pandas dataframe objects to a file, maintaining column data types and other Pandas-specific information that would be lost if the dataframe was saved in other formats. Another, more modern, option is to use the [*parquet* file format](https://arrow.apache.org/docs/python/parquet.html), but *pickle* is most commonly used for individual projects. To pickle a pandas dataframe, execute the following statement:

```python
df1.to_pickle("product_info.pkl")
```

To read back the picked dataframe, execute the following statement:

```python
new_df = pd.read_pickle("product_info.pkl")
```


## Conclusion

You have learned enough to read data from an SQL database into a Pandas dataframe. You can use Pandas to read entire database tables into dataframes, then operate on them locally on your PC. You can also use Pandas to send an SQL query to the database and read the results into a dataframe. 

In the end, your decision about whether you read entire tables into separate dataframes and then join and manipulate them in Pandas, or whether you run SQL queries that load already selected and joined data into one or more dataframes, will depend on issues like the purpose of your application, the size of the database tables and pandas dataframes, database server performance, and the processing and memory resources available on your workstation.

In my opinion, if your data comes from a database, you should do most of your data joining and filtering using the database and then use Pandas for additional data cleaning and analysis. If your data comes from spreadsheets or CSV files, you have to use Pandas to combine, filter, clean, and analyze data.