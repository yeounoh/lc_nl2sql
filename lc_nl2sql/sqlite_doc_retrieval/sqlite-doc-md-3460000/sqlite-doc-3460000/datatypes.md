




Datatypes In SQLite version 2




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







## Datatypes In SQLite Version 2


### 1\.0   Typelessness



SQLite is "typeless". This means that you can store any
kind of data you want in any column of any table, regardless of the
declared datatype of that column. 
(See the one exception to this rule in section 2\.0 below.)
This behavior is a feature, not
a bug. A database is supposed to store and retrieve data and it 
should not matter to the database what format that data is in.
The strong typing system found in most other SQL engines and
codified in the SQL language spec is a misfeature \-
it is an example of the implementation showing through into the
interface. SQLite seeks to overcome this misfeature by allowing
you to store any kind of data into any kind of column and by
allowing flexibility in the specification of datatypes.




A datatype to SQLite is any sequence of zero or more names
optionally followed by a parenthesized lists of one or two
signed integers. Notice in particular that a datatype may
be *zero* or more names. That means that an empty
string is a valid datatype as far as SQLite is concerned.
So you can declare tables where the datatype of each column
is left unspecified, like this:




> ```
> 
> CREATE TABLE ex1(a,b,c);
> 
> ```



Even though SQLite allows the datatype to be omitted, it is
still a good idea to include it in your CREATE TABLE statements,
since the data type often serves as a good hint to other
programmers about what you intend to put in the column. And
if you ever port your code to another database engine, that
other engine will probably require a datatype of some kind.
SQLite accepts all the usual datatypes. For example:




> ```
> 
> CREATE TABLE ex2(
>   a VARCHAR(10),
>   b NVARCHAR(15),
>   c TEXT,
>   d INTEGER,
>   e FLOAT,
>   f BOOLEAN,
>   g CLOB,
>   h BLOB,
>   i TIMESTAMP,
>   j NUMERIC(10,5)
>   k VARYING CHARACTER (24),
>   l NATIONAL VARYING CHARACTER(16)
> );
> 
> ```



And so forth. Basically any sequence of names optionally followed by 
one or two signed integers in parentheses will do.



### 2\.0   The INTEGER PRIMARY KEY



One exception to the typelessness of SQLite is a column whose type
is INTEGER PRIMARY KEY. (And you must use "INTEGER" not "INT".
A column of type INT PRIMARY KEY is typeless just like any other.)
INTEGER PRIMARY KEY columns must contain a 32\-bit signed integer. Any
attempt to insert non\-integer data will result in an error.




INTEGER PRIMARY KEY columns can be used to implement the equivalent
of AUTOINCREMENT. If you try to insert a NULL into an INTEGER PRIMARY
KEY column, the column will actually be filled with an integer that is
one greater than the largest key already in the table. Or if the
largest key is 2147483647, then the column will be filled with a
random integer. Either way, the INTEGER PRIMARY KEY column will be
assigned a unique integer. You can retrieve this integer using
the **sqlite\_last\_insert\_rowid()** API function or using the
**last\_insert\_rowid()** SQL function in a subsequent SELECT statement.



### 3\.0   Comparison and Sort Order



SQLite is typeless for the purpose of deciding what data is allowed
to be stored in a column. But some notion of type comes into play
when sorting and comparing data. For these purposes, a column or
an expression can be one of two types: **numeric** and **text**.
The sort or comparison may give different results depending on which
type of data is being sorted or compared.




If data is of type **text** then the comparison is determined by
the standard C data comparison functions **memcmp()** or
**strcmp()**. The comparison looks at bytes from two inputs one
by one and returns the first non\-zero difference.
Strings are '\\000' terminated so shorter
strings sort before longer strings, as you would expect.




For numeric data, this situation is more complex. If both inputs
look like well\-formed numbers, then they are converted
into floating point values using **atof()** and compared numerically.
If one input is not a well\-formed number but the other is, then the
number is considered to be less than the non\-number. If neither inputs
is a well\-formed number, then **strcmp()** is used to do the
comparison.




Do not be confused by the fact that a column might have a "numeric"
datatype. This does not mean that the column can contain only numbers.
It merely means that if the column does contain a number, that number
will sort in numerical order.




For both text and numeric values, NULL sorts before any other value.
A comparison of any value against NULL using operators like "\<" or
"\>\=" is always false.



### 4\.0   How SQLite Determines Datatypes



For SQLite version 2\.6\.3 and earlier, all values used the numeric datatype.
The text datatype appears in version 2\.7\.0 and later. In the sequel it
is assumed that you are using version 2\.7\.0 or later of SQLite.




For an expression, the datatype of the result is often determined by
the outermost operator. For example, arithmetic operators ("\+", "\*", "%")
always return a numeric results. The string concatenation operator
("\|\|") returns a text result. And so forth. If you are ever in doubt
about the datatype of an expression you can use the special **typeof()**
SQL function to determine what the datatype is. For example:




> ```
> 
> sqlite> SELECT typeof('abc'+123);
> numeric
> sqlite> SELECT typeof('abc'||123);
> text
> 
> ```



For table columns, the datatype is determined by the type declaration
of the CREATE TABLE statement. The datatype is text if and only if
the type declaration contains one or more of the following strings:




> BLOB  
> 
> CHAR  
> 
> CLOB  
> 
> TEXT



The search for these strings in the type declaration is case insensitive,
of course. If any of the above strings occur anywhere in the type
declaration, then the datatype of the column is text. Notice that
the type "VARCHAR" contains "CHAR" as a substring so it is considered
text.


If none of the strings above occur anywhere in the type declaration,
then the datatype is numeric. Note in particular that the datatype for columns
with an empty type declaration is numeric.



### 5\.0   Examples



Consider the following two command sequences:




> ```
> 
> CREATE TABLE t1(a INTEGER UNIQUE);        CREATE TABLE t2(b TEXT UNIQUE);
> INSERT INTO t1 VALUES('0');               INSERT INTO t2 VALUES(0);
> INSERT INTO t1 VALUES('0.0');             INSERT INTO t2 VALUES(0.0);
> 
> ```


In the sequence on the left, the second insert will fail. In this case,
the strings '0' and '0\.0' are treated as numbers since they are being 
inserted into a numeric column but 0\=\=0\.0 which violates the uniqueness
constraint. However, the second insert in the right\-hand sequence works. In
this case, the constants 0 and 0\.0 are treated a strings which means that
they are distinct.


SQLite always converts numbers into double\-precision (64\-bit) floats
for comparison purposes. This means that a long sequence of digits that
differ only in insignificant digits will compare equal if they
are in a numeric column but will compare unequal if they are in a text
column. We have:



> ```
> 
> INSERT INTO t1                            INSERT INTO t2
>    VALUES('12345678901234567890');           VALUES(12345678901234567890);
> INSERT INTO t1                            INSERT INTO t2
>    VALUES('12345678901234567891');           VALUES(12345678901234567891);
> 
> ```


As before, the second insert on the left will fail because the comparison
will convert both strings into floating\-point number first and the only
difference in the strings is in the 20\-th digit which exceeds the resolution
of a 64\-bit float. In contrast, the second insert on the right will work
because in that case, the numbers being inserted are strings and are
compared using memcmp().



Numeric and text types make a difference for the DISTINCT keyword too:




> ```
> 
> CREATE TABLE t3(a INTEGER);               CREATE TABLE t4(b TEXT);
> INSERT INTO t3 VALUES('0');               INSERT INTO t4 VALUES(0);
> INSERT INTO t3 VALUES('0.0');             INSERT INTO t4 VALUES(0.0);
> SELECT DISTINCT * FROM t3;                SELECT DISTINCT * FROM t4;
> 
> ```



The SELECT statement on the left returns a single row since '0' and '0\.0'
are treated as numbers and are therefore indistinct. But the SELECT 
statement on the right returns two rows since 0 and 0\.0 are treated
a strings which are different.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


