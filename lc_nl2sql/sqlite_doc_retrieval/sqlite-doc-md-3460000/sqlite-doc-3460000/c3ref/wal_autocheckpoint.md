




Configure an auto\-checkpoint




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Configure an auto\-checkpoint




> ```
> 
> int sqlite3_wal_autocheckpoint(sqlite3 *db, int N);
> 
> ```



The [sqlite3\_wal\_autocheckpoint(D,N)](../c3ref/wal_autocheckpoint.html) is a wrapper around
[sqlite3\_wal\_hook()](../c3ref/wal_hook.html) that causes any database on [database connection](../c3ref/sqlite3.html) D
to automatically [checkpoint](../wal.html#ckpt)
after committing a transaction if there are N or
more frames in the [write\-ahead log](../wal.html) file. Passing zero or
a negative value as the nFrame parameter disables automatic
checkpoints entirely.


The callback registered by this function replaces any existing callback
registered using [sqlite3\_wal\_hook()](../c3ref/wal_hook.html). Likewise, registering a callback
using [sqlite3\_wal\_hook()](../c3ref/wal_hook.html) disables the automatic checkpoint mechanism
configured by this function.


The [wal\_autocheckpoint pragma](../pragma.html#pragma_wal_autocheckpoint) can be used to invoke this interface
from SQL.


Checkpoints initiated by this mechanism are
[PASSIVE](../c3ref/wal_checkpoint_v2.html).


Every new [database connection](../c3ref/sqlite3.html) defaults to having the auto\-checkpoint
enabled with a threshold of 1000 or [SQLITE\_DEFAULT\_WAL\_AUTOCHECKPOINT](../compile.html#default_wal_autocheckpoint)
pages. The use of this interface
is only necessary if the default setting is found to be suboptimal
for a particular application.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


