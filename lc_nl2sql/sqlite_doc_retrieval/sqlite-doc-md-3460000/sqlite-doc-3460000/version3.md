




SQLite Version 3 Overview




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










| **Editorial Note:** This document was written in 2004 as a guide to programmers who were transitioning from SQLite2 to SQLite3\. It is retained as part of the historical record of SQLite. Modern programmers should refer to more up\-to\-date documentation on SQLite available elsewhere on this website. |
| --- |


## SQLite Version 3 Overview



SQLite version 3\.0 introduces important changes to the library, including:



* A more compact format for database files.
* Manifest typing and BLOB support.
* Support for both UTF\-8 and UTF\-16 text.
* User\-defined text collating sequences.
* 64\-bit ROWIDs.
* Improved Concurrency.



This document is a quick introduction to the changes for SQLite 3\.0
for users who are already familiar with SQLite version 2\.8\.



### Naming Changes



SQLite version 2\.8 will continue to be supported with bug fixes
for the foreseeable future. In order to allow SQLite version 2\.8
and SQLite version 3\.0 to peacefully coexist, the names of key files
and APIs in SQLite version 3\.0 have been changed to include the
character "3". For example, the include file used by C programs
has been changed from "sqlite.h" to "sqlite3\.h". And the name of
the shell program used to interact with databases has been changed
from "sqlite.exe" to "sqlite3\.exe". With these changes, it is possible
to have both SQLite 2\.8 and SQLite 3\.0 installed on the same system at
the same time. And it is possible for the same C program to link
against both SQLite 2\.8 and SQLite 3\.0 at the same time and to use
both libraries at the same time.



### New File Format



The format used by SQLite database files has been completely revised.
The old version 2\.1 format and the new 3\.0 format are incompatible with
one another. Version 2\.8 of SQLite will not read a version 3\.0 database
files and version 3\.0 of SQLite will not read a version 2\.8 database file.




To convert an SQLite 2\.8 database into an SQLite 3\.0 database, have
ready the command\-line shells for both version 2\.8 and 3\.0\. Then
enter a command like the following:




> ```
> 
> sqlite OLD.DB .dump | sqlite3 NEW.DB
> 
> ```



The new database file format uses B\+trees for tables. In a B\+tree, all
data is stored in the leaves of the tree instead of in both the leaves and
the intermediate branch nodes. The use of B\+trees for tables allows for
better scalability and the storage of larger data fields without the use of
overflow pages. Traditional B\-trees are still used for indices.



The new file format also supports variable pages sizes between 512 and
65536 bytes. The size of a page is stored in the file header so the
same library can read databases with different pages sizes, in theory,
though this feature has not yet been implemented in practice.




The new file format omits unused fields from its disk images. For example,
indices use only the key part of a B\-tree record and not the data. So
for indices, the field that records the length of the data is omitted.
Integer values such as the length of key and data are stored using
a variable\-length encoding so that only one or two bytes are required to
store the most common cases but up to 64\-bits of information can be encoded
if needed. 
Integer and floating point data is stored on the disk in binary rather
than being converted into ASCII as in SQLite version 2\.8\.
These changes taken together result in database files that are typically
25% to 35% smaller than the equivalent files in SQLite version 2\.8\.




Details of the low\-level B\-tree format used in SQLite version 3\.0 can
be found in header comments to the 
[btreeInt.h](https://www.sqlite.org/src/finfo?name=src/btreeInt.h)
source file and in the [file format](fileformat2.html) documentation.



### Manifest Typing and BLOB Support



SQLite version 2\.8 will deal with data in various formats internally,
but when writing to the disk or interacting through its API, SQLite 2\.8
always converts data into ASCII text. SQLite 3\.0, in contrast, exposes 
its internal data representations to the user and stores binary representations
to disk when appropriate. The exposing of non\-ASCII representations was
added in order to support BLOBs.




SQLite version 2\.8 had the feature that any type of data could be stored
in any table column regardless of the declared type of that column. This
feature is retained in version 3\.0, though in a slightly modified form.
Each table column will store any type of data, though columns have an
affinity for the format of data defined by their declared datatype.
When data is inserted into a column, that column will make an attempt
to convert the data format into the column's declared type. All SQL
database engines do this. The difference is that SQLite 3\.0 will 
still store the data even if a format conversion is not possible.




For example, if you have a table column declared to be of type "INTEGER"
and you try to insert a string, the column will look at the text string
and see if it looks like a number. If the string does look like a number
it is converted into a number and into an integer if the number does not
have a fractional part, and stored that way. But if the string is not
a well\-formed number it is still stored as a string. A column with a
type of "TEXT" tries to convert numbers into an ASCII\-Text representation
before storing them. But BLOBs are stored in TEXT columns as BLOBs because
you cannot in general convert a BLOB into text.




In most other SQL database engines the datatype is associated with
the table column that holds the data \- with the data container.
In SQLite 3\.0, the datatype is associated with the data itself, not
with its container.
[Paul Graham](http://www.paulgraham.com/) in his book 
*[ANSI Common Lisp](http://www.paulgraham.com/acl.html)*
calls this property "Manifest Typing".
Other writers have other definitions for the term "manifest typing",
so beware of confusion. But by whatever name, that is the datatype
model supported by SQLite 3\.0\.




Additional information about datatypes in SQLite version 3\.0 is
available
[separately](datatype3.html).



### Support for UTF\-8 and UTF\-16



The new API for SQLite 3\.0 contains routines that accept text as
both UTF\-8 and UTF\-16 in the native byte order of the host machine.
Each database file manages text as either UTF\-8, UTF\-16BE (big\-endian),
or UTF\-16LE (little\-endian). Internally and in the disk file, the
same text representation is used everywhere. If the text representation
specified by the database file (in the file header) does not match
the text representation required by the interface routines, then text
is converted on\-the\-fly.
Constantly converting text from one representation to another can be
computationally expensive, so it is suggested that programmers choose a
single representation and stick with it throughout their application.




In the current implementation of SQLite, the SQL parser only works
with UTF\-8 text. So if you supply UTF\-16 text it will be converted.
This is just an implementation issue and there is nothing to prevent
future versions of SQLite from parsing UTF\-16 encoded SQL natively.




When creating new user\-defined SQL functions and collating sequences,
each function or collating sequence can specify if it works with
UTF\-8, UTF\-16be, or UTF\-16le. Separate implementations can be registered
for each encoding. If an SQL function or collating sequence is required
but a version for the current text encoding is not available, then 
the text is automatically converted. As before, this conversion takes
computation time, so programmers are advised to pick a single
encoding and stick with it in order to minimize the amount of unnecessary
format juggling.




SQLite is not particular about the text it receives and is more than
happy to process text strings that are not normalized or even
well\-formed UTF\-8 or UTF\-16\. Thus, programmers who want to store
ISO8859 data can do so using the UTF\-8 interfaces. As long as no
attempts are made to use a UTF\-16 collating sequence or SQL function,
the byte sequence of the text will not be modified in any way.



### User\-defined Collating Sequences



A collating sequence is just a defined order for text. When SQLite 3\.0
sorts (or uses a comparison operator like "\<" or "\>\=") the sort
order is first determined by the data type.



* NULLs sort first
* Numeric values sort next in numerical order
* Text values come after numerics
* BLOBs sort last



Collating sequences are used for comparing two text strings.
The collating sequence does not change the ordering of NULLs, numbers,
or BLOBs, only text.




A collating sequence is implemented as a function that takes the
two strings being compared as inputs and returns negative, zero, or
positive if the first string is less than, equal to, or greater than
the second.
SQLite 3\.0 comes with a single built\-in collating sequence named "BINARY"
which is implemented using the memcmp() routine from the standard C library.
The BINARY collating sequence works well for English text. For other
languages or locales, alternative collating sequences may be preferred.




The decision of which collating sequence to use is controlled by the
COLLATE clause in SQL. A COLLATE clause can occur on a table definition,
to define a default collating sequence to a table column, or on field
of an index, or in the ORDER BY clause of a SELECT statement.
Planned enhancements to SQLite are to include standard CAST() syntax
to allow the collating sequence of an expression to be defined.



### 64\-bit ROWIDs



Every row of a table has a unique rowid.
If the table defines a column with the type "INTEGER PRIMARY KEY" then that
column becomes an alias for the rowid. But with or without an INTEGER PRIMARY
KEY column, every row still has a rowid.




In SQLite version 3\.0, the rowid is a 64\-bit signed integer.
This is an expansion of SQLite version 2\.8 which only permitted
rowids of 32\-bits.




To minimize storage space, the 64\-bit rowid is stored as a variable length
integer. Rowids between 0 and 127 use only a single byte. 
Rowids between 0 and 16383 use just 2 bytes. Up to 2097152 uses three
bytes. And so forth. Negative rowids are allowed but they always use
nine bytes of storage and so their use is discouraged. When rowids
are generated automatically by SQLite, they will always be non\-negative.



### Improved Concurrency



SQLite version 2\.8 allowed multiple simultaneous readers or a single
writer but not both. SQLite version 3\.0 allows one process to begin
writing the database while other processes continue to read. The
writer must still obtain an exclusive lock on the database for a brief
interval in order to commit its changes, but the exclusive lock is no
longer required for the entire write operation.
A [more detailed report](lockingv3.html) on the locking
behavior of SQLite version 3\.0 is available separately.




A limited form of table\-level locking is now also available in SQLite.
If each table is stored in a separate database file, those separate
files can be attached to the main database (using the ATTACH command)
and the combined databases will function as one. But locks will only
be acquired on individual files as needed. So if you redefine "database"
to mean two or more database files, then it is entirely possible for
two processes to be writing to the same database at the same time.
To further support this capability, commits of transactions involving
two or more ATTACHed database are now atomic.



### Credits



SQLite version 3\.0 is made possible in part by AOL developers
supporting and embracing great Open\-Source Software.





