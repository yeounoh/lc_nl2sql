




Built\-in Aggregate Functions




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Built\-in Aggregate Functions


# 1\. Syntax


**[aggregate\-function\-invocation:](syntax/aggregate-function-invocation.html)**
hide








aggregate\-func



(





DISTINCT







expr



)



filter\-clause












,





\*











ORDER



BY



ordering\-term

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









**[filter\-clause:](syntax/filter-clause.html)**
show








FILTER



(



WHERE



expr



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











The aggregate functions shown below are available by default. 
There are two more aggregates grouped with the [JSON SQL functions](json1.html).
Applications can define custom aggregate functions using the
[sqlite3\_create\_function()](c3ref/create_function.html) interface.
API.



In any aggregate function that takes a single argument, that argument
can be preceded by the keyword DISTINCT. In such cases, duplicate
elements are filtered before being passed into the aggregate function.
For example, the function "count(distinct X)" will return the number
of distinct values of column X instead of the total number of non\-null
values in column X.





If a FILTER clause is provided, then only rows for which the *expr* is
true are included in the aggregate.





If an ORDER BY clause is provided, that clause determines the order in which
the inputs to the aggregate are processed. For aggregate functions like max()
and count(), the input order does not matter. But for things like
[string\_agg()](lang_aggfunc.html#group_concat) and [json\_group\_object()](json1.html#jgroupobject), the ORDER BY clause will make a
difference in the result. If no ORDER BY clause is specified, the inputs to the
aggregate occur in an arbitrary order that might change from one invocation
to the next.




See also: [scalar functions](lang_corefunc.html) and [window functions](windowfunctions.html).




# 2\. List of built\-in aggregate functions



* [avg(X)](lang_aggfunc.html#avg)
* [count(\*)](lang_aggfunc.html#count)
* [count(X)](lang_aggfunc.html#count)
* [group\_concat(X)](lang_aggfunc.html#group_concat)
* [group\_concat(X,Y)](lang_aggfunc.html#group_concat)
* [max(X)](lang_aggfunc.html#max_agg)
* [min(X)](lang_aggfunc.html#min_agg)
* [string\_agg(X,Y)](lang_aggfunc.html#group_concat)
* [sum(X)](lang_aggfunc.html#sumunc)
* [total(X)](lang_aggfunc.html#sumunc)



# 3\. Descriptions of built\-in aggregate functions




**avg(*X*)**


 The avg() function
 returns the average value of all non\-NULL *X* within a
 group. String and BLOB values that do not look like numbers are
 interpreted as 0\.
 The result of avg() is always a floating point value whenever
 there is at least one non\-NULL input even if all
 inputs are integers. The result of avg() is NULL if
 there are no non\-NULL inputs. The result of avg() is computed
 as [total()](lang_aggfunc.html#sumunc)/[count()](lang_aggfunc.html#count) so all of the constraints that apply to
 [total()](lang_aggfunc.html#sumunc) also apply to avg().




**count(*X*)**


 The count(X) function returns
 a count of the number of times
 that *X* is not NULL in a group. The count(\*) function
 (with no arguments) returns the total number of rows in the group.




**group\_concat(*X*)  
group\_concat(*X*,*Y*)  
string\_agg(*X*,*Y*)**


 The group\_concat() function returns
 a string which is the concatenation of
 all non\-NULL values of *X*. If parameter *Y* is present then
 it is used as the separator
 between instances of *X*.A comma (",") is used as the separator
 if *Y* is omitted.
 
 The string\_agg(X,Y) function is an alias
 for group\_concat(X,Y). String\_agg() is compatible with PostgreSQL
 and SQL\-Server and group\_concat() is compatible with MySQL.
 
 The order of the concatenated elements is arbitrary unless an
 ORDER BY argument is included immediately after the last parameter.








**max(*X*)**


 The max() aggregate function
 returns the maximum value of all values in the group.
 The maximum value is the value that would be returned last in an
 ORDER BY on the same column. Aggregate max() returns NULL 
 if and only if there are no non\-NULL values in the group.




**min(*X*)**


 The min() aggregate function
 returns the minimum non\-NULL value of all values in the group.
 The minimum value is the first non\-NULL value that would appear
 in an ORDER BY of the column.
 Aggregate min() returns NULL if and only if there are no non\-NULL
 values in the group.




**sum(*X*)  
total(*X*)**


 The sum() and total() aggregate functions
 return the sum of all non\-NULL values in the group.
 If there are no non\-NULL input rows then sum() returns
 NULL but total() returns 0\.0\.
 NULL is not normally a helpful result for the sum of no rows
 but the SQL standard requires it and most other
 SQL database engines implement sum() that way so SQLite does it in the
 same way in order to be compatible. The non\-standard total() function
 is provided as a convenient way to work around this design problem
 in the SQL language.


The result of total() is always a floating point value.
 The result of sum() is an integer value if all non\-NULL inputs are integers.
 If any input to sum() is neither an integer nor a NULL,
 then sum() returns a floating point value
 which is an approximation of the mathematical sum.


Sum() will throw an "integer overflow" exception if all inputs
 are integers or NULL
 and an integer overflow occurs at any point during the computation.
 No overflow error is ever raised if any prior input was a floating point
 value.
 Total() never throws an integer overflow.

 When summing floating\-point values, if the magnitudes of the values
 differ wildly then the resulting sum might be imprecise due to the fact that
 [IEEE 754 floating point values are approximations](floatingpoint.html#fpapprox).
 Use the decimal\_sum(X) aggregate in the [decimal extension](floatingpoint.html#decext) to obtain
 an exact summation of floating point numbers. Consider this test case:


> ```
> 
> CREATE TABLE t1(x REAL);
> INSERT INTO t1 VALUES(1.55e+308),(1.23),(3.2e-16),(-1.23),(-1.55e308);
> SELECT sum(x), decimal_sum(x) FROM t1;
> 
> ```




The large values ±1\.55e\+308 cancel each other out, but the
 cancellation does not occur until the end of the sum and in the meantime
 the large \+1\.55e\+308 swamps the tiny 3\.2e\-16 value. The end result is
 an imprecise result for the sum(). The decimal\_sum() aggregate
 generates an exact answer, at the cost of additional CPU and memory usage.
 Note also that decimal\_sum() is not built into the SQLite core; it is a
 [loadable extension](loadext.html).

 If sum of inputs is too large to represent as a IEEE 754 floating
 point value, then a \+Infinity or \-Infinity result may be returned.
 If very large values with differing signs are used
 such that the SUM() or TOTAL() function is
 unable to determine if the correct result is \+Infinity or \-Infinity
 or some other value in between, then the result is NULL. Hence, for
 example, the following query returns NULL:


> ```
> 
> WITH t1(x) AS (VALUES(1.0),(-9e+999),(2.0),(+9e+999),(3.0))
>  SELECT sum(x) FROM t1;
> 
> ```














*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


