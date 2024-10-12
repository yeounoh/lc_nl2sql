




Quirks, Caveats, and Gotchas In SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Quirks, Caveats, and Gotchas In SQLite


►
Table Of Contents
[1\. Overview](#overview)
[2\. SQLite Is Embedded, Not Client\-Server](#sqlite_is_embedded_not_client_server)
[3\. Flexible Typing](#flexible_typing)
[3\.1\. No Separate BOOLEAN Datatype](#no_separate_boolean_datatype)
[3\.2\. No Separate DATETIME Datatype](#no_separate_datetime_datatype)
[3\.3\. The datatype is optional](#the_datatype_is_optional)
[4\. Foreign Key Enforcement Is Off By Default](#foreign_key_enforcement_is_off_by_default)
[5\. PRIMARY KEYs Can Sometimes Contain NULLs](#primary_keys_can_sometimes_contain_nulls)
[6\. Aggregate Queries Can Contain Non\-Aggregate Result Columns
That Are Not In The GROUP BY Clause](#aggregate_queries_can_contain_non_aggregate_result_columns_that_are_not_in_the_group_by_clause)
[7\. Does Not Do Full Unicode Case Folding By Default](#does_not_do_full_unicode_case_folding_by_default)
[8\. Double\-quoted String Literals Are Accepted](#double_quoted_string_literals_are_accepted)
[9\. Keywords Can Often Be Used As Identifiers](#keywords_can_often_be_used_as_identifiers)
[10\. Dubious SQL Is Allowed Without Any Error Or Warning](#dubious_sql_is_allowed_without_any_error_or_warning)
[11\. AUTOINCREMENT Does Not Work The Same As MySQL](#autoincrement_does_not_work_the_same_as_mysql)
[12\. NUL Characters Are Allowed In Text Strings](#nul_characters_are_allowed_in_text_strings)
[13\. SQLite Distinguishes Between Integer And Text Literals](#sqlite_distinguishes_between_integer_and_text_literals)
[14\. SQLite Gets The Precedence Of Comma\-Joins Wrong](#sqlite_gets_the_precedence_of_comma_joins_wrong)




# 1\. Overview



The SQL language is a "standard".
Even so, no two SQL database engines work exactly alike.
Every SQL implementation has it own peculiarities and oddities,
and SQLite is no exception to this rule.




This document strives to highlight the principal differences
between SQLite and other SQL implementations, as an aid to developers
that are porting to or from SQLite or who are trying to build a
system that works across multiple database engines.




If you are an SQLite user whose has stumbled over some quirk of
SQLite that is not mentioned here, please let the developers know
by posting a brief message on the
[SQLite Forum](https://sqlite.org/forum/forum).



# 2\. SQLite Is Embedded, Not Client\-Server



Whenever comparing SQLite to other SQL database engines like
SQL Server, PostgreSQL, MySQL, or Oracle, it is important first of all
to realize that SQLite is not intended as a replacement or competitor to
any of those systems. SQLite is [serverless](serverless.html). There is no separate
server process that manages the database. An application interacts
with the database engine using function calls, not by sending messages
to a separate process or thread.




The fact that SQLite is embedded and [serverless](serverless.html) instead of being
client/server is a feature, not a bug.




Client/server databases like MySQL, PostgreSQL, SQL Server, Oracle, and
others are an important component of modern systems.
These systems solve an important problem.
But SQLite solves a different problem.
Both SQLite and client/server databases have their role.
Developers who are comparing SQLite against other SQL database engines need
to clearly understand this distinction.




See the [Appropriate Uses For SQLite](whentouse.html) document for additional information.



# 3\. Flexible Typing



SQLite is flexible with regard to datatypes. Datatypes are advisory
rather than mandatory.




Some commentators say that SQLite is "weakly typed" and that other
SQL databases are "strongly typed". We consider these terms to be
inaccurate and even pejorative. We prefer to say that SQLite is
"flexibly typed" and that other SQL database engines are
"rigidly typed".




See the [Datatypes in SQLite](datatype3.html) document for a detailed
discussion of the type system in SQLite.




The key point is that SQLite is very forgiving of the type of data that
you put into the database. For example, if a column has a datatype of
"INTEGER" and the application inserts a text string into that column,
SQLite will first try to convert the text string into an integer, just like
every other SQL database engine. Thus, if one inserts **'1234'** into
an INTEGER column, that value is converted into an integer 1234 and stored.
But, if you insert a non\-numeric string like **'wxyz'** into an INTEGER
column, unlike other SQL databases, SQLite does not throw an error. Instead,
SQLite stores the actual string value in the column.




Similarly, SQLite allows you to store a 2000\-character string into a
column of type VARCHAR(50\). Other SQL implementations would either throw
an error or truncate the string. SQLite stores the entire 2000\-character
string with no loss of information and without complaint.




Where this ends up causing problems is when developers do some initial
coding work using SQLite and get their application working, but then try
to convert to another database like PostgreSQL or SQL Server for deployment.
If the application is initially taking advantage of SQLite's flexible typing,
then it will fail when moved to another database that uses a more rigid
and unforgiving type enforcement policy.




[Flexible typing is a feature](flextypegood.html) of SQLite, not a bug. Flexible typing
is about freedom.
Nevertheless, we recognize that this feature does sometimes cause
confusion for developers who are accustomed to working with
other databases that are more strict with regard to data type rules.
In retrospect, perhaps it would have been less confusing if SQLite had merely
implemented an ANY datatype so that developers could explicitly state
when they wanted to use flexible typing, rather than making flexible
typing the default.
As an accommodation for those who expect rigid typing, SQLite version 3\.37\.0
(2021\-11\-27\) introduced the option of [STRICT tables](stricttables.html).
These either impose
the mandatory datatype constraints found in other SQL database engines,
or allow the explicit ANY datatype to retain SQLite's flexible typing.



## 3\.1\. No Separate BOOLEAN Datatype



Unlike most other SQL implementations,
SQLite does not have a separate BOOLEAN data type.
Instead, TRUE and FALSE are (normally) represented as integers 1 and 0,
respectively.
This does not seem to cause many problems, as we seldom get complaints
about it. But it is important to recognize.




Beginning with SQLite [version 3\.23\.0](releaselog/3_23_0.html) (2018\-04\-02\), SQLite also
recognizes TRUE and FALSE keywords as aliases for integer values 1 and 0,
respectively.
This provides better compatibility with other SQL implementations.
But for backwards compatibility, if there are columns named TRUE or
FALSE, then the keywords are treated as identifiers referencing those
columns, rather than BOOLEAN literals.



## 3\.2\. No Separate DATETIME Datatype



SQLite has no DATETIME datatype.
Instead, dates and times can be stored in any of these ways:



* As a TEXT string in the ISO\-8601 format. Example: '2018\-04\-02 12:13:46'.
* As an INTEGER number of seconds since 1970 (also known as "unix time").
* As a REAL value that is the fractional
 [Julian day number](https://en.wikipedia.org/wiki/Julian_day).



The built\-in [date and time functions](lang_datefunc.html) of SQLite understand date/times in
all of the formats above, and can freely change between them.
Which format you use, is entirely up to your application.



## 3\.3\. The datatype is optional



Because SQLite is flexible and forgiving with regard to datatypes,
table columns can be created that have no specified datatype at all.
For example:



```
CREATE TABLE t1(a,b,c,d);

```

The table "t1" has four columns "a", "b", "c", and "d" that have
no particular datatype assigned. You can store anything you want in
any of those columns.


# 4\. Foreign Key Enforcement Is Off By Default


SQLite has parsed foreign key constraints for time out of mind,
but added the ability to actually enforce those constraints much later,
with [version 3\.6\.19](releaselog/3_6_19.html) (2009\-10\-14\). By the time foreign key constraint
enforcement was added, there were already countless millions of databases
in circulation that contained foreign key constraints, some of which
were not correct. To avoid breaking those legacy databases, foreign key
constraint enforcement is turned off by default in SQLite.



Applications can activate foreign key enforcement at run\-time using
the [PRAGMA foreign\_keys](pragma.html#pragma_foreign_keys) statement. Or, foreign key enforcement can
be activated at compile\-time using the
[\-DSQLITE\_DEFAULT\_FOREIGN\_KEYS\=1](compile.html#default_foreign_keys) compile\-time option.



# 5\. PRIMARY KEYs Can Sometimes Contain NULLs



Usually (the exceptions are [INTEGER PRIMARY KEY](lang_createtable.html#rowid) tables and
[WITHOUT ROWID](withoutrowid.html) tables) a PRIMARY KEY in an SQLite table is really
the same as a UNIQUE constraint. Due to an historical oversight,
the column values of such a PRIMARY KEY are allowed to be NULL.
This is a bug, but by the time the problem was discovered there
where so many databases in circulation that depended on the bug that
the decision was made to support the buggy behavior moving forward.



The value of an [INTEGER PRIMARY KEY](lang_createtable.html#rowid) column must always be a
non\-NULL integer. The PRIMARY KEY columns of a [WITHOUT ROWID](withoutrowid.html)
table are also required to be non\-NULL.



# 6\. Aggregate Queries Can Contain Non\-Aggregate Result Columns
That Are Not In The GROUP BY Clause



In most SQL implementations, output columns of an aggregate query
may only reference aggregate functions or columns named in the
GROUP BY clause. It does not make good sense to reference an ordinary
column in an aggregate query because each output row might be composed
from two or more rows in the input table(s).




SQLite does not enforce this restriction.
The output columns from an aggregate query can be arbitrary expressions
that include columns not found in GROUP BY clause.
This feature has two uses:



1. With SQLite (but not any other SQL implementation that we know of) if
an aggregate query contains a single min() or max() function, then the
values of columns used in the output are taken from the row where
the min() or max() value was achieved. If two or more rows have the
same min() or max() value, then the columns values will be chosen arbitrarily
from one of those rows.



For example to find the highest paid employee:



```
SELECT max(salary), first_name, last_name FROM employee;

```


In the query above, the values for the first\_name and last\_name columns
will correspond to the row that satisfied the max(salary) condition.
2. If a query contains no aggregate functions at all, then a GROUP BY
clause can be added as a substitute for the DISTINCT ON clause. In other words,
output rows are filtered so that only one row is shown for each distinct
set of values in the GROUP BY clause. If two or more output rows would
have otherwise had the same set of values for the GROUP BY columns, then
one of the rows is chosen arbitrarily. (SQLite supports DISTINCT but not
DISTINCT ON, whose functionality is provided instead by GROUP BY.)


# 7\. Does Not Do Full Unicode Case Folding By Default



SQLite does not know about the upper\-case/lower\-case distinction
for all unicode characters. SQL functions like
upper() and lower() only work on ASCII characters. There are two
reasons for this:


1. Though stable now, when SQLite was first designed, the rules for
 unicode case folding were still in flux. That means that the
 behavior might have changed with each new unicode release, disrupting
 applications and corrupting indexes in the process.
2. The tables necessary to do full and proper unicode case folding are
 larger than the whole SQLite library.



Full unicode case folding is supported in SQLite if it is compiled
with the [\-DSQLITE\_ENABLE\_ICU](compile.html#enable_icu) option and linked against the
[International Components for Unicode](https://icu.unicode.org)
library.




# 8\. Double\-quoted String Literals Are Accepted



The SQL standard requires double\-quotes around identifiers
and single\-quotes around string literals. For example:


* "this is a legal SQL column name"
* 'this is an SQL string literal'



SQLite accepts both of the above. But, in an effort to be compatible
with MySQL 3\.x (which was one of the most widely used RDBMSes
when SQLite was first being designed) SQLite will also interpret
a double\-quotes string as
string literal if it does not match any valid identifier.



This misfeature means that a misspelled double\-quoted
identifier will be interpreted as a string literal, rather than generating
an error.
It also lures developers who are new to the SQL language into the
bad habit of using double\-quoted string literals when they
really need to learn to use the correct single\-quoted string literal form.



In hindsight, we should not have tried to make SQLite accept MySQL 3\.x
syntax, and should have never allowed double\-quoted string literals.
However, there are countless applications that make use of
double\-quoted string literals and so we continue to support
that capability to avoid breaking legacy.



As of SQLite 3\.27\.0 (2019\-02\-07\) the use of a double\-quoted
string literal causes a warning message to be sent to the [error log](errlog.html).



As of SQLite 3\.29\.0 (2019\-07\-10\) the use of double\-quoted
string literals can be disabled at run\-time using the
[SQLITE\_DBCONFIG\_DQS\_DDL](c3ref/c_dbconfig_defensive.html#sqlitedbconfigdqsddl) and [SQLITE\_DBCONFIG\_DQS\_DML](c3ref/c_dbconfig_defensive.html#sqlitedbconfigdqsdml) actions
to [sqlite3\_db\_config()](c3ref/db_config.html). The default settings can be altered
at compile\-time using the [\-DSQLITE\_DQS\=*N*](compile.html#dqs) compile\-time
option. Application developers are encouraged to compile using
\-DSQLITE\_DQS\=0 in order to disable the double\-quoted string literal
misfeature by default. If that is not possible, then disable
double\-quoted string literals for individual database connections
using C\-code like this:



> ```
> 
> sqlite3_db_config(db, SQLITE_DBCONFIG_DQS_DDL, 0, (void*)0);
> sqlite3_db_config(db, SQLITE_DBCONFIG_DQS_DML, 0, (void*)0);
> 
> ```


Or, if double\-quoted string literals are disabled by default, but need
to be selectively enabled for some historical database connections,
that can be done using the same C\-code as shown above except with the
third parameter changed from 0 to 1\.



As of SQLite 3\.41\.0 (2023\-02\-21\) SQLITE\_DBCONFIG\_DQS\_DDL and
SQLITE\_DBCONFIG\_DQS\_DML are disabled by default in the [CLI](cli.html). Use
the ".dbconfig" dot\-command to reenable the legacy behavior if
desired.



# 9\. Keywords Can Often Be Used As Identifiers



The SQL language is rich in keywords.
Most SQL implementations do not allow keywords to be used as identifiers
(names of tables or columns) unless they are enclosed in double\-quotes.
But SQLite is more flexible. Many keywords can be used as identifiers without
needing to be quoted, as long as those keywords are used in a context where
it is clear that they are intended to be an identifier.



For example, the following statement is valid in SQLite:



```
CREATE TABLE union(true INT, with BOOLEAN);

```


The same SQL statement will fail on every other SQL implementation that
we know of due to the use of keywords "union", "true", and "with" as
identifiers.



The ability to use keywords as identifiers promotes backwards compatibility.
As new keywords are added, legacy schemas that just happen to use those
keywords as table or column names continue to work. However, the ability
to use a keyword as an identifier sometimes leads to surprising outcomes.
For example:



```
CREATE TRIGGER AFTER INSERT ON tableX BEGIN
  INSERT INTO tableY(b) VALUES(new.a);
END;

```

The trigger created by the previous statement is named "AFTER"
and it is a "BEFORE" trigger. The "AFTER" token is used as an identifier
instead of as a keyword, as that is the only way to parse the statement.
Another example:



```
CREATE TABLE tableZ(INTEGER PRIMARY KEY);

```

The tableZ table has a single column named "INTEGER". That column
has no datatype specified, but it is the PRIMARY KEY.
The column is *not* the [INTEGER PRIMARY KEY](lang_createtable.html#rowid) for the table because
it has no datatype. The "INTEGER" token is used as an identifier for the
column name, not as a datatype keyword.


# 10\. Dubious SQL Is Allowed Without Any Error Or Warning



The original implementation of SQLite sought to follow
[Postel's Law](https://en.wikipedia.org/wiki/Robustness_principle) which
states in part "Be liberal in what you accept".
This used to be considered good design \- that a system would accept
dodgy inputs and try to do the best it could without complaining too much.
But lately, people have come to realize that it is sometimes better to
be strict in what you accept, so as to more easily find errors in the
input.





# 11\. AUTOINCREMENT Does Not Work The Same As MySQL


The [AUTOINCREMENT](autoinc.html) feature in SQLite works differently than
it does in MySQL. This often causes confusion for people who
initially learned SQL on MySQL and then start using SQLite, and
expect the two systems to work identically.



See the [SQLite AUTOINCREMENT documentation](autoinc.html) for
detailed instructions on what AUTOINCREMENT does and does not do
in SQLite.



# 12\. NUL Characters Are Allowed In Text Strings


NUL characters (ASCII code 0x00 and Unicode \\u0000\) may appear in
the middle of strings in SQLite. This can lead to unexpected behavior.
See the "[NUL characters in strings](nulinstr.html)" document for further information.



# 13\. SQLite Distinguishes Between Integer And Text Literals


SQLite says that the following query returns false:



```
SELECT 1='1';

```

It does this because an integer is not a string. 
Every other major SQL database engine says this is true, for reasons
that the creator of SQLite does not understand.



# 14\. SQLite Gets The Precedence Of Comma\-Joins Wrong


SQLite gives all join operators equal precedence and processes them
from left to right. But this is not quite correct. It should be that
comma\-joins have lower precedence than all others join operators.
In other words, a FROM clause like this:




> ... FROM a, b RIGHT JOIN c, d ...


This FROM clause should be parsed as follows:






JOIN





JOIN

D





RIGHT JOIN

A





B

C



But SQLite instead parses the FROM clause like this:






JOIN





RIGHT JOIN

D





JOIN

C





A

B



The problem can only makes a difference in the result when using
RIGHT OUTER JOIN or FULL OUTER JOIN in the same FROM clause with
comma\-joins, which rarely happens in practice. And
the problem can be easily overcome using parentheses in the FROM clause:




> ... FROM a, (b RIGHT JOIN c), d ...


*This page last modified on [2024\-05\-22 18:42:01](https://sqlite.org/docsrc/honeypot) UTC* 


