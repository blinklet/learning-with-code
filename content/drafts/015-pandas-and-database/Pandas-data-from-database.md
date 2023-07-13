# Python, pandas, and databases

[Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) is a Python package that makes working with relational or labeled data both easy and intuitive. It aims to be the fundamental high-level building block for doing practical, real-world data analysis in Python [^2].

[^2]: From the [Pandas package overview documentation](https://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html), accessed on March 17, 2023

Data scientists commonly load data into Pandas dataframes from databases. However, when you are learning to use Pandas, it is hard to find a public database with which you can practice meaningful data operations. I believe this is why many data-science books and blogs show you how to work with other data sources like [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values). There are already many [public sources of interesting data](https://www.dropbase.io/post/top-11-open-and-public-data-sources) in CSV files and there are also [many](https://alongrandomwalk.com/2020/09/14/read-and-write-files-with-jupyter-notebooks/) [tutorials](https://www.digitalocean.com/community/tutorials/data-analysis-and-visualization-with-pandas-and-jupyter-notebook-in-python-3) [available](https://www.datacamp.com/tutorial/python-excel-tutorial) that show you how to load data from CSV files into Pandas dataframes. 

This post shows you how to Pandas to read data from a database that contains enough data to be interesting and how to perform basic data preparation. The examples in this tutorial will use the Microsoft AdventureWorks LT sample database. You may [create your own version of this database]({filename}/articles/012-create-sample-db-azure/create-sample-db-azure.md) or you may use the [public AdventureWorks SQL Server](https://www.sqlservercentral.com/articles/sqlservercentral-hosts-adventureworks-on-azure). In this post, you will use the public server so that you can immediately get started with the examples.

## The short answer

Once you are connected to a database, Pandas makes it easy to load data from it. But, Pandas only supports database connections using SQLAlchemy

If you read my previous posts about [reading databases schema information]({filename}/articles/013-read-database-python-odbc/read-db-python-odbc-driver.md) or [using Python programs to read data from a database]({filename}/articles/014-read-data-from-database-with-python/python-program-read-database-data.md), you have already learned how to connect to a database. 

Programmers can use the Pandas *read_sql_table()* method to read entire SQL database tables into Pandas dataframes simply by passing in the table name as a parameter. Then, they can use Pandas to join, transform, and filter those dataframes until they create the dataset that they need.

Python programmers who are proficient in writing [SQL queries](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select/) may pass a string containing an SQL query in the Pandas *read_sql_query()* method to extract and transform a dataset before loading it into a Pandas dataframe. 


## Set up your environment

Before you start working through this tutorial, create a Python virtual environment and install the packages you need in it. The start a Jupyter Notebook so you can follow along with this tutorial. You may use the Python REPL instead, if you do not want to use Jupyter.

I have already covered the process in my previous posts so I will just list the required commands here, without explanation.

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
``````

Finally, install Pandas.

```bash
(.venv) $ pip install pandas
(.venv) $ pip install openpyxl xlsxwriter xlrd
```

When Pandas is installed, [NumPy](https://numpy.org/) will also be installed. NumPy (Numerical Python) is an open source Python library that’s used for working with numerical data in Python.

Start a new Jupyter Notebook. 

```bash
(.venv) $ jupyter-lab
```

When following along with the code examples in this document, open a new notebook cell for each example, enter the code, and run it. The results of code run in previous cells is held in memory and is available to subsequent cells. For example, a dataframe created in one cell can be used in a later cell.

## Connect to a database

Many data sets that are [available to the public](https://www.dropbase.io/post/top-11-open-and-public-data-sources) but very few of them run on database servers. 

Fortunately, there is a [public SQL server](https://www.sqlservercentral.com/articles/sqlservercentral-hosts-adventureworks-on-azure) that contains most of the AdventureWorks LT sample database. It is supported by the *[sqlservercentral.com](https://www.sqlservercentral.com/about)* web site. 

I do not know that this public server will be supported indefinitely so, if it is not available when you read this post, you can [create your own AdventureWorks LT database]({filename}/articles/012-create-sample-db-azure/create-sample-db-azure.md) on a free server in Microsoft Azure. Or, you can run a version of the same database locally on your PC with [SQLite](https://database.guide/2-sample-databases-sqlite/) or [Docker](https://github.com/pthom/northwind_psql). 

To connect to the database, first define an environment variable that contains the connection string. The connection string is based on the [database and user information](https://www.sqlservercentral.com/articles/connecting-to-adventureworks-on-azure) provided on the *sqlservercentral.com* web site. 

In your terminal window, run the following command to crete a *dotenv* file the contains the correct connection string:

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

Pandas does not support *pyodbc* connection objects. It only supports *SQLAlchemy* connections, *sqlite* connections, or a database string URI. So, you will have to convert the connection string into a database URI.

The code below will perform the conversion. All you need to do is append a prefix that identifies the driver Pandas will use. Run the code below to set up the database URI:

```python
from urllib.parse import quote_plus

url_string = quote_plus(connection_string)
uri = f'mssql+pyodbc:///?odbc_connect={url_string}'
```

The [*quote_plus* function](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote_plus) replaces spaces and special characters with escape codes so if you have a password in your connection string and if that password contains special characters, Pandas can still use it.

Pandas will use the database URI to create and manage its own *pyodbc* connection. Now, you are ready to use Pandas to read data from the database.


# Read database tables into Pandas dataframes

To read data from the database, you need to know the schema information. Ideally, the database administrator would provide you with documentation that describes the schemas, tables, and data relationships. You can read more information about the AdventureWorks LT database in my previous posts. For this example, you just need to know the schema and table names.

The only schema available to you (other than system schemas) is the *SalesLT* schema. It contains the following tables:

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


### The *read_sql_table* method

Developers who want to use Pandas to read entire tables from the SQL database into Pandas dataframes may use the Pandas [*read_sql_table()* method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql_table.html). Simply pass it the name of the table in the database, the database URI, and the schema name.

Pandas does the work of creating a connection to the database, reading all the columns in the table, exporting them into a Pandas dataframe, and returning the dataframe. For example, we will read the contents of the *ProductCategories* table and print the first few lines.

```python
import pandas as pd

categories = pd.read_sql_table('ProductCategory', uri, 'SalesLT')

print(categories.shape)
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

To get more interesting data sets, we need to [join database tables](https://learnsql.com/blog/how-to-join-tables-sql/). For now, we will accomplish this by reading different tables into Pandas dataframes and [merging the dataframes](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html). 

It is easier to merge dataframes if you already understand the relationships between them. If you imported entire tables into dataframes, look at the database documentation and find the primary keys and foreign keys that define relationships. 

Print the output of each dataframe's *columns* attribute:

```python
print(products.columns)
print(categories.columns)
print(models.columns)
```

the output shows the columns names in each dataframe

```
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

You see that the *ProductCategoryID* column in the *products* dataframe matches with the *ParentProductCategoryID* column in the *categories* dataframe. It's not obvious (which is why you need to document your database schema), but the *ParentProductCategoryID* in the *categories* dataframe is has a foreign-key relationship with the *ProductCategoryID* in the same table. The *ProductModelID* column in the *products* dataframe matches with the *ProductModelID* column in the *models* dataframe.

### Merging dataframes

I want to create a dataframe that lists selected product information, including the product name, model, category. So, I will [merge](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#database-style-dataframe-or-named-series-joining-merging) the dataframe *products* and the dataframe *models* into a new dataframe named *df1*. By default, the [pandas merge method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge.html) operates like an [*inner join*](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#database-style-dataframe-or-named-series-joining-merging) operation so it returns merged rows that match between the left and right side of the join.

You can join two dataframes together using the Pandas *merge()* function, or you can join any number of dataframes together using each dataframe's *merge()* method. Pandas does not know about the relationships between the tables in the database. In simple cases Pandas will perform the inner join by matching columns from each dataframe that have the same name. If you need to join on columns that do not have the same names, or if there are more than one set of columns with the same names, you can specify which columns to join on in the Pandas *merge()* function's parameters.

For example, to merge the albums and artists dataframes, use the following code:

```python
df1 = pd.merge(left=products, right=categories, on='ProductCategoryID')
print(df1.shape)
print(df1.head())
```

I used the Pandas dataframe *shape* attribute to check the number of rows and columns in the dataframe, since I am only displaying the first two rows.

```
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

Pandas dataframes have a [*merge()* method](https://www.w3schools.com/python/pandas/ref_df_merge.asp) that works the same as the Pandas *merge()* function with the calling dataFrame being considered the left side in the join.

You can chain multiple *merge()* methods together to join multiple dataframes in one statement. But you have to be careful if you have multiple columns that have the same name, as you get in this case. Pandas will return only the rows that match in all columns with same names. To avoid this problem, specify the column that each merge should match on.

```python
df1 = albums.merge(artists, on='ArtistId').merge(tracks, on='AlbumId')

print(df1.shape)
display(df1.head(3))
```


You can keep chaining Pandas dataframe methods to create complex operations that merge dataframes, rename and delete columns, and more. For example:

```python
df1 = (
    albums
    .merge(artists, on='ArtistId')
    .merge(tracks, on='AlbumId', suffixes=['_artist','_track'])
    .rename(columns = {'Title':'Album','Name_artist':'Artist', 
                       'Name_track':'Track', 'Milliseconds':'Length',})
    .drop(['AlbumId', 'TrackId', 'MediaTypeId', 
           'GenreId', 'Bytes', 'UnitPrice', 'ArtistId'], axis=1)
)

print(df1.shape)
display(df1.head(3))
```

Which displays the following output:

![Result of merging multiple tables and chaining multiple methods](./Images/pandas052.png)

Now you have a dataframe that has 3,503 rows. Each row contains  information about a track's album, artists, composer, and length.


### Merging dataframes with outer joins

When merging dataframes, you may want to include rows from one or both dataframes that do not match on the defined columns in each dataframe. This is called an [*outer join*](https://www.freecodecamp.org/news/sql-join-types-inner-join-vs-outer-join-example/).

For example, imagine that we need to create a dataframe that shows the number of customers supported by each employee. 

Consider the Employee and Customer tables in the Chinook database.  

```python
customers = pd.read_sql_table('Customer', url)
employees = pd.read_sql_table('Employee', url)

print(f"customers columns:  {customers.columns}\n")
print(f"employees columns:  {employees.columns}")
```

You see the column names of each dataframe, below:

```
customers columns:  Index(['CustomerId', 'FirstName', 'LastName', 'Company', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email', 'SupportRepId'], dtype='object')

employees columns:  Index(['EmployeeId', 'LastName', 'FirstName', 'Title', 'ReportsTo', 'BirthDate', 'HireDate', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email'], dtype='object')
``` 

There are no column names that suggest they might provide a match between the two tables. Read the database documentation to determine the related columns, if any, that are in the dataframes you created from the tables. Or, if you were accessing the data using an SQL client or an ORM, you could manually document the relationship between the two database tables.

If you do not have database documentation, you may still be able to figure out the relationships between two dataframes you want to merge. To find potential matches, display a few rows of each dataframe.

```python
display(customers.sample(2))
display(employees.sample(2))
```

You can see in the output that the ID numbers in the *customers* dataframe's SupportRepId column match the ID numbers *employees* dataframe's EmployeeId column to create a many-to-one relationship between the *customers* and *employees* dataframes.

![Customer and Employee data to be merged](./Images/pandas053.png)

Using this information, you can create a Pandas merge statement that [executes an outer join](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#brief-primer-on-merge-methods-relational-algebra) of the *customers* and *employees* dataframes. The following code merges the *customers* and *employees* dataframes, adds appropriate suffixes to overlapping table names:

```python
df2 = pd.merge(
    employees, 
    customers, 
    left_on='EmployeeId', 
    right_on='SupportRepId',
    suffixes=['_emp','_cust'],
    how = 'outer'
)
```

All the employees records are in the merged dataframe whether or not customers' *SupportRepId* fields match their *EmployeeId* field. Now, you can analyze the merged data.  Group employees and count the number of customers each employee supports.

```python
df2 = (
    df2
    .groupby(['EmployeeId','LastName_emp', 
              'FirstName_emp', 'Title'], 
             as_index=False, dropna=False)['CustomerId']
    .count()
    .rename(columns = {'CustomerId':'Num_Customers'})
)
```

Organize the grouped dataframe so it is more presentable. Combine the employee name columns into one and re-order the columns in the dataframe.

```python
df2['Employee_Name'] = (
    df2['FirstName_emp'] + ' ' + df2['LastName_emp']
)
df2 = df2.drop(['FirstName_emp', 'LastName_emp'], axis=1)
df2 = df2[['EmployeeId', 'Employee_Name', 'Title', 'Num_Customers']]
print(df2.to_string(index=False))
```

We see the following output:

```
 EmployeeId    Employee_Name               Title  Num_Customers
          1     Andrew Adams     General Manager              0
          2    Nancy Edwards       Sales Manager              0
          3     Jane Peacock Sales Support Agent             21
          4    Margaret Park Sales Support Agent             20
          5    Steve Johnson Sales Support Agent             18
          6 Michael Mitchell          IT Manager              0
          7      Robert King            IT Staff              0
          8   Laura Callahan            IT Staff              0
```

We see that five employees supported no customers. This makes sense when you look at the employees' titles.

# Select data from the database using SQL queries

When working with large amounts of data, you may prefer to perform most of your data joins, grouping, and filter operations on the database server instead of locally on your PC. The Pandas *read_sql_query* enables you to send an SQL query to the database and then load the selected data into a dataframe.

## The *read_sql_query* function

To select data from the SQL database, you need to create an SQL query statement using the [SQL language](https://en.wikipedia.org/wiki/SQL). For example, see the SQL statement below that selects all the columns in a table:

```sql
SELECT * FROM Album
```

To use that statement with Pandas, run the following code:

```python
statement = "SELECT * FROM Album"

albums = pd.read_sql_query(statement, url)
print(albums.shape)
print(albums.sample(4))
```

The output shows a random sample of four rows from the *albums* dataframe, which contains the entire contents, 347 rows, of the *Album* table.

```
(347, 3)
     AlbumId                        Title  ArtistId
78        79       In Your Honor [Disc 1]        84
23        24               Afrociberdelia        18
195      196  Retrospective I (1974-1980)       128
218      219                     Tangents       143
```

## Filtering data

When you use SQL queries in Pandas, you can select a smaller subset of data to read into your dataframe. This is more efficient than reading in all the data from a table and then using Pandas to remove data you don't need.

For example, if you only need a list four random Album titles from the Album table, select only data from the *Title* column and limit the number of returned rows to four:

```python
statement = """
SELECT "Album"."Title" 
FROM Album 
ORDER BY random()
LIMIT 4
"""

albums = pd.read_sql_query(statement, url)
print(albums.shape)
print(albums)
```

The output shows that the *albums* dataframe now contains only four rows of album titles so we do not need to perform any additional Pandas operations to reduce the data to only what we need.

```
(4, 1)
                                       Title
0  Beethoven: Symphony No. 6 'Pastoral' Etc.
1                           Live After Death
2                               Supernatural
3            Vinícius De Moraes - Sem Limite
```

## Joining tables into one dataframe

Another benefit of SQL is that, when working with large databases, you can join tables and filter data more efficiently on the SQL server because it is optimized for these kinds of operations.

SQL query statements can select specific columns from tables, filter returned rows based on your criteria, join tables, rename columns, and more. For example, the query below merges data from the Album, Artist, and Track tables and then returns only the tracks performed by the artist named "Alanis Morissette":

```python
statement = """
SELECT "Track"."Name" AS "Track_Name", 
    "Album"."Title" AS "Album_Title", 
    "Artist"."Name" AS "Artist_Name", 
    "Track"."Composer" AS "Track_Composer", 
    "Track"."Milliseconds" AS "Track_Length", 
    "Track"."UnitPrice" AS "Track_Price" 
FROM "Album" 
JOIN "Track" ON "Album"."AlbumId" = "Track"."AlbumId" 
JOIN "Artist" ON "Artist"."ArtistId" = "Album"."ArtistId"
WHERE "Artist"."Name" = "Alanis Morissette"
"""

df1 = pd.read_sql_query(statement, url)
display(df1.style.format(thousands=","))
```

The *df1* dataframe contains only thirteen rows and only the columns needed. Each column has been renamed to make it easier to understand the data.

![Data selected by Pandas using an SQL query](./Images/pandas054.png)

If you know the relationships defined between tables in the SQL database, you can write simpler SQL join statements because you don't always need to state which columns to join on.  

# Saving pandas dataframes

Pandas works in your computer's memory. The pandas workflow does not require that you save work to disk and then read it back later. If you are re-starting a data analysis project, you would normally go back to the original data source, read in the data again and apply the Pandas functions you wish to apply. If you are [handing the dataframe off to another program](https://sparkbyexamples.com/pandas/convert-pandas-to-pyspark-dataframe/), you would normally do that in memory.

One case where you might want to save a dataframe to disk is when you wish to output the results to a spreadsheet for an end user, who may have asked for a spreadsheet version of the results. To [save a dataframe to an Excel spreadsheet](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_pickle.html), execute the following statement:

```python
df1.to_excel("artist_info.xlsx", index=False)  
```

You can [add style methods](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.io.formats.style.Styler.to_excel.html#pandas.io.formats.style.Styler.to_excel) to make the Excel spreadsheet look nice for your stakeholder. You can also output [complex spreadsheets with multiple worksheets](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html).

Another case might be where you want to convert the Pandas dataframe into a CSV file for use by Power BI. This is not the best way to integrate Pandas and Power BI; it is better to [use pandas in Power BI](https://realpython.com/power-bi-python/). But, sometimes you have to work the way others are working. To save a Pandas dataframe as a CSV file, execute the following statement:

```python
df1.to_csv("artist_info.csv", index=False)
```

You will not normally need to save your Pandas dataframe to disk for your own use. However, if you want to save your Pandas dataframe to disk so you can use it later, the best option is to [*pickle*](https://realpython.com/python-pickle-module/) the dataframe. This saves pandas dataframe objects to a file, maintaining column data types and other Pandas-specific information that would be lost if the dataframe was saved in other formats. To pickle a pandas dataframe, execute the following statement:

```python
df1.to_pickle("artist_info.pkl")
```

To read back the picked dataframe, execute the following statement:

```python
new_df = pd.read_pickle("artist_info.pkl")
```


# Conclusion

You have learned enough to read data from an SQL database into a Pandas dataframe. You can use Pandas to read entire database tables into dataframes, then operate on them locally on your PC. You can also use Pandas to send an SQL query to the database and read the results into a dataframe. 

You may most often use SQL queries to select the data from the database before reading it into a Pandas dataframe. The SQL language is relatively simple to learn for queries and joins. If you prefer to work exclusively in Python, you may want to use the [SQLalchemy ORM](https://www.sqlalchemy.org/SQLAlchemy) to build the SQL statements used by the Pandas *read_sql_query* function.

In the next document, I will describe how to use SQLAlchemy ORM to automatically build a Python object model that represents an existing database and to create SQL statements that can be used by Pandas to read selected data into dataframes.


