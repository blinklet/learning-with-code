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
