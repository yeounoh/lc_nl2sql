




Full\-Featured SQL




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Full\-Featured SQL



Do not be misled by the "Lite" in the name. SQLite has a full\-featured
SQL implementation, including:



* [Tables](lang_createtable.html), [indexes](lang_createindex.html),
 [triggers](lang_createtrigger.html), and [views](lang_createview.html)
 in unlimited quantity
* Up to 32K columns in a table and unlimited rows
* Multi\-column indexes
* Indexes can use [DESC](lang_createindex.html#descidx) and [COLLATE](lang_createindex.html#collidx)
* [Partial indexes](partialindex.html)
* [Indexes On Expressions](expridx.html)
* [Clustered indexes](withoutrowid.html)
* [Covering indexes](queryplanner.html#covidx)
* [CHECK](lang_createtable.html#ckconst), [UNIQUE](lang_createtable.html#uniqueconst), [NOT NULL](lang_createtable.html#notnullconst), and [FOREIGN KEY constraints](foreignkeys.html).
* ACID transactions using [BEGIN](lang_transaction.html), [COMMIT](lang_transaction.html), and [ROLLBACK](lang_transaction.html)
* Nested transactions using [SAVEPOINT](lang_savepoint.html), [RELEASE](lang_savepoint.html), and 
 [ROLLBACK TO](lang_transaction.html)
* [Subqueries](lang_expr.html#subq), including [correlated subqueries](lang_expr.html#cosub)
* Up to 64\-way joins
* LEFT, RIGHT, and FULL OUTER JOINs
* DISTINCT, ORDER BY, GROUP BY, HAVING, LIMIT, and OFFSET
* UNION, UNION ALL, INTERSECT, and EXCEPT
* A rich library of [standard SQL functions](lang_corefunc.html)
* [Aggregate functions](lang_aggfunc.html) including DISTINCT aggregates
* [Window functions](windowfunctions.html)
* [UPDATE](lang_update.html), [DELETE](lang_delete.html), and [INSERT](lang_insert.html) (of course)
* [Common table expressions](lang_with.html) including
 [recursive common table expressions](lang_with.html#recursivecte)
* [Row values](rowvalue.html)
* [UPSERT](lang_upsert.html)
* An advanced [query planner](optoverview.html)
* [Full\-text search](fts5.html)
* [R\-tree indexes](rtree.html)
* [JSON support](json1.html)
* The [IS operator](lang_expr.html#isisnot)
* [Table\-valued functions](vtab.html#tabfunc2)
* [REPLACE INTO](lang_replace.html)
* [VACUUM](lang_vacuum.html)
* [REINDEX](lang_reindex.html)
* The [GLOB](lang_expr.html#glob) operator
* [Hexadecimal integer literals](lang_expr.html#hexint)
* The [ON CONFLICT](lang_conflict.html) clause
* The [INDEXED BY](lang_indexedby.html) clause
* [Virtual tables](vtab.html)
* Multiple databases on the same [database connection](c3ref/sqlite3.html) using
 [ATTACH DATABASE](lang_attach.html)
* The ability to add [application\-defined SQL functions](appfunc.html), including
 aggregate and table\-valued functions.
* [Application\-defined collating functions](c3ref/create_collation.html)



There are many more features not listed above.
SQLite may be small in size and have "Lite" in its name, but it is
not lacking in capability.


*This page last modified on [2022\-05\-10 17:29:14](https://sqlite.org/docsrc/honeypot) UTC* 


