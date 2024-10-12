




The Checksum VFS Shim




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Checksum VFS Shim


►
Table Of Contents
[1\. Overview](#overview)
[2\. Compiling](#compiling)
[3\. Loading](#loading)
[4\. Usage](#usage)
[5\. Verification Of Checksums](#verification_of_checksums)
[6\. Controlling Checksum Verification](#controlling_checksum_verification)




# 1\. Overview


The checksum VFS extension is a [VFS shim](vfs.html#shim) that adds an 8\-byte
checksum to the end of every page in an SQLite database. The checksum
is added as each page is written and verified as each page is read.
The checksum is intended to help detect database corruption caused by
random bit\-flips in the mass storage device.



The checksum VFS extension requires 
SQLite version 3\.32\.0 (2020\-05\-22\) or later. It will not
work with earlier versions of SQLite.



# 2\. Compiling


The checksum VFS module is a [loadable extension](loadext.html). It is not
included in the [amalgamation](amalgamation.html). It must be added to SQLite
either at compile\-time or at run\-time. The source code to
the checksum VFS module is in the
[ext/misc/cksumvfs.c](https://sqlite.org/src/file/ext/misc/cksumvfs.c)
source file in the
[SQLite source tree](https://sqlite.org/src).



To build the checksum VFS module into a run\-time loadable
extension, use commands similar to the following:



* (linux) → gcc \-fPIC \-shared cksumvfs.c \-o cksumvfs.so
* (mac) → clang \-fPIC \-dynamiclib cksumvfs.c \-o cksumvfs.dylib
* (windows) → cl cksumvfs.c \-link \-dll \-out:cksumvfs.dll


You may want to add additional compiler options, of course,
according to the needs of your project.



To statically link this extension with your product,
compile it like any other C\-language module but add the
"\-DSQLITE\_CKSUMVFS\_STATIC" option so that this module knows that
it is being statically linked rather than dynamically linked.



# 3\. Loading


To load this extension as a shared library, you first have to
bring up a dummy SQLite database connection to use as the argument
to the [sqlite3\_load\_extension()](c3ref/load_extension.html) API call. Then you invoke the
[sqlite3\_load\_extension()](c3ref/load_extension.html) API and shutdown the dummy database
connection. All subsequent database connections that are opened
will include this extension. For example:




```
sqlite3 *db;
sqlite3_open(":memory:", &db);
sqlite3_load_extension(db, "./cksumvfs");
sqlite3_close(db);

```

If this extension is compiled with \-DSQLITE\_CKSUMVFS\_STATIC and
statically linked against the application, initialize it using
a single API call as follows:




```
sqlite3_cksumvfs_init();

```

Cksumvfs is a [VFS shim](vfs.html#shim). When loaded, "cksmvfs" becomes the new
default VFS, and it uses the prior default VFS as the next VFS
down in the stack. This is normally what you want. However, in
complex situations where multiple VFS shims are being loaded,
it might be important to ensure that cksumvfs is loaded in the
correct order so that it sequences itself into the default VFS
Shim stack in the right order.



# 4\. Usage


Open database connections using the [sqlite3\_open()](c3ref/open.html) or 
[sqlite3\_open\_v2()](c3ref/open.html) interfaces, as normal. Ordinary database files
(without a checksum) will operate normally. Databases with 
checksums will return an SQLITE\_IOERR\_DATA error if a page is
encountered that contains an invalid checksum.



Checksumming only works on databases that have a [reserve bytes](fileformat2.html#resbyte)
value of exactly 8\. The default value for reserve\-bytes is 0\.
Hence, newly created database files will omit the checksum by
default. To create a database that includes a checksum, change
the reserve\-bytes value to 8 by running code similar to this:




```
int n = 8;
sqlite3_file_control(db, 0, SQLITE_FCNTL_RESERVE_BYTES, &n);

```

If you do this immediately after creating a new database file,
before anything else has been written into the file, then that
might be all that you need to do. Otherwise, the API call
above should be followed by:




```
sqlite3_exec(db, "VACUUM", 0, 0, 0);

```

It never hurts to run the VACUUM, even if you don't need it.
If the database is in WAL mode, you should shutdown and
reopen all database connections before continuing.



From the CLI, use the ".filectrl reserve\_bytes 8" command, 
followed by "VACUUM;".



Note that SQLite allows the number of reserve\-bytes to be
increased but not decreased. So if a database file already
has a reserve\-bytes value greater than 8, there is no way to
activate checksumming on that database, other than to dump
and restore the database file. Note also that other extensions
might also make use of the reserve\-bytes. Checksumming will
be incompatible with those other extensions.



# 5\. Verification Of Checksums


If any checksum is incorrect, the "PRAGMA quick\_check" command
will find it. To verify that checksums are actually enabled
and running, use SQL like the following:




```
SELECT count(*), verify_checksum(data)
  FROM sqlite_dbpage
 GROUP BY 2;

```

There are three possible outputs from the verify\_checksum()
function: 1, 0, and NULL. 1 is returned if the checksum is
correct. 0 is returned if the checksum is incorrect. NULL
is returned if the page is unreadable. If checksumming is
enabled, the read will fail if the checksum is wrong, so the
usual result from verify\_checksum() on a bad checksum is NULL.



If everything is OK, the query above should return a single
row where the second column is 1\. Any other result indicates
either that there is a checksum error, or checksum validation
is disabled.



# 6\. Controlling Checksum Verification


The cksumvfs extension implements a new PRAGMA statement that can
be used to disable, re\-enable, or query the status of checksum
verification:




```
PRAGMA checksum_verification;          -- query status
PRAGMA checksum_verification=OFF;      -- disable verification
PRAGMA checksum_verification=ON;       -- re-enable verification

```

The "checksum\_verification" pragma will return "1" (true) or "0"
(false) if checksum verification is enabled or disabled, respectively.
"Verification" in this context means the feature that causes
SQLITE\_IOERR\_DATA errors if a checksum mismatch is detected while
reading. Checksums are always kept up\-to\-date as long as the
[reserve bytes](fileformat2.html#resbyte) value of the database is 8, regardless of the setting
of this pragma. Checksum verification can be disabled (for example)
to do forensic analysis of a database that has previously reported
a checksum error.



The "checksum\_verification" pragma will always respond with "0" if
the database file does not have a [reserve bytes](fileformat2.html#resbyte) value of 8\. The
pragma will return no rows at all if the cksumvfs extension is
not loaded.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


