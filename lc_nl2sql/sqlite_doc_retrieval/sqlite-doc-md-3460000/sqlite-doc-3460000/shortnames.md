




8\+3 Filenames




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# SQLite And 8\+3 Filenames



The default configuration of SQLite assumes the underlying filesystem
supports long filenames.




SQLite does not impose any naming requirements on database files.
SQLite will happily work with a database file that has any filename extension
or with no extension at all.
When auxiliary files are needed for a [rollback journal](lockingv3.html#rollback) or
a [write\-ahead log](wal.html) or for one of the other kinds of
[temporary disk files](tempfiles.html), then the name for the auxiliary file is normally
constructed by appending a suffix onto the end of the database file name.
For example, if the original database is call "app.db" then
the [rollback journal](lockingv3.html#rollback) will be called "app.db\-journal"
and the [write\-ahead log](wal.html) will be called "app.db\-wal".
This approach to auxiliary file naming works great on systems that
support long filenames. But on systems that impose 8\+3 filename
constraints, the auxiliary files do not fit the 8\+3 format even though
the original database file does.



## Changing Filesystems



The recommended fix for this problem is to select a different
filesystem. These days, there is a huge selection of high\-performance, 
reliable, patent\-free filesystems that support long filenames. 
Where possible, it is recommended that embedded devices use one
of these other filesystems. This will avoid compatibility issues
and the danger of
[database corruption caused by inconsistent use of 8\+3 filenames](shortnames.html#db83corrupt).



## Adjusting SQLite To Use 8\+3 Filenames



Some devices are compelled to use an older filesystem with 8\+3
filename restrictions for backwards compatibility, or due
to other non\-technical factors. In such situations, SQLite can be
coerced into using auxiliary files that fit the 8\+3 pattern as follows:



1. Compile the SQLite library with the either the compile\-time
 options [SQLITE\_ENABLE\_8\_3\_NAMES\=1](compile.html#enable_8_3_names) or
 [SQLITE\_ENABLE\_8\_3\_NAMES\=2](compile.html#enable_8_3_names).
 Support for 8\+3 filenames is not included in SQLite by default
 because it does introduce some overhead. The overhead is tiny,
 but even so, we do not want to burden the billions of SQLite
 applications that do not need 8\+3 filename support.

- If the [SQLITE\_ENABLE\_8\_3\_NAMES\=1](compile.html#enable_8_3_names) option
 is used, then SQLite is capable of using 8\+3 filenames but that
 capabilities is disabled and must be enabled separately for each
 database connection by using
 using [URI filenames](uri.html) when [opening](c3ref/open.html) or
 [ATTACH\-ing](lang_attach.html) the database files and include the
 "8\_3\_names\=1" query parameter in the URI. If SQLite
 is compiled with
 [SQLITE\_ENABLE\_8\_3\_NAMES\=2](compile.html#enable_8_3_names) then
 8\+3 filenames are enabled by default and this step can be
 skipped.

- Make sure that database filenames follow the 8\+3 filename
 format and that they do not have an empty name or extension.
 In other words, the database filename must contain between
 1 and 8 characters in the base name and between 1 and 3 characters
 in the extension. Blank extensions are not allowed.



When the steps above are used, SQLite will shorten filename extensions
by only using the last 3 characters of
the extension. Thus, for example, a file that would normally be called
"app.db\-journal" is shortened to just "app.nal".
Similarly, "app.db\-wal" will become "app.wal" and
"app.db\-shm" becomes "app.shm".




Note that it is very important that the database filename have some kind
of extension. If there is no extension, then SQLite creates auxiliary
filenames by appending to the base name of the file. Thus, a database
named "db01" would have a [rollback journal](lockingv3.html#rollback) file named
"db01\-journal". And as this filename has no extension to shorten
to 3 characters, it will be used as\-is, and will violate 8\+3 naming rules.




## Database Corruption Warning



If a database file is accessed using 8\+3 naming rather than the default
long filename, then it must be consistently accessed 
using 8\+3 naming by every database
connection every time it is opened, or else there is a risk of database
corruption.
The auxiliary [rollback journal](lockingv3.html#rollback) and [write\-ahead log](wal.html) files are essential
to SQLite for being about to recover from a crash. If an application is
using 8\+3 names and crashes, then the information needed to safely recover
from the crash is stored in files with the ".nal" or
".wal" extension. If the next application to open the database
does not specify the "8\_3\_names\=1" URI parameter, then SQLite
will use the long filenames to try to locate the rollback journal or
write\-ahead log files. It will not find them, since they were saved using
8\+3 names by the application that crashed, and hence the database will not
be properly recovered and will likely go corrupt.




Using a database file with 8\+3 filenames in some cases while in 
other cases using long filenames is equivalent to
[deleting a hot journal](howtocorrupt.html#delhotjrnl).



*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


