




Set a table filter on a Session Object.




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Set a table filter on a Session Object.


> ```
> void sqlite3session_table_filter(
>   sqlite3_session *pSession,      /* Session object */
>   int(*xFilter)(
>     void *pCtx,                   /* Copy of third arg to _filter_table() */
>     const char *zTab              /* Table name */
>   ),
>   void *pCtx                      /* First argument passed to xFilter */
> );
> 
> ```


The second argument (xFilter) is the "filter callback". For changes to rows 
in tables that are not attached to the Session object, the filter is called
to determine whether changes to the table's rows should be tracked or not. 
If xFilter returns 0, changes are not tracked. Note that once a table is 
attached, xFilter will not be called again.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


