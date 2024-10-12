




The CSV Virtual Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The CSV Virtual Table


# 1\. Overview



The CSV virtual table reads
[RFC 4180](https://www.ietf.org/rfc/rfc4180.txt) formatted comma\-separated
values, and returns that content as if it were rows and columns of an SQL
table.




The CSV virtual table is useful to applications that need to bulk\-load
large amounts of comma\-separated value content.
The CSV virtual table is also useful as a template source file for
implementing other virtual tables.




The CSV virtual table is not built into the SQLite amalgamation.
It is available as a
[separate source file](https://www.sqlite.org/src/artifact?ci=trunk&filename=ext/misc/csv.c)
that can be compiled into a [loadable extension](loadext.html).
Typical usage of the CSV virtual table from the
[command\-line shell](cli.html) would be something like this:




```
.load ./csv
CREATE VIRTUAL TABLE temp.t1 USING csv(filename='thefile.csv');
SELECT * FROM t1;

```


The first line of the script above causes the [command\-line shell](cli.html) to
read and activate the run\-time loadable extension for CSV. For an
application, the equivalent C\-language API is
[sqlite3\_load\_extension()](c3ref/load_extension.html).
Observe that the filename extension (ex: ".dll" or ".so" or ".dylib") is
omitted from the extension filename. Omitting the filename extension is
not required, but it helps in making the script cross\-platform. SQLite
will automatically append the appropriate extension.




The second line above creates a virtual table named "t1" that reads
the content of the file named in the argument. The number and names of
the columns is determined automatically by reading the first line of
content. Other options to the CSV virtual table provide the ability to
take the CSV content from a string rather than a separate file, and give 
the programmer more control over the number and names of the columns.
The options are detailed below. The CSV virtual table is usually
created as a TEMP table so that it exists only for the current database
connection and does not become a permanent part of the database schema.
Note that there is no "CREATE TEMP VIRTUAL TABLE" command in SQLite.
Instead, prepend the "temp." schema prefix to the name of the virtual
table.




The third line of the example shows the virtual table being used, to read
all content of the CSV file. This is perhaps the simplest possible use
of the virtual table. The CSV virtual table can be used anywhere an ordinary
virtual table can be used. One can use the CSV virtual table inside subqueries,
or [common table expressions](lang_with.html) or add WHERE, GROUP BY, HAVING, ORDER BY,
and LIMIT clauses as required.



# 2\. Arguments



The example above showed a single **filename\='thefile.csv'** argument
for the CSV virtual table. But other arguments are also possible.



* **filename\=***FILENAME*


The **filename\=** argument specifies an external file from which
CSV content is read. Every CSV virtual table must have either a 
**filename\=** argument or a **data\=** argument and not both.
* **data\=***TEXT*


The **data\=** argument specifies that *TEXT* is the literal
content of the CSV file.
* **schema\=***SCHEMA*


 The **schema\=** argument specifies a [CREATE TABLE](lang_createtable.html) statement that
the CSV virtual table passes to the [sqlite3\_declare\_vtab()](c3ref/declare_vtab.html) interface in
order to define the names of the columns in the virtual table.
* **columns\=***N*


The **columns\=***N* argument specifies the number of columns
in the CSV file.
If the input data contains more columns than this,
then the excess columns are ignored. If the input data contains fewer columns,
then extra columns are filled with NULL.
If the **columns\=***N* argument is omitted, the first line of the
CSV file is read to determine the number of columns.
* **header\=***BOOLEAN*  

or just  

**header**


If the **header** argument is true then the first row of the CSV file
to be treated as a header rather than as data. The second line of the CSV
file becomes the first row of content.
If the **schema\=** options is omitted, then the first line of the CSV
file determines the names of the columns.


# 3\. Column Names



The column names of the virtual table are determined primarily by the
**schema\=** argument.
If the **schema\=** argument is omitted, but **header** is true, then
the values found in the first line of the CSV file become the column names.
If the **schema\=** argument is omitted and **header** is false, then
the columns are named "c0", "c1", "c2", and so forth.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


