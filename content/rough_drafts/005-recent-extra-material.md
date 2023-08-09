


### Other frameworks

While Pandas and NumPy are often used for data analytics in Python, some other projects claim to be more modern and efficient. 

[Apache Arrow](https://arrow.apache.org/) could be used in place of NumPy. Arrow uses memory in a more efficient way and supports faster data processing operations. The next major release of [Pandas will use Apache Arrow](https://datapythonista.me/blog/pandas-20-and-the-arrow-revolution-part-i) as its back end.

[Polars](https://www.pola.rs/) could be used in place of Pandas. It supports parallel processing, which delivers better performance on modern CPUs. It also uses Apache Arrow as its back end for data processing.

For very large use-cases, Python programmers may use a "big data" framework like [Apache Spark](https://spark.apache.org/), which provides dataframe functionality [similar to Pandas and Polars](https://towardsdatascience.com/spark-vs-pandas-part-2-spark-c57f8ea3a781) and processes data sets stored across multiple computers. Spark is incorporated into [Databricks](https://www.databricks.com/). PySpark provides a [Python API](https://spark.apache.org/docs/latest/api/python/index.html) and a [Pandas API](https://spark.apache.org/docs/3.2.0/api/python/user_guide/pandas_on_spark/). Spark also [does a lot more](https://www.toptal.com/spark/introduction-to-apache-spark) than just process data in dataframes.






