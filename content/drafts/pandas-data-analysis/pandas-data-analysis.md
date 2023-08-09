title: unknown1
slug: unknown1
summary: tbd
date: 2023-08-07
modified: 2023-08-07
category: Databases
status: draft


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








You can remove the "ArtistId" column from the data frame because it is now redundant. Keep the *AlbumId* column because you will use it to join data from the Track table in the next step. 

```python
df1.drop('ArtistId', axis=1)
```

You can also rename the *Name* column to *Artist* so it is clearer.

```
df1.rename(columns = {'Name':'Artist'})
```

Also, you could have done everything in one statement when you merged the dataframes by chaining pandas methods together:

```python
df1 = (pd
     .merge(albums, artists)
     .drop('ArtistId', axis=1)
     .rename(columns = {'Name':'Artist'}))
```

Now get data from a third table and merge it with the dataframe *df1*. Get the data from the Track table and load it into a pandas dataframe named *tracks*:

```python
tracks = pd.read_sql_table(table_name='Track', con=engine)
```

If you print the first few rows of the *tracks* dataframe, you can see it has 3,503 rows and nine columns. You should expect that Pandas will use the *AlbumId* column in the dataframe *df1* to join on the AlbumId column in dataframe *tracks*.

```python
print(tracks.head())
print(tracks.shape)
```
```
   TrackId                                     Name  AlbumId  MediaTypeId  \
0        1  For Those About To Rock (We Salute You)        1            1   
1        2                        Balls to the Wall        2            2   
2        3                          Fast As a Shark        3            2   
3        4                        Restless and Wild        3            2   
4        5                     Princess of the Dawn        3            2   

   GenreId                                           Composer  Milliseconds  \
0        1          Angus Young, Malcolm Young, Brian Johnson        343719   
1        1                                               None        342562   
2        1  F. Baltes, S. Kaufman, U. Dirkscneider & W. Ho...        230619   
3        1  F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. D...        252051   
4        1                         Deaffy & R.A. Smith-Diesel        375418   

      Bytes  UnitPrice  
0  11170334       0.99  
1   5510424       0.99  
2   3990994       0.99  
3   4331779       0.99  
4   6290521       0.99  
(3503, 9)
```

You can see how Pandas displays the nine columns by spitting the displayed tables into three "rows". And you can see that we have 3,503 rows in the Tracks table.

Finally, merge the *tracks* dataframe with the *df1* dataframe and, at the same time, delete unneeded columns and rename other columns:

```python
df3 = (pd
     .merge(df1, tracks)
     .drop(['AlbumId','TrackId',
            'Bytes','UnitPrice',
            'MediaTypeId','GenreId'], axis=1)
     .rename(columns = {'Name':'Track', 
                        'Title':'Album',
                        'Milliseconds':'Length(ms)'}))

print(df3.shape)
display(df3.head().style.format(thousands=","))
```













# NaN and NULL and None


Check that every customer has a support representative assigned to them. 

```python
test = customers.loc[customers['SupportRepId'].isnull()] 
print(len(test))
```
```
0
```

We see zero customers have a null, or "NaN", value in their *SupportRepId* column. So, we can place the *customers* dataframe on the right side of the merge function and perform a *left outer join*.










## Data analysis using Pandas

<!--fix-->
Use SQLAlchemy ORM to create a joined table containing the data we need for analysis and load that data into a dataframe. 

For example, Load data from the database into a dataframe named *df4* that contains track information, including prices. 

```python
albums = pd.read_sql_table(table_name='Album', con=engine)
artists = pd.read_sql_table(table_name='Artist', con=engine)
tracks = pd.read_sql_table(table_name='Track', con=engine)

df1 = (pd
     .merge(albums, artists)
     .rename(columns = {'Name':'Artist'}))

data = (pd
     .merge(df1, tracks)
     .rename(columns = {'Name':'Track', 
                        'Title':'Album',
                        'Milliseconds':'Length'}))

print(f"Longest track: {data.Length.max():d}")
print(f"Shortest track: {data.Length.min():,}")
print(f"How many blanks in Composer column?: "
      f"{data.Composer.isnull().sum():,}")
print(f"Track length mean: {data.Length.mean():,.2f}")
print(f"Track length median: {data.Length.median():,.2f}")
print(f"Artist mode: {data.Artist.mode()[0]}")
print(f"Correlation between Length and UnitPrice: "
      f"{data['Length'].corr(data['UnitPrice']):,.2f}")
print(f"Track length standard deviation: "
      f"{data.Length.std():,.2f}")
```

Which outputs the following:

```
Longest track: 5286953
Shortest track: 1,071
How many blanks in Composer column?: 978
Track length mean: 393,599.21
Track length median: 255,634.00
Artist mode: Iron Maiden
Correlation between Length and UnitPrice: 0.93
Track length standard deviation: 535,005.44
```

You can also use the Pandas *describe* function to get statistical information about any column in a dataframe. For example, to get statistics about the length of all tracks in the dataframe:

```python
print(data.Length.describe())
```
```
count    3.503000e+03
mean     3.935992e+05
std      5.350054e+05
min      1.071000e+03
25%      2.072810e+05
50%      2.556340e+05
75%      3.216450e+05
max      5.286953e+06
Name: Length, dtype: float64
```

Or, to get statistics about the artist names in the dataframe:

```python
print(data.Artist.describe())
```
```
count            3503
unique            204
top       Iron Maiden
freq              213
Name: Artist, dtype: object
```

You can see that the type of information you get depends on the data type of the column.

Group and select data. You can use Pandas to [group and aggregate data](https://realpython.com/pandas-groupby/).

For example, the following code groups the dataframe by Artist and calculates the standard deviation of all the track lengths created by each artist. 

```python
print(f"Track length standard deviation for a sample of artists:")
pd.options.display.float_format = '{:,.2f}'.format
pd.options.styler.format.thousands= ','

display(
    data
    .groupby(['Artist'])['Length'] 
    .std()
    .dropna()
    .sample(3)
    .to_frame()
)
```

The following code displays the three longest tracks in the dataframe:

![](./Images/pandas020.png)

```python
print(f"Longest tracks, with artist name:")
display(
    data[['Track','Length','Artist']]
    .nlargest(3, 'Length')
    .style.hide(axis="index")
)
```

![](./Images/pandas021.png)

The following code counts the number of tracks created by each artist artist, from a random sample of artists:

```python
print(f"Number of tracks per artist, from a sample of artists::")
display(
    data
    .groupby('Artist')['Track']
    .count()
    .sample(3)
    .to_frame()
)
```

![](./Images/pandas022.png)

The following code lists the shortest tracks by the artist named "Guns N' Roses":

```python
print(f"Shortest tracks by Artist=Guns N' Roses: ")
gnr = data.loc[data.Artist == "Guns N' Roses"]
gnr_shortest = gnr[['Track','Length']].nsmallest(3, 'Length')
display(
    gnr_shortest
    .style.hide(axis="index")
)   
```

![](./Images/pandas023.png)