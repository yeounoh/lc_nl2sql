




Online Backup Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Online Backup Object




> ```
> 
> typedef struct sqlite3_backup sqlite3_backup;
> 
> ```



The sqlite3\_backup object records state information about an ongoing
online backup operation. The sqlite3\_backup object is created by
a call to [sqlite3\_backup\_init()](../c3ref/backup_finish.html#sqlite3backupinit) and is destroyed by a call to
[sqlite3\_backup\_finish()](../c3ref/backup_finish.html#sqlite3backupfinish).


See Also: [Using the SQLite Online Backup API](../backup.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


