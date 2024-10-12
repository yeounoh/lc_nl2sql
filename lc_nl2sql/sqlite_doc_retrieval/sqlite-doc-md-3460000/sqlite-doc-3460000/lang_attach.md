




ATTACH DATABASE




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










ATTACH DATABASE


# 1\. Overview


**[attach\-stmt:](syntax/attach-stmt.html)**
hide








ATTACH





DATABASE



expr



AS



schema\-name








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










 The ATTACH DATABASE statement adds another database 
file to the current [database connection](c3ref/sqlite3.html). 
Database files that were previously attached can be removed using
the [DETACH DATABASE](lang_detach.html) command.



# 2\. Details


The filename for the database to be attached is the value of
the expression that occurs before the AS keyword.
The filename of the database follows the same semantics as the
filename argument to [sqlite3\_open()](c3ref/open.html) and [sqlite3\_open\_v2()](c3ref/open.html); the
special name "[:memory:](inmemorydb.html)" results in an [in\-memory database](inmemorydb.html) and an
empty string results in a new temporary database.
The filename argument can be a [URI filename](uri.html) if URI filename processing
is enabled on the database connection. The default behavior is for
URI filenames to be disabled, however that might change in a future release
of SQLite, so application developers are advised to plan accordingly.



The name that occurs after the AS keyword is the name of the database
used internally by SQLite.
The schema\-names 'main' and 
'temp' refer to the main database and the database used for 
temporary tables. The main and temp databases cannot be attached or
detached.


 Tables in an attached database can be referred to using the syntax 
*schema\-name.table\-name*. If the name of the table is unique
across all attached databases and the main and temp databases, then the
*schema\-name* prefix is not required. If two or more tables in
different databases have the same name and the 
*schema\-name* prefix is not used on a table reference, then the
table chosen is the one in the database that was least recently attached.



Transactions involving multiple attached databases are atomic,
assuming that the main database is not "[:memory:](inmemorydb.html)" and the 
[journal\_mode](pragma.html#pragma_journal_mode) is not [WAL](wal.html). If the main
database is ":memory:" or if the journal\_mode is WAL, then 
transactions continue to be atomic within each individual
database file. But if the host computer crashes in the middle
of a [COMMIT](lang_transaction.html) where two or more database files are updated,
some of those files might get the changes where others
might not.



 There is a limit, set using [sqlite3\_limit()](c3ref/limit.html) and 
[SQLITE\_LIMIT\_ATTACHED](c3ref/c_limit_attached.html#sqlitelimitattached), to the number of databases that can be
simultaneously attached to a single database connection.


*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


