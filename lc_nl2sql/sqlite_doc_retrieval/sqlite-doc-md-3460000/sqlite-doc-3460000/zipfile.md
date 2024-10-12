




The SQLite Zipfile Module




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The SQLite Zipfile Module


►
Table Of Contents
[1\. Overview](#overview)
[2\. Obtaining and Compiling Zipfile](#obtaining_and_compiling_zipfile)
[3\. Using Zipfile](#using_zipfile)
[3\.1\. Table\-Valued Function (read\-only access)](#table_valued_function_read_only_access_)
[3\.2\. Virtual Table Interface (read/write access)](#virtual_table_interface_read_write_access_)
[3\.2\.1\. Adding Entries to a Zip Archive](#adding_entries_to_a_zip_archive)
[3\.2\.2\. Deleting Zip Archive Entries](#_deleting_zip_archive_entries_) 
[3\.2\.3\. Updating Existing Zip Archive Entries](#_updating_existing_zip_archive_entries_) 
[3\.3\. The zipfile() Aggregate Function](#_the_zipfile_aggregate_function_) 




# 1\. Overview


 The zipfile module provides read/write access to simple 
[ZIP archives](https://en.wikipedia.org/wiki/Zip_%28file_format%29).
The current implementation has the following restrictions:



* Does not support encryption.
* Does not support ZIP archives that span multiple files.
* Does not support zip64 extensions.
* The only compression algorithm supported is
 ["deflate"](https://zlib.net).


 Some or all of these restrictions may be removed in the future.



# 2\. Obtaining and Compiling Zipfile


The code for the zipfile module is found in the 
[ext/misc/zipfile.c](https://sqlite.org/src/file/ext/misc/zipfile.c)
file of the
[main SQLite source tree](https://sqlite.org/src).
It may be compiled into an SQLite 
[loadable extension](loadext.html) using a command like:




```
gcc -g -fPIC -shared zipfile.c -o zipfile.so

```

Alternatively, the zipfile.c file may be compiled into the application. 
In this case, the following function should be invoked to register the
extension with each new database connection:




```
int sqlite3_zipfile_init(sqlite3 *db, void*, void*);

```

 The first argument passed should be the database handle to register the
extension with. The second and third arguments should both be passed 0\.



 Zipfile is included in most builds of the [command\-line shell](cli.html).



# 3\. Using Zipfile


The zipfile module provides three similar interfaces for accessing, updating
and creating zip file archives:



1. A table\-valued function, which provides read\-only access to existing
 archives, either from the file\-system or in\-memory.
2. A virtual table, which provides read and write access to archives
 stored in the file\-system.
3. An SQL aggregate function, which can be used to create new archives
 in memory.


The zipfile module provides two similar interfaces for accessing zip
archives. A table\-valued function, which provides read\-only access to
existing archives, and a virtual table interface, which provides both
read and write access.



## 3\.1\. Table\-Valued Function (read\-only access)


For reading existing zip archives, the Zipfile module provides a
[table\-valued function](vtab.html#tabfunc2) that accepts a single argument. If the argument
is a text value, then it is a path to a zip archive to read from the
file\-system. Or, if the argument is an SQL blob, then it is the zip
archive data itself.



For example, to inspect the contents of zip archive "test.zip" from 
the current directory:




```
SELECT * FROM zipfile('test.zip');

```

Or, from the SQLite shell tool (the [readfile()](cli.html#fileio) 
function reads the contents of a file from the file\-system and returns it as a
blob):




```
SELECT * FROM zipfile( readfile('test.zip') );

```

The table\-valued function returns one row for each record (file, 
directory or symbolic link) in the zip archive. Each row has the 
following columns:





| Column Name | Contents |
| --- | --- |
| name | File name/path for the zip file record. |
| mode | UNIX mode, as returned by stat(2\) for the zip file record (an  integer). This identifies the type of record (file, directory  or symbolic link), and the associated user/group/all   permissions. |
| mtime | UTC timestamp, in seconds since the UNIX epoch (an integer). |
| sz | Size of associated data in bytes after it has been   uncompressed (an integer). |
| rawdata | Raw (possibly compressed) data associated with zip file  entry (a blob). |
| data | If the compression method for the record is either 0 or 8  (see below), then the uncompressed data associated with the  zip file entry. Or, if the compression method is not 0 or 8,   this column contains a NULL value. |
| method | The compression method used to compress the data (an  integer). The value 0 indicates that the data is stored  in the zip archive without compression. 8 means the  raw deflate algorithm. |


## 3\.2\. Virtual Table Interface (read/write access)


In order to create or modify an existing zip file, a "zipfile" virtual 
table must be created in the database schema. The CREATE VIRTUAL TABLE
statement expects a path to the zip file as its only argument. For example, to
write to zip file "test.zip" in the current directory, a zipfile table may be
created using:




```
CREATE VIRTUAL TABLE temp.zip USING zipfile('test.zip');

```

Such a virtual table has the same columns as the table\-valued function
described in the previous section. It may be read from using a SELECT 
statement in the same way as the table\-valued function can. 



Using the virtual table interface, new entries may be added to a zip
archive by inserting new rows into the virtual table. Entries may be
removed by deleting rows or modified by updating them.




### 3\.2\.1\. Adding Entries to a Zip Archive


Entries may be added to a zip archive by inserting new rows. The easiest
way to do this is to specify values for the "name" and "data" columns only and
have zipfile fill in sensible defaults for other fields. To insert a directory
into the archive, set the "data" column to NULL. For example, to add the
directory "dir1" and the file "m.txt" containing the text "abcdefghi" to zip
archive "test.zip":




```
INSERT INTO temp.zip(name, data) VALUES('dir1', NULL);           -- Add directory 
INSERT INTO temp.zip(name, data) VALUES('m.txt', 'abcdefghi');   -- Add regular file 

```

When a directory is inserted, if the "name" value does not end with
a '/' character, the zipfile module appends one. This is necessary for
compatibility with other programs (most notably "info\-zip") that 
manipulate zip archives.



To insert a symbolic link, the user must also supply a "mode" value.
For example, to add a symbolic link from "link.txt" to "m.txt":




```
INSERT INTO temp.zip(name, mode, data) VALUES('link.txt', 'lrwxrw-rw-', 'm.txt');

```

The following rules and caveats apply to the values specified as part of
each INSERT statement:





| Columns | Notes |
| --- | --- |
| name | A non\-NULL text value must be specified for the name column.   It is an error if the specified name already exists in the  archive. |
| mode | If NULL is inserted into the mode column, then the mode of the  new archive entry is automatically set to either 33188 (\-rw\-r\-\-r\-\-)  or 16877 (drwxr\-xr\-x), depending on whether or not the values   specified for columns "sz", "data" and "rawdata" indicate that  the new entry is a directory.    If the specified value is an integer (or text that looks like  an integer), it is inserted verbatim. If the value is not a valid UNIX  mode, some programs may behave unexpectedly when extracting files  from the archive.   Finally, if the value specified for this column is not an integer  or a NULL, then it is assumed to be a UNIX permissions string similar  to those output by the "ls \-l" command (e.g. "\-rw\-r\-\-r\-\-", "drwxr\-xr\-x"  etc.). In this case, if the string cannot be parsed it is an error. |
| mtime | If NULL is inserted into the mtime column, then the timestamp  of the new entry is set to the current time. Otherwise, the specified  value is interpreted as an integer and used as is. |
| sz | This column must be set to NULL. If a non\-NULL value is inserted into  this column, or if a new non\-NULL value is provided using an UPDATE  statement, it is an error. |
| rawdata | This column must be set to NULL. If a non\-NULL value is inserted into  this column, or if a new non\-NULL value is provided using an UPDATE  statement, it is an error. |
| data | To insert a directory into the archive, this field must be set to   NULL. In this case if a value was explicitly specified for the "mode"  column, then it must be consistent with a directory (i.e. it must be  true that (mode \& 0040000\)\=0040000\).    Otherwise, the value inserted into this field is the file contents  for a regular file, or the target of a symbolic link. |
| method | This field must be set one of integer values 0 and 8, or else to  NULL.    For a directory entry, any value inserted into this field is ignored.  Otherwise, if it is set to 0, then the file data or symbolic link  target is stored as is in the zip archive and the compression method  set to 0\. If it is set to 8, then the file data or link target is  compressed using deflate compression before it is stored and the  compression method set to 8\. Finally, if a NULL value is written  to this field, the zipfile module automatically decides whether  or not to compress the data before storing it. |


 Specifying an explicit value for the rowid field as part of an INSERT
statement is not supported. Any value supplied is ignored.



### 3\.2\.2\.  Deleting Zip Archive Entries


Records may be removed from an existing zip archive by deleting the
corresponding rows. For example, to remove file "m.txt" from zip archive
"test.zip" using the virtual table created above:




```
DELETE FROM temp.zip WHERE name = 'm.txt';

```

Note that deleting records from a zip archive does not reclaim the 
space used within the archive \- it merely removes an entry from the
archives "Central Directory Structure", making the entry inaccessible.
One way to work around this inefficiency is to create a new zip 
archive based on the contents of the edited archive. For example, after
editing the archive accessed via virtual table temp.zzz:




```
-- Create a new, empty, archive: 
CREATE VIRTUAL TABLE temp.newzip USING zipfile('new.zip');

-- Copy the contents of the existing archive into the new archive
INSERT INTO temp.newzip(name, mode, mtime, data, method)
    SELECT name, mode, mtime, data, method FROM temp.zzz;

```

### 3\.2\.3\.  Updating Existing Zip Archive Entries


Existing zip archive entries may be modified using UPDATE statements.



The three leftmost columns of a zipfile virtual table, "name", "mode" 
and "mtime", may each be set to any value that may be inserted into the same
column (see above). If either "mode" or "mtime" is set to NULL, the final 
value is determined as described for an INSERT of a NULL value \- the current
time for "mtime" and either 33188 or 16877 for "mode", depending on whether 
or not the values specified for the next four columns of the zipfile table
indicate that the entry is a directory or a file.



It is an error to attempt to set the sz or rawdata field to any value
other than NULL. 



The data and method columns may also be set as described for an INSERT
above. 



## 3\.3\.  The zipfile() Aggregate Function


 New zip archives may be constructed entirely within memory using the
zipfile() aggregate function. Each row visited by the aggregate function
adds an entry to the zip archive. The value returned is a blob containing
the entire archive image.



 The zipfile() aggregate function may be called with 2, 4 or 5 
arguments. If it is called with 5 arguments, then the entry added to
the archive is equivalent to inserting the same values into the "name", 
"mode", "mtime", "data" and "method" columns of a zipfile virtual table.



 If zipfile() is invoked with 2 arguments, then the entry added to
the archive is equivalent to that added by inserting the same two values into
the "name" and "data" columns of a zipfile virtual table, with all
other values set to NULL. If invoked with 4 arguments, it is equivalent
to inserting the 4 values into the "name", "mode", "mtime" and "data"
columns. In other words, the following pairs of queries are equivalent:




```
SELECT zipfile(name, data) ...
SELECT zipfile(name, NULL, NULL, data, NULL) ...

SELECT zipfile(name, mode, mtime, data) ...
SELECT zipfile(name, mode, mtime, data, NULL) ...

```

 For example, to create an archive containing two text files, "a.txt" and
"b.txt", containing the text "abc" and "123" respectively:




```
WITH contents(name, data) AS (
  VALUES('a.txt', 'abc') UNION ALL
  VALUES('b.txt', '123')
)
SELECT zipfile(name, data) FROM contents;

```

*This page last modified on [2023\-06\-07 13:17:51](https://sqlite.org/docsrc/honeypot) UTC* 


