




Obtain Values For URI Parameters




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Obtain Values For URI Parameters




> ```
> 
> const char *sqlite3_uri_parameter(sqlite3_filename z, const char *zParam);
> int sqlite3_uri_boolean(sqlite3_filename z, const char *zParam, int bDefault);
> sqlite3_int64 sqlite3_uri_int64(sqlite3_filename, const char*, sqlite3_int64);
> const char *sqlite3_uri_key(sqlite3_filename z, int N);
> 
> ```



These are utility routines, useful to [custom VFS implementations](../vfs.html),
that check if a database file was a URI that contained a specific query
parameter, and if so obtains the value of that query parameter.


The first parameter to these interfaces (hereafter referred to
as F) must be one of:
* A database filename pointer created by the SQLite core and
passed into the xOpen() method of a VFS implementation, or
* A filename obtained from [sqlite3\_db\_filename()](../c3ref/db_filename.html), or
* A new filename constructed using [sqlite3\_create\_filename()](../c3ref/create_filename.html).


If the F parameter is not one of the above, then the behavior is
undefined and probably undesirable. Older versions of SQLite were
more tolerant of invalid F parameters than newer versions.


If F is a suitable filename (as described in the previous paragraph)
and if P is the name of the query parameter, then
sqlite3\_uri\_parameter(F,P) returns the value of the P
parameter if it exists or a NULL pointer if P does not appear as a
query parameter on F. If P is a query parameter of F and it
has no explicit value, then sqlite3\_uri\_parameter(F,P) returns
a pointer to an empty string.


The sqlite3\_uri\_boolean(F,P,B) routine assumes that P is a boolean
parameter and returns true (1\) or false (0\) according to the value
of P. The sqlite3\_uri\_boolean(F,P,B) routine returns true (1\) if the
value of query parameter P is one of "yes", "true", or "on" in any
case or if the value begins with a non\-zero number. The
sqlite3\_uri\_boolean(F,P,B) routines returns false (0\) if the value of
query parameter P is one of "no", "false", or "off" in any case or
if the value begins with a numeric zero. If P is not a query
parameter on F or if the value of P does not match any of the
above, then sqlite3\_uri\_boolean(F,P,B) returns (B!\=0\).


The sqlite3\_uri\_int64(F,P,D) routine converts the value of P into a
64\-bit signed integer and returns that integer, or D if P does not
exist. If the value of P is something other than an integer, then
zero is returned.


The sqlite3\_uri\_key(F,N) returns a pointer to the name (not
the value) of the N\-th query parameter for filename F, or a NULL
pointer if N is less than zero or greater than the number of query
parameters minus 1\. The N value is zero\-based so N should be 0 to obtain
the name of the first query parameter, 1 for the second parameter, and
so forth.


If F is a NULL pointer, then sqlite3\_uri\_parameter(F,P) returns NULL and
sqlite3\_uri\_boolean(F,P,B) returns B. If F is not a NULL pointer and
is not a database file pathname pointer that the SQLite core passed
into the xOpen VFS method, then the behavior of this routine is undefined
and probably undesirable.


Beginning with SQLite [version 3\.31\.0](../releaselog/3_31_0.html) (2020\-01\-22\) the input F
parameter can also be the name of a rollback journal file or WAL file
in addition to the main database file. Prior to version 3\.31\.0, these
routines would only work if F was the name of the main database file.
When the F parameter is the name of the rollback journal or WAL file,
it has access to all the same query parameters as were found on the
main database file.


See the [URI filename](../uri.html) documentation for additional information.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


