




SQLite Database Speed Comparison




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







## Database Speed Comparison


**Note: This document is very very old. It describes a speed comparison between
archaic versions of SQLite, MySQL and PostgreSQL.

The numbers here have become meaningless. This page has been retained only
as an historical artifact.**
### Executive Summary


A series of tests were run to measure the relative performance of
SQLite 2\.7\.6, PostgreSQL 7\.1\.3, and MySQL 3\.23\.41\.
The following are general
conclusions drawn from these experiments:



* SQLite 2\.7\.6 is significantly faster (sometimes as much as 10 or
 20 times faster) than the default PostgreSQL 7\.1\.3 installation
 on RedHat 7\.2 for most common operations.
* SQLite 2\.7\.6 is often faster (sometimes
 more than twice as fast) than MySQL 3\.23\.41
 for most common operations.
* SQLite does not execute CREATE INDEX or DROP TABLE as fast as
 the other databases. But this is not seen as a problem because
 those are infrequent operations.
* SQLite works best if you group multiple operations together into
 a single transaction.



The results presented here come with the following caveats:



* These tests did not attempt to measure multi\-user performance or
 optimization of complex queries involving multiple joins and subqueries.
* These tests are on a relatively small (approximately 14 megabyte) database.
 They do not measure how well the database engines scale to larger problems.


### Test Environment



The platform used for these tests is a 1\.6GHz Athlon with 1GB or memory
and an IDE disk drive. The operating system is RedHat Linux 7\.2 with
a stock kernel.




The PostgreSQL and MySQL servers used were as delivered by default on
RedHat 7\.2\. (PostgreSQL version 7\.1\.3 and MySQL version 3\.23\.41\.)
No effort was made to tune these engines. Note in particular
the default MySQL configuration on RedHat 7\.2 does not support
transactions. Not having to support transactions gives MySQL a
big speed advantage, but SQLite is still able to hold its own on most
tests.




I am told that the default PostgreSQL configuration in RedHat 7\.3
is unnecessarily conservative (it is designed to
work on a machine with 8MB of RAM) and that PostgreSQL could
be made to run a lot faster with some knowledgeable configuration
tuning.
Matt Sergeant reports that he has tuned his PostgreSQL installation
and rerun the tests shown below. His results show that
PostgreSQL and MySQL run at about the same speed. For Matt's
results, visit




> Obsolete URL: http://www.sergeant.org/sqlite\_vs\_pgsync.html



SQLite was tested in the same configuration that it appears
on the website. It was compiled with \-O6 optimization and with
the \-DNDEBUG\=1 switch which disables the many "assert()" statements
in the SQLite code. The \-DNDEBUG\=1 compiler option roughly doubles
the speed of SQLite.




All tests are conducted on an otherwise quiescent machine.
A simple Tcl script was used to generate and run all the tests.
A copy of this Tcl script can be found in the SQLite source tree
in the file **tools/speedtest.tcl**.




The times reported on all tests represent wall\-clock time
in seconds. Two separate time values are reported for SQLite.
The first value is for SQLite in its default configuration with
full disk synchronization turned on. With synchronization turned
on, SQLite executes
an **fsync()** system call (or the equivalent) at key points
to make certain that critical data has
actually been written to the disk drive surface. Synchronization
is necessary to guarantee the integrity of the database if the
operating system crashes or the computer powers down unexpectedly
in the middle of a database update. The second time reported for SQLite is
when synchronization is turned off. With synchronization off,
SQLite is sometimes much faster, but there is a risk that an
operating system crash or an unexpected power failure could
damage the database. Generally speaking, the synchronous SQLite
times are for comparison against PostgreSQL (which is also
synchronous) and the asynchronous SQLite times are for
comparison against the asynchronous MySQL engine.



### Test 1: 1000 INSERTs



> CREATE TABLE t1(a INTEGER, b INTEGER, c VARCHAR(100\));  
> 
> INSERT INTO t1 VALUES(1,13153,'thirteen thousand one hundred fifty three');  
> 
> INSERT INTO t1 VALUES(2,75560,'seventy five thousand five hundred sixty');  
> 
> *... 995 lines omitted*  
> 
> INSERT INTO t1 VALUES(998,66289,'sixty six thousand two hundred eighty nine');  
> 
> INSERT INTO t1 VALUES(999,24322,'twenty four thousand three hundred twenty two');  
> 
> INSERT INTO t1 VALUES(1000,94142,'ninety four thousand one hundred forty two');



| PostgreSQL: | 4\.373 |
| --- | --- |
| MySQL: | 0\.114 |
| SQLite 2\.7\.6: | 13\.061 |
| SQLite 2\.7\.6 (nosync): | 0\.223 |



Because it does not have a central server to coordinate access,
SQLite must close and reopen the database file, and thus invalidate
its cache, for each transaction. In this test, each SQL statement
is a separate transaction so the database file must be opened and closed
and the cache must be flushed 1000 times. In spite of this, the asynchronous
version of SQLite is still nearly as fast as MySQL. Notice how much slower
the synchronous version is, however. SQLite calls **fsync()** after
each synchronous transaction to make sure that all data is safely on
the disk surface before continuing. For most of the 13 seconds in the
synchronous test, SQLite was sitting idle waiting on disk I/O to complete.


### Test 2: 25000 INSERTs in a transaction



> BEGIN;  
> 
> CREATE TABLE t2(a INTEGER, b INTEGER, c VARCHAR(100\));  
> 
> INSERT INTO t2 VALUES(1,59672,'fifty nine thousand six hundred seventy two');  
> 
> *... 24997 lines omitted*  
> 
> INSERT INTO t2 VALUES(24999,89569,'eighty nine thousand five hundred sixty nine');  
> 
> INSERT INTO t2 VALUES(25000,94666,'ninety four thousand six hundred sixty six');  
> 
> COMMIT;



| PostgreSQL: | 4\.900 |
| --- | --- |
| MySQL: | 2\.184 |
| SQLite 2\.7\.6: | 0\.914 |
| SQLite 2\.7\.6 (nosync): | 0\.757 |



When all the INSERTs are put in a transaction, SQLite no longer has to
close and reopen the database or invalidate its cache between each statement.
It also does not
have to do any fsync()s until the very end. When unshackled in
this way, SQLite is much faster than either PostgreSQL and MySQL.



### Test 3: 25000 INSERTs into an indexed table



> BEGIN;  
> 
> CREATE TABLE t3(a INTEGER, b INTEGER, c VARCHAR(100\));  
> 
> CREATE INDEX i3 ON t3(c);  
> 
> *... 24998 lines omitted*  
> 
> INSERT INTO t3 VALUES(24999,88509,'eighty eight thousand five hundred nine');  
> 
> INSERT INTO t3 VALUES(25000,84791,'eighty four thousand seven hundred ninety one');  
> 
> COMMIT;



| PostgreSQL: | 8\.175 |
| --- | --- |
| MySQL: | 3\.197 |
| SQLite 2\.7\.6: | 1\.555 |
| SQLite 2\.7\.6 (nosync): | 1\.402 |



There were reports that SQLite did not perform as well on an indexed table.
This test was recently added to disprove those rumors. It is true that
SQLite is not as fast at creating new index entries as the other engines
(see Test 6 below) but its overall speed is still better.



### Test 4: 100 SELECTs without an index



> BEGIN;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=0 AND b\<1000;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=100 AND b\<1100;  
> 
> *... 96 lines omitted*  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=9800 AND b\<10800;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=9900 AND b\<10900;  
> 
> COMMIT;



| PostgreSQL: | 3\.629 |
| --- | --- |
| MySQL: | 2\.760 |
| SQLite 2\.7\.6: | 2\.494 |
| SQLite 2\.7\.6 (nosync): | 2\.526 |



This test does 100 queries on a 25000 entry table without an index,
thus requiring a full table scan. Prior versions of SQLite used to
be slower than PostgreSQL and MySQL on this test, but recent performance
enhancements have increased its speed so that it is now the fastest
of the group.



### Test 5: 100 SELECTs on a string comparison



> BEGIN;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE c LIKE '%one%';  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE c LIKE '%two%';  
> 
> *... 96 lines omitted*  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE c LIKE '%ninety nine%';  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE c LIKE '%one hundred%';  
> 
> COMMIT;



| PostgreSQL: | 13\.409 |
| --- | --- |
| MySQL: | 4\.640 |
| SQLite 2\.7\.6: | 3\.362 |
| SQLite 2\.7\.6 (nosync): | 3\.372 |



This test still does 100 full table scans but it uses
uses string comparisons instead of numerical comparisons.
SQLite is over three times faster than PostgreSQL here and about 30%
faster than MySQL.



### Test 6: Creating an index



> CREATE INDEX i2a ON t2(a);  
> CREATE INDEX i2b ON t2(b);



| PostgreSQL: | 0\.381 |
| --- | --- |
| MySQL: | 0\.318 |
| SQLite 2\.7\.6: | 0\.777 |
| SQLite 2\.7\.6 (nosync): | 0\.659 |



SQLite is slower at creating new indices. This is not a huge problem
(since new indices are not created very often) but it is something that
is being worked on. Hopefully, future versions of SQLite will do better
here.



### Test 7: 5000 SELECTs with an index



> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=0 AND b\<100;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=100 AND b\<200;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=200 AND b\<300;  
> 
> *... 4994 lines omitted*  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=499700 AND b\<499800;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=499800 AND b\<499900;  
> 
> SELECT count(\*), avg(b) FROM t2 WHERE b\>\=499900 AND b\<500000;



| PostgreSQL: | 4\.614 |
| --- | --- |
| MySQL: | 1\.270 |
| SQLite 2\.7\.6: | 1\.121 |
| SQLite 2\.7\.6 (nosync): | 1\.162 |



All three database engines run faster when they have indices to work with.
But SQLite is still the fastest.



### Test 8: 1000 UPDATEs without an index



> BEGIN;  
> 
> UPDATE t1 SET b\=b\*2 WHERE a\>\=0 AND a\<10;  
> 
> UPDATE t1 SET b\=b\*2 WHERE a\>\=10 AND a\<20;  
> 
> *... 996 lines omitted*  
> 
> UPDATE t1 SET b\=b\*2 WHERE a\>\=9980 AND a\<9990;  
> 
> UPDATE t1 SET b\=b\*2 WHERE a\>\=9990 AND a\<10000;  
> 
> COMMIT;



| PostgreSQL: | 1\.739 |
| --- | --- |
| MySQL: | 8\.410 |
| SQLite 2\.7\.6: | 0\.637 |
| SQLite 2\.7\.6 (nosync): | 0\.638 |



For this particular UPDATE test, MySQL is consistently
five or ten times
slower than PostgreSQL and SQLite. I do not know why. MySQL is
normally a very fast engine. Perhaps this problem has been addressed
in later versions of MySQL.



### Test 9: 25000 UPDATEs with an index



> BEGIN;  
> 
> UPDATE t2 SET b\=468026 WHERE a\=1;  
> 
> UPDATE t2 SET b\=121928 WHERE a\=2;  
> 
> *... 24996 lines omitted*  
> 
> UPDATE t2 SET b\=35065 WHERE a\=24999;  
> 
> UPDATE t2 SET b\=347393 WHERE a\=25000;  
> 
> COMMIT;



| PostgreSQL: | 18\.797 |
| --- | --- |
| MySQL: | 8\.134 |
| SQLite 2\.7\.6: | 3\.520 |
| SQLite 2\.7\.6 (nosync): | 3\.104 |



As recently as version 2\.7\.0, SQLite ran at about the same speed as
MySQL on this test. But recent optimizations to SQLite have more
than doubled speed of UPDATEs.



### Test 10: 25000 text UPDATEs with an index



> BEGIN;  
> 
> UPDATE t2 SET c\='one hundred forty eight thousand three hundred eighty two' WHERE a\=1;  
> 
> UPDATE t2 SET c\='three hundred sixty six thousand five hundred two' WHERE a\=2;  
> 
> *... 24996 lines omitted*  
> 
> UPDATE t2 SET c\='three hundred eighty three thousand ninety nine' WHERE a\=24999;  
> 
> UPDATE t2 SET c\='two hundred fifty six thousand eight hundred thirty' WHERE a\=25000;  
> 
> COMMIT;



| PostgreSQL: | 48\.133 |
| --- | --- |
| MySQL: | 6\.982 |
| SQLite 2\.7\.6: | 2\.408 |
| SQLite 2\.7\.6 (nosync): | 1\.725 |



Here again, version 2\.7\.0 of SQLite used to run at about the same speed
as MySQL. But now version 2\.7\.6 is over two times faster than MySQL and
over twenty times faster than PostgreSQL.




In fairness to PostgreSQL, it started thrashing on this test. A
knowledgeable administrator might be able to get PostgreSQL to run a lot
faster here by tweaking and tuning the server a little.



### Test 11: INSERTs from a SELECT



> BEGIN;  
> INSERT INTO t1 SELECT b,a,c FROM t2;  
> INSERT INTO t2 SELECT b,a,c FROM t1;  
> COMMIT;



| PostgreSQL: | 61\.364 |
| --- | --- |
| MySQL: | 1\.537 |
| SQLite 2\.7\.6: | 2\.787 |
| SQLite 2\.7\.6 (nosync): | 1\.599 |



The asynchronous SQLite is just a shade slower than MySQL on this test.
(MySQL seems to be especially adept at INSERT...SELECT statements.)
The PostgreSQL engine is still thrashing \- most of the 61 seconds it used
were spent waiting on disk I/O.



### Test 12: DELETE without an index



> DELETE FROM t2 WHERE c LIKE '%fifty%';



| PostgreSQL: | 1\.509 |
| --- | --- |
| MySQL: | 0\.975 |
| SQLite 2\.7\.6: | 4\.004 |
| SQLite 2\.7\.6 (nosync): | 0\.560 |



The synchronous version of SQLite is the slowest of the group in this test,
but the asynchronous version is the fastest.
The difference is the extra time needed to execute fsync().



### Test 13: DELETE with an index



> DELETE FROM t2 WHERE a\>10 AND a\<20000;



| PostgreSQL: | 1\.316 |
| --- | --- |
| MySQL: | 2\.262 |
| SQLite 2\.7\.6: | 2\.068 |
| SQLite 2\.7\.6 (nosync): | 0\.752 |



This test is significant because it is one of the few where
PostgreSQL is faster than MySQL. The asynchronous SQLite is,
however, faster then both the other two.



### Test 14: A big INSERT after a big DELETE



> INSERT INTO t2 SELECT \* FROM t1;



| PostgreSQL: | 13\.168 |
| --- | --- |
| MySQL: | 1\.815 |
| SQLite 2\.7\.6: | 3\.210 |
| SQLite 2\.7\.6 (nosync): | 1\.485 |



Some older versions of SQLite (prior to version 2\.4\.0\)
would show decreasing performance after a
sequence of DELETEs followed by new INSERTs. As this test shows, the
problem has now been resolved.



### Test 15: A big DELETE followed by many small INSERTs



> BEGIN;  
> 
> DELETE FROM t1;  
> 
> INSERT INTO t1 VALUES(1,10719,'ten thousand seven hundred nineteen');  
> 
> *... 11997 lines omitted*  
> 
> INSERT INTO t1 VALUES(11999,72836,'seventy two thousand eight hundred thirty six');  
> 
> INSERT INTO t1 VALUES(12000,64231,'sixty four thousand two hundred thirty one');  
> 
> COMMIT;



| PostgreSQL: | 4\.556 |
| --- | --- |
| MySQL: | 1\.704 |
| SQLite 2\.7\.6: | 0\.618 |
| SQLite 2\.7\.6 (nosync): | 0\.406 |



SQLite is very good at doing INSERTs within a transaction, which probably
explains why it is so much faster than the other databases at this test.



### Test 16: DROP TABLE



> DROP TABLE t1;  
> DROP TABLE t2;  
> DROP TABLE t3;



| PostgreSQL: | 0\.135 |
| --- | --- |
| MySQL: | 0\.015 |
| SQLite 2\.7\.6: | 0\.939 |
| SQLite 2\.7\.6 (nosync): | 0\.254 |



SQLite is slower than the other databases when it comes to dropping tables.
This probably is because when SQLite drops a table, it has to go through and
erase the records in the database file that deal with that table. MySQL and
PostgreSQL, on the other hand, use separate files to represent each table
so they can drop a table simply by deleting a file, which is much faster.




On the other hand, dropping tables is not a very common operation
so if SQLite takes a little longer, that is not seen as a big problem.



*This page last modified on [2023\-01\-02 14:22:42](https://sqlite.org/docsrc/honeypot) UTC* 


