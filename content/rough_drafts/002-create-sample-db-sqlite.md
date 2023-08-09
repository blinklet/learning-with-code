Maybe retry Northwind on SQLite?
* [SQLite](https://database.guide/2-sample-databases-sqlite/)
* because I think it is the same as the sample data in SQL Server...




The best solution is to install an SQL database engine like [SQLite](https://www.sqlite.org/index.html) on your PC and download a database backup from a public repository. In this document, we will use the *[Chinook database](https://github.com/lerocha/chinook-database)*, which is a public database that tries to emulate a media store's database. It contains customer names and addresses, sales data, and inventory data.

[Download the *Chinook_Sqlite.sqlite* file](https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite) from the Chinook Database project's [downloads folder]() and save it to your computer.




I believe this is why many data-science books and blogs show you how to work with other data sources like [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values). There are already many [public sources of interesting data](https://www.dropbase.io/post/top-11-open-and-public-data-sources) in CSV files and there are also [many](https://alongrandomwalk.com/2020/09/14/read-and-write-files-with-jupyter-notebooks/) [tutorials](https://www.digitalocean.com/community/tutorials/data-analysis-and-visualization-with-pandas-and-jupyter-notebook-in-python-3) [available](https://www.datacamp.com/tutorial/python-excel-tutorial) that show you how to load data from CSV files into Pandas dataframes. 





