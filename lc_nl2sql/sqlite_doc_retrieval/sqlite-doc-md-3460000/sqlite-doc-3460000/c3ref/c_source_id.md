




Compile\-Time Library Version Numbers




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Compile\-Time Library Version Numbers




> ```
> 
> #define SQLITE_VERSION        "3.46.0"
> #define SQLITE_VERSION_NUMBER 3046000
> #define SQLITE_SOURCE_ID      "2024-05-23 13:25:27 96c92aba00c8375bc32fafcdf12429c58bd8aabfcadab6683e35bbb9cdebf19e"
> 
> ```



The [SQLITE\_VERSION](../c3ref/c_source_id.html) C preprocessor macro in the sqlite3\.h header
evaluates to a string literal that is the SQLite version in the
format "X.Y.Z" where X is the major version number (always 3 for
SQLite3\) and Y is the minor version number and Z is the release number.
The [SQLITE\_VERSION\_NUMBER](../c3ref/c_source_id.html) C preprocessor macro resolves to an integer
with the value (X\*1000000 \+ Y\*1000 \+ Z) where X, Y, and Z are the same
numbers used in [SQLITE\_VERSION](../c3ref/c_source_id.html).
The SQLITE\_VERSION\_NUMBER for any given release of SQLite will also
be larger than the release from which it is derived. Either Y will
be held constant and Z will be incremented or else Y will be incremented
and Z will be reset to zero.


Since [version 3\.6\.18](../releaselog/3_6_18.html) (2009\-09\-11\),
SQLite source code has been stored in the
[Fossil configuration management
system](http://www.fossil-scm.org/). The SQLITE\_SOURCE\_ID macro evaluates to
a string which identifies a particular check\-in of SQLite
within its configuration management system. The SQLITE\_SOURCE\_ID
string contains the date and time of the check\-in (UTC) and a SHA1
or SHA3\-256 hash of the entire source tree. If the source code has
been edited in any way since it was last checked in, then the last
four hexadecimal digits of the hash may be modified.


See also: [sqlite3\_libversion()](../c3ref/libversion.html),
[sqlite3\_libversion\_number()](../c3ref/libversion.html), [sqlite3\_sourceid()](../c3ref/libversion.html),
[sqlite\_version()](../lang_corefunc.html#sqlite_version) and [sqlite\_source\_id()](../lang_corefunc.html#sqlite_source_id).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


