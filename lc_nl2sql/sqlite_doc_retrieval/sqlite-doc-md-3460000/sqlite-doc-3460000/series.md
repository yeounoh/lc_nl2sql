




The generate\_series Table\-Valued Function




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The generate\_series Table\-Valued Function


►
Table Of Contents
[1\. Overview](#overview)
[1\.1\. Equivalent Recursive Common Table Expression](#equivalent_recursive_common_table_expression)
[2\. Usage Examples](#usage_examples)




# 1\. Overview


The generate\_series(START,STOP,STEP) [table\-valued function](vtab.html#tabfunc2) is a
[loadable extension](loadext.html) included in the SQLite source tree, and compiled into
the [command\-line shell](cli.html). The generate\_series() table has one visible
result column named "value" holding integer values
and a number of rows determined by the
parameters START, STOP, and STEP. The first row of the table has
a value of START. Subsequent rows increment by STEP to a value
not exceeding STOP.



The generate\_series() table has additional, hidden columns
named "start", "stop", and "step" whose values are the effective
values of START, STOP and STEP as provided or defaulted.
It also has a rowid, accessible by its usual names.



Omitted parameters take on default values. STEP defaults to 1\.
STOP defaults to 4294967295\. The START parameter is required
as of version 3\.37\.0 (2021\-11\-27\) and later and an error will
be raised if START is omitted or has a self\-referential or otherwise
uncomputable value. Older versions used a default of 0 for START.
The legacy behavior can be obtained from recent code by compiling
with \-DZERO\_ARGUMENT\_GENERATE\_SERIES.



## 1\.1\. Equivalent Recursive Common Table Expression


The generate\_series table can be simulated for positive step values
using a [recursive common table expression](lang_with.html#recursivecte). If the three parameters
are $start, $end, and $step, then the equivalent common table
expression is:




```
WITH RECURSIVE generate_series(value) AS (
  SELECT $start
  UNION ALL
  SELECT value+$step FROM generate_series
   WHERE value+$step<=$end
) ...

```

The common table expression works without having to load an
extension. On the other hand, the extension is easier to program
and faster.



# 2\. Usage Examples


Generate all multiples of 5 less than or equal to 100:




```
SELECT value FROM generate_series(5,100,5);

```

Generate the 20 random integer values:




```
SELECT random() FROM generate_series(1,20);

```

Find the name of every customer whose account number
 is an even multiple of 100 between 10000 and 20000\.




```
SELECT customer.name
  FROM customer, generate_series(10000,20000,100)
 WHERE customer.id=value;
/* or */
SELECT name FROM customer
 WHERE id IN (SELECT value
                FROM generate_series(10000,20000,200));

```

*This page last modified on [2023\-05\-01 21:49:55](https://sqlite.org/docsrc/honeypot) UTC* 


