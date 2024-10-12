




CREATE TABLE




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










CREATE TABLE


►
Table Of Contents
[1\. Syntax](#syntax)
[2\. The CREATE TABLE command](#the_create_table_command)
[2\.1\. CREATE TABLE ... AS SELECT Statements](#create_table_as_select_statements)
[3\. Column Definitions](#column_definitions)
[3\.1\. Column Data Types](#column_data_types)
[3\.2\. The DEFAULT clause](#the_default_clause)
[3\.3\. The COLLATE clause](#the_collate_clause)
[3\.4\. The GENERATED ALWAYS AS clause](#the_generated_always_as_clause)
[3\.5\. The PRIMARY KEY](#the_primary_key)
[3\.6\. UNIQUE constraints](#unique_constraints)
[3\.7\. CHECK constraints](#check_constraints)
[3\.8\. NOT NULL constraints](#not_null_constraints)
[4\. Constraint enforcement](#constraint_enforcement)
[4\.1\. Response to constraint violations](#response_to_constraint_violations)
[5\. ROWIDs and the INTEGER PRIMARY KEY](#rowids_and_the_integer_primary_key)




# 1\. Syntax


**[create\-table\-stmt:](syntax/create-table-stmt.html)**
hide








CREATE

TEMP

TEMPORARY

TABLE













IF



NOT



EXISTS








schema\-name



.



table\-name








(



column\-def

table\-constraint



,

)



table\-options

,




















AS



select\-stmt





**[column\-def:](syntax/column-def.html)**
show








column\-name





type\-name



column\-constraint














**[column\-constraint:](syntax/column-constraint.html)**
show












CONSTRAINT



name






PRIMARY



KEY



DESC





conflict\-clause





AUTOINCREMENT














ASC






NOT



NULL



conflict\-clause






UNIQUE



conflict\-clause






CHECK



(



expr



)






DEFAULT





(



expr



)






literal\-value






signed\-number






COLLATE



collation\-name






foreign\-key\-clause






GENERATED



ALWAYS



AS



(



expr



)









VIRTUAL






STORED





**[conflict\-clause:](syntax/conflict-clause.html)**
show










ON



CONFLICT



ROLLBACK

ABORT

FAIL

IGNORE

REPLACE































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











**[foreign\-key\-clause:](syntax/foreign-key-clause.html)**
show








REFERENCES



foreign\-table



(



column\-name



)

,




ON



DELETE



SET



NULL

UPDATE




SET



DEFAULT




CASCADE




RESTRICT




NO



ACTION




MATCH



name























NOT



DEFERRABLE



INITIALLY



DEFERRED

INITIALLY



IMMEDIATE




















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








**[signed\-number:](syntax/signed-number.html)**
show








\+



numeric\-literal






\-








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























**[table\-constraint:](syntax/table-constraint.html)**
show








CONSTRAINT



name

PRIMARY



KEY



(



indexed\-column



)



conflict\-clause











,




UNIQUE




CHECK



(



expr



)






FOREIGN



KEY



(



column\-name



)



foreign\-key\-clause






,





**[conflict\-clause:](syntax/conflict-clause.html)**
show










ON



CONFLICT



ROLLBACK

ABORT

FAIL

IGNORE

REPLACE































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









**[foreign\-key\-clause:](syntax/foreign-key-clause.html)**
show








REFERENCES



foreign\-table



(



column\-name



)

,




ON



DELETE



SET



NULL

UPDATE




SET



DEFAULT




CASCADE




RESTRICT




NO



ACTION




MATCH



name























NOT



DEFERRABLE



INITIALLY



DEFERRED

INITIALLY



IMMEDIATE




















**[indexed\-column:](syntax/indexed-column.html)**
show








column\-name



COLLATE



collation\-name





DESC








expr









ASC









**[table\-options:](syntax/table-options.html)**
show








WITHOUT



ROWID





STRICT





,







# 2\. The CREATE TABLE command


The "CREATE TABLE" command is used to create a new table in an SQLite 
database. A CREATE TABLE command specifies the following attributes of the
new table:



* The name of the new table.
* The database in which the new table is created. Tables may be 
 created in the main database, the temp database, or in any attached
 database.
* The name of each column in the table.
* The declared type of each column in the table.
* A default value or expression for each column in the table.
* A default collation sequence to use with each column.
* Optionally, a PRIMARY KEY for the table. Both single column and
 composite (multiple column) primary keys are supported.
* A set of SQL constraints for each table. SQLite supports UNIQUE, NOT
 NULL, CHECK and FOREIGN KEY constraints.
* Optionally, a [generated column](gencol.html) constraint.
* Whether the table is a [WITHOUT ROWID](withoutrowid.html) table.
* Whether the table is subject to [strict type checking](stricttables.html).


Every CREATE TABLE statement must specify a name for the new table.
 Table names that begin with "sqlite\_" are reserved for internal use. It
 is an error to attempt to create a table with a name that starts with
 "sqlite\_".



 If a schema\-name is specified, it must be either "main", 
 "temp", or the name of an [attached database](lang_attach.html). In this case
 the new table is created in the named database. If the "TEMP" or "TEMPORARY"
 keyword occurs between the "CREATE" and "TABLE" then the new table is
 created in the temp database. It is an error to specify both a 
 schema\-name and the TEMP or TEMPORARY keyword, unless the
 schema\-name is "temp". 
 If no schema name is specified and the
 TEMP keyword is not present then the table is created in the main
 database.




 It is usually an error to attempt to create a new table in a database that
 already contains a table, index or view of the same name. However, if the
 "IF NOT EXISTS" clause is specified as part of the CREATE TABLE statement and
 a table or view of the same name already exists, the CREATE TABLE command
 simply has no effect (and no error message is returned). An error is still
 returned if the table cannot be created because of an existing index, even 
 if the "IF NOT EXISTS" clause is specified.



It is not an error to create a table that has the same name as an 
 existing [trigger](lang_createtrigger.html).



Tables are removed using the [DROP TABLE](lang_droptable.html) statement. 



## 2\.1\. CREATE TABLE ... AS SELECT Statements


A "CREATE TABLE ... AS SELECT" statement creates and populates a database
table based on the results of a SELECT statement. The table has the same
number of columns as the SELECT statement returns. The name of
each column is the same as the name of the corresponding column in the result
set of the SELECT statement. The declared type of each column is determined
by the [expression affinity](datatype3.html#expraff) of the corresponding expression in the result set
of the SELECT statement, as follows:





| Expression Affinity | Column Declared Type |
| --- | --- |
| TEXT | "TEXT" |
| NUMERIC | "NUM" |
| INTEGER | "INT" |
| REAL | "REAL" |
| BLOB (a.k.a "NONE") | "" (empty string) |


A table created using CREATE TABLE AS has no PRIMARY KEY and no
constraints of any kind. The default value of each column is NULL. The default
collation sequence for each column of the new table is BINARY.



Tables created using CREATE TABLE AS are initially populated with the
rows of data returned by the SELECT statement. Rows are assigned contiguously
ascending [rowid](lang_createtable.html#rowid) values, starting with 1, in the [order](lang_select.html#orderby) that they
are returned by the SELECT statement.




# 3\. Column Definitions


Unless it is a CREATE TABLE ... AS SELECT statement, a CREATE TABLE includes
one or more [column definitions](syntax/column-def.html), optionally followed by a list of
[table constraints](syntax/table-constraint.html). Each column definition consists of the
name of the column, optionally followed by the declared type of the column,
then one or more optional [column constraints](syntax/column-constraint.html). Included in
the definition of "column constraints" for the purposes of the previous
statement are the COLLATE and DEFAULT clauses, even though these are not really
constraints in the sense that they do not restrict the data that the table may
contain. The other constraints \- NOT NULL, CHECK, UNIQUE, PRIMARY KEY and
FOREIGN KEY constraints \- impose restrictions on the table data.



The number of columns in a table is limited by the [SQLITE\_MAX\_COLUMN](limits.html#max_column)
compile\-time parameter. A single row of a table cannot store more than
[SQLITE\_MAX\_LENGTH](limits.html#max_length) bytes of data. Both of these limits can be lowered at
runtime using the [sqlite3\_limit()](c3ref/limit.html) C/C\+\+ interface.


## 3\.1\. Column Data Types


Unlike most SQL databases, SQLite does not restrict the type of data that
may be inserted into a column based on the columns declared type. Instead,
SQLite uses [dynamic typing](datatype3.html). The declared type of a column is used to
determine the [affinity](datatype3.html#affinity) of the column only.




## 3\.2\. The DEFAULT clause


The DEFAULT clause specifies a default value to use for the column if no
value is explicitly provided by the user when doing an [INSERT](lang_insert.html). If there
is no explicit DEFAULT clause attached to a column definition, then the 
default value of the column is NULL. An explicit DEFAULT clause may specify
that the default value is NULL, a string constant, a blob constant, a
signed\-number, or any constant expression enclosed in parentheses. A
default value may also be one of the special case\-independent keywords
CURRENT\_TIME, CURRENT\_DATE or CURRENT\_TIMESTAMP. For the purposes of the
DEFAULT clause, an expression is considered constant if it
contains no sub\-queries, column or table references, [bound parameters](lang_expr.html#varparam),
or string literals enclosed in double\-quotes instead of single\-quotes.



Each time a row is inserted into the table by an INSERT statement that 
does not provide explicit values for all table columns the values stored in
the new row are determined by their default values, as follows:



* If the default value of the column is a constant NULL, text, blob or
 signed\-number value, then that value is used directly in the new row.
* If the default value of a column is an expression in parentheses, then
 the expression is evaluated once for each row inserted and the results
 used in the new row.
* If the default value of a column is CURRENT\_TIME, CURRENT\_DATE or
 CURRENT\_TIMESTAMP, then the value used in the new row is a text
 representation of the current UTC date and/or time. For CURRENT\_TIME, the
 format of the value is "HH:MM:SS". For CURRENT\_DATE, "YYYY\-MM\-DD". The
 format for CURRENT\_TIMESTAMP is "YYYY\-MM\-DD HH:MM:SS".



## 3\.3\. The COLLATE clause


The COLLATE clause specifies the name of a [collating sequence](datatype3.html#collation) to use as
the default collation sequence for the column. If no COLLATE clause is
specified, the default collation sequence is [BINARY](datatype3.html#collation).



## 3\.4\. The GENERATED ALWAYS AS clause


A column that includes a GENERATED ALWAYS AS clause is a [generated column](gencol.html).
Generated columns are supported beginning with SQLite version 3\.31\.0 (2020\-01\-22\).
See the [separate documentation](gencol.html) for details on the capabilities and
limitations of generated columns.




## 3\.5\. The PRIMARY KEY


Each table in SQLite may have at most one PRIMARY KEY. If the
 keywords PRIMARY KEY are added to a column definition, then the primary key
 for the table consists of that single column. Or, if a PRIMARY KEY clause 
 is specified as a [table\-constraint](syntax/table-constraint.html), then the primary key of the table
 consists of the list of columns specified as part of the PRIMARY KEY clause.
 The PRIMARY KEY clause must contain only column names — the use of 
 expressions in an [indexed\-column](syntax/indexed-column.html) of a PRIMARY KEY is not supported.
 An error is raised if more than one PRIMARY KEY clause appears in a
 CREATE TABLE statement. The PRIMARY KEY is optional for ordinary tables
 but is required for [WITHOUT ROWID](withoutrowid.html) tables.



If a table has a single column primary key and the declared type of that
 column is "INTEGER" and the table is not a [WITHOUT ROWID](withoutrowid.html) table,
 then the column is known as an [INTEGER PRIMARY KEY](lang_createtable.html#rowid).
 See [below](lang_createtable.html#rowid) for a description of the special properties and behaviors
 associated with an [INTEGER PRIMARY KEY](lang_createtable.html#rowid).



Each row in a table with a primary key must have a unique combination
 of values in its primary key columns. For the purposes of determining
 the uniqueness of primary key values, NULL values are considered distinct from
 all other values, including other NULLs. If an [INSERT](lang_insert.html) or [UPDATE](lang_update.html)
 statement attempts to modify the table content so that two or more rows
 have identical primary key values, that is a constraint violation.



 According to the SQL standard, PRIMARY KEY should always imply NOT NULL.
 Unfortunately, due to a bug in some early versions, this is not the
 case in SQLite. Unless the column is an [INTEGER PRIMARY KEY](lang_createtable.html#rowid) or
 the table is a [WITHOUT ROWID](withoutrowid.html) table or a [STRICT](stricttables.html) table 
 or the column is declared NOT NULL,
 SQLite allows NULL values in a PRIMARY KEY column. SQLite could be fixed to
 conform to the standard, but doing so might break legacy applications.
 Hence, it has been decided to merely document the fact that SQLite
 allows NULLs in most PRIMARY KEY columns.




## 3\.6\. UNIQUE constraints


A UNIQUE constraint is similar to a PRIMARY KEY constraint, except
 that a single table may have any number of UNIQUE constraints. For each
 UNIQUE constraint on the table, each row must contain a unique combination
 of values in the columns identified by the UNIQUE constraint. 
 For the purposes of UNIQUE constraints, NULL values
 are considered distinct from all other values, including other NULLs.
 As with PRIMARY KEYs, a UNIQUE [table\-constraint](syntax/table-constraint.html) clause must contain
 only column names — the use of 
 expressions in an [indexed\-column](syntax/indexed-column.html) of a UNIQUE [table\-constraint](syntax/table-constraint.html)
 is not supported.
 



In most cases, UNIQUE and PRIMARY KEY
 constraints are implemented by creating a unique index in the database.
 (The exceptions are [INTEGER PRIMARY KEY](lang_createtable.html#rowid) and PRIMARY KEYs on 
 [WITHOUT ROWID](withoutrowid.html) tables.)
 Hence, the following schemas are logically equivalent:

 

1. CREATE TABLE t1(a, b UNIQUE);
2. CREATE TABLE t1(a, b PRIMARY KEY);
3. CREATE TABLE t1(a, b);  

 CREATE UNIQUE INDEX t1b ON t1(b);



## 3\.7\. CHECK constraints


A CHECK constraint may be attached to a column definition or
 specified as a table constraint. In practice it makes no difference. Each
 time a new row is inserted into the table or an existing row is updated,
 the expression associated with each CHECK constraint is evaluated and
 cast to a NUMERIC value in the same way as a [CAST expression](lang_expr.html#castexpr). If the 
 result is zero (integer value 0 or real value 0\.0\), then a constraint
 violation has occurred. If the CHECK expression evaluates to NULL, or
 any other non\-zero value, it is not a constraint violation.
 The expression of a CHECK constraint may not contain a subquery.



CHECK constraints are only verified when the table is written, not when
 it is read. Furthermore, verification of CHECK constraints can be
 temporarily disabled using the "[PRAGMA ignore\_check\_constraints\=ON;](pragma.html#pragma_ignore_check_constraints)"
 statement. Hence, it is possible that a query might produce results that
 violate the CHECK constraints.




## 3\.8\. NOT NULL constraints


A NOT NULL constraint may only be attached to a column definition,
 not specified as a table constraint. Not surprisingly, a NOT NULL
 constraint dictates that the associated column may not contain a NULL value.
 Attempting to set the column value to NULL when inserting a new row or
 updating an existing one causes a constraint violation. NOT NULL
 constraints are not verified during queries, so a query of a column might
 produce a NULL value even though the column is marked as NOT NULL, if the
 database file is corrupt.




# 4\. Constraint enforcement


Constraints are checked during [INSERT](lang_insert.html) and [UPDATE](lang_update.html) and by
[PRAGMA integrity\_check](pragma.html#pragma_integrity_check) and [PRAGMA quick\_check](pragma.html#pragma_quick_check) and sometimes
by [ALTER TABLE](lang_altertable.html). Queries and [DELETE](lang_delete.html)
statements do not normally verify constraints.
Hence, if a database file has been corrupted (perhaps by an external
program making direct changes to the database file without going through 
the SQLite library) a query might return data that violates a constraint.
For example:




```
CREATE TABLE t1(x INT CHECK( x>3 ));
/* Insert a row with X less than 3 by directly writing into the
** database file using an external program */
PRAGMA integrity_check;  -- Reports row with x less than 3 as corrupt
INSERT INTO t1(x) VALUES(2);  -- Fails with SQLITE_CORRUPT
SELECT x FROM t1;  -- Returns an integer less than 3 in spite of the CHECK constraint

```

Enforcement of CHECK constraints can be temporarily disabled using
the [PRAGMA ignore\_check\_constraints\=ON;](pragma.html#pragma_ignore_check_constraints) statement.



## 4\.1\. Response to constraint violations


The response to a constraint violation is determined by the
 [constraint conflict resolution algorithm](lang_conflict.html). Each 
 PRIMARY KEY, UNIQUE, NOT NULL and CHECK constraint has a default conflict
 resolution algorithm. PRIMARY KEY, UNIQUE and NOT NULL constraints may be
 explicitly assigned another default conflict resolution algorithm by
 including a [conflict\-clause](syntax/conflict-clause.html) in their definitions.
 Or, if a constraint definition does not include a [conflict\-clause](syntax/conflict-clause.html),
 the default conflict resolution algorithm is ABORT.
 The conflict resolution algorithm for CHECK constraints is always ABORT.
 (For historical compatibility only, table CHECK constraints are allowed
 to have a conflict resolution clause, but that has no effect.)
 Different constraints within the
 same table may have different default conflict resolution algorithms. See
 the section titled [ON CONFLICT](lang_conflict.html) for additional information.




# 5\. ROWIDs and the INTEGER PRIMARY KEY


Except for [WITHOUT ROWID](withoutrowid.html) tables, all rows within SQLite tables
have a 64\-bit signed integer key that uniquely identifies the row within its table.
This integer is usually
called the "rowid". The rowid value can be accessed using one of the special
case\-independent names "rowid", "oid", or "\_rowid\_" in place of a column name.
If a table contains a user defined column named "rowid", "oid" or "\_rowid\_",
then that name always refers the explicitly declared column and cannot be used
to retrieve the integer rowid value.



The rowid (and "oid" and "\_rowid\_") is omitted in [WITHOUT ROWID](withoutrowid.html) tables.
WITHOUT ROWID tables are only available in SQLite [version 3\.8\.2](releaselog/3_8_2.html)
(2013\-12\-06\) and later.
A table that lacks the WITHOUT ROWID clause is called a "rowid table".



The data for rowid tables is stored as a B\-Tree structure containing
one entry for each table row, using the rowid value as the key. This means that
retrieving or sorting records by rowid is fast. Searching for a record with a
specific rowid, or for all records with rowids within a specified range is
around twice as fast as a similar search made by specifying any other PRIMARY
KEY or indexed value.



 With one exception noted below, if a rowid table has a primary key that consists
of a single column and the declared type of that column is "INTEGER" in any mixture of
upper and lower case, then the column becomes an alias for the rowid. Such a
column is usually referred to as an "integer primary key". A PRIMARY KEY column
only becomes an integer primary key if the declared type name is exactly
"INTEGER". Other integer type names like "INT" or "BIGINT" or "SHORT INTEGER"
or "UNSIGNED INTEGER" causes the primary key column to behave as an ordinary
table column with integer [affinity](datatype3.html#affinity) and a unique index, not as an alias for
the rowid.



 The exception mentioned above is that if the declaration of a column with
declared type "INTEGER" includes an "PRIMARY KEY DESC" clause, it does not
become an alias for the rowid and is not classified as an integer primary key.
This quirk is not by design. It is due to a bug in early versions of SQLite.
But fixing the bug could result in backwards incompatibilities.
Hence, the original behavior has been retained (and documented) because odd
behavior in a corner case is far better than a compatibility break. This means
that the following three table declarations all cause the column "x" to be an
alias for the rowid (an integer primary key):



* CREATE TABLE t(x INTEGER PRIMARY KEY ASC, y, z);
* CREATE TABLE t(x INTEGER, y, z, PRIMARY KEY(x ASC));
* CREATE TABLE t(x INTEGER, y, z, PRIMARY KEY(x DESC));


But the following declaration does not result in "x" being an alias for
the rowid:


* CREATE TABLE t(x INTEGER PRIMARY KEY DESC, y, z);


Rowid values may be modified using an UPDATE statement in the same
way as any other column value can, either using one of the built\-in aliases
("rowid", "oid" or "\_rowid\_") or by using an alias created by an integer
primary key. Similarly, an INSERT statement may provide a value to use as the
rowid for each row inserted. Unlike normal SQLite columns, an integer primary
key or rowid column must contain integer values. Integer primary key or rowid
columns are not able to hold floating point values, strings, BLOBs, or NULLs.



If an UPDATE statement attempts to set an integer primary key or rowid column
to a NULL or blob value, or to a string or real value that cannot be losslessly
converted to an integer, a "datatype mismatch" error occurs and the statement
is aborted. If an INSERT statement attempts to insert a blob value, or a string
or real value that cannot be losslessly converted to an integer into an
integer primary key or rowid column, a "datatype mismatch" error occurs and the
statement is aborted.



If an INSERT statement attempts to insert a NULL value into a rowid or
integer primary key column, the system chooses an integer value to use as the
rowid automatically. A detailed description of how this is done is provided
[separately](autoinc.html).


The [parent key](foreignkeys.html#parentchild) of a [foreign key constraint](foreignkeys.html) is not allowed to
use the rowid. The parent key must used named columns only.


