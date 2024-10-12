




Number Of SQL Parameters




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Number Of SQL Parameters




> ```
> 
> int sqlite3_bind_parameter_count(sqlite3_stmt*);
> 
> ```



This routine can be used to find the number of [SQL parameters](../c3ref/bind_blob.html)
in a [prepared statement](../c3ref/stmt.html). SQL parameters are tokens of the
form "?", "?NNN", ":AAA", "$AAA", or "@AAA" that serve as
placeholders for values that are [bound](../c3ref/bind_blob.html)
to the parameters at a later time.


This routine actually returns the index of the largest (rightmost)
parameter. For all forms except ?NNN, this will correspond to the
number of unique parameters. If parameters of the ?NNN form are used,
there may be gaps in the list.


See also: [sqlite3\_bind()](../c3ref/bind_blob.html),
[sqlite3\_bind\_parameter\_name()](../c3ref/bind_parameter_name.html), and
[sqlite3\_bind\_parameter\_index()](../c3ref/bind_parameter_index.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


