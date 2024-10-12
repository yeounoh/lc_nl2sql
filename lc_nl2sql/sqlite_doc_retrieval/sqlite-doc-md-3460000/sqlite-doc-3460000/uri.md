




Uniform Resource Identifiers




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Uniform Resource Identifiers


# 1\. URI Filenames In SQLite



Beginning with [version 3\.7\.7](releaselog/3_7_7.html) (2011\-06\-23\),
the SQLite database file argument to the
[sqlite3\_open()](c3ref/open.html), [sqlite3\_open16()](c3ref/open.html), and [sqlite3\_open\_v2()](c3ref/open.html) interfaces
and to the [ATTACH](lang_attach.html) command can be specified
either as an ordinary filename or as a Uniform Resource Identifier or URI.
The advantage of using a URI filename is that query parameters on the URI can
be used to control details of the newly created database connection.
For example, an alternative [VFS](vfs.html) can be specified using a
"vfs\=" query parameter.
Or the database can be opened read\-only by using "mode\=ro" as a query
parameter.



# 2\. Backwards Compatibility



In order to maintain full backwards compatibility for legacy applications,
the URI filename capability is disabled by default.
URI filenames can be enabled or disabled using the [SQLITE\_USE\_URI\=1](compile.html#use_uri)
or [SQLITE\_USE\_URI\=0](compile.html#use_uri) compile\-time options.
The compile\-time setting for URI filenames can be changed
at start\-time using the [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_URI](c3ref/c_config_covering_index_scan.html#sqliteconfiguri),1\)
or [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_URI](c3ref/c_config_covering_index_scan.html#sqliteconfiguri),0\) configuration calls.
Regardless of the compile\-time or start\-time settings, URI filenames
can be enabled for individual database connections by including the
[SQLITE\_OPEN\_URI](c3ref/c_open_autoproxy.html) bit in the set of bits passed as the F parameter
to [sqlite3\_open\_v2(N,P,F,V)](c3ref/open.html).




If URI filenames are recognized when the database connection is originally
opened, then URI filenames will also be recognized on [ATTACH](lang_attach.html) statements.
Similarly, if URI filenames are not recognized when the database connection
is first opened, they will not be recognized by [ATTACH](lang_attach.html).




Since SQLite always interprets any filename that does not begin
with "file:"
as an ordinary filename regardless of the URI setting, and because it is
very unusual to have an actual file begin with "file:",
it is safe for most applications to enable URI processing even if URI
filenames are not currently being used.



# 3\. URI Format



According to [RFC 3986](http://tools.ietf.org/html/rfc3986), a URI consists
of a scheme, an authority, a path, a query string, and a fragment. The
scheme is always required. One of either the authority or the path is also
always required. The query string and fragment are optional.




SQLite uses the "file:" URI syntax to identify database files.
SQLite strives to interpret file: URIs in exactly the same way as
popular web\-browsers such as
[Firefox](http://www.mozilla.com/en-US/firefox/new/),
[Chrome](http://www.google.com/chrome/),
[Safari](http://www.apple.com/safari/),
[Internet Explorer](http://windows.microsoft.com/en-US/internet-explorer/products/ie/home), and
[Opera](http://www.opera.com/),
and command\-line programs such as Windows
["cmd start"](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/start)
or
["powershell start"](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-7.3),
or the macOS "open" or Linux "xdg\-open" commands.
A succinct summary of the URI parsing rules follows:



* The scheme of the URI must be "file:". Any other scheme
 results in the input being treated as an ordinary filename.
* The authority may be omitted, may be blank, or may be
 "localhost". Any other authority results in an error.
 Exception: If SQLite is compiled with [SQLITE\_ALLOW\_URI\_AUTHORITY](compile.html#allow_uri_authority)
 then any authority value other than "localhost" is passed through to the
 underlying operating system as a UNC filename.
* The path is optional if the authority is present. If the authority
 is omitted then the path is required.
* The query string is optional. If the query string is present, then
 all query parameters are passed through into the xOpen method of
 the underlying [VFS](vfs.html).
* The fragment is optional. If present, it is ignored.


Zero or more escape sequences of the form "**%*HH***"
(where ***H*** represents any hexadecimal digit) can occur
in the path, query string, or fragment.


A filename that is not a well\-formed URI is interpreted as an
ordinary filename.


URIs are processed as UTF8 text.
The filename argument sqlite3\_open16() is converted from UTF16
native byte order into UTF8 prior to processing.



## 3\.1\. The URI Path


The path component of the URI specifies the disk file that is the
SQLite database to be opened. If the path component is omitted, then
the database is stored in a temporary file that will be automatically
deleted when the database connection closes. If the authority section
is present, then the path is always an absolute pathname. If the
authority section is omitted, then the path is an absolute pathname if it
begins with the "/" character (ASCII code 0x2f) and is a relative
pathname otherwise. On windows, if the absolute path begins with
"**/*X*:/**" where ***X*** is any single ASCII alphabetic
character ("a" through "z" or "A" through "Z") then the "***X:***"
is understood to be the drive letter of the volume containing the file,
not the toplevel directory.



An ordinary filename can usually be converted into an equivalent URI
by the steps shown below. The one exception is that a relative windows
pathname with a drive letter cannot be converted directly into a URI; it must
be changed into an absolute pathname first.


1. Convert all "?" characters into "%3f".
2. Convert all "\#" characters into "%23".
3. On windows only, convert all "\\" characters into "/".
4. Convert all sequences of two or more "/" characters into a
 single "/" character.
5. On windows only, if the filename begins with a drive letter, prepend
 a single "/" character.
6. Prepend the "file:" scheme.


## 3\.2\. Query String


A URI filename can optionally be followed by a query string.
The query string consists of text following the first "?"
character but excluding the optional fragment that begins with
"\#". The query string is divided into key/value pairs.
We usually refer to these key/value pairs as "query parameters".
Key/value pairs are separated by a single "\&" character.
The key comes first and is separated from the value by a single
"\=" character.
Both key and value may contain **%HH** escape sequences.



The text of query parameters is appended to the filename argument of
the xOpen method of the [VFS](vfs.html).
Any %HH escape sequences in the query parameters are resolved prior to
being appended to the xOpen filename.
A single zero\-byte separates the xOpen filename argument from the key of
the first query parameters, each key and value, and each subsequent key
from the prior value.
The list of query parameters appended to the xOpen filename
is terminated by a single zero\-length key.
Note that the value of a query parameter can be an empty string.




## 3\.3\. Recognized Query Parameters



Some query parameters are interpreted by the SQLite core and used to
modify the characteristics of the new connection. All query parameters
are always passed through into the xOpen method of the [VFS](vfs.html) even if
they are previously read and interpreted by the SQLite core.




The following query parameters are recognized by SQLite as of
[version 3\.15\.0](releaselog/3_15_0.html) (2016\-10\-14\).
New query parameters might be added in the future.





**cache\=shared  
cache\=private**
The cache query parameter determines if the new database is opened
using [shared cache mode](sharedcache.html) or with a private cache.




**immutable\=1**
The immutable query parameter is a boolean that signals to
SQLite that the underlying database file is held on read\-only media
and cannot be modified, even by another process with elevated
privileges. SQLite always opens immutable database files
read\-only and it skips all file locking and change detection
on immutable database files. If this query parameter (or
the [SQLITE\_IOCAP\_IMMUTABLE](c3ref/c_iocap_atomic.html) bit in xDeviceCharacteristics)
asserts that a database file is immutable and that file
changes anyhow, then SQLite might return incorrect query
results and/or [SQLITE\_CORRUPT](rescode.html#corrupt) errors.




**mode\=ro  
mode\=rw  
mode\=rwc  
mode\=memory**
The mode query parameter determines if the new database is opened
read\-only, read\-write, read\-write and created if it does not exist, or
that the database is a pure in\-memory database that never interacts with
disk, respectively.




**modeof\=***filename*
When creating a new database file during [sqlite3\_open\_v2()](c3ref/open.html)
on unix systems, SQLite will try to set the permissions of the new
database file to match the existing file "*filename*".




**nolock\=1**
The nolock query parameter is a boolean that disables all calls
to the xLock, xUnlock, and xCheckReservedLock methods of the VFS when true.
The nolock query parameter might be used, for example, when trying to
access a file on a filesystem that does not support file locking.
Caution: If two or more [database connections](c3ref/sqlite3.html) try to interact with
the same SQLite database and one or more of those connections has
enabled "nolock", then database corruption can result. The "nolock"
query parameter should only be used if the application can guarantee
that writes to the database are serialized.




**psow\=0  
psow\=1**
The psow query parameter overrides the [powersafe overwrite](psow.html)
property of the database file being opened. The psow query parameter
works with the default windows and unix [VFSes](vfs.html) but might be a no\-op for
other proprietary or non\-standard VFSes.




**vfs\=***NAME*
The vfs query parameter causes the database connection to be opened
using the [VFS](vfs.html) called *NAME*.
The open attempt fails if *NAME* is not the name of a [VFS](vfs.html) that
is built into SQLite or that has been previously registered using
[sqlite3\_vfs\_register()](c3ref/vfs_find.html).



# 4\. See Also


* [URI filenames in sqlite3\_open()](c3ref/open.html#urifilenamesinsqlite3open)
* [URI filename examples](c3ref/open.html#urifilenameexamples)


*This page last modified on [2023\-01\-02 14:22:42](https://sqlite.org/docsrc/honeypot) UTC* 


