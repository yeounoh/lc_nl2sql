




Row Values




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Row Values


►
Table Of Contents
[1\. Definitions](#definitions)
[2\. Syntax](#syntax)
[2\.1\. Row Value Comparisons](#row_value_comparisons)
[2\.2\. Row Value IN Operators](#row_value_in_operators)
[2\.3\. Row Values In UPDATE Statements](#row_values_in_update_statements)
[3\. Example Uses Of Row Values](#example_uses_of_row_values)
[3\.1\. Scrolling Window Queries](#scrolling_window_queries)
[3\.2\. Comparison of dates stored as separate fields](#comparison_of_dates_stored_as_separate_fields)
[3\.3\. Search against multi\-column keys](#search_against_multi_column_keys)
[3\.4\. Update multiple columns of a table based on a query](#update_multiple_columns_of_a_table_based_on_a_query)
[3\.5\. Clarity of presentation](#clarity_of_presentation)
[4\. Backwards Compatibility](#backwards_compatibility)




# 1\. Definitions


A "value" is a single number, string, BLOB or NULL.
Sometimes the qualified name "scalar value" is used to emphasize that
only a single quantity is involved.



A "row value" is an ordered list of two or more scalar values.
In other words, a "row value" is a vector or tuple.



The "size" of a row value is the number of scalar values the row value contains.
The size of a row value is always at least 2\.
A row value with a single column is just a scalar value.
A row value with no columns is a syntax error.



# 2\. Syntax


SQLite allows row values to be expressed in two ways:


1. A parenthesized, comma\-separated list of scalar values.
2. A subquery expression with two or more result columns.


SQLite can use row values in two contexts:


1. Two row values of the same size 
can be compared using operators \<, \<\=, \>, \>\=,
\=, \<\>, IS, IS NOT, IN, NOT IN, BETWEEN, or CASE.
2. In an [UPDATE](lang_update.html) statement, a list of column names can be set to a row value of
the same size.


The syntax for row values and the circumstances in which row values
can be used are illustrated in examples below.



## 2\.1\. Row Value Comparisons


Two row values are compared by looking at the constituent scalar
values from left to right.
A NULL means of "unknown". 
The overall result of comparison is NULL if it is possible to make the
result either true or false by substituting alternative values in place
of the constituent NULLs.
The following query demonstrates some row value comparisons:




```
SELECT
  (1,2,3) = (1,2,3),          -- 1
  (1,2,3) = (1,NULL,3),       -- NULL
  (1,2,3) = (1,NULL,4),       -- 0
  (1,2,3) < (2,3,4),          -- 1
  (1,2,3) < (1,2,4),          -- 1
  (1,2,3) < (1,3,NULL),       -- 1
  (1,2,3) < (1,2,NULL),       -- NULL
  (1,3,5) < (1,2,NULL),       -- 0
  (1,2,NULL) IS (1,2,NULL);   -- 1

```

The result of "(1,2,3\)\=(1,NULL,3\)" is NULL because the result might be
true if we replaced NULL→2 or false if we replaced NULL→9\.
The result of "(1,2,3\)\=(1,NULL,4\)" is not NULL because there is no
substitutions of the constituent NULL that will make the expression true,
since 3 will never equal 4 in the third column.



Any of the row values in the previous example could be replace by a
subquery that returns three columns and the same answer would result.
For example:




```
CREATE TABLE t1(a,b,c);
INSERT INTO t1(a,b,c) VALUES(1,2,3);
SELECT (1,2,3)=(SELECT * FROM t1); -- 1

```


## 2\.2\. Row Value IN Operators


For a row\-value [IN operator](lang_expr.html#in_op), the left\-hand side (hereafter "LHS") can be either
a parenthesized list of values or a subquery with multiple columns. But the
right\-hand side (hereafter "RHS") must be a subquery expression.




```
CREATE TABLE t2(x,y,z);
INSERT INTO t2(x,y,z) VALUES(1,2,3),(2,3,4),(1,NULL,5);
SELECT
   (1,2,3) IN (SELECT * FROM t2),  -- 1
   (7,8,9) IN (SELECT * FROM t2),  -- 0
   (1,3,5) IN (SELECT * FROM t2);  -- NULL

```

## 2\.3\. Row Values In UPDATE Statements


Row values can also be used in the SET clause of an [UPDATE](lang_update.html) statement.
The LHS must be a list of column names. The RHS can be any row value.
For example:




```
UPDATE tab3 
   SET (a,b,c) = (SELECT x,y,z
                    FROM tab4
                   WHERE tab4.w=tab3.d)
 WHERE tab3.e BETWEEN 55 AND 66;

```

# 3\. Example Uses Of Row Values


## 3\.1\. Scrolling Window Queries


Suppose an application wants to display a list of contacts
in alphabetical order by lastname, firstname, in a scrolling window
that can only show 7 contacts at a time. Initialize the scrolling
window to the first 7 entries is easy:




```
SELECT * FROM contacts
 ORDER BY lastname, firstname
 LIMIT 7;

```

When the user scrolls down, the application needs to find the
second set of 7 entries. One way to do this is to use the OFFSET clause:




```
SELECT * FROM contacts
 ORDER BY lastname, firstname
 LIMIT 7 OFFSET 7;

```

OFFSET gives the correct answer. However, OFFSET requires time
proportional to the offset value. What really happens
with "LIMIT x OFFSET y" is that SQLite computes the query as
"LIMIT x\+y" and discards the first y values without returning them
to the application. So as the window scrolls down toward
the bottom of a long list, and the y value becomes larger and larger,
successive offset computations take more and more time.



A more efficient approach is to remember the last entry currently
displayed and then use a row value comparison in the WHERE
clause:




```
SELECT * FROM contacts
 WHERE (lastname,firstname) > (?1,?2)
 ORDER BY lastname, firstname
 LIMIT 7;

```

If the lastname and firstname on the bottom row of the previous
screen are bound to ?1 and ?2, then the query above computes the next
7 rows. And, assuming there is an appropriate index, it does so
very efficiently — much more efficiently than OFFSET.



## 3\.2\. Comparison of dates stored as separate fields


The usual way of storing a date in a database table is as a single
field, as either a unix timestamp, a julian day number, or an ISO\-8601
dates string. But some application store dates as three separate
fields for the year, month, and day. 




```
CREATE TABLE info(
  year INT,          -- 4 digit year
  month INT,         -- 1 through 12
  day INT,           -- 1 through 31
  other_stuff BLOB   -- blah blah blah
);

```

When dates are stored this way, row value comparisons provide a
convenient way to compare dates:




```
SELECT * FROM info
 WHERE (year,month,day) BETWEEN (2015,9,12) AND (2016,9,12);

```

## 3\.3\. Search against multi\-column keys


Suppose we want to know the order number, product number, and quantity
for any item in which the product number and quantity match the product
number and quantity of any item in order number 365:




```
SELECT ordid, prodid, qty
  FROM item
 WHERE (prodid, qty) IN (SELECT prodid, qty
                           FROM item
                          WHERE ordid = 365);

```

The query above could be rewritten as a join and without the use
of row values:




```
SELECT t1.ordid, t1.prodid, t1.qty
  FROM item AS t1, item AS t2
 WHERE t1.prodid=t2.prodid
   AND t1.qty=t2.qty
   AND t2.ordid=365;

```

Because the same query could be written without the use of row values,
row values do not provide new capabilities. However, many developers say
that the row value format is easier to read, write, and debug.



Even in the JOIN form, the query can be made clearer through the use of
row values:




```
SELECT t1.ordid, t1.prodid, t1.qty
  FROM item AS t1, item AS t2
 WHERE (t1.prodid,t1.qty) = (t2.prodid,t2.qty)
   AND t2.ordid=365;

```

This later query generates exactly the same [bytecode](opcode.html) as the previous
scalar formulation, but using syntax that it cleaner and
easier to read.



## 3\.4\. Update multiple columns of a table based on a query


The row\-value notation is useful for updating two or more columns
of a table from the result of a single query.
An example of this is in the full\-text search feature of the
[Fossil version control system](https://www.fossil-scm.org/).



In the Fossil full\-text search system,
documents that participate in the full\-text search (wiki pages, tickets,
check\-ins, documentation files, etc) are tracked by a table called
"ftsdocs" (full text search documents).
As new documents are added to the repository, they are not indexed right
away. Indexing is deferred until there is a search request. The
ftsdocs table contains an "idxed" field which is true if the document
has been indexed and false if not.



When a search request occurs and pending documents are indexed for the
first time, the ftsdocs table must be updated by setting the idxed column
to true and also filling in several other columns with information pertinent
to the search. That other information is obtained from a join. The
query is this:




```
UPDATE ftsdocs SET
  idxed=1,
  name=NULL,
  (label,url,mtime) = 
      (SELECT printf('Check-in [%%.16s] on %%s',blob.uuid,
                     datetime(event.mtime)),
              printf('/timeline?y=ci&c=%%.20s',blob.uuid),
              event.mtime
         FROM event, blob
        WHERE event.objid=ftsdocs.rid
          AND blob.rid=ftsdocs.rid)
WHERE ftsdocs.type='c' AND NOT ftsdocs.idxed

```

(See the 
[source code](https://www.fossil-scm.org/fossil/artifact/e5d6a82d?ln=1594-1605)
for further detail. Other examples
[here](https://www.fossil-scm.org/fossil/artifact/e5d6a82d?ln=1618-1628) and
[here](https://www.fossil-scm.org/fossil/artifact/e5d6a82d?ln=1641-1650).)



Five out of nine columns in the ftsdocs table are updated. Two of
the modified columns, "idxed" and "name", can be updated independently of
the query. But the three columns "label", "url", and "mtime" all require
a join query against the "event" and "blob" tables. Without row values,
the equivalent UPDATE would require that the join be repeated three times, 
once for each column to be updated.



## 3\.5\. Clarity of presentation


Sometimes the use of row values just makes the SQL easier to read
and write. Consider the following two UPDATE statements:




```
UPDATE tab1 SET (a,b)=(b,a);
UPDATE tab1 SET a=b, b=a;

```

Both UPDATE statements do exactly the same thing. (They generate
identical [bytecode](opcode.html).) But the first form, the row value form, seems
to make it clearer that the intent of the statement is to swap the
values in columns A and B.



Or consider these identical queries:




```
SELECT * FROM tab1 WHERE a=?1 AND b=?2;
SELECT * FROM tab1 WHERE (a,b)=(?1,?2);

```

Once again, the SQL statements generate identical bytecode and thus
do exactly the same job in exactly the same way. But the second form
is made easier for humans to read by grouping the query parameters together
into a single row value rather than scattering them across the WHERE
clause.



# 4\. Backwards Compatibility


Row values were added to SQLite
[version 3\.15\.0](releaselog/3_15_0.html) (2016\-10\-14\). Attempts to use row values in
prior versions of SQLite will generate syntax errors.


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


