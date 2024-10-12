




RETURNING




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










RETURNING


►
Table Of Contents
[1\. Overview](#overview)
[1\.1\. Typical Use](#typical_use)
[2\. Details](#details)
[2\.1\. Processing Order](#processing_order)
[2\.2\. Self\-Referential Subqueries Are Indeterminate](#self_referential_subqueries_are_indeterminate)
[2\.3\. ACID Changes](#acid_changes)
[3\. Limitations And Caveats](#limitations_and_caveats)




# 1\. Overview


**[returning\-clause:](syntax/returning-clause.html)**
hide








RETURNING



expr



AS



column\-alias














\*






,






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











The RETURNING clause is not a statement itself, but a clause that can
optionally appear near the end of top\-level
[DELETE](lang_delete.html), [INSERT](lang_insert.html), and [UPDATE](lang_update.html) statements.
The effect of the RETURNING clause is to cause the statement to return
one result row for each database row that is deleted, inserted, or updated.
 RETURNING is not standard SQL. It is an extension.
SQLite's syntax for RETURNING is modelled after 
[PostgreSQL](https://www.postgresql.org).
 



The RETURNING syntax has been supported by SQLite since version 3\.35\.0
(2021\-03\-12\).



## 1\.1\. Typical Use



The RETURNING clause is designed to provide the application with the
values of columns that are filled in automatically by SQLite. For
example:




```
CREATE TABLE t0(
  a INTEGER PRIMARY KEY,
  b DATE DEFAULT CURRENT_TIMESTAMP,
  c INTEGER
);
INSERT INTO t0(c) VALUES(random()) RETURNING *;

```


In the INSERT statement above, SQLite computes the values for all
three columns. The RETURNING clause causes SQLite to report the chosen
values back to the application. This saves the application from having
to issue a separate query to figure out exactly what values were inserted.



# 2\. Details



The RETURNING clause is followed by a comma\-separated list of
expressions. These expressions are similar to the expressions following
the SELECT keyword in a [SELECT statement](lang_select.html) in that they
define the values of the columns in the result set. Each expression
defines the value for a single column. Each expression may be
optionally followed by an AS clause that determines the name of
the result column. The special "\*" expression expands into a list
of all [non\-hidden](vtab.html#hiddencol) columns of the table being deleted,
inserted, or updated.




For INSERT and UPDATE statements, references to columns in the table
being modified refer to the value of that column *after* the change
has been applied. For DELETE statements, references to columns mean
the value *before* the delete occurs.




The RETURNING clause only returns rows that are directly modified
by the DELETE, INSERT, or UPDATE statement. The RETURNING clause
does not report any additional database changes
caused by [foreign key constraints](foreignkeys.html) or [triggers](lang_createtrigger.html).




A RETURNING clause for an [UPSERT](lang_upsert.html) reports both inserted and
updated rows.



## 2\.1\. Processing Order



When a DELETE, INSERT, or UPDATE statement with a RETURNING clause
is run, all of the database changes occur during the first invocation
of [sqlite3\_step()](c3ref/step.html). The RETURNING clause output is accumulated in
memory. The first sqlite3\_step() call returns one row of RETURNING
output and subsequent rows of RETURNING output are returned by subsequent
calls to sqlite3\_step().
To put this another way, all RETURNING clause output is embargoed
until after all database modification actions are completed.




This means that if a statement has a RETURNING clause that generates
a large amount of output, either many rows or large
string or BLOB values, then the statement might use a lot of 
temporary memory to hold those values while it is running.




While SQLite does guarantee that all database changes will occur
before any RETURNING output is emitted, it does *not* guarantee
that the order of individual RETURNING rows will match the order in
which those rows were changed in the database. The output order
for the RETURNING rows is arbitrary and is not necessarily related
to the order in which the rows were processed internally.



## 2\.2\. Self\-Referential Subqueries Are Indeterminate



SQLite guarantees that all database changes will occur before
any RETURNING output is *emitted*, but SQLite makes no
guarantees about the order in which database changes occur nor
when the RETURNING output is *computed* in relation to
those database changes. RETURNING clause outputs are all computed and
placed in temporary storage during the first call to sqlite3\_step() 
but the specific order of when those output are computed and the
order in which database changes occur is unspecified. The order 
can change from one query to the next.




Hence if column of RETURNING output contains a
subquery that references the table being modified, then the result
of that subquery might depend on unspecified behavior and hence
could vary from one invocation of the query to the next.



## 2\.3\. ACID Changes



When the previous "*Processing Order*" section says that
"database changes occur during the first invocation of sqlite3\_step()",
that means that the changes are stored in the private page cache of
the database connection that is running the statement. It does
*not* mean that the changes are actually committed. The commit
does not occur until the statement finishes, and maybe not even then
if the statement is part of a larger transaction. Changes to the
database are still atomic, consistent, isolated, and durable (ACID).
When the previous section says "changes occur",
this means that internal data structures are adjusted pending a transaction
commit. Some of those changes may or may not spill into the
[write\-ahead log](wal.html), depending on how much pressure there is on the
page cache. If the page cache is not under memory pressure, then
probably nothing will be written to disk until after the transaction
completes, which is after sqlite3\_step() returns SQLITE\_DONE.




In other words, when the previous section says "database changes
occur", that means that the changes occur in the memory of the
specific database connection that is running the statement, *not* that
the changes are written to disk.



# 3\. Limitations And Caveats


1. The RETURNING clause is not available on DELETE and UPDATE statements
against [virtual tables](vtab.html).
This limitation might be removed in future versions of SQLite.
2. The RETURNING clause is only available in top\-level DELETE, INSERT,
and UPDATE statements. The RETURNING clause cannot be used by
statements within triggers.
3. Even though a DML statement with a RETURNING clause returns table content,
it cannot be used as a subquery. The RETURNING clause can only return
data to the application. It is not currently possible to divert the
RETURNING output into another table or query. PostgreSQL has the ability
to use a DML statement with a RETURNING clause like a view in a 
[common table expressions](lang_with.html). SQLite does not currently have that
ability, though that is something that might be added in a future release.
4. The rows emitted by the RETURNING clause appear in an arbitrary order.
That order might change depending on the database schema, upon the specific
release of SQLite used, or even from one execution of the same statement
to the next.
There is no way to cause the output rows to appear in a particular order.
Even if SQLite is compiled with the [SQLITE\_ENABLE\_UPDATE\_DELETE\_LIMIT](compile.html#enable_update_delete_limit)
option such that ORDER BY clauses are allowed on DELETE and UPDATE
statements, those ORDER BY clauses do not constrain the output order
of RETURNING.
5. The values emitted by the RETURNING clause are the values as seen
by the top\-level DELETE, INSERT, or UPDATE statement
and do not reflect any subsequent value changes made by [triggers](lang_createtrigger.html).
Thus, if the database includes AFTER triggers that modifies some
of the values of each row inserted or updated, the RETURNING clause
emits the original values that are computed before those triggers run.
6. The RETURNING clause may not contain top\-level [aggregate functions](lang_aggfunc.html) or
[window functions](windowfunctions.html). If there are subqueries in the RETURNING clause,
those subqueries may contain aggregates and window functions, but
aggregates cannot occur at the top level.
7. The RETURNING clause may only reference the table being modified.
In an [UPDATE FROM](lang_update.html#upfrom) statement, the auxiliary tables named in the FROM
clause may not participate in the RETURNING clause.


*This page last modified on [2024\-05\-08 20:36:57](https://sqlite.org/docsrc/honeypot) UTC* 


