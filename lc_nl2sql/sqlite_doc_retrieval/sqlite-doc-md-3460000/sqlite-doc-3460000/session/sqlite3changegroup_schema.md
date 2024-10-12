




Add a Schema to a Changegroup




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Add a Schema to a Changegroup


> ```
> int sqlite3changegroup_schema(sqlite3_changegroup*, sqlite3*, const char *zDb);
> 
> ```


This method may be used to optionally enforce the rule that the changesets
added to the changegroup handle must match the schema of database zDb
("main", "temp", or the name of an attached database). If
sqlite3changegroup\_add() is called to add a changeset that is not compatible
with the configured schema, SQLITE\_SCHEMA is returned and the changegroup
object is left in an undefined state.


A changeset schema is considered compatible with the database schema in
the same way as for sqlite3changeset\_apply(). Specifically, for each
table in the changeset, there exists a database table with:


* The name identified by the changeset, and
 * at least as many columns as recorded in the changeset, and
 * the primary key columns in the same position as recorded in 
 the changeset.



The output of the changegroup object always has the same schema as the
database nominated using this function. In cases where changesets passed
to sqlite3changegroup\_add() have fewer columns than the corresponding table
in the database schema, these are filled in using the default column
values from the database schema. This makes it possible to combined 
changesets that have different numbers of columns for a single table
within a changegroup, provided that they are otherwise compatible.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


