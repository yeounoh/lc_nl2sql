




Enable Or Disable Shared Pager Cache




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Enable Or Disable Shared Pager Cache




> ```
> 
> int sqlite3_enable_shared_cache(int);
> 
> ```



This routine enables or disables the sharing of the database cache
and schema data structures between [connections](../c3ref/sqlite3.html)
to the same database. Sharing is enabled if the argument is true
and disabled if the argument is false.


This interface is omitted if SQLite is compiled with
[\-DSQLITE\_OMIT\_SHARED\_CACHE](../compile.html#omit_shared_cache). The [\-DSQLITE\_OMIT\_SHARED\_CACHE](../compile.html#omit_shared_cache)
compile\-time option is recommended because the
[use of shared cache mode is discouraged](../sharedcache.html#dontuse).


Cache sharing is enabled and disabled for an entire process.
This is a change as of SQLite [version 3\.5\.0](../releaselog/3_5_0.html) (2007\-09\-04\).
In prior versions of SQLite,
sharing was enabled or disabled for each thread separately.


The cache sharing mode set by this interface effects all subsequent
calls to [sqlite3\_open()](../c3ref/open.html), [sqlite3\_open\_v2()](../c3ref/open.html), and [sqlite3\_open16()](../c3ref/open.html).
Existing database connections continue to use the sharing mode
that was in effect at the time they were opened.


This routine returns [SQLITE\_OK](../rescode.html#ok) if shared cache was enabled or disabled
successfully. An [error code](../rescode.html) is returned otherwise.


Shared cache is disabled by default. It is recommended that it stay
that way. In other words, do not use this routine. This interface
continues to be provided for historical compatibility, but its use is
discouraged. Any use of shared cache is discouraged. If shared cache
must be used, it is recommended that shared cache only be enabled for
individual database connections using the [sqlite3\_open\_v2()](../c3ref/open.html) interface
with the [SQLITE\_OPEN\_SHAREDCACHE](../c3ref/c_open_autoproxy.html) flag.


Note: This method is disabled on MacOS X 10\.7 and iOS version 5\.0
and will always return SQLITE\_MISUSE. On those systems,
shared cache mode should be enabled per\-database connection via
[sqlite3\_open\_v2()](../c3ref/open.html) with [SQLITE\_OPEN\_SHAREDCACHE](../c3ref/c_open_autoproxy.html).


This interface is threadsafe on processors where writing a
32\-bit integer is atomic.


See Also: [SQLite Shared\-Cache Mode](../sharedcache.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


