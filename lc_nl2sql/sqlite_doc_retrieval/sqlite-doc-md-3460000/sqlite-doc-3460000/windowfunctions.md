




Window Functions




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Window Functions


►
Table Of Contents
[1\. Introduction to Window Functions](#introduction_to_window_functions)
[2\. Aggregate Window Functions](#aggregate_window_functions)
[2\.1\. The PARTITION BY Clause](#the_partition_by_clause)
[2\.2\. Frame Specifications](#frame_specifications)
[2\.2\.1\. Frame Type](#frame_type)
[2\.2\.2\. Frame Boundaries](#frame_boundaries)
[2\.2\.3\. The EXCLUDE Clause](#the_exclude_clause)
[2\.3\. The FILTER Clause](#the_filter_clause)
[3\. Built\-in Window Functions](#built_in_window_functions)
[4\. Window Chaining](#window_chaining)
[5\. User\-Defined Aggregate Window Functions](#user_defined_aggregate_window_functions)
[6\. History](#history)




# 1\. Introduction to Window Functions


A window function is an SQL function where the input
values are taken from
a "window" of one or more rows in the results set of a SELECT statement.



Window functions are distinguished from [scalar functions](lang_corefunc.html) and
[aggregate functions](lang_aggfunc.html) by the
presence of an OVER clause. If a function has an OVER clause,
then it is a window function. If it lacks an OVER clause, then it is an
ordinary aggregate or scalar function. Window functions might also
have a FILTER clause in between the function and the OVER clause.



The syntax for a window function is like this:


**[window\-function\-invocation:](syntax/window-function-invocation.html)**
hide








window\-func



(



expr



)



filter\-clause



OVER



window\-name







window\-defn


,







\*





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
hide








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









**[filter\-clause:](syntax/filter-clause.html)**
hide








FILTER



(



WHERE



expr



)






**[window\-defn:](syntax/window-defn.html)**
hide








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
hide








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













Unlike ordinary functions, window functions
cannot use the DISTINCT keyword.
Also, Window functions may only appear in the result set and in the
ORDER BY clause of a SELECT statement.



Window functions come in two varieties:
[aggregate window functions](windowfunctions.html#aggwinfunc) and
[built\-in window functions](windowfunctions.html#builtins). Every aggregate window function
can also work as an ordinary aggregate function, simply by omitting
the OVER and FILTER clauses. Furthermore, all of the built\-in
[aggregate functions](lang_aggfunc.html) of SQLite can be used as an
aggregate window function by adding an appropriate OVER clause.
Applications can register new aggregate window functions using
the [sqlite3\_create\_window\_function()](c3ref/create_function.html) interface.
The built\-in window functions, however, require special\-case
handling in the query planner and hence new window functions
that exhibit the exceptional properties found in the built\-in
window functions cannot be added by the application.



Here is an example using the built\-in row\_number()
window function:




```
CREATE TABLE t0(x INTEGER PRIMARY KEY, y TEXT);
INSERT INTO t0 VALUES (1, 'aaa'), (2, 'ccc'), (3, 'bbb');

-- The following SELECT statement returns:
-- 
--   x | y | row_number
-----------------------
--   1 | aaa | 1         
--   2 | ccc | 3         
--   3 | bbb | 2         
-- 
SELECT x, y, row_number() OVER (ORDER BY y) AS row_number FROM t0 ORDER BY x;

```


The row\_number() window function
assigns consecutive integers to each
row in order of the "ORDER BY" clause within the
window\-defn (in this case "ORDER BY y"). Note that
this does not affect the order in which results are returned from
the overall query. The order of the final output is
still governed by the ORDER BY clause attached to the SELECT
statement (in this case "ORDER BY x").



Named window\-defn clauses may also be added to a SELECT
statement using a WINDOW clause and then referred to by name within window
function invocations. For example, the following SELECT statement contains
two named window\-defs clauses, "win1" and "win2":




```
SELECT x, y, row_number() OVER win1, rank() OVER win2
FROM t0
WINDOW win1 AS (ORDER BY y RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
       win2 AS (PARTITION BY y ORDER BY x)
ORDER BY x;

```

The WINDOW clause, when one is present, comes after any HAVING clause and
before any ORDER BY.




# 2\. Aggregate Window Functions


 The examples in this section all assume that the database is populated as
follows:




```
CREATE TABLE t1(a INTEGER PRIMARY KEY, b, c);
INSERT INTO t1 VALUES   (1, 'A', 'one'  ),
                        (2, 'B', 'two'  ),
                        (3, 'C', 'three'),
                        (4, 'D', 'one'  ),
                        (5, 'E', 'two'  ),
                        (6, 'F', 'three'),
                        (7, 'G', 'one'  );

```

 An aggregate window function is similar to an
[ordinary aggregate function](lang_aggfunc.html), except
adding it to a query does not change the number of rows returned. Instead,
for each row the result of the aggregate window function is as if the
corresponding aggregate were run over all rows in the "window frame"
specified by the OVER clause.





```
-- The following SELECT statement returns:
-- 
--   a | b | group_concat
-------------------------
--   1 | A | A.B         
--   2 | B | A.B.C       
--   3 | C | B.C.D       
--   4 | D | C.D.E       
--   5 | E | D.E.F       
--   6 | F | E.F.G       
--   7 | G | F.G         
-- 
SELECT a, b, group_concat(b, '.') OVER (
  ORDER BY a ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
) AS group_concat FROM t1;

```

 In the example above, the window frame consists of all rows between the
previous row ("1 PRECEDING") and the following row ("1 FOLLOWING"), inclusive,
where rows are sorted according to the ORDER BY clause in the
window\-defn (in this case "ORDER BY a").
For example, the frame for the row with (a\=3\) consists of rows (2, 'B', 'two'),
(3, 'C', 'three') and (4, 'D', 'one'). The result of group\_concat(b, '.')
for that row is therefore 'B.C.D'.



 All of SQLite's [aggregate functions](lang_aggfunc.html) may
be used as aggregate window functions. It is also possible to
[create user\-defined aggregate window functions](windowfunctions.html#udfwinfunc).





## 2\.1\. The PARTITION BY Clause


 For the purpose of computing window functions, the result set
of a query is divided into one or more "partitions". A partition consists
of all rows that have the same value for all terms of the PARTITION BY clause
in the window\-defn. If there is no PARTITION BY clause,
then the entire result set of the query is a single partition.
Window\-function processing is performed separately for each partition.



 For example:




```
-- The following SELECT statement returns:
-- 
--   c     | a | b | group_concat
---------------------------------
--   one   | 1 | A | A.D.G       
--   one   | 4 | D | D.G         
--   one   | 7 | G | G           
--   three | 3 | C | C.F         
--   three | 6 | F | F           
--   two   | 2 | B | B.E         
--   two   | 5 | E | E           
-- 
SELECT c, a, b, group_concat(b, '.') OVER (
  PARTITION BY c ORDER BY a RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
) AS group_concat
FROM t1 ORDER BY c, a;

```

 In the query above, the "PARTITION BY c" clause breaks the
result set up into three partitions. The first partition has
three rows with c\=\='one'. The second partition has two rows with
c\=\='three' and the third partition has two rows with c\=\='two'.



 In the example above, all the rows for each partition are
grouped together in the final output. This is because the PARTITION BY
clause is a prefix of the ORDER BY clause on the overall query.
But that does not have
to be the case. A partition can be composed of rows scattered
about haphazardly within the result set. For example:




```
-- The following SELECT statement returns:
-- 
--   c     | a | b | group_concat
---------------------------------
--   one   | 1 | A | A.D.G       
--   two   | 2 | B | B.E         
--   three | 3 | C | C.F         
--   one   | 4 | D | D.G         
--   two   | 5 | E | E           
--   three | 6 | F | F           
--   one   | 7 | G | G           
-- 
SELECT c, a, b, group_concat(b, '.') OVER (
  PARTITION BY c ORDER BY a RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
) AS group_concat
FROM t1 ORDER BY a;

```


## 2\.2\. Frame Specifications


 The frame\-spec determines which output rows are
read by an aggregate window function. The
frame\-spec consists of four parts:



* A frame type \- either ROWS, RANGE or GROUPS,
* A starting frame boundary,
* An ending frame boundary,
* An EXCLUDE clause.


 Here are the syntax details:

**[frame\-spec:](syntax/frame-spec.html)**
hide








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












The ending frame boundary can be omitted (if the
BETWEEN and AND keywords that surround the starting frame boundary
are also omitted),
in which case the ending frame boundary defaults to CURRENT ROW.



 If the frame type is RANGE or GROUPS, then rows with the same values for
all ORDER BY expressions are considered "peers". Or, if there are no ORDER BY
terms, all rows are peers. Peers are always within the same frame.



The default frame\-spec is:




```
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE NO OTHERS

```

The default means that aggregate window functions read all
rows from the beginning of the partition up to and including the
current row and its peers. This implies that rows that have the same values for
all ORDER BY expressions will also have the same value for the result of the
window function (as the window frame is the same). For example:




```
-- The following SELECT statement returns:
-- 
--   a | b | c | group_concat
-----------------------------
--   1 | A | one   | A.D.G       
--   2 | B | two   | A.D.G.C.F.B.E
--   3 | C | three | A.D.G.C.F   
--   4 | D | one   | A.D.G       
--   5 | E | two   | A.D.G.C.F.B.E
--   6 | F | three | A.D.G.C.F   
--   7 | G | one   | A.D.G       
-- 
SELECT a, b, c,
       group_concat(b, '.') OVER (ORDER BY c) AS group_concat
FROM t1 ORDER BY a;

```


### 2\.2\.1\. Frame Type



There are three frame types: ROWS, GROUPS, and RANGE.
The frame type determines how the starting and ending boundaries
of the frame are measured.



* **ROWS**:
The ROWS frame type means that the starting and ending boundaries
for the frame are determined by counting individual rows relative
to the current row.
* **GROUPS**:
The GROUPS frame type means that the starting and ending boundaries
are determine by counting "groups" relative to the current group.
A "group" is a set of rows that all have equivalent values for all
all terms of the window ORDER BY clause. ("Equivalent" means that
the [IS operator](lang_expr.html#isisnot) is true when comparing the two values.)
In other words, a group consists of all peers of a row.
* **RANGE**:
The RANGE frame type requires that the ORDER BY clause of the
window have exactly one term. Call that term "X". With the
RANGE frame type, the elements of the frame are determined by
computing the value of expression X for all rows in the partition
and framing those rows for which the value of X is within a certain
range of the value of X for the current row. See the description
in the "[\<expr\> PRECEDING](windowfunctions.html#exprrange)" boundary
specification below for details.


The ROWS and GROUPS frame types are similar in that they
both determine the extent of a frame by counting relative to
the current row. The difference is that ROWS counts individual
rows and GROUPS counts peer groups.
The RANGE frame type is different.
The RANGE frame type determines the extent of a frame by
looking for expression values that are within some band of
values relative to the current row.




### 2\.2\.2\. Frame Boundaries


 There are five ways to describe starting and ending frame boundaries:



1. **UNBOUNDED PRECEDING**  

 The frame boundary is the first
 row in the [partition](windowfunctions.html#ptxn).
2. **\<expr\> PRECEDING**  

 \<expr\> must be a non\-negative constant numeric expression.
 The boundary is a row that is \<expr\> "units" prior to
 the current row. The meaning of "units" here depends on the
 frame type:
 


	* **ROWS →**
	 The frame boundary is the row that is \<expr\>
	 rows before the current row, or the first row of the
	 partition if there are fewer than \<expr\> rows
	 before the current row. \<expr\> must be an integer.
	* **GROUPS →**
	 A "group" is a set of peer rows \- rows that all have
	 the same values for every term in the ORDER BY clause.
	 The frame boundary is the group that is \<expr\>
	 groups before the group containing the current row, or the
	 first group of the partition if there are fewer
	 than \<expr\> groups before the current row.
	 For the starting boundary of a frame, the first
	 row of the group is used and for the ending boundary
	 of a frame, the last row of the group is used.
	 \<expr\> must be an integer.
	* **RANGE →**
	 For this form, the ORDER BY clause of the
	 window\-defn must have a single
	 term. Call that ORDER BY term "X". Let
	 Xi be the value of the X
	 expression for the i\-th row in the partition and let
	 Xc be the value of X for the
	 current row. Informally, a RANGE bound is the first row
	 for which Xi is within
	 the \<expr\> of Xc.
	 More precisely:
	 
	
	
		1. If either Xi or
		 Xc are non\-numeric, then
		 the boundary is the first row for which the expression
		 "Xi IS Xc"
		 is true.
		2. Else if the ORDER BY is ASC then the boundary
		 is the first row for which
		 Xi\>\=Xc\-\<expr\>.
		3. Else if the ORDER BY is DESC then the boundary
		 is the first row for which
		 Xi\<\=Xc\+\<expr\>.
	 For this form, the \<expr\> does not have to be an
	 integer. It can evaluate to a real number as long as
	 it is constant and non\-negative.
 The boundary description "0 PRECEDING" always means the same
 thing as "CURRENT ROW".
3. **CURRENT ROW**  

 The current row. For RANGE and GROUPS frame types,
 peers of the current row are also included in the frame,
 unless specifically excluded by the EXCLUDE clause.
 This is true regardless of whether CURRENT ROW is used
 as the starting or ending frame boundary.
4. **\<expr\> FOLLOWING**  

 This is the same as "\<expr\> PRECEDING" except that
 the boundary is \<expr\> units after the current
 rather than before the current row.
5. **UNBOUNDED FOLLOWING**  

 The frame boundary is the last
 row in the [partition](windowfunctions.html#ptxn).


 The ending frame boundary may not take a form that appears higher in
the above list than the starting frame boundary.



 In the following example, the window frame for each row consists of all
rows from the current row to the end of the set, where rows are sorted
according to "ORDER BY a".




```
-- The following SELECT statement returns:
-- 
--   c     | a | b | group_concat
---------------------------------
--   one   | 1 | A | A.D.G.C.F.B.E
--   one   | 4 | D | D.G.C.F.B.E 
--   one   | 7 | G | G.C.F.B.E   
--   three | 3 | C | C.F.B.E     
--   three | 6 | F | F.B.E       
--   two   | 2 | B | B.E         
--   two   | 5 | E | E           
-- 
SELECT c, a, b, group_concat(b, '.') OVER (
  ORDER BY c, a ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
) AS group_concat
FROM t1 ORDER BY c, a;

```


### 2\.2\.3\. The EXCLUDE Clause


 The optional EXCLUDE clause may take any of the following four forms:



* **EXCLUDE NO OTHERS**: This is the default. In this case no
 rows are excluded from the window frame as defined by its starting and ending
 frame boundaries.
* **EXCLUDE CURRENT ROW**: In this case the current row is
 excluded from the window frame. Peers of the current row remain in
 the frame for the GROUPS and RANGE frame types.
* **EXCLUDE GROUP**: In this case the current row and all other
 rows that are peers of the current row are excluded from the frame. When
 processing an EXCLUDE clause, all rows with the same ORDER BY values, or all
 rows in the partition if there is no ORDER BY clause, are considered peers,
 even if the frame type is ROWS.
* **EXCLUDE TIES**: In this case the current row is part of the
 frame, but peers of the current row are excluded.


 The following example demonstrates the effect of the various
forms of the EXCLUDE clause:




```
-- The following SELECT statement returns:
-- 
--   c    | a | b | no_others     | current_row | grp       | ties
--  one   | 1 | A | A.D.G         | D.G         |           | A
--  one   | 4 | D | A.D.G         | A.G         |           | D
--  one   | 7 | G | A.D.G         | A.D         |           | G
--  three | 3 | C | A.D.G.C.F     | A.D.G.F     | A.D.G     | A.D.G.C
--  three | 6 | F | A.D.G.C.F     | A.D.G.C     | A.D.G     | A.D.G.F
--  two   | 2 | B | A.D.G.C.F.B.E | A.D.G.C.F.E | A.D.G.C.F | A.D.G.C.F.B
--  two   | 5 | E | A.D.G.C.F.B.E | A.D.G.C.F.B | A.D.G.C.F | A.D.G.C.F.E
-- 
SELECT c, a, b,
  group_concat(b, '.') OVER (
    ORDER BY c GROUPS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE NO OTHERS
  ) AS no_others,
  group_concat(b, '.') OVER (
    ORDER BY c GROUPS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE CURRENT ROW
  ) AS current_row,
  group_concat(b, '.') OVER (
    ORDER BY c GROUPS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE GROUP
  ) AS grp,
  group_concat(b, '.') OVER (
    ORDER BY c GROUPS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE TIES
  ) AS ties
FROM t1 ORDER BY c, a;

```

## 2\.3\. The FILTER Clause


**[filter\-clause:](syntax/filter-clause.html)**
hide








FILTER



(



WHERE



expr



)





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










If a FILTER clause is provided, then only rows for which the *expr* is
true are included in the window frame. The aggregate window still returns a
value for every row, but those for which the FILTER expression evaluates to
other than true are not included in the window frame for any row. For example:




```
-- The following SELECT statement returns:
-- 
--   c     | a | b | group_concat
---------------------------------
--   one   | 1 | A | A           
--   two   | 2 | B | A           
--   three | 3 | C | A.C         
--   one   | 4 | D | A.C.D       
--   two   | 5 | E | A.C.D       
--   three | 6 | F | A.C.D.F     
--   one   | 7 | G | A.C.D.F.G   
-- 
SELECT c, a, b, group_concat(b, '.') FILTER (WHERE c!='two') OVER (
  ORDER BY a
) AS group_concat
FROM t1 ORDER BY a;

```


# 3\. Built\-in Window Functions


 As well as aggregate window functions, SQLite features a set of built\-in
window functions based on
[those supported by PostgreSQL](https://www.postgresql.org/docs/10/static/functions-window.html).



 Built\-in window functions honor any PARTITION BY clause in the same way
as aggregate window functions \- each selected row is assigned to a partition
and each partition is processed separately. The ways in which any ORDER BY
clause affects each built\-in window function is described below. Some of
the window functions (rank(), dense\_rank(), percent\_rank() and ntile()) use
the concept of "peer groups" (rows within the same partition that have the
same values for all ORDER BY expressions). In these cases, it does not matter
whether the frame\-spec specifies ROWS, GROUPS, or RANGE.
For the purposes of built\-in window function processing, rows with the same values
for all ORDER BY expressions are considered peers regardless of the frame type.



 Most built\-in window functions ignore the
frame\-spec, the exceptions being first\_value(),
last\_value() and nth\_value(). It is a syntax error to specify a FILTER
clause as part of a built\-in window function invocation.




 SQLite supports the following 11 built\-in window functions:




**row\_number()**


 The number of the row within the current partition. Rows are
 numbered starting from 1 in the order defined by the ORDER BY clause in
 the window definition, or in arbitrary order otherwise.
 

**rank()**


 The row\_number() of the first peer in each group \- the rank of the
 current row with gaps. If there is no ORDER BY clause, then all rows
 are considered peers and this function always returns 1\.
 

**dense\_rank()**


 The number of the current row's peer group within its partition \- the
 rank of the current row without gaps. Rows are numbered starting
 from 1 in the order defined by the ORDER BY clause in the window
 definition. If there is no ORDER BY clause, then all rows are
 considered peers and this function always returns 1\.
 

**percent\_rank()**


 Despite the name, this function always returns a value between 0\.0
 and 1\.0 equal to (*rank* \- 1\)/(*partition\-rows* \- 1\), where
 *rank* is the value returned by built\-in window function rank()
 and *partition\-rows* is the total number of rows in the
 partition. If the partition contains only one row, this function
 returns 0\.0\.
 

**cume\_dist()**


 The cumulative distribution. Calculated as
 *row\-number*/*partition\-rows*, where *row\-number* is
 the value returned by row\_number() for the last peer in the group
 and *partition\-rows* the number of rows in the partition.
 

**ntile(N)**


 Argument *N* is handled as an integer. This function divides the
 partition into N groups as evenly as possible and assigns an integer
 between 1 and *N* to each group, in the order defined by the ORDER
 BY clause, or in arbitrary order otherwise. If necessary, larger groups
 occur first. This function returns the integer value assigned to the
 group that the current row is a part of.

 

**lag(expr)  
lag(expr, offset)  
lag(expr, offset, default)**


 The first form of the lag() function returns the result of evaluating
 expression *expr* against the previous row in the partition. Or, if
 there is no previous row (because the current row is the first), NULL.

 

 If the *offset* argument is provided, then it must be a
 non\-negative integer. In this case the value returned is the result
 of evaluating *expr* against the row *offset* rows before the
 current row within the partition. If *offset* is 0, then
 *expr* is evaluated against the current row. If there is no row
 *offset* rows before the current row, NULL is returned.

 

 If *default* is also provided, then it is returned instead of
 NULL if the row identified by *offset* does not exist.

 

**lead(expr)  
lead(expr, offset)  
lead(expr, offset, default)**


 The first form of the lead() function returns the result of evaluating
 expression *expr* against the next row in the partition. Or, if
 there is no next row (because the current row is the last), NULL.

 

 If the *offset* argument is provided, then it must be a
 non\-negative integer. In this case the value returned is the result
 of evaluating *expr* against the row *offset* rows after the
 current row within the partition. If *offset* is 0, then
 *expr* is evaluated against the current row. If there is no row
 *offset* rows after the current row, NULL is returned.

 

 If *default* is also provided, then it is returned instead of
 NULL if the row identified by *offset* does not exist.
 

**first\_value(expr)**


 This built\-in window function calculates the window frame for each
 row in the same way as an aggregate window function. It returns the
 value of *expr* evaluated against the first row in the window frame
 for each row.
 

**last\_value(expr)**


 This built\-in window function calculates the window frame for each
 row in the same way as an aggregate window function. It returns the
 value of *expr* evaluated against the last row in the window frame
 for each row.
 

**nth\_value(expr, N)**


 This built\-in window function calculates the window frame for each
 row in the same way as an aggregate window function. It returns the
 value of *expr* evaluated against the row *N* of the window
 frame. Rows are numbered within the window frame starting from 1 in
 the order defined by the ORDER BY clause if one is present, or in
 arbitrary order otherwise. If there is no *N*th row in the
 partition, then NULL is returned.
 



The examples in this section use the
[previously defined T1 table](windowfunctions.html#aggwinfunc)
as well as the following T2 table:




```
CREATE TABLE t2(a, b);
INSERT INTO t2 VALUES('a', 'one'),
                     ('a', 'two'),
                     ('a', 'three'),
                     ('b', 'four'),
                     ('c', 'five'),
                     ('c', 'six');

```

The following example illustrates the behaviour of the five ranking
functions \- row\_number(), rank(), dense\_rank(), percent\_rank() and
cume\_dist().




```
-- The following SELECT statement returns:
-- 
--   a | row_number | rank | dense_rank | percent_rank | cume_dist
------------------------------------------------------------------
--   a |          1 |    1 |          1 |          0.0 |       0.5
--   a |          2 |    1 |          1 |          0.0 |       0.5
--   a |          3 |    1 |          1 |          0.0 |       0.5
--   b |          4 |    4 |          2 |          0.6 |       0.66
--   c |          5 |    5 |          3 |          0.8 |       1.0
--   c |          6 |    5 |          3 |          0.8 |       1.0
-- 
SELECT a                        AS a,
       row_number() OVER win    AS row_number,
       rank() OVER win          AS rank,
       dense_rank() OVER win    AS dense_rank,
       percent_rank() OVER win  AS percent_rank,
       cume_dist() OVER win     AS cume_dist
FROM t2
WINDOW win AS (ORDER BY a);

```

The example below uses ntile() to divide the six rows into two groups (the
ntile(2\) call) and into four groups (the ntile(4\) call). For ntile(2\), there
are three rows assigned to each group. For ntile(4\), there are two groups of
two and two groups of one. The larger groups of two appear first.




```
-- The following SELECT statement returns:
-- 
--   a | b     | ntile_2 | ntile_4
----------------------------------
--   a | one   |       1 |       1
--   a | two   |       1 |       1
--   a | three |       1 |       2
--   b | four  |       2 |       2
--   c | five  |       2 |       3
--   c | six   |       2 |       4
-- 
SELECT a                        AS a,
       b                        AS b,
       ntile(2) OVER win        AS ntile_2,
       ntile(4) OVER win        AS ntile_4
FROM t2
WINDOW win AS (ORDER BY a);

```

 The next example demonstrates lag(), lead(), first\_value(), last\_value()
and nth\_value(). The frame\-spec is ignored by
both lag() and lead(), but respected by first\_value(), last\_value()
and nth\_value().




```
-- The following SELECT statement returns:
-- 
--   b | lead | lag  | first_value | last_value | nth_value_3
-------------------------------------------------------------
--   A | C    | NULL | A           | A          | NULL       
--   B | D    | A    | A           | B          | NULL       
--   C | E    | B    | A           | C          | C          
--   D | F    | C    | A           | D          | C          
--   E | G    | D    | A           | E          | C          
--   F | n/a  | E    | A           | F          | C          
--   G | n/a  | F    | A           | G          | C          
-- 
SELECT b                          AS b,
       lead(b, 2, 'n/a') OVER win AS lead,
       lag(b) OVER win            AS lag,
       first_value(b) OVER win    AS first_value,
       last_value(b) OVER win     AS last_value,
       nth_value(b, 3) OVER win   AS nth_value_3
FROM t1
WINDOW win AS (ORDER BY b ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

```


# 4\. Window Chaining



Window chaining is a shorthand that allows one window to be defined in terms
of another. Specifically, the shorthand allows the new window to implicitly
copy the PARTITION BY and optionally ORDER BY clauses of the base window. For
example, in the following:




```
SELECT group_concat(b, '.') OVER (
  win ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
FROM t1
WINDOW win AS (PARTITION BY a ORDER BY c)

```


the window used by the group\_concat() function is equivalent
to "PARTITION BY a ORDER BY c ROWS BETWEEN UNBOUNDED PRECEDING
AND CURRENT ROW". In order to use window
chaining, all of the following must be true:



* The new window definition must not include a PARTITION BY clause. The
 PARTITION BY clause, if there is one, must be supplied by the base
 window specification.
* If the base window has an ORDER BY clause, it is copied into the new
 window. In this case the new window must not specify an ORDER BY clause.
 If the base window has no ORDER BY clause, one may be specified as part
 of the new window definition.
* The base window may not specify a frame specification. The frame
 specification can only be given in the new window specification.


The two fragments of SQL below are similar, but not entirely equivalent, as
the latter will fail if the definition of window "win" contains a frame
specification.




```
SELECT group_concat(b, '.') OVER win ...
SELECT group_concat(b, '.') OVER (win) ...

```


# 5\. User\-Defined Aggregate Window Functions


 User\-defined aggregate window functions may be created using the
[sqlite3\_create\_window\_function](c3ref/create_function.html)() API. Implementing an aggregate window
function is very similar to an ordinary aggregate function. Any user\-defined
aggregate window function may also be used as an ordinary aggregate. To
implement a user\-defined aggregate window function the application must
supply four callback functions:





| Callback | Description |
| --- | --- |
| xStep | This method is required by both window aggregate and legacy aggregate  function implementations. It is invoked to add a row to the current  window. The function arguments, if any, corresponding to the row being  added are passed to the implementation of xStep. |
| xFinal | This method is required by both window aggregate and legacy aggregate  function implementations. It is invoked to return the current value  of the aggregate (determined by the contents of the current window),  and to free any resources allocated by earlier calls to xStep. |
| xValue | This method is only required for window aggregate functions. The presence  of this method is what distinguishes a window aggregate function from a  legacy aggregate function. This method is invoked to return the current  value of the aggregate. Unlike xFinal, the implementation should not  delete any context. |
| xInverse | This method is only required for window aggregate functions, not legacy  aggregate function implementations. It is invoked to remove the oldest  presently aggregated result of xStep from the current window.  The function arguments, if any, are those  passed to xStep for the row being removed. |


 The C code below implements a simple window aggregate function named
sumint(). This works in the same way as the built\-in sum() function, except
that it throws an exception if passed an argument that is not an integer
value.




```

```

/*
** xStep for sumint().
**
** Add the value of the argument to the aggregate context (an integer).
*/
static void sumintStep(
  [sqlite3_context](c3ref/context.html) *ctx,
  int nArg,
  [sqlite3_value](c3ref/value.html) *apArg[]
){
  [sqlite3_int64](c3ref/int64.html) *pInt;

  assert( nArg==1 );
  if( [sqlite3_value_type](c3ref/value_blob.html)(apArg[0])!=SQLITE_INTEGER ){
    [sqlite3_result_error](c3ref/result_blob.html)(ctx, "invalid argument", -1);
    return;
  }
  pInt = (sqlite3_int64*)sqlite3_aggregate_context(ctx, sizeof([sqlite3_int64](c3ref/int64.html)));
  if( pInt ){
    *pInt += [sqlite3_value_int64](c3ref/value_blob.html)(apArg[0]);
  }
}

/*
** xInverse for sumint().
**
** This does the opposite of xStep() - subtracts the value of the argument
** from the current context value. The error checking can be omitted from
** this function, as it is only ever called after xStep() (so the aggregate
** context has already been allocated) and with a value that has already
** been passed to xStep() without error (so it must be an integer).
*/
static void sumintInverse(
  [sqlite3_context](c3ref/context.html) *ctx,
  int nArg,
  [sqlite3_value](c3ref/value.html) *apArg[]
){
  [sqlite3_int64](c3ref/int64.html) *pInt;
  assert( [sqlite3_value_type](c3ref/value_blob.html)(apArg[0])==SQLITE_INTEGER );
  pInt = (sqlite3_int64*)sqlite3_aggregate_context(ctx, sizeof([sqlite3_int64](c3ref/int64.html)));
  *pInt -= [sqlite3_value_int64](c3ref/value_blob.html)(apArg[0]);
}

/*
** xFinal for sumint().
**
** Return the current value of the aggregate window function. Because
** this implementation does not allocate any resources beyond the buffer
** returned by [sqlite3_aggregate_context](c3ref/aggregate_context.html), which is automatically freed
** by the system, there are no resources to free. And so this method is
** identical to xValue().
*/
static void sumintFinal([sqlite3_context](c3ref/context.html) *ctx){
  [sqlite3_int64](c3ref/int64.html) res = 0;
  [sqlite3_int64](c3ref/int64.html) *pInt;
  pInt = (sqlite3_int64*)[sqlite3_aggregate_context](c3ref/aggregate_context.html)(ctx, 0);
  if( pInt ) res = *pInt;
  [sqlite3_result_int64](c3ref/result_blob.html)(ctx, res);
}

/*
** xValue for sumint().
**
** Return the current value of the aggregate window function.
*/
static void sumintValue([sqlite3_context](c3ref/context.html) *ctx){
  [sqlite3_int64](c3ref/int64.html) res = 0;
  [sqlite3_int64](c3ref/int64.html) *pInt;
  pInt = (sqlite3_int64*)[sqlite3_aggregate_context](c3ref/aggregate_context.html)(ctx, 0);
  if( pInt ) res = *pInt;
  [sqlite3_result_int64](c3ref/result_blob.html)(ctx, res);
}

/*
** Register sumint() window aggregate with database handle db.
*/
int register_sumint([sqlite3](c3ref/sqlite3.html) *db){
  return [sqlite3_create_window_function](c3ref/create_function.html)(db, "sumint", 1, SQLITE_UTF8, 0,
      sumintStep, sumintFinal, sumintValue, sumintInverse, 0
  );
}

```



```

 The following example uses the sumint() function implemented by the above
C code. For each row, the window consists of the preceding row (if any), the current row and the following row (again, if any):




```
CREATE TABLE t3(x, y);
INSERT INTO t3 VALUES('a', 4),
                     ('b', 5),
                     ('c', 3),
                     ('d', 8),
                     ('e', 1);

-- Assuming the database is populated using the above script, the 
-- following SELECT statement returns:
-- 
--   x | sum_y
--------------
--   a | 9    
--   b | 12   
--   c | 16   
--   d | 12   
--   e | 9    
-- 
SELECT x, sumint(y) OVER (
  ORDER BY x ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
) AS sum_y
FROM t3 ORDER BY x;

```

In processing the query above, SQLite invokes the sumint callbacks as
follows:






1. **xStep(4\)** \- add "4" to the current window.
2. **xStep(5\)** \- add "5" to the current window.
3. **xValue()** \- invoke xValue() to obtain the value of sumint() for
 the row with (x\='a'). The window currently consists of values 4 and 5,
 and so the result is 9\.
4. **xStep(3\)** \- add "3" to the current window.
5. **xValue()** \- invoke xValue() to obtain the value of sumint() for
 the row with (x\='b'). The window currently consists of values 4, 5 and
 3, and so the result is 12\.
6. **xInverse(4\)** \- remove "4" from the window.
7. **xStep(8\)** \- add "8" to the current window. The window now consists
 of values 5, 3 and 8\.
8. **xValue()** \- invoked to obtain the value for the row with (x\='c').
 In this case, 16\.
9. **xInverse(5\)** \- remove value "5" from the window.
10. **xStep(1\)** \- add value "1" to the window.
11. **xValue()** \- invoked to obtain the value for row (x\='d').
12. **xInverse(3\)** \- remove value "3" from the window. The window now
 contains values 8 and 1 only.
13. **xFinal()** \- invoked to reclaim any allocated resources and to
 obtain the value for row (x\='e'). 9\. .


If the user were to abandon query execution by calling sqlite3\_reset() or
sqlite3\_finalize() on the statement handle before SQLite has called xFinal(),
then xFinal() is called automatically from within the sqlite3\_reset() or
sqlite3\_finalize() call in order to reclaim any allocated resources, even
though the value is not required. In this case any error returned by the xFinal
implementation is silently discarded.



# 6\. History


Window function support was first added to SQLite with release
[version 3\.25\.0](releaselog/3_25_0.html) (2018\-09\-15\). The SQLite developers used
the [PostgreSQL](http://www.postgresql.org) window function
documentation as their primary reference for how window functions
ought to behave. Many test cases have been run against PostgreSQL
to ensure that window functions operate the same way in both
SQLite and PostgreSQL.



In SQLite [version 3\.28\.0](releaselog/3_28_0.html) (2019\-04\-16\),
windows function support was extended to include the EXCLUDE clause,
GROUPS frame types, window chaining, and support for
"\<expr\> PRECEDING" and "\<expr\> FOLLOWING" boundaries
in RANGE frames.


*This page last modified on [2024\-04\-16 17:22:18](https://sqlite.org/docsrc/honeypot) UTC* 


