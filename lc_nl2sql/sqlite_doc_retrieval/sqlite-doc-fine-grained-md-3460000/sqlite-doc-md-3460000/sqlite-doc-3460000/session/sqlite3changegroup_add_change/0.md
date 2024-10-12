




Add A Single Change To A Changegroup




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Add A Single Change To A Changegroup


> ```
> int sqlite3changegroup_add_change(
>   sqlite3_changegroup*,
>   sqlite3_changeset_iter*
> );
> 
> ```


This function adds the single change currently indicated by the iterator
passed as the second argument to the changegroup object. The rules for
adding the change are just as described for [sqlite3changegroup\_add()](../session/sqlite3changegroup_add.html).


If the change is successfully added to the changegroup, SQLITE\_OK is
returned. Otherwise, an SQLite error code is returned.


The iterator must point to a valid entry when this function is called.
If it does not, SQLITE\_ERROR is returned and no change is added to the
changegroup. Additionally, the iterator must not have been opened with
the SQLITE\_CHANGESETAPPLY\_INVERT flag. In this case SQLITE\_ERROR is also
returned.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


