




UPSERT




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










UPSERT


# 1\. Syntax


**[upsert\-clause:](syntax/upsert-clause.html)**
hide









ON



CONFLICT



(



indexed\-column



)



WHERE



expr





DO





,



conflict target





UPDATE



SET



column\-name\-list



\=



expr



WHERE



expr




NOTHING






,








column\-name








**[column\-name\-list:](syntax/column-name-list.html)**
show








(





column\-name



)




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









**[indexed\-column:](syntax/indexed-column.html)**
show








column\-name



COLLATE



collation\-name





DESC








expr









ASC









# 2\. Description


UPSERT is a clause added to [INSERT](lang_insert.html) that causes the
INSERT to behave as an [UPDATE](lang_update.html) or a no\-op if the INSERT would violate
a uniqueness constraint.
UPSERT is not standard SQL. UPSERT in SQLite follows the
syntax established by PostgreSQL, with generalizations.



An UPSERT is an ordinary [INSERT](lang_insert.html) statement that is followed by
one or more ON CONFLICT clauses, as shown in the syntax diagram above.



The syntax in between the "ON CONFLICT" and "DO" keywords
is called the "conflict target". The conflict target specifies a
uniqueness constraint that will trigger the upsert. The conflict target
may be omitted on the last ON CONFLICT clause in the INSERT statement, but
is required for all other ON CONFLICT clauses.



If the insert operation would cause the conflict target uniqueness
constraint to fail, then the insert is omitted and
the corresponding DO NOTHING or DO UPDATE operation is performed instead.
The ON CONFLICT clauses are checked in the order specified. If the last
ON CONFLICT clause omits the conflict target, then it will fire if any
uniqueness constraint fails which is not captured by prior ON CONFLICT clauses.



Only a single ON CONFLICT clause, specifically the first ON CONFLICT
clause with a matching conflict target, may run for each row of the INSERT.
When an ON CONFLICT clause fires, all subsequent ON CONFLICT clauses are
bypassed for that one row.




In the case of a multi\-row insert, the upsert decision is made separately
for each row of the insert.



The UPSERT processing happens only for uniqueness constraints.
A "uniqueness constraint"
is an explicit UNIQUE or PRIMARY KEY constraint within
the CREATE TABLE statement, or a [unique index](lang_createindex.html#uniqueidx).
UPSERT does not intervene for failed NOT NULL, CHECK,
or foreign key constraints
or for constraints that are implemented using triggers.



Column names in the expressions of a DO UPDATE refer to the original
unchanged value of the column, before the attempted INSERT. To use the
value that would have been inserted had the constraint not failed,
add the special "excluded." table qualifier to the column name.



## 2\.1\. Examples


Some examples will help illustrate how UPSERT works:




> ```
> 
> CREATE TABLE vocabulary(word TEXT PRIMARY KEY, count INT DEFAULT 1);
> INSERT INTO vocabulary(word) VALUES('jovial')
>   ON CONFLICT(word) DO UPDATE SET count=count+1;
> 
> ```


The upsert above inserts the new vocabulary word "jovial" if that
word is not already in the dictionary, or if it is already in the
dictionary, it increments the counter. The "count\+1" expression
could also be written as "vocabulary.count". PostgreSQL requires the
second form, but SQLite accepts either.




> ```
> 
> CREATE TABLE phonebook(name TEXT PRIMARY KEY, phonenumber TEXT);
> INSERT INTO phonebook(name,phonenumber) VALUES('Alice','704-555-1212')
>   ON CONFLICT(name) DO UPDATE SET phonenumber=excluded.phonenumber;
> 
> ```


In the second example, the expression in the DO UPDATE clause is
of the form "excluded.phonenumber". The "excluded." prefix causes the
"phonenumber" to refer to the value for phonenumber that would have been
inserted had there been no conflict. Hence, the effect of the upsert
is to insert a phonenumber of Alice if none exists, or to overwrite
any prior phonenumber for Alice with the new one.



Note that the DO UPDATE clause acts only on the single row
that experienced the constraint error during INSERT. It is not
necessary to include a WHERE clause that restricts the action
to that one row. The only use for the WHERE clause at
the end of the DO UPDATE is to optionally change the DO UPDATE
into a no\-op depending on the original and/or new values.
For example:




> ```
> 
> CREATE TABLE phonebook2(
>   name TEXT PRIMARY KEY,
>   phonenumber TEXT,
>   validDate DATE
> );
> INSERT INTO phonebook2(name,phonenumber,validDate)
>   VALUES('Alice','704-555-1212','2018-05-08')
>   ON CONFLICT(name) DO UPDATE SET
>     phonenumber=excluded.phonenumber,
>     validDate=excluded.validDate
>   WHERE excluded.validDate>phonebook2.validDate;
> 
> ```


In this last example, the phonebook2 entry is only
updated if the validDate for the newly inserted value is
newer than the entry already in the table. If the table already
contains an entry with the same name and a current validDate,
then the WHERE clause causes the DO UPDATE to become a no\-op.




## 2\.2\. Parsing Ambiguity


When the [INSERT](lang_insert.html) statement to which the UPSERT is attached
takes its values from a [SELECT](lang_select.html) statement, there is a potential
parsing ambiguity. The parser might not be able to tell if the
"ON" keyword is introducing the UPSERT or if it is the ON clause
of a join. To work around this, the SELECT statement should always
include a WHERE clause, even if that WHERE clause is just
"WHERE true".



Ambiguous use of ON:




> ```
> 
> INSERT INTO t1 SELECT * FROM t2
> ON CONFLICT(x) DO UPDATE SET y=excluded.y;
> 
> ```


Ambiguity resolved using a WHERE clause:




> ```
> 
> INSERT INTO t1 SELECT * FROM t2 WHERE true
> ON CONFLICT(x) DO UPDATE SET y=excluded.y;
> 
> ```


# 3\. Limitations


UPSERT does not currently work for [virtual tables](vtab.html).



The [conflict resolution algorithm](lang_conflict.html) for the update operation
of the DO UPDATE clause is always ABORT. In other words, the behavior
is as if the DO UPDATE clause were actually written as
"DO UPDATE OR ABORT". If the DO UPDATE clause encounters any
constraint violation, the entire INSERT statement rolls back and
halts. This is true even if the DO UPDATE clause is
contained within an INSERT statement or a trigger that specifies some
other conflict resolution algorithm.



# 4\. History


UPSERT syntax was added to SQLite with version 3\.24\.0 (2018\-06\-04\).
The original implementation closely followed the PostgreSQL syntax in that
it only permitted a single ON CONFLICT clause and it required a
conflict target for on DO UPDATE.
The syntax was generalized to permit multiple ON CONFLICT clauses and
to allow DO UPDATE resolution without a conflict target in
SQLite version 3\.35\.0 (2021\-03\-12\).


*This page last modified on [2024\-04\-11 23:26:09](https://sqlite.org/docsrc/honeypot) UTC* 


