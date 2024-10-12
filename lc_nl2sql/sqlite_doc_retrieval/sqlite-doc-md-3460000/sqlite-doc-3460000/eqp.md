




EXPLAIN QUERY PLAN




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










EXPLAIN QUERY PLAN


►
Table Of Contents
[1\. The EXPLAIN QUERY PLAN Command](#the_explain_query_plan_command)
[1\.1\. Table and Index Scans](#table_and_index_scans)
[1\.2\. Temporary Sorting B\-Trees](#temporary_sorting_b_trees)
[1\.3\. Subqueries](#subqueries)
[1\.4\. Compound Queries](#compound_queries)




# 1\. The EXPLAIN QUERY PLAN Command



**Warning:** The data returned by the EXPLAIN QUERY PLAN command is 
intended for interactive debugging only. The output format may change
between SQLite releases. Applications should not depend on the output
format of the EXPLAIN QUERY PLAN command.




**Alert:** As warned above, the EXPLAIN QUERY PLAN output format did
change substantially with the version 3\.24\.0 release (2018\-06\-04\).
Additional minor changes occurred in version 3\.36\.0 (2021\-06\-18\).
Further changes are possible in subsequent releases.




The [EXPLAIN QUERY PLAN](lang_explain.html) SQL command is used to obtain a high\-level
description of the strategy or plan that SQLite uses to implement a specific
SQL query. Most significantly, EXPLAIN QUERY PLAN reports on the way in 
which the query uses database indices. This document is a guide to
understanding and interpreting the EXPLAIN QUERY PLAN output. Background
information is available separately:



* A primer on [How SQLite Works](howitworks.html).
* Notes on the [query optimizer](optoverview.html).
* How [indexing](queryplanner.html) works.
* The [next generation query planner](queryplanner-ng.html).


A query plan is represented as a tree.
In raw form, as returned by [sqlite3\_step()](c3ref/step.html), each node of the tree
consists of four fields: An integer node id, an integer parent id,
an auxiliary integer field that is not currently used, and a description
of the node.
The entire tree is therefore a table with four columns and zero or more
rows.
The [command\-line shell](cli.html) will usually intercept this table and renders
it as an ASCII\-art graph for more convenient viewing. To disable the
shells automatic graph rendering and to display EXPLAIN QUERY PLAN
output in its tabular format, run the command ".explain off" to set
the "EXPLAIN formatting mode" to off. To restore automatic graph rendering,
run ".explain auto". You can see the current "EXPLAIN formatting mode" 
setting using the ".show" command.



One can also set the [CLI](cli.html) into automatic EXPLAIN QUERY PLAN mode
using the ".eqp on" command:




```
sqlite> .eqp on

```

 In automatic EXPLAIN QUERY PLAN mode, the shell automatically runs
a separate EXPLAIN QUERY PLAN query for each statement you enter and
displays the result before actually running the query. Use the
".eqp off" command to turn automatic EXPLAIN QUERY PLAN mode back off.



EXPLAIN QUERY PLAN is most useful on a SELECT statement,
but may also appear with other statements that read data from database
tables (e.g. UPDATE, DELETE, INSERT INTO ... SELECT).



## 1\.1\. Table and Index Scans



 When processing a SELECT (or other) statement, SQLite may retrieve data from
 database tables in a variety of ways. It may scan through all the records in
 a table (a full\-table scan), scan a contiguous subset of the records in a
 table based on the rowid index, scan a contiguous subset of the entries in a
 database [index](lang_createtable.html), or use a combination of the above strategies
 in a single scan. The various ways in which SQLite may retrieve data from a
 table or index are described in detail [here](queryplanner.html#searching).




 For each table read by the query, the output of EXPLAIN QUERY 
 PLAN includes a record for which the value in the "detail" column begins
 with either "SCAN" or "SEARCH". "SCAN" is used for a full\-table scan,
 including cases where SQLite iterates through all records in a table
 in an order defined by an index. "SEARCH" indicates that only a subset of 
 the table rows are visited. Each SCAN or SEARCH record includes the
 following information:



* The name of the table, view, or subquery that data is read from.
* Whether or not an index or [automatic index](optoverview.html#autoindex) is used.
* Whether or not the [covering index](queryplanner.html#covidx) optimization applies.
* Which terms of the WHERE clause are used for indexing.



 For example, the following EXPLAIN QUERY PLAN command operates on a SELECT
 statement that is implemented by performing a full\-table scan on table t1:



```
sqlite> EXPLAIN QUERY PLAN SELECT a, b FROM t1 WHERE a=1;
QUERY PLAN
`--SCAN t1

```


 The example above shows
 SQLite picking full\-table scan will visit all rows in the table.
 If the query were able to use an index, then the 
 SCAN/SEARCH record would include the name of the index and, for a
 SEARCH record, an indication of how the subset of rows visited is
 identified. For example:



```
sqlite> CREATE INDEX i1 ON t1(a);
sqlite> EXPLAIN QUERY PLAN SELECT a, b FROM t1 WHERE a=1;
QUERY PLAN
`--SEARCH t1 USING INDEX i1 (a=?)

```


 The previous example, SQLite uses index "i1" to optimize
 a WHERE clause term of the form (a\=?) \- in this case "a\=1".
 The previous example could not use a [covering index](queryplanner.html#covidx), but the following
 example can, and that fact is reflected in the output:



```
sqlite> CREATE INDEX i2 ON t1(a, b);
sqlite> EXPLAIN QUERY PLAN SELECT a, b FROM t1 WHERE a=1; 
QUERY PLAN
`--SEARCH t1 USING COVERING INDEX i2 (a=?)

```


 All joins in SQLite are [implemented using nested scans](optoverview.html#joins). When a
 SELECT query that features a join is analyzed using EXPLAIN QUERY PLAN, one
 SCAN or SEARCH record is output for each nested loop. For example:



```
sqlite> EXPLAIN QUERY PLAN SELECT t1.*, t2.* FROM t1, t2 WHERE t1.a=1 AND t1.b>2;
QUERY PLAN
|--SEARCH t1 USING INDEX i2 (a=? AND b>?)
`--SCAN t2

```


 The order of the entries indicates the nesting order. In
 this case, the scan of table t1 using index i2 is the outer loop (since it
 appears first)
 and the full\-table scan of table t2 is the inner loop (since it appears
 last).
 In the following example, the positions of t1 and t2 in the FROM 
 clause of the SELECT are reversed. The query strategy remains the same.
 The output from EXPLAIN QUERY PLAN shows how the query is actually
 evaluated, not how it is specified in the SQL statement.



```
sqlite> EXPLAIN QUERY PLAN SELECT t1.*, t2.* FROM t2, t1 WHERE t1.a=1 AND t1.b>2;
QUERY PLAN
|--SEARCH t1 USING INDEX i2 (a=? AND b>?)
`--SCAN t2

```



 If the WHERE clause of a query contains an OR expression, then SQLite might
 use the ["OR by union"](queryplanner.html#or_in_where) strategy (also known as the
 [OR optimization](optoverview.html#or_opt)). In this case there will be single top\-level record
 for the search, with two sub\-records, one for each index:



```
sqlite> CREATE INDEX i3 ON t1(b);
sqlite> EXPLAIN QUERY PLAN SELECT * FROM t1 WHERE a=1 OR b=2;
QUERY PLAN
`--MULTI-INDEX OR
   |--SEARCH t1 USING COVERING INDEX i2 (a=?)
   `--SEARCH t1 USING INDEX i3 (b=?)

```

## 1\.2\. Temporary Sorting B\-Trees



 If a SELECT query contains an ORDER BY, GROUP BY or DISTINCT clause, 
 SQLite may need to use a temporary b\-tree structure to sort the output
 rows. Or, it might [use an index](queryplanner.html#sorting). Using an index is 
 almost always much more efficient than performing a sort.
 If a temporary b\-tree is required, a record is added to the EXPLAIN
 QUERY PLAN output with the "detail" field set to a string value of
 the form "USE TEMP B\-TREE FOR xxx", where xxx is one of "ORDER BY",
 "GROUP BY" or "DISTINCT". For example:




```
sqlite> EXPLAIN QUERY PLAN SELECT c, d FROM t2 ORDER BY c;
QUERY PLAN
|--SCAN t2
`--USE TEMP B-TREE FOR ORDER BY

```


 In this case using the temporary b\-tree can be avoided by creating an index
 on t2(c), as follows:




```
sqlite> CREATE INDEX i4 ON t2(c);
sqlite> EXPLAIN QUERY PLAN SELECT c, d FROM t2 ORDER BY c; 
QUERY PLAN
`--SCAN t2 USING INDEX i4

```

## 1\.3\. Subqueries



 In all the examples above, there has only been a single SELECT statement.
 If a query contains sub\-selects, those are shown as being children of
 the outer SELECT. For example:




```
sqlite> EXPLAIN QUERY PLAN SELECT (SELECT b FROM t1 WHERE a=0), (SELECT a FROM t1 WHERE b=t2.c) FROM t2;
|--SCAN TABLE t2 USING COVERING INDEX i4
|--SCALAR SUBQUERY
|  `--SEARCH t1 USING COVERING INDEX i2 (a=?)
`--CORRELATED SCALAR SUBQUERY
   `--SEARCH t1 USING INDEX i3 (b=?)

```


 The example above contains two "SCALAR" subqueries. The subqueries
 are SCALAR in the sense that they return a single value \- a one\-row,
 one\-column table. If the actual query returns more than that, then
 only the first column of the first row is used.



 The first subquery above is constant with respect to the outer query.
 The value for the first subquery can be computed once and then reused
 for each row of the outer SELECT. The second subquery, however, is
 "CORRELATED". The value of the second subquery changes depending
 on values in the current row of the outer query. Hence, the second
 subquery must be run once for each output row in the outer SELECT.




 Unless the [flattening optimization](optoverview.html#flattening) is applied, if a subquery appears in
 the FROM clause of a SELECT statement, SQLite can either run the subquery and
 stores the results in a temporary table, or it can run the subquery as a
 co\-routine. The following query is an example of the latter. The subquery
 is run by a co\-routine. The outer query blocks whenever it needs another
 row of input from the subquery. Control switches to the co\-routine which
 produces the desired output row, then control switches back to the main
 routine which continues processing. 




```
sqlite> EXPLAIN QUERY PLAN SELECT count(*)
      > FROM (SELECT max(b) AS x FROM t1 GROUP BY a) AS qqq
      > GROUP BY x;
QUERY PLAN
|--CO-ROUTINE qqq
|  `--SCAN t1 USING COVERING INDEX i2
|--SCAN qqqq
`--USE TEMP B-TREE FOR GROUP BY

```


 
 If the [flattening optimization](optoverview.html#flattening) is used on a subquery in the FROM clause
 of a SELECT statement, that effectively merges the subquery into the outer
 query. The output of EXPLAIN QUERY PLAN reflects this, as in the following
 example:




```
sqlite> EXPLAIN QUERY PLAN SELECT * FROM (SELECT * FROM t2 WHERE c=1) AS t3, t1;
QUERY PLAN
|--SEARCH t2 USING INDEX i4 (c=?)
`--SCAN t1

```



 If the content of a subquery might need to be visited more than once, then
 the use of a co\-routine is undesirable, as the co\-routine would then have to
 compute the data more than once. And if the subquery cannot be flattened,
 that means the subquery must be manifested into a transient table.




```
sqlite> SELECT * FROM
      >   (SELECT * FROM t1 WHERE a=1 ORDER BY b LIMIT 2) AS x,
      >   (SELECT * FROM t2 WHERE c=1 ORDER BY d LIMIT 2) AS y;
QUERY PLAN
|--MATERIALIZE x
|  `--SEARCH t1 USING COVERING INDEX i2 (a=?)
|--MATERIALIZE y
|  |--SEARCH t2 USING INDEX i4 (c=?)
|  `--USE TEMP B-TREE FOR ORDER BY
|--SCAN x
`--SCAN y

```

## 1\.4\. Compound Queries



 Each component query of a [compound query](lang_select.html#compound) (UNION, UNION ALL, EXCEPT or 
 INTERSECT) is assigned computed separately and is given its own line in
 the EXPLAIN QUERY PLAN output.




```
sqlite> EXPLAIN QUERY PLAN SELECT a FROM t1 UNION SELECT c FROM t2;
QUERY PLAN
`--COMPOUND QUERY
   |--LEFT-MOST SUBQUERY
   |  `--SCAN t1 USING COVERING INDEX i1
   `--UNION USING TEMP B-TREE
      `--SCAN t2 USING COVERING INDEX i4

```


 The "USING TEMP B\-TREE" clause in the above output indicates that a 
 temporary b\-tree structure is used to implement the UNION of the results
 of the two sub\-selects. An alternative method of computing a compound
 is to run each subquery as a co\-routine, arrange for their outputs to
 appear in sorted order, and merge the results together. When the query
 planner chooses this latter approach, the EXPLAIN QUERY PLAN output
 looks like this:




```
sqlite> EXPLAIN QUERY PLAN SELECT a FROM t1 EXCEPT SELECT d FROM t2 ORDER BY 1;
QUERY PLAN
`--MERGE (EXCEPT)
   |--LEFT
   |  `--SCAN t1 USING COVERING INDEX i1
   `--RIGHT
      |--SCAN t2
      `--USE TEMP B-TREE FOR ORDER BY

```

*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


