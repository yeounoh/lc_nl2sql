




CREATE INDEX




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










CREATE INDEX


# 1\. Syntax


**[create\-index\-stmt:](syntax/create-index-stmt.html)**
hide








CREATE

UNIQUE

INDEX










IF



NOT



EXISTS








schema\-name



.



index\-name



ON



table\-name



(



indexed\-column



)

,







WHERE



expr












**[expr:](syntax/expr.html)**
show








literal\-value




bind\-parameter






schema\-name



.



table\-name



.



column\-name












unary\-operator



expr






expr



binary\-operator



expr






function\-name



(



function\-arguments



)



filter\-clause





over\-clause












(



expr



)






,




CAST



(



expr



AS



type\-name



)






expr



COLLATE



collation\-name






expr



NOT



LIKE

GLOB

REGEXP

MATCH

expr

expr



ESCAPE



expr

































expr



ISNULL






NOTNULL

NOT



NULL












expr



IS



NOT





DISTINCT



FROM



expr








expr



NOT



BETWEEN



expr



AND



expr







expr



NOT



IN



(



select\-stmt



)








expr




,




schema\-name



.



table\-function



(



expr



)




table\-name






,










NOT



EXISTS



(



select\-stmt



)










CASE



expr



WHEN



expr



THEN



expr



ELSE



expr



END











raise\-function







**[filter\-clause:](syntax/filter-clause.html)**
show








FILTER



(



WHERE



expr



)






**[function\-arguments:](syntax/function-arguments.html)**
show










DISTINCT







expr








,





\*











ORDER



BY



ordering\-term

,







**[ordering\-term:](syntax/ordering-term.html)**
show








expr



COLLATE



collation\-name








DESC



ASC









NULLS



FIRST



NULLS



LAST










**[literal\-value:](syntax/literal-value.html)**
show








CURRENT\_TIMESTAMP






numeric\-literal




string\-literal






blob\-literal






NULL






TRUE






FALSE






CURRENT\_TIME






CURRENT\_DATE








**[over\-clause:](syntax/over-clause.html)**
show








OVER



window\-name



(



base\-window\-name

PARTITION



BY



expr

,













ORDER



BY



ordering\-term

,











frame\-spec



)



















**[frame\-spec:](syntax/frame-spec.html)**
show








GROUPS




BETWEEN



UNBOUNDED



PRECEDING



AND



UNBOUNDED



FOLLOWING




RANGE






ROWS






UNBOUNDED



PRECEDING




expr



PRECEDING






CURRENT



ROW






expr



PRECEDING






CURRENT



ROW






expr



FOLLOWING








expr



PRECEDING




CURRENT



ROW






expr



FOLLOWING






EXCLUDE



CURRENT



ROW




EXCLUDE



GROUP




EXCLUDE



TIES




EXCLUDE



NO



OTHERS





















**[ordering\-term:](syntax/ordering-term.html)**
show








expr



COLLATE



collation\-name








DESC



ASC









NULLS



FIRST



NULLS



LAST










**[raise\-function:](syntax/raise-function.html)**
show








RAISE



(



ROLLBACK



,



error\-message



)






IGNORE




ABORT




FAIL










**[select\-stmt:](syntax/select-stmt.html)**
show









WITH

RECURSIVE





common\-table\-expression






,













SELECT



DISTINCT



result\-column

,







ALL






FROM



table\-or\-subquery

join\-clause

,

















WHERE



expr










GROUP



BY



expr



HAVING



expr

,


















WINDOW



window\-name



AS



window\-defn

,



















VALUES



(



expr



)




,

,









compound\-operator





select\-core

ORDER



BY

LIMIT



expr



ordering\-term

,

















OFFSET



expr



,



expr




















**[common\-table\-expression:](syntax/common-table-expression.html)**
show








table\-name





(





column\-name



)



AS

NOT

MATERIALIZED


(



select\-stmt



)




,






















**[compound\-operator:](syntax/compound-operator.html)**
show










UNION

UNION

INTERSECT

EXCEPT



ALL





















**[join\-clause:](syntax/join-clause.html)**
show








table\-or\-subquery



join\-operator



table\-or\-subquery



join\-constraint











**[join\-constraint:](syntax/join-constraint.html)**
show








USING



(



column\-name



)






,






ON



expr









**[join\-operator:](syntax/join-operator.html)**
show








NATURAL





LEFT



OUTER





JOIN




,












RIGHT





FULL




INNER






CROSS







**[ordering\-term:](syntax/ordering-term.html)**
show








expr



COLLATE



collation\-name








DESC



ASC









NULLS



FIRST



NULLS



LAST









**[result\-column:](syntax/result-column.html)**
show








expr



AS



column\-alias














\*






table\-name



.



\*






**[table\-or\-subquery:](syntax/table-or-subquery.html)**
show








schema\-name



.



table\-name



AS



table\-alias






INDEXED



BY



index\-name

NOT



INDEXED









table\-function\-name



(



expr



)



,












AS



table\-alias











(



select\-stmt



)









(



table\-or\-subquery



)






,






join\-clause




**[window\-defn:](syntax/window-defn.html)**
show








(



base\-window\-name

PARTITION



BY



expr

,













ORDER



BY



ordering\-term

,











frame\-spec



)
















**[frame\-spec:](syntax/frame-spec.html)**
show








GROUPS




BETWEEN



UNBOUNDED



PRECEDING



AND



UNBOUNDED



FOLLOWING




RANGE






ROWS






UNBOUNDED



PRECEDING




expr



PRECEDING






CURRENT



ROW






expr



PRECEDING






CURRENT



ROW






expr



FOLLOWING








expr



PRECEDING




CURRENT



ROW






expr



FOLLOWING






EXCLUDE



CURRENT



ROW




EXCLUDE



GROUP




EXCLUDE



TIES




EXCLUDE



NO



OTHERS























**[type\-name:](syntax/type-name.html)**
show








name



(



signed\-number



,



signed\-number



)






(



signed\-number



)











**[signed\-number:](syntax/signed-number.html)**
show








\+



numeric\-literal






\-









**[indexed\-column:](syntax/indexed-column.html)**
show








column\-name



COLLATE



collation\-name





DESC








expr









ASC









The CREATE INDEX command consists of the keywords "CREATE INDEX" followed
by the name of the new index, the keyword "ON", the name of a previously
created table that is to be indexed, and a parenthesized list of table column
names and/or expressions that are used for the index key.
If the optional WHERE clause is included, then the index is a "[partial index](partialindex.html)".



If the optional IF NOT EXISTS clause is present and another index
with the same name already exists, then this command becomes a no\-op.


There are no arbitrary limits on the number of indices that can be
attached to a single table. The number of columns in an index is 
limited to the value set by
[sqlite3\_limit](c3ref/limit.html)([SQLITE\_LIMIT\_COLUMN](c3ref/c_limit_attached.html#sqlitelimitcolumn),...).


Indexes are removed with the [DROP INDEX](lang_dropindex.html) command.



## 1\.1\. Unique Indexes


If the UNIQUE keyword appears between CREATE and INDEX then duplicate
index entries are not allowed. Any attempt to insert a duplicate entry
will result in an error.


For the purposes of unique indices, all NULL values
are considered different from all other NULL values and are thus unique.
This is one of the two possible interpretations of the SQL\-92 standard
(the language in the standard is ambiguous). The interpretation used
by SQLite is the same and is the interpretation
followed by PostgreSQL, MySQL, Firebird, and Oracle. Informix and
Microsoft SQL Server follow the other interpretation of the standard, which
is that all NULL values are equal to one another.



## 1\.2\. Indexes on Expressions


Expressions in an index may not reference other tables
and may not use subqueries nor functions whose result might
change (ex: [random()](lang_corefunc.html#random) or [sqlite\_version()](lang_corefunc.html#sqlite_version)).
Expressions in an index may only refer to columns in the table
that is being indexed.
Indexes on expression will not work with versions of SQLite prior
to [version 3\.9\.0](releaselog/3_9_0.html) (2015\-10\-14\).
See the [Indexes On Expressions](expridx.html) document for additional information
about using general expressions in CREATE INDEX statements.




## 1\.3\. Descending Indexes


Each column name or expression can be followed by one
of the "ASC" or "DESC" keywords to indicate sort order.
The sort order may or may not be ignored depending
on the database file format, and in particular the [schema format number](fileformat2.html#schemaformat).
The "legacy" schema format (1\) ignores index
sort order. The descending index schema format (4\) takes index sort order
into account. Only versions of SQLite 3\.3\.0 (2006\-01\-11\)
and later are able to understand
the descending index format. For compatibility, version of SQLite between 3\.3\.0
and 3\.7\.9 use the legacy schema format by default. The newer schema format is
used by default in version 3\.7\.10 (2012\-01\-16\) and later.
The [legacy\_file\_format pragma](pragma.html#pragma_legacy_file_format) can be used to change set the specific
behavior for any version of SQLite.


## 1\.4\. NULLS FIRST and NULLS LAST


The NULLS FIRST and NULLS LAST predicates are not supported
for indexes. For [sorting purposes](datatype3.html#sortorder), SQLite considers NULL values 
to be smaller than all other values. Hence NULL values always appear at
the beginning of an ASC index and at the end of a DESC index.



## 1\.5\. Collations


The COLLATE clause optionally following each column name
or expression defines a
collating sequence used for text entries in that column.
The default collating
sequence is the collating sequence defined for that column in the
[CREATE TABLE](lang_createtable.html) statement. Or if no collating sequence is otherwise defined,
the built\-in BINARY collating sequence is used.


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


