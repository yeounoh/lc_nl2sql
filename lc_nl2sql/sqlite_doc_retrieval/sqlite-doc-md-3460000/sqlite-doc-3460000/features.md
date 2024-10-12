




Features Of SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# Features Of SQLite


* [Transactions](transactional.html)
 are atomic, consistent, isolated, and durable (ACID)
 even after system crashes and power failures.
* [Zero\-configuration](zeroconf.html)
 \- no setup or administration needed.
* [Full\-featured SQL](fullsql.html) implementation
 with advanced capabilities like [partial indexes](partialindex.html),
 [indexes on expressions](expridx.html), [JSON](json1.html),
 [common table expressions](lang_with.html), and [window functions](windowfunctions.html).
 ([Omitted features](omitted.html))
* A complete database is stored in a 
 [single cross\-platform disk file](onefile.html).
 Great for use as an [application file format](appfileformat.html).
* Supports terabyte\-sized databases and gigabyte\-sized strings
 and blobs. (See <limits.html>.)
* Small code [footprint](footprint.html): 
 less than 750KiB fully configured or much less
 with optional features omitted.
* Simple, easy to use [API](cintro.html).
* Fast: In some cases, SQLite is 
 [faster than direct filesystem I/O](fasterthanfs.html)* Written in ANSI\-C. [TCL bindings](tclsqlite.html) included.
 Bindings for dozens of other languages available separately.
* Well\-commented source code with
 [100% branch test coverage](testing.html#coverage).
* Available as a 
 [single ANSI\-C source\-code file](amalgamation.html) 
 that is [easy to compile](howtocompile.html) and hence is easy
 to add into a larger project.
* [Self\-contained](selfcontained.html):
 no external dependencies.
* Cross\-platform: Android, \*BSD, iOS, Linux, Mac, Solaris, VxWorks, 
 and Windows (Win32, WinCE, WinRT)
 are supported out of the box. Easy to port to other systems.
* Sources are in the [public domain](copyright.html).
 Use for any purpose.
* Comes with a standalone [command\-line interface](cli.html)
 (CLI) client that can be used to administer SQLite databases.





## Suggested Uses For SQLite:


* **Database For The Internet Of Things.**
SQLite is popular choice for the database engine in cellphones,
PDAs, MP3 players, set\-top boxes, and other electronic gadgets.
SQLite has a small code footprint, makes efficient use of memory,
disk space, and disk bandwidth, is highly reliable, and requires
no maintenance from a Database Administrator.
* **Application File Format.**
Rather than using fopen() to write XML, JSON, CSV,
or some proprietary format into
disk files used by your application, use an SQLite database.
You'll avoid having to write and troubleshoot a parser, your data
will be more easily accessible and cross\-platform, and your updates
will be transactional. ([more...](appfileformat.html))
* **Website Database.**
Because it requires no configuration and stores information in ordinary
disk files, SQLite is a popular choice as the database to back small
to medium\-sized websites.
* **Stand\-in For An Enterprise RDBMS.**
SQLite is often used as a surrogate for an enterprise RDBMS for
demonstration purposes or for testing. SQLite is fast and requires
no setup, which takes a lot of the hassle out of testing and which
makes demos perky and easy to launch.
* [More suggestions...](./whentouse.html)


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 




