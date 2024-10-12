




Indexes On Expressions




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Indexes On Expressions



Normally, an SQL index references columns of a table. But an index
can also be formed on expressions involving table columns.




As an example, consider the following table that tracks
dollar\-amount changes on various "accounts":




```
CREATE TABLE account_change(
  chng_id INTEGER PRIMARY KEY,
  acct_no INTEGER REFERENCES account,
  location INTEGER REFERENCES locations,
  amt INTEGER,  -- in cents
  authority TEXT,
  comment TEXT
);
CREATE INDEX acctchng_magnitude ON account_change(acct_no, abs(amt));

```


Each entry in the account\_change table records a deposit or a withdrawal
into an account. Deposits have a positive "amt" and withdrawals have
a negative "amt".




The acctchng\_magnitude index is over the account number ("acct\_no") and
on the absolute value of the amount. This index allows one to do 
efficient queries over the magnitude of a change to the account.
For example, to list all changes to account number $xyz that are
more than $100\.00, one can say:





```
SELECT * FROM account_change WHERE acct_no=$xyz AND abs(amt)>=10000;

```


Or, to list all changes to one particular account ($xyz) in order of
decreasing magnitude, one can write:




```
SELECT * FROM account_change WHERE acct_no=$xyz
 ORDER BY abs(amt) DESC;

```


Both of the above example queries would work fine without the
acctchng\_magnitude index.
The acctchng\_magnitude index merely helps the queries to run
faster, especially on databases where there are many entries in
the table for each account.



# 1\. How To Use Indexes On Expressions



Use a [CREATE INDEX](lang_createindex.html) statement to create a new index on one or more
expressions just like you would to create an index on columns. The only
difference is that expressions are listed as the elements to be indexed
rather than column names.




The SQLite query planner will consider using an index on an expression
when the expression that is indexed appears in the WHERE clause or in
the ORDER BY clause of a query, *exactly* as it is written in the
CREATE INDEX statement. The query planner does not do algebra. In order
to match WHERE clause constraints and ORDER BY terms to indexes, SQLite
requires that the expressions be the same, except for minor syntactic
differences such as white\-space changes. So if you have:




```
CREATE TABLE t2(x,y,z);
CREATE INDEX t2xy ON t2(x+y);

```


And then you run the query:




```
SELECT * FROM t2 WHERE y+x=22;

```


Then the index will not be used because 
the expression on the CREATE INDEX
statement (x\+y) is not the same as the expression as it appears in the 
query (y\+x). The two expressions might be mathematically equivalent, but
the SQLite query planner insists that they be the same, not merely
equivalent. Consider rewriting the query thusly:




```
SELECT * FROM t2 WHERE x+y=22;

```


This second query will likely use the index because now the expression
in the WHERE clause (x\+y) matches the expression in the index exactly.




# 2\. Restrictions



There are certain reasonable restrictions on expressions that appear in
CREATE INDEX statements:



1. Expressions in CREATE INDEX statements
may only refer to columns of the table being indexed, not to
columns in other tables.
2. Expressions in CREATE INDEX statements
may contain function calls, but only to functions whose output
is always determined completely by its input parameters (a.k.a.:
[deterministic functions](deterministic.html)). Obviously, functions like [random()](lang_corefunc.html#random) will not
work well in an index. But also functions like [sqlite\_version()](lang_corefunc.html#sqlite_version), though
they are constant across any one database connection, are not constant
across the life of the underlying database file, and hence may not be
used in a CREATE INDEX statement.




Note that [application\-defined SQL functions](appfunc.html) are by default considered
non\-deterministic and may not be used in a CREATE INDEX statement unless
the [SQLITE\_DETERMINISTIC](c3ref/c_deterministic.html#sqlitedeterministic) flag is used when the function is registered.
3. Expressions in CREATE INDEX statements may not use subqueries.
4. Expressions may only be used in CREATE INDEX statements, not within
[UNIQUE](lang_createtable.html#uniqueconst) or [PRIMARY KEY](lang_createtable.html#primkeyconst) constraints within the [CREATE TABLE](lang_createtable.html) statement.


# 3\. Compatibility



The ability to index expressions was added to SQLite with 
[version 3\.9\.0](releaselog/3_9_0.html) (2015\-10\-14\). A database that uses an index on
expressions will not be usable by earlier versions of SQLite.


*This page last modified on [2023\-02\-11 20:57:33](https://sqlite.org/docsrc/honeypot) UTC* 


