




UPDATE




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










UPDATE


►
Table Of Contents
[1\. Overview](#overview)
[2\. Details](#details)
[2\.1\. Restrictions on UPDATE Statements Within CREATE TRIGGER](#restrictions_on_update_statements_within_create_trigger)
[2\.2\. UPDATE FROM](#update_from)
[2\.2\.1\. UPDATE FROM in other SQL database engines](#update_from_in_other_sql_database_engines)
[2\.3\. Optional LIMIT and ORDER BY Clauses](#optional_limit_and_order_by_clauses)




# 1\. Overview


**[update\-stmt:](syntax/update-stmt.html)**
hide








WITH

RECURSIVE





common\-table\-expression






,








UPDATE






OR



ROLLBACK





qualified\-table\-name

OR



REPLACE






OR



IGNORE






OR



FAIL






OR



ABORT











SET



column\-name\-list



\=



expr



column\-name


,







FROM



table\-or\-subquery

,






join\-clause








WHERE



expr











returning\-clause




**[column\-name\-list:](syntax/column-name-list.html)**
show








(





column\-name



)




,







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




















**[compound\-operator:](syntax/compound-operator.html)**
show










UNION

UNION

INTERSECT

EXCEPT



ALL





















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




















**[compound\-operator:](syntax/compound-operator.html)**
show










UNION

UNION

INTERSECT

EXCEPT



ALL





















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







**[qualified\-table\-name:](syntax/qualified-table-name.html)**
show








schema\-name



.



table\-name



AS



alias









INDEXED



BY



index\-name

NOT



INDEXED




















**[returning\-clause:](syntax/returning-clause.html)**
show








RETURNING



expr



AS



column\-alias














\*






,







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




















**[compound\-operator:](syntax/compound-operator.html)**
show










UNION

UNION

INTERSECT

EXCEPT



ALL





















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

























An UPDATE statement is used to modify a subset of the values stored in 
zero or more rows of the database table identified by the 
[qualified\-table\-name](syntax/qualified-table-name.html) specified as part of the UPDATE statement.



# 2\. Details


If the UPDATE statement does not have a WHERE clause, all rows in the
table are modified by the UPDATE. Otherwise, the UPDATE affects only those
rows for which the WHERE clause
[boolean expression is true](lang_expr.html#booleanexpr). It is not an error if the
WHERE clause does not evaluate to true for any row in the table \- this just
means that the UPDATE statement affects zero rows.



The modifications made to each row affected by an UPDATE statement are
determined by the list of assignments following the SET keyword. Each
assignment specifies a column\-name to the left of the 
equals sign and a scalar expression to the right. 
For each affected row, the named columns
are set to the values found by evaluating the corresponding scalar 
expressions. If a single column\-name appears more than once in the list of
assignment expressions, all but the rightmost occurrence is ignored. Columns
that do not appear in the list of assignments are left unmodified. The scalar
expressions may refer to columns of the row being updated. In this case all
scalar expressions are evaluated before any assignments are made.



Beginning in SQLite [version 3\.15\.0](releaselog/3_15_0.html) (2016\-10\-14\), an assignment in
the SET clause can be a 
[parenthesized list of column names](syntax/column-name-list.html) on the left and a
[row value](rowvalue.html) of the same size on the right.




The optional "OR *action*" conflict clause that follows the
UPDATE keyword allows the user to nominate a specific
constraint conflict resolution algorithm to use during this one UPDATE command.
Refer to the section entitled [ON CONFLICT](lang_conflict.html) for additional information.



## 2\.1\. Restrictions on UPDATE Statements Within CREATE TRIGGER


The following additional syntax restrictions apply to UPDATE statements that
occur within the body of a [CREATE TRIGGER](lang_createtrigger.html) statement. 



* The table\-name specified as part of an UPDATE 
 statement within
 a trigger body must be unqualified. In other words, the
 *schema\-name***.** prefix on the table name of the UPDATE is
 not allowed within triggers. Unless the table to which the trigger
 is attached is in the TEMP database, the table being updated by the
 trigger program must reside in the same database as it. If the table
 to which the trigger is attached is in the TEMP database, then the
 unqualified name of the table being updated is resolved in the same way
 as it is for a top\-level statement (by searching first the TEMP database,
 then the main database, then any other databases in the order they were
 attached).
* The INDEXED BY and NOT INDEXED clauses are not allowed on UPDATE
 statements within triggers.
* The LIMIT and ORDER BY clauses for UPDATE are unsupported within
 triggers, regardless of the compilation options used to build SQLite.



## 2\.2\. UPDATE FROM


The UPDATE\-FROM idea is an extension to SQL that allows an UPDATE
statement to be driven by other tables in the database. 
The "target" table is the specific table that is being
updated. With UPDATE\-FROM you can join the target table
against other tables in the database in order to help compute which
rows need updating and what the new values should be on those rows.
UPDATE\-FROM is supported beginning in SQLite version 3\.33\.0
(2020\-08\-14\).



Other relation database engines also implement UPDATE\-FROM, but
because the construct is not part of the SQL standards, each product
implements UPDATE\-FROM differently. The SQLite implementation strives
to be compatible with PostgreSQL. The SQL Server and MySQL implementations
of the same idea work a little differently.



As an example of how UPDATE\-FROM can be useful, 
suppose you have a point\-of\-sale application that accumulates
purchases in the SALES table. At the end of the day, you want to adjust
the INVENTORY table according to the daily sales. To do this, you can
run an UPDATE against the INVENTORY table that adjusts the quantity by
the aggregated sales for the day. The statement would look like this:




```
UPDATE inventory
   SET quantity = quantity - daily.amt
  FROM (SELECT sum(quantity) AS amt, itemId FROM sales GROUP BY 2) AS daily
 WHERE inventory.itemId = daily.itemId;

```


The subquery in the FROM clause computes the amount by which the
inventory should be reduced for each itemId. That subquery is joined
against the inventory table and the quantity of each affected inventory
row is reduced by the appropriate amount.




The target table is not included in the FROM clause, unless the intent
is to do a self\-join against the target table. In the event of a self\-join,
the table in the FROM clause must be aliased to a different name
than the target table.




If the join between the target table and the FROM clause results in
multiple output rows for the same target table row, then only one of
those output rows is used for updating the target table. The output
row selected is arbitrary and might change from one release of SQLite
to the next, or from one run to the next.



### 2\.2\.1\. UPDATE FROM in other SQL database engines


SQL Server also supports UPDATE FROM, but in SQL Server the target
table must be included in the FROM clause. In other words, the
target table is named twice in the statement. With SQL Server,
the inventory adjustment statement demonstrated above would be written
like this:




```
UPDATE inventory
   SET quantity = quantity - daily.amt
  FROM inventory, 
       (SELECT sum(quantity) AS amt, itemId FROM sales GROUP BY 2) AS daily
 WHERE inventory.itemId = daily.itemId;

```

MySQL supports the UPDATE FROM idea, but it does so without using
a FROM clause. Instead, the complete join specification is given in between
the UPDATE and SET keywords. The equivalent MySQL statement would be
like this:




```
UPDATE inventory JOIN
       (SELECT sum(quantity) AS amt, itemId FROM sales GROUP BY 2) AS daily
       USING( itemId )
   SET inventory.quantity = inventory.quantity - daily.amt;

```

The MySQL UPDATE statement does not have just one target table like
other systems. Any of the tables that participate in the join can
be modified in the SET clause. The MySQL UPDATE syntax allows you to
update multiple tables at once!



## 2\.3\. Optional LIMIT and ORDER BY Clauses


If SQLite is built with the [SQLITE\_ENABLE\_UPDATE\_DELETE\_LIMIT](compile.html#enable_update_delete_limit)
compile\-time option then the syntax of the UPDATE statement is extended
with optional ORDER BY and LIMIT clauses as follows:


**[update\-stmt\-limited:](syntax/update-stmt-limited.html)**







WITH

RECURSIVE





common\-table\-expression






,








UPDATE






OR



ROLLBACK





qualified\-table\-name

OR



REPLACE






OR



IGNORE






OR



FAIL






OR



ABORT











SET



column\-name\-list



\=



expr



column\-name


,







FROM



table\-or\-subquery

,






join\-clause








WHERE



expr






returning\-clause





ORDER



BY



ordering\-term

,

LIMIT



expr



OFFSET



expr

,



expr




























If an UPDATE statement has a LIMIT clause, the maximum number of rows that
will be updated is found by evaluating the accompanying expression and casting
it to an integer value. A negative value is interpreted as "no limit".



If the LIMIT expression evaluates to non\-negative value *N* and the
UPDATE statement has an ORDER BY clause, then all rows that would be updated in
the absence of the LIMIT clause are sorted according to the ORDER BY and the
first *N* updated. If the UPDATE statement also has an OFFSET clause,
then it is similarly evaluated and cast to an integer value. If the OFFSET
expression evaluates to a non\-negative value *M*, then the first *M*
rows are skipped and the following *N* rows updated instead.



If the UPDATE statement has no ORDER BY clause, then all rows that
would be updated in the absence of the LIMIT clause are assembled in an
arbitrary order before applying the LIMIT and OFFSET clauses to determine 
which are actually updated.



The ORDER BY clause on an UPDATE statement is used only to determine which
rows fall within the LIMIT. The order in which rows are modified is arbitrary
and is not influenced by the ORDER BY clause.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


