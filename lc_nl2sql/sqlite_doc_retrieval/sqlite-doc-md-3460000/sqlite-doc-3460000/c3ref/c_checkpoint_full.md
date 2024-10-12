




Checkpoint Mode Values




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Checkpoint Mode Values




> ```
> 
> #define SQLITE_CHECKPOINT_PASSIVE  0  /* Do as much as possible w/o blocking */
> #define SQLITE_CHECKPOINT_FULL     1  /* Wait for writers, then checkpoint */
> #define SQLITE_CHECKPOINT_RESTART  2  /* Like FULL but wait for readers */
> #define SQLITE_CHECKPOINT_TRUNCATE 3  /* Like RESTART but also truncate WAL */
> 
> ```



These constants define all valid values for the "checkpoint mode" passed
as the third parameter to the [sqlite3\_wal\_checkpoint\_v2()](../c3ref/wal_checkpoint_v2.html) interface.
See the [sqlite3\_wal\_checkpoint\_v2()](../c3ref/wal_checkpoint_v2.html) documentation for details on the
meaning of each of these checkpoint modes.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


