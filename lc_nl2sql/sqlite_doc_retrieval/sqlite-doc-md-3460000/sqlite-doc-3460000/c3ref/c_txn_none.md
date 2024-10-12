




Allowed return values from sqlite3\_txn\_state()




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Allowed return values from sqlite3\_txn\_state()




> ```
> 
> #define SQLITE_TXN_NONE  0
> #define SQLITE_TXN_READ  1
> #define SQLITE_TXN_WRITE 2
> 
> ```



These constants define the current transaction state of a database file.
The [sqlite3\_txn\_state(D,S)](../c3ref/txn_state.html) interface returns one of these
constants in order to describe the transaction state of schema S
in [database connection](../c3ref/sqlite3.html) D.




SQLITE\_TXN\_NONE
The SQLITE\_TXN\_NONE state means that no transaction is currently
pending.



SQLITE\_TXN\_READ
The SQLITE\_TXN\_READ state means that the database is currently
in a read transaction. Content has been read from the database file
but nothing in the database file has changed. The transaction state
will advanced to SQLITE\_TXN\_WRITE if any changes occur and there are
no other conflicting concurrent write transactions. The transaction
state will revert to SQLITE\_TXN\_NONE following a [ROLLBACK](../lang_transaction.html) or
[COMMIT](../lang_transaction.html).



SQLITE\_TXN\_WRITE
The SQLITE\_TXN\_WRITE state means that the database is currently
in a write transaction. Content has been written to the database file
but has not yet committed. The transaction state will change to
to SQLITE\_TXN\_NONE at the next [ROLLBACK](../lang_transaction.html) or [COMMIT](../lang_transaction.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


