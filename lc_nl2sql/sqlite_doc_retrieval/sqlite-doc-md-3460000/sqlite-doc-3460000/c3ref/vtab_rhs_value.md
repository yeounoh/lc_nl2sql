




Constraint values in xBestIndex()




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Constraint values in xBestIndex()




> ```
> 
> int sqlite3_vtab_rhs_value(sqlite3_index_info*, int, sqlite3_value **ppVal);
> 
> ```



This API may only be used from within the [xBestIndex method](../vtab.html#xbestindex)
of a [virtual table](../vtab.html) implementation. The result of calling this interface
from outside of an xBestIndex method are undefined and probably harmful.


When the sqlite3\_vtab\_rhs\_value(P,J,V) interface is invoked from within
the [xBestIndex](../vtab.html#xbestindex) method of a [virtual table](../vtab.html) implementation, with P being
a copy of the [sqlite3\_index\_info](../c3ref/index_info.html) object pointer passed into xBestIndex and
J being a 0\-based index into P\-\>aConstraint\[], then this routine
attempts to set \*V to the value of the right\-hand operand of
that constraint if the right\-hand operand is known. If the
right\-hand operand is not known, then \*V is set to a NULL pointer.
The sqlite3\_vtab\_rhs\_value(P,J,V) interface returns SQLITE\_OK if
and only if \*V is set to a value. The sqlite3\_vtab\_rhs\_value(P,J,V)
inteface returns SQLITE\_NOTFOUND if the right\-hand side of the J\-th
constraint is not available. The sqlite3\_vtab\_rhs\_value() interface
can return an result code other than SQLITE\_OK or SQLITE\_NOTFOUND if
something goes wrong.


The sqlite3\_vtab\_rhs\_value() interface is usually only successful if
the right\-hand operand of a constraint is a literal value in the original
SQL statement. If the right\-hand operand is an expression or a reference
to some other column or a [host parameter](../c3ref/bind_blob.html), then sqlite3\_vtab\_rhs\_value()
will probably return [SQLITE\_NOTFOUND](../rescode.html#notfound).


Some constraints, such as [SQLITE\_INDEX\_CONSTRAINT\_ISNULL](../c3ref/c_index_constraint_eq.html) and
[SQLITE\_INDEX\_CONSTRAINT\_ISNOTNULL](../c3ref/c_index_constraint_eq.html), have no right\-hand operand. For such
constraints, sqlite3\_vtab\_rhs\_value() always returns SQLITE\_NOTFOUND.


The [sqlite3\_value](../c3ref/value.html) object returned in \*V is a protected sqlite3\_value
and remains valid for the duration of the xBestIndex method call.
When xBestIndex returns, the sqlite3\_value object returned by
sqlite3\_vtab\_rhs\_value() is automatically deallocated.


The "\_rhs\_" in the name of this routine is an abbreviation for
"Right\-Hand Side".


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


