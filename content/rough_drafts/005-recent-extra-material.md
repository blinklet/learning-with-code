This is from the pandas database post. adapt it as an intro to using SQLAlchemy


% Python, pandas, and databases

Python programmers who use Pandas to perform data analysis have many options for gathering data from databases and incorporating it into their programs. Pandas users may get data from SQL databases using Pandas functions, using a Python database driver combined with SQL queries, using an [object-relational mapping (ORM) framework](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping), or some combination of these tools.

Many [Pandas](https://pandas.pydata.org/) books and blogs do not show you how to get data stored in databases. Instead, they work with simpler-to-use data sources like [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values). There are already [many](https://alongrandomwalk.com/2020/09/14/read-and-write-files-with-jupyter-notebooks/) [tutorials](https://www.digitalocean.com/community/tutorials/data-analysis-and-visualization-with-pandas-and-jupyter-notebook-in-python-3) [available](https://www.datacamp.com/tutorial/python-excel-tutorial) for these simpler examples so this document will focus only on using Pandas to read data from databases.

<!--more-->

# Data from a database

Programmers who do not wish to use SQL can use Pandas to read individual SQL database tables into Pandas dataframes. Then, they can use Pandas to join, transform, and filter those dataframes until they create the dataset that they need.

Python programmers who are already proficient in writing [SQL queries](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select/) may use them in Pandas to extract and transform a dataset before loading it into a Pandas dataframe. Or, they may directly access the data by passing their SQL queries to an SQL database driver. [^1]

[^1]: Use the appropriate driver that is compatible with the SQL database you are using, such as [psycopg](https://www.psycopg.org/) for PostgreSQL, or [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) for MySQL. Since we are using an SQLite database, we could use the [sqlite package](https://www.sqlite.org/index.html), which is part of the Python standard library.

Finally, Python programmers who do not wish to use SQL, but who still want to build powerful SQL queries in Python programs, may use the [SQLAlchemy ORM](https://www.sqlalchemy.org/SQLAlchemy). It can be used to create queries for Pandas functions or to select data directly from the database. I will discuss SQLAlchemy in another document.




So, there are only a few practical tutorials available in books or in blogs about how to integrate [database data and Pandas dataframes](https://www.mssqltips.com/sqlservertip/7324/python-pandas-read-sql-server-data-dataframe/) in Python programs.




Python programmers who use the [Pandas](https://pandas.pydata.org/) library to perform data analysis may get their data from various sources. They may query data from SQL Databases, import data from Excel and CSV files stored on a server, call APIs of data services, or [scrape data](https://towardsdatascience.com/a-tutorial-of-what-kaggle-wont-teach-you-web-scraping-data-cleaning-and-more-16d402a206e8) from web sites. 




### Other frameworks

While Pandas and NumPy are often used for data analytics in Python, some other projects claim to be more modern and efficient. 

[Apache Arrow](https://arrow.apache.org/) could be used in place of NumPy. Arrow uses memory in a more efficient way and supports faster data processing operations. The next major release of [Pandas will use Apache Arrow](https://datapythonista.me/blog/pandas-20-and-the-arrow-revolution-part-i) as its back end.

[Polars](https://www.pola.rs/) could be used in place of Pandas. It supports parallel processing, which delivers better performance on modern CPUs. It also uses Apache Arrow as its back end for data processing.

For very large use-cases, Python programmers may use a "big data" framework like [Apache Spark](https://spark.apache.org/), which provides dataframe functionality [similar to Pandas and Polars](https://towardsdatascience.com/spark-vs-pandas-part-2-spark-c57f8ea3a781) and processes data sets stored across multiple computers. Spark is incorporated into [Databricks](https://www.databricks.com/). PySpark provides a [Python API](https://spark.apache.org/docs/latest/api/python/index.html) and a [Pandas API](https://spark.apache.org/docs/3.2.0/api/python/user_guide/pandas_on_spark/). Spark also [does a lot more](https://www.toptal.com/spark/introduction-to-apache-spark) than just process data in dataframes.







The best solution is to install an SQL database engine like [SQLite](https://www.sqlite.org/index.html) on your PC and download a database backup from a public repository. In this document, we will use the *[Chinook database](https://github.com/lerocha/chinook-database)*, which is a public database that tries to emulate a media store's database. It contains customer names and addresses, sales data, and inventory data.

[Download the *Chinook_Sqlite.sqlite* file](https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite) from the Chinook Database project's [downloads folder]() and save it to your computer.




I believe this is why many data-science books and blogs show you how to work with other data sources like [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values). There are already many [public sources of interesting data](https://www.dropbase.io/post/top-11-open-and-public-data-sources) in CSV files and there are also [many](https://alongrandomwalk.com/2020/09/14/read-and-write-files-with-jupyter-notebooks/) [tutorials](https://www.digitalocean.com/community/tutorials/data-analysis-and-visualization-with-pandas-and-jupyter-notebook-in-python-3) [available](https://www.datacamp.com/tutorial/python-excel-tutorial) that show you how to load data from CSV files into Pandas dataframes. 




You can keep chaining Pandas dataframe methods to create complex operations that merge dataframes, rename and delete columns, and more. For example:

```python
df4 = (products[['Name', 'ProductCategoryID', 
                 'ProductModelID']]
       .merge(categories[['ProductCategoryID', 'ParentProductCategoryID', 
                          'Name']],
              on='ProductCategoryID', 
              suffixes=['_product','_category'])
       .merge(models[['ProductModelID', 'Name']],
              suffixes=['_productcategory','_model'])
       .rename(columns={'Name_product':'ProductName',
                        'Name_category':'CategoryName',
                        'Name':'ModelName',})
       .merge(categories[['ProductCategoryID', 'Name']],
              left_on='ParentProductCategoryID',
              right_on='ProductCategoryID',
              suffixes=['_left','_right'])
       .rename(columns={'Name':'ParentCategory',})
       .drop(columns=['ProductModelID', 'ParentProductCategoryID',
             'ProductCategoryID_left', 'ProductCategoryID_right'])
      )

print(df4.shape)
with pd.option_context('display.width', 1000):
    print(df4.sample(8))
```

Which displays the following output:

```
(295, 4)
                       ProductName     CategoryName               ModelName ParentCategory
279        Touring-1000 Yellow, 54    Touring Bikes            Touring-1000          Bikes
160          Fender Set - Mountain          Fenders   Fender Set - Mountain    Accessories
125                  HL Road Pedal           Pedals           HL Road Pedal     Components
124                  ML Road Pedal           Pedals           ML Road Pedal     Components
82          LL Mountain Rear Wheel           Wheels  LL Mountain Rear Wheel     Components
179        Men's Sports Shorts, XL           Shorts     Men's Sports Shorts       Clothing
50   ML Mountain Frame - Black, 48  Mountain Frames       ML Mountain Frame     Components
128                    ML Crankset        Cranksets             ML Crankset     Components
```








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


