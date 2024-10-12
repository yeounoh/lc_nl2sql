




SQLite Archive Files




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










SQLite Archive Files


►
Table Of Contents
[1\. Introduction](#introduction)
[1\.1\. Database As Container Object](#database_as_container_object)
[1\.2\. Applications Using SQLite Archives](#applications_using_sqlite_archives)
[2\. Advantages Of SQLite Archives](#advantages_of_sqlite_archives)
[3\. Disadvantages Of SQLite Archives](#disadvantages_of_sqlite_archives)
[4\. Managing An SQLite Archive From The Command\-Line](#managing_an_sqlite_archive_from_the_command_line)
[4\.1\. Other command\-line tools](#other_command_line_tools)
[5\. Managing SQLite Archives From Application Code](#managing_sqlite_archives_from_application_code)




# 1\. Introduction



An "SQLite Archive" is a file container similar to a
[ZIP archive](https://en.wikipedia.org/wiki/Zip_(file_format)) or
[Tarball](https://en.wikipedia.org/wiki/Tar_(computing)) but
based on an SQLite database.




An SQLite Archive is an ordinary SQLite database file that contains the
following table as part of its schema:




```
CREATE TABLE sqlar(
  name TEXT PRIMARY KEY,  -- name of the file
  mode INT,               -- access permissions
  mtime INT,              -- last modification time
  sz INT,                 -- original file size
  data BLOB               -- compressed content
);

```


Each row of the SQLAR table holds the content of a single file.
The filename (the full pathname relative to the root of the archive)
is in the "name" field.
The "mode" field is an integer which is the unix\-style access permissions
for the file. "mtime" is the modification time of the file in seconds
since 1970\. "sz" is the original uncompressed size of the file.
The "data" field contains the file content. The content is usually
compressed using [Deflate](http://zlib.net/), though not always. If the
"sz" field is equal to the size of the "data" field, then the content
is stored uncompressed.




## 1\.1\. Database As Container Object



An SQLite Archive is one example of a more general
idea that an SQLite database can behave as a container object holding
lots of smaller data components.




With client/server databases like PostgreSQL or Oracle, users and
developers tend to think of the database as a service or a "node", not
as an object. This is because the database content is spread out across
multiple files on the server, or possibly across multiple servers in a
service cluster. One cannot point to a single file or even a single
directory and say "this is the database".




SQLite, in contrast, stores all content in a [single file on disk](fileformat2.html).
That single file is something you can point to and say
"this is the database". It behaves as an object.
An SQLite database file can be copied, renamed, sent as an
email attachment, passed as the argument a POST HTTP request,
or otherwise treated as other data object such as an image,
document, or media file.




Studies show that many applications already use
SQLite as a container object. For example,
[Kennedy](https://odin.cse.buffalo.edu/papers/2015/TPCTC-sqlite-final.pdf)
(no relation to the [SQLite developer](crew.html#dan)) reports that 14% of
Android applications never write to their SQLite databases. It is
believed that these applications are downloading entire databases
from the cloud and then using the information locally as needed. In other
words, the applications are using SQLite not so much as a database but as
a queryable wire\-transfer format.



## 1\.2\. Applications Using SQLite Archives



The [Fossil Distributed Version Control](https://fossil-scm.org/) system
provides users with the option to download check\-ins as either Tarballs,
ZIP Archives, or SQLite Archives.


# 2\. Advantages Of SQLite Archives


1. An SQLite Archive is flexible.
ZIP Archives and Tarballs are limited to storing only files. An
SQLite Archive stores files plus whatever other tabular
and/or relational data seems useful to the application.
2. An SQLite Archive is transactional.
Updates are atomic and durable, even if there are crashes
or power losses in the middle of the update.
Readers see a consistent and unchanging version of the content even
is some other process is simultaneously updating the archive.
3. An SQLite Archive can be updated incrementally.
Individual files can be added or removed or replaced without having
to rewrite the entire archive.
4. An SQLite Archive can be queried using a high\-level query language (SQL).
Some examples:



	* What is the total size of all files in the archive whose names
	 end in ".h" or ".cpp"?
	* What percentage of the files are compressed by less than 25%?
	* How many executable files are in the archive?
Questions like these (and countless others) can be answered without
having to uncompress or extract any content.
5. Applications that already use SQLite for other purposes can easily
add support for SQLite Archives using a small extension
(<https://sqlite.org/src/file/ext/misc/sqlar.c>) to handle the compression
and decompression of content. Even this tiny extension can be omitted
if the files in the archive are uncompressed. In contrast, supporting
ZIP Archives and/or Tarballs requires either separate libraries or
lots of extra custom code, or sometimes both.
6. An SQLite Archive can work around firewall\-imposed censorship.
For example, certain file types that are considered "dangerous"
(examples: DLLs) will be
[blocked by Gmail](https://support.google.com/mail/answer/6590)
and probably many other email services and firewalls, even if the
files are wrapped inside a ZIP Archive or Tarball.
But these firewalls usually do not (yet) know about SQLite Archives and
so content can be put inside an SQLite Archive to evade censorship.


# 3\. Disadvantages Of SQLite Archives


1. The SQLite Archive is a relatively new format. It was first described in
in 2014\. ZIP Archives and Tarballs, on the other hand, have been around
for decades and are well\-entrenched as standard formats. Most programmers
know what a ZIP Archive or Tarball is, but if you say "SQLite Archive" you
are more likely to get a reply of "What?" Tooling to process ZIP Archives
and Tarballs is more likely to be installed on stock computers.
2. Since an SQLite database is a more general format (it is designed to do
much more than simply store a bunch of files) it is not as compact as either
the ZIP Archive or Tarball formats. An SQLite Archive is usually about 1%
larger than the equivalent ZIP Archive. Tarballs are compressed as a single
unit rather than compressing each file separately as is done by both
SQLite and ZIP Archives. For these reason, Tarballs tend to be smaller
than either ZIP or SQLite Archives.



As an example, the following table show the relative sizes for an
SQLite Archive, a ZIP Archive, and a Tarball of the 1,743 files
in the SQLite 3\.22\.0 source tree:




| SQLite Archive | 10,754,048 |
| --- | --- |
| ZIP Archive (using Info\-ZIP 3\.0\) | 10,662,365 |
| ZIP Archive (using [zipfile](zipfile.html)) | 10,390,215 |
| Tarball | 9,781,109 |
3. An SQLite Archive supports only the [Deflate](https://zlib.net/) compression
method. Tarballs and ZIP Archive support a wider assortment of
compression methods.



# 4\. Managing An SQLite Archive From The Command\-Line



The recommended way of creating, updating, listing, and extracting
an SQLite Archive is to use the [sqlite3\.exe command\-line shell](cli.html)
for SQLite [version 3\.23\.0](releaselog/3_23_0.html) (2018\-04\-02\) or later. This CLI
supports the \-A command\-line option that allows easy management
of SQLite Archives.
The CLI for SQLite [version 3\.22\.0](releaselog/3_22_0.html) (2018\-01\-22\) has the
[.archive command](cli.html#sqlar) for managing SQLite Archives, but that requires
interacting with the shell.




To list all of the files in an SQLite Archive named "example.sqlar"
using one of these commands:




```
sqlite3 example.sqlar -At
sqlite3 example.sqlar -Atv

```


To extract all files from an SQLite Archive named "example.sqlar":




```
sqlite3 example.sqlar -Ax

```


To create a new SQLite Archive named "alltxt.sqlar" containing all \*.txt
files in the current directory:




```
sqlite3 alltxt.sqlar -Ac *.txt

```


To add or update files in an existing SQLite Archive:




```
sqlite3 example.sqlar -Au *.md

```


For usage hints and a summary of all options, simply give the [CLI](cli.html)
the \-A option with no additional arguments:




```
sqlite3 -A

```


All of these commands work the same way if the filename argument is
is a ZIP Archive instead of an SQLite database.



## 4\.1\. Other command\-line tools



Just as there is the "zip" program to manage ZIP Archives, and the
"tar" program to manage Tarballs, the
["sqlar" program](https://sqlite.org/sqlar) exists to manage SQL Archives.
The "sqlar" program is able to create a new SQLite Archive, list the
content of an existing archive, add or remove files from the archive,
and/or extract files from the archive.
A separate "sqlarfs" program is able to mount the SQLite Archive as
a [Fuse Filesystem](https://github.com/libfuse/libfuse).



# 5\. Managing SQLite Archives From Application Code



Applications can easily read or write SQLite Archives by linking against
SQLite and including the
[ext/misc/sqlar.c](https://sqlite.org/src/file/ext/misc/sqlar.c) extension
to handle the compression and decompression. The sqlar.c extension
creates two new SQL functions.




**sqlar\_compress(X)**

The sqlar\_compress(X) function attempts to compress a copy of the
blob X using the [Default](https://zlib.net/) algorithm and returns the
result as a blob. If the input X is not a compressible blob, then
a copy of X is returned. This routine is used when inserting content
into an SQLite Archive.


**sqlar\_uncompress(Y,SZ)**

The sqlar\_uncompress(Y,SZ) function will undo the compression accomplished
by sqlar\_compress(X). The Y parameter is the compressed content (the output
from a prior call to sqlar\_compress()) and SZ is the original uncompressed
size of the input X that generated Y. If SZ is less than or equal to the
size of Y, that indicates that no compression occurred, and so
sqlar\_uncompress(Y,SZ) returns a copy of Y. Otherwise, sqlar\_uncompress(Y,SZ)
runs the Inflate algorithm on Y to uncompress it and restore it to its
original form and returns the uncompressed content.
This routine is used when extracting content from an SQLite Archive.




Using the two routines above, it is simple for applications to insert
new records into or extract existing records from an SQLite Archive.
Insert a new into an SQLite Archive using code like this:




```
INSERT INTO sqlar(name,mode,mtime,sz,data)
 VALUES ($name,$mode,strftime('%s',$mtime),
         length($content),sqlar_compress($content));

```


Extract an entry from the SQLite Archive using code like this:




```
SELECT name, mode, datetime(mtime,'unixepoch'), sqlar_uncompress(data,sz)
  FROM sqlar
 WHERE ...;

```


The code above is for the general case. For the special case of an
SQLite Archive that only stores uncompressed or uncompressible content
(this might come up, for example, in an SQLite Archive that stores only
JPEG, GIF, and/or PNG images) then the content can be inserted into
and extracted from the database without using the sqlar\_compress()
and sqlar\_uncompress() functions, and the sqlar.c extension is not
required.



