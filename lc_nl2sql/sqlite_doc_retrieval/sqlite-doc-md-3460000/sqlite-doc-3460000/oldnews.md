




SQLite Older News




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







xml version\="1\.0" encoding\="Windows\-1252"?
### 2015\-11\-02 \- Release 3\.9\.2


> SQLite [version 3\.9\.2](releaselog/3_9_2.html) is a patch release fixing two obscure bugs.
> (Details: [(1\)](https://www.sqlite.org/src/tktview?name=8a2adec166),
> [(2\)](https://www.sqlite.org/src/tktview?name=ac661962a2)).
> Upgrade only if you are having problems.



---

### 2015\-10\-16 \- Release 3\.9\.1


> SQLite [version 3\.9\.1](releaselog/3_9_1.html) is a
> [small patch](https://www.sqlite.org/src/vpatch?from=version-3.9.0&to=version-3.9.1)
> to [version 3\.9\.0](releaselog/3_9_0.html) that includes
> a few simple build script and \#ifdef tweaks to make the code easier to
> compile on a wider variety of platform. There are no functional changes,
> except for a single
> [minor bug\-fix](https://www.sqlite.org/src/info/57eec374ae1d0a1d4a) in
> [the json1 extension](json1.html) to stop it from recognizing form\-feed
> (ASCII 0x0c) as a whitespace character, in conformance with
> [RFC7159](http://www.rfc-editor.org/rfc/rfc7159.txt).



---

### 2015\-10\-14 \- Release 3\.9\.0


> SQLite version 3\.9\.0 is a regularly schedule maintenance release.
> Key changes include:
> * Begin using [semantic versioning](http://semver.org/).
> * [JSON SQL functions](json1.html)* The [FTS5](fts5.html) full\-text search engine
> * Support for [indexes on expressions](expridx.html)* Support for [table\-valued functions](vtab.html#tabfunc2)
> 
> 
> See the [change log](releaselog/3_9_0.html) for a long and more complete list
> of changes.



---

### 2015\-07\-29 \- Release 3\.8\.11\.1


> SQLite version 3\.8\.11\.1 is a patch release that fixes two arcane
>  issues that were reported shortly after 3\.8\.11 was released. Upgrade
>  from 3\.8\.11 only in the unlikely event that one of these obscure
>  issues affect your code.



---

### 2015\-07\-27 \- Release 3\.8\.11


> SQLite version 3\.8\.11 is a regularly scheduled maintenance release.
>  See the [change log](releaselog/3_8_11.html) for details.



---

### 2015\-05\-20 \- Release 3\.8\.10\.2


> Yikes! Index corruption after a sequence of valid SQL statements!
> It has been many years since anything like
>  [this bug](https://www.sqlite.org/src/info/34cd55d6) has snuck into
>  an official SQLite release. But for the pasts seven months
>  ([version 3\.8\.7](releaselog/3_8_7.html) through [version 3\.8\.10\.1](releaselog/3_8_10_1.html))
>  if you do an INSERT into a carefully
>  crafted schema in which there are two nested triggers that convert
>  an index key value from TEXT to INTEGER and then back
>  to TEXT again, the INTEGER value might get inserted as the index
>  key instead of the correct TEXT, resulting in index corruption.
>  This patch release adds a single line of code to fix the problem.
> If you do actually encounter this problem, running [REINDEX](lang_reindex.html) on the
>  damaged indexes will clear it.



---

### 2015\-05\-09 \- Release 3\.8\.10\.1


> The 3\.8\.10 release did not add the new [SQLITE\_ENABLE\_DBSTAT\_VTAB](compile.html#enable_dbstat_vtab)
>  compile\-time option to the [sqlite3\_compileoption\_used()](c3ref/compileoption_get.html) interface.
>  This patch release fixes that omission. And while we are at it,
>  the associated [dbstat virtual table](dbstat.html) was enhanced slightly and a
>  harmless compiler warning was fixed.
> 
> 
>  There is no reason to upgrade from version 3\.8\.10 unless you are
>  using the new [SQLITE\_ENABLE\_DBSTAT\_VTAB](compile.html#enable_dbstat_vtab) compile\-time option.



---

### 2015\-05\-07 \- Release 3\.8\.10


> SQLite version 3\.8\.10 is a regularly scheduled maintenance release.
>  This release features performance improvements, fixes to several
>  arcane bugs found by the AFL fuzzer, the new "sqldiff.exe" command\-line
>  utility, improvements to the documentation, and other enhancements.
>  See the [release notes](releaselog/3_8_10.html) for
>  additional information.



---

### 2015\-04\-08 \- Release 3\.8\.9


> SQLite version 3\.8\.9 is a regularly scheduled maintenance release.
>  New features in this release include the
>  [PRAGMA index\_xinfo](pragma.html#pragma_index_xinfo) command, the [sqlite3\_status64()](c3ref/status.html) interface,
>  and the ".dbinfo" command of the [command\-line shell](cli.html).
>  See the [release notes](releaselog/3_8_9.html) for
>  additional information.



---

### 2015\-02\-25 \- Release 3\.8\.8\.3


> The 3\.8\.8\.3 patch release fixes an obscure problem in the SQLite code
>  generator that can cause incorrect results when the qualifying expression
>  of a [partial index](partialindex.html) is used inside the ON clause of a LEFT JOIN.
>  This problem has been in the code since support for partial indexes
>  was first added in version 3\.8\.0\. However, it is difficult to imagine
>  a valid reason to every put the qualifying constraint inside the ON
>  clause of a LEFT JOIN, and so this issue has never come up before.
> 
> 
> Any applications that is vulnerable to this bug would have encountered
>  problems already. Hence, upgrading from the previous release is optional.



---

### 2015\-01\-30 \- Release 3\.8\.8\.2


> The 3\.8\.8\.2 patch release fixes a single minor problem: It ensures
>  that the [sqlite3\_wal\_checkpoint(TRUNCATE)](c3ref/wal_checkpoint.html) operation will always truncate
>  the [write\-ahead log](wal.html) even if log had already been reset and contained
>  no new content. It is unclear if this is a bug fix or a new feature.
> 
> 
> Something like this would normally go into the next regularly scheduled
>  release, but a prominent SQLite user needed the change in a hurry so
>  we were happy to rush it out via this patch.
> 
> 
> There is no reason to upgrade unless you actually need the enhanced
>  behavior of [sqlite3\_wal\_checkpoint(TRUNCATE)](c3ref/wal_checkpoint.html).



---

### 2015\-01\-20 \- Release 3\.8\.8\.1


> Within hours of releasing version 3\.8\.8, a bug was reported against
>  the 10\-month\-old 3\.8\.4 release. As that bug exists in all subsequent
>  releases, the decision was made to issue a small patch to the
>  3\.8\.8 before it came into widespread use.
> 
> 
> See ticket
>  [f97c4637102a3ae72b7911](https://www.sqlite.org/src/info/f97c4637102a3ae72b7911)
>  for a description of the bug.
> 
> 
> The changes between versions 3\.8\.8 and 3\.8\.8\.1 are minimal.



---

### 2015\-01\-16 \- Release 3\.8\.8


> SQLite [version 3\.8\.8](releaselog/3_8_8.html) is a regularly schedule maintenance release of
>  SQLite.
> 
> 
> There are no dramatic new features or performance enhancements in this
>  release, merely incremental improvements. Most of the performance gain
>  in this release comes from refactoring the B\-Tree rebalancing logic to
>  avoid unnecessary memcpy() operations. New features include the
>  [PRAGMA data\_version](pragma.html#pragma_data_version) statement and the ability to accept a
>  [VALUES clause](lang_select.html#values) with no arbitrary limit on the number of rows.
>  Several obscure bugs have been fixed, including some multithreading
>  races and a work\-around for a compiler bug on some Macs.
> 
> 
> See the [change log](releaselog/3_8_8.html) for a longer list of
>  enhancements and bug fixes.



---

### 2014\-12\-09 \- Release 3\.8\.7\.4


> SQLite [version 3\.8\.7\.4](releaselog/3_8_7_4.html) an unscheduled bug\-fix release. Changes from
>  the previous release and from [version 3\.8\.7](releaselog/3_8_7.html) are minimal.
> 
> 
> This release fixes adds in a mutex that is required by the changes of
>  the 3\.8\.7\.3 patch but was accidentally omitted. The mutex was not required
>  by any of the internal SQLite tests, but Firefox crashes without it.
>  Test cases have been added to ensure that mutex is never again missed.



---

### 2014\-12\-06 \- Release 3\.8\.7\.3


> SQLite [version 3\.8\.7\.3](releaselog/3_8_7_3.html) an unscheduled bug\-fix release. Changes from
>  the previous release and from [version 3\.8\.7](releaselog/3_8_7.html) are minimal.
> 
> 
> This release fixes two obscure bugs that can result in incorrect
>  query results and/or application crashes, but not (as far as we can
>  tell) security vulnerabilities. Both bugs have been latent in the
>  code across multiple prior releases and have never before been encountered,
>  so they are unlikely to cause problems. Nevertheless
>  it seems prudent to publish fixes for them both. See the
>  change log for details.



---

### 2014\-11\-19 \- Release 3\.8\.7\.2


> SQLite [version 3\.8\.7\.2](releaselog/3_8_7_2.html) is a patch and bug\-fix release. Changes from
>  the previous release are minimal.
> 
> 
> The primary reason for this release is to enhance the [ROLLBACK](lang_transaction.html) command
>  so that it allows running queries on the same database connection to
>  continue running as long as the ROLLBACK does not change the schema.
>  In all previous versions of SQLite, a ROLLBACK would cause pending
>  queries to stop immediately and return [SQLITE\_ABORT](rescode.html#abort) or
>  [SQLITE\_ABORT\_ROLLBACK](rescode.html#abort_rollback). Pending queries still abort if the ROLLBACK
>  changes the database schema, but as of this patch release, the queries
>  are allowed to continue running if the schema is unmodified.
> 
> 
> In addition to the ROLLBACK enhancement, this patch release also
>  includes fixes for three obscure bugs. See the
>  [change log](releaselog/3_8_7_2.html) for details.



---

### 2014\-10\-30 \- Release 3\.8\.7\.1


> SQLite [version 3\.8\.7\.1](releaselog/3_8_7_1.html) is a bug\-fix release.
> 
> 
> The primary reason for this bug\-fix release is to address a problem with
>  updating the value of fields at the end of a table that were added
>  using [ALTER TABLE ADD COLUMN](lang_altertable.html). This problem
>  [1](https://www.sqlite.org/src/info/43107840f1c02) first appeared in the
>  3\.8\.7 release.
> 
> 
> Another minor annoyance in the 3\.8\.7 release was the fact that the
>  Android build tried to use the strchrnul() function from the standard
>  C library but that function is not available on Android. Android builds
>  had to add \-DHAVE\_STRCHRNUL\=0 to work around the problem. This patch
>  fixes that so that Android builds should now work without any changes.
> 
> 
> The operation of [PRAGMA journal\_mode\=TRUNCATE](pragma.html#pragma_journal_mode) has been enhanced so that
>  it invokes fsync() after truncating the journal file when
>  [PRAGMA synchronous\=FULL](pragma.html#pragma_synchronous). This helps to preserve transaction durability
>  in the case of a power loss occurring shortly after commit.
> 
> 
> Finally, a couple of long\-standing and obscure problems associated with run
>  UPDATE and DELETE on VIEWs were fixed.
> 
> 
> The [changes from 3\.8\.7](https://www.sqlite.org/src/vdiff?from=e4ab094f8afce0817f4074e823fabe59fc29ebb4&to=83afe23e553e802c0947c80d0ffdd120423e7c52&sbs=1) are minimal.



---

### 2014\-10\-17 \- Release 3\.8\.7


> SQLite [version 3\.8\.7](releaselog/3_8_7.html) is a regularly scheduled maintenance release.
>  Upgrading from all prior versions is recommended.
> 
> 
> Most of the changes from the previous release have been micro\-optimizations
>  designed to help SQLite run a little faster. Each individual optimization
>  has an unmeasurably small performance impact. But the improvements add up.
>  Measured on a well\-defined workload (which the SQLite developers use
>  as a proxy for a typical application workload) using cachegrind on Linux
>  and compiled with gcc 4\.8\.1 and \-Os on x64 linux, the current release
>  does over 20% more work for the same number of CPU cycles compared to the
>  previous release. Cachegrind is not a real CPU, and the workload
>  used for measurement is only a proxy. So your performance may vary.
>  We expect to see about half the measured and reported improvement in
>  real\-world applications. 10% is less than 20% but it is still pretty
>  good, we think.
> 
> 
> This release includes a new set of C\-language interfaces that have
>  unsigned 64\-bit instead of signed 32\-bit length parameters. The new
>  APIs do not provide any new capabilities. But they do make it easier
>  to write applications that are more resistant to integer overflow
>  vulnerabilities.
> 
> 
> This release also includes a new sorter that is able to use multiple
>  threads to help with large sort operations. (Sort operations are
>  sometimes required to implement ORDER BY and/or GROUP BY clauses and
>  are almost always required for CREATE INDEX.) The multi\-threads sorter
>  is turned off by default and must be enabled using the
>  [PRAGMA threads](pragma.html#pragma_threads) SQL command. Note that the multi\-threaded sorter
>  provides faster real\-time performance for large sorts, but it also
>  uses more CPU cycles and more energy.



---

### 2014\-08\-15 \- Release 3\.8\.6


> SQLite [version 3\.8\.6](releaselog/3_8_6.html) is a regularly scheduled maintenance release.
>  Upgrading from all previous versions is recommended.
> 
> 
> This release contains the usual assortment of obscure bug fixes.
>  One bug, however, deserves special attention.
>  A problem appeared in the [CREATE INDEX](lang_createindex.html) command beginning with
>  [version 3\.8\.2](releaselog/3_8_2.html) (2013\-12\-06\) that allowed, under some circumstances,
>  a UNIQUE index to be created on a column that was not unique. Once
>  the index was created, no new non\-unique entries could be inserted, but
>  preexisting non\-unique entries would remain. See ticket
>  [9a6daf340df99ba93c](https://www.sqlite.org/src/info/9a6daf340df99ba93c)
>  for further information. In addition to fixing this bug, the
>  [PRAGMA integrity\_check](pragma.html#pragma_integrity_check) command has been enhanced to detect
>  non\-uniqueness in UNIQUE indices, so that if this bug did introduce
>  any problems in databases, those problems can be easily detected.
> 
> 
> Other noteworthy changes include the addition of support for
>  [hexadecimal integers](lang_expr.html#hexint) (ex: 0x1234\), and performance enhancements
>  to the [IN operator](lang_expr.html#in_op) which, according to
>  [mailing list reports](http://www.mail-archive.com/sqlite-users%40sqlite.org/msg85350.html),
>  help some queries run up to five times faster.
> 
> 
> Version 3\.8\.6 uses 25% fewer CPU cycles than version 3\.8\.0 from
>  approximately one year ago, according to [valgrind](http://valgrind.org/)
>  and the
>  [test/speedtest1\.c](https://www.sqlite.org/src/artifact/d29c8048beb7e)
>  test program.
>  On the other hand,
>  the compiled binary for version 3\.8\.6 is about 5% larger than 3\.8\.0\.
>  The size increase is
>  due in part to the addition of new features such as [WITHOUT ROWID](withoutrowid.html)
>  tables and [common table expressions](lang_with.html).



---

### 2014\-06\-04 \- Release 3\.8\.5


> SQLite [version 3\.8\.5](releaselog/3_8_5.html) is a regularly scheduled maintenance release.
>  Upgrading from the previous version is recommended.
> 
> 
> Version 3\.8\.5 fixes more than a dozen obscure bugs. None of these
>  bugs should be a problem for existing applications. Nor do any of
>  the bugs represent a security vulnerability. Nevertheless, upgrading
>  is recommended to prevent future problems.
> 
> 
> In addition to bug fixes, the 3\.8\.5 release adds improvements to the
>  query planner, especially regarding sorting using indices and handling
>  OR terms
>  in the WHERE clause for WITHOUT ROWID tables. The ".system" and
>  ".once" dot\-commands were added to the command\-line interface. And
>  there were enhancements to the FTS4 and RTREE virtual tables. See
>  the change log for details.



---

### 2014\-04\-03 \- Release 3\.8\.4\.3


> The optimizations added in [version 3\.8\.4](releaselog/3_8_4.html) caused some queries that involve
>  subqueries in the FROM clause, DISTINCT, and ORDER BY clauses, to give an incorrect
>  result. See
>  [ticket 98825a79ce145](https://www.sqlite.org/src/info/98825a79ce145686392d8074032ae54863aa21a3)
>  for details.
>  This release adds a
>  [one\-character change](https://www.sqlite.org/src/fdiff?sbs=1&v1=7d539cedb1c&v2=ebad891b7494d&smhdr)
>  to a single line of code to fix the problem.



---

### 2014\-03\-26 \- Release 3\.8\.4\.2


> The code changes that resulted in the performance improvements
>  in [version 3\.8\.4](releaselog/3_8_4.html) missed a single buffer overflow test, which could
>  result in a read past the end of a buffer while searching a database
>  that is corrupted in a particular way. [Version 3\.8\.4\.2](releaselog/3_8_4_2.html) fixes that
>  problem using a
>  [one\-line patch](https://www.sqlite.org/src/fdiff?v1=e45e3f9daf38c5be&v2=714df4e1c82f629d&sbs=1).
> 
> 
> We are not aware of any problems in [version 3\.8\.4](releaselog/3_8_4.html)
>  when working with well\-formed database files. The problem fixed by this
>  release only comes up when reading corrupt database files.



---

### 2014\-03\-11 \- Release 3\.8\.4\.1


> SQLite [version 3\.8\.4\.1](releaselog/3_8_4_1.html) is a patch against [version 3\.8\.4](releaselog/3_8_4.html) that fixes
>  two minor issues:
> 1. Work around a C\-preprocessor macro conflict that causes compilation
>  problems for some configurations of Visual Studio.
> - Adjust the cost computation for the [skip\-scan optimization](optoverview.html#skipscan) for
>  improved performance.
> 
> 
> Both of these issues came to light within minutes of tagging the previous
> release. Neither issue is serious but they can be annoying. Hence, the
> decision was made to do a quick patch release to address both issues.



---

### 2014\-03\-10 \- Release 3\.8\.4


> SQLite [version 3\.8\.4](releaselog/3_8_4.html) is a maintenance release featuring performance
>  enhancements and fixes for a number of obscure bugs.
>  There are no significant new features in SQLite version 3\.8\.4\.
>  However, the number of CPU cycles (measured by valgrind) needed to
>  do many common operations has be reduced by about 12% relative to the
>  previous release, and by about 25% relative to [version 3\.7\.16](releaselog/3_7_16.html)
>  from approximately one year ago.
> 
> 
> Version 3\.8\.4 of SQLite fixes several corner\-case bugs that were
>  found since the previous release. These bugs were unlikely to appear
>  in practice, and none represent a security vulnerability.
>  Nevertheless, developers are encouraged to upgrade from all prior releases.



---

### 2014\-02\-11 \- Release 3\.8\.3\.1


> SQLite [version 3\.8\.3\.1](releaselog/3_8_3_1.html) fixes a bug present in versions 3\.8\.1,
>  3\.8\.2 and 3\.8\.3 that can cause queries to omit valid output rows.
>  Upgrading from those versions is recommended.
> 
> 
> The problem only comes up if SQLite is compiled with either the
>  [SQLITE\_ENABLE\_STAT3](compile.html#enable_stat3) or [SQLITE\_ENABLE\_STAT4](compile.html#enable_stat4) compile\-time options.
>  In that case, if a query has a WHERE clause that contains expressions
>  like this:
>  
> > WHERE (expr1 OR expr2 OR ... OR exprN) AND column IS NOT NULL
> 
> 
>  Where all of expr1 through exprN are suitable for use by indexes,
>  then during query planning SQLite might mistakenly converted
>  the "column IS NOT NULL" term into "column\>NULL". But the latter
>  term is never true, and so the query would return no rows.
> 
> 
> The trouble ticket for this bug is
>  \[[4c86b126f2](https://www.sqlite.org/src/info/4c86b126f2)].
>  It is recommended that all users upgrade to avoid this problem.



---

### 2014\-02\-03 \- Release 3\.8\.3


> SQLite [version 3\.8\.3](releaselog/3_8_3.html) is a regularly scheduled maintenance release.
>  Upgrading from the previous release is optional.
> 
> 
>  The most visible change in version 3\.8\.3 is the addition of
>  support for [common table expressions](lang_with.html). It is now possible to write a
>  single [SELECT](lang_select.html) statement that will query a tree or graph, using either
>  a depth\-first or a breadth\-first search. A single SQLite query will
>  even [solve Sudoku puzzles](lang_with.html#sudoku) or [compute the Mandelbrot set](lang_with.html#mandelbrot). As part
>  of this change, SQLite now accepts a [VALUES clause](lang_select.html#values) anyplace that
>  a [SELECT](lang_select.html) statement is valid.
> 
> 
>  This release also includes many small performance enhancements which
>  should give a small speed boost to legacy applications. And there are
>  other minor enhancements such as the addition of the [printf()](lang_corefunc.html#printf) SQL
>  function. See the [change log](releaselog/3_8_3.html) for details.



---

### 2013\-12\-06 \- Release 3\.8\.2


> SQLite [version 3\.8\.2](releaselog/3_8_2.html) is a regularly scheduled maintenance release.
>  Upgrading from the previous release is optional.
> 
> 
>  Version 3\.8\.2 adds support for [WITHOUT ROWID](withoutrowid.html) tables. This is a
>  significant extension to SQLite. Database files that contain WITHOUT ROWID
>  tables are not readable or writable by prior versions of SQLite, however
>  databases that do not use WITHOUT ROWID tables are fully backwards
>  and forwards compatible.
> 
> 
>  The 3\.8\.2 release contains a potentially incompatible change. In
>  all prior versions of SQLite, a [cast](lang_expr.html#castexpr) from a very large positive
>  floating point number into an integer resulted in the most negative integer.
>  In other words, CAST(\+99\.9e99 to INT) would yield \-9223372036854775808\.
>  This behavior came about because it is what x86/x64 hardware does
>  for the equivalent cast in the C language. But the behavior is
>  bizarre. And so it has been changed effective with this release so that
>  a cast from a floating point number into an integer returns the integer
>  between the floating point value and zero that is closest to the floating
>  point value. Hence, CAST(\+99\.9e99 to INT) now returns \+9223372036854775807\.
>  Since routines like [sqlite3\_column\_int64()](c3ref/column_blob.html) do an implicit cast if the
>  value being accessed is really a floating point number, they are also
>  affected by this change.
> 
> 
>  Besides the two changes mentioned above, the 3\.8\.2 release also
>  includes a number of performance enhancements. The
>  [skip\-scan optimization](optoverview.html#skipscan) is now available for databases that have been
>  processed by [ANALYZE](lang_analyze.html). Constant SQL functions are now factored out of
>  inner loops, which can result in a significant speedup for queries that
>  contain WHERE clause terms like "date\>datetime('now','\-2 days')". And
>  various high\-runner internal routines have been refactored for reduced
>  CPU load.



---

### 2013\-10\-17 \- Release 3\.8\.1


> SQLite [version 3\.8\.1](releaselog/3_8_1.html) is a regularly scheduled maintenance release.
>  Upgrading from the previous release is optional, though you should upgrade
>  if you are using [partial indices](partialindex.html) as there was a
>  [bug](https://www.sqlite.org/src/info/a5c8ed66ca) related to partial
>  indices in the previous release that could result in an incorrect answer
>  for count(\*) queries.
> 
> 
>  The [next generation query planner](queryplanner-ng.html) that was premiered in the previous
>  release continues to work well.
>  The new query planner has been tweaked slightly
>  in the current release to help it make better decisions in some
>  cases, but is largely unchanged. Two new SQL functions, [likelihood()](lang_corefunc.html#likelihood) and
>  [unlikely()](lang_corefunc.html#unlikely), have been added to allow developers to give hints to the
>  query planner without forcing the query planner into a particular decision.
> 
> 
>  Version 3\.8\.1 is the first SQLite release to take into account the
>  estimated size of table and index rows when choosing a query plan.
>  Row size estimates are based on the declared datatypes of columns.
>  For example, a column of type VARCHAR(1000\) is assumed
>  to use much more space than a column of type INT. The datatype\-based
>  row size estimate can be
>  overridden by appending a term of the form "sz\=NNN" (where NNN is the
>  average row size in bytes) to the end of the [sqlite\_stat1\.stat](fileformat2.html#stat1tab)
>  record for a table or index. Currently, row sizes are only used to help the
>  query planner choose between a table or one of its indices when doing a
>  table scan or a count(\*) operation, though future releases are likely
>  to use the estimated row size in other contexts as well. The new
>  [PRAGMA stats](pragma.html#pragma_stats) statement can be used to view row size estimates.
> 
> 
>  Version 3\.8\.1 adds the [SQLITE\_ENABLE\_STAT4](compile.html#enable_stat4) compile\-time option.
>  STAT4 is very similar to STAT3 in that it uses samples from indices to
>  try to guess how many rows of the index will be satisfy by WHERE clause
>  constraints. The difference is that STAT4 samples all columns of the
>  index whereas the older STAT3 only sampled the left\-most column. Users
>  of STAT3 are encouraged to upgrade to STAT4\. Application developers should
>  use STAT3 and STAT4 with caution since both options, by design, violate
>  the [query planner stability guarantee](queryplanner-ng.html#qpstab), making it more difficult to ensure
>  uniform performance is widely\-deployed and mass\-produced embedded
>  applications.



---

### 2013\-09\-03 \- Release 3\.8\.0\.2


> SQLite [version 3\.8\.0\.2](releaselog/3_8_0_2.html) contains a one\-line fix to a bug in the
>  new optimization that tries to omit unused LEFT JOINs from a query.



---

### 2013\-08\-29 \- Release 3\.8\.0\.1


> SQLite [version 3\.8\.0\.1](releaselog/3_8_0_1.html) fixes some obscure bugs that were uncovered by
>  users in the 3\.8\.0 release. Changes from 3\.8\.0 are minimal.



---

### 2013\-08\-26 \- Release 3\.8\.0


> **Do not fear the zero!**
>  SQLite [version 3\.8\.0](releaselog/3_8_0.html) might easily have been called "3\.7\.18" instead.
>  However, this release features the cutover of the
>  [next generation query planner](queryplanner-ng.html) or [NGQP](queryplanner-ng.html), and there is a small chance of
>  [breaking legacy programs](queryplanner-ng.html#hazards) that
>  rely on undefined behavior in previous SQLite releases, and so the
>  minor version number was incremented for that reason.
>  But the risks are low and there is a [query planner checklist](queryplanner-ng.html#howtofix) is
>  available to application developers to aid in avoiding problems.
> 
> 
>  SQLite [version 3\.8\.0](releaselog/3_8_0.html) is actually one of the most heavily tested
>  SQLite releases ever. Thousands and thousands of beta copies have
>  be downloaded, and presumably tested, and there have been no problem
>  reports.
> 
> 
>  In addition to the [next generation query planner](queryplanner-ng.html), the 3\.8\.0 release
>  adds support for [partial indices](partialindex.html), as well as several other new features.
>  See the [change log](releaselog/3_8_0.html) for further detail.



---

### 2013\-05\-20 \- Release 3\.7\.17


> SQLite [version 3\.7\.17](releaselog/3_7_17.html) is a regularly schedule maintenance release.
>  Visit the [change log](releaselog/3_7_17.html) for a full explanation of the
>  changes in this release.
>  There are many bug fixes in version 3\.7\.17\. But this does not indicate
>  that 3\.7\.16 was a problematic release. All of the bugs in 3\.7\.17 are
>  obscure and are unlikely to impact any particular application. And most
>  of the bugs that are fixed in 3\.7\.17 predate 3\.7\.16 and have been in
>  the code for years without ever before being noticed.
>  Nevertheless, due to the large number of fixes,
>  all users are encouraged to upgrade when possible.



---

### 2013\-04\-12 \- Release 3\.7\.16\.2


> SQLite [version 3\.7\.16\.2](releaselog/3_7_16_2.html) fixes a long\-standing flaw in the Windows
>  OS interface that
>  can result in database corruption under a rare race condition.
>  See <https://www.sqlite.org/src/info/7ff3120e4f> for a full description
>  of the problem.
>  As far as we know, this bug has never been seen in the wild. The
>  problem was discovered by the SQLite developers while writing stress tests
>  for a separate component of SQLite. Those stress tests have not yet
>  found any problems with the component they were intended to verify, but
>  they did find the bug which is the subject of this patch release.
> 
> 
>  Other than updates to version numbers, the only difference between this
>  release and 3\.7\.16\.1 is a two\-character change in a single identifier,
>  which is contained in the windows\-specific OS interface logic. There
>  are no changes in this release (other than version numbers) for platforms
>  other than Windows.



---

### 2013\-03\-29 \- Release 3\.7\.16\.1


> SQLite [version 3\.7\.16\.1](releaselog/3_7_16_1.html) is a bug fix release that fixes a few problems
>  that were present in the previous releases.
>  The primary motivation for version 3\.7\.16\.1 is to fix a bug in the
>  query optimizer that was introduced as part of [version 3\.7\.15](releaselog/3_7_15.html). The
>  query optimizer was being a little overzealous in optimizing out some
>  ORDER BY clauses, which resulted in sorting being omitted on occasions
>  where sorting is required to get the correct answer. See
>  ticket [a179fe7465](https://www.sqlite.org/src/info/a179fe7465) for
>  details.
> 
> 
>  In addition to the ORDER BY fix, several other patches to fix obscure
>  (and mostly harmless) bugs and to fix spelling errors in source code
>  comments are also included in this release.



---

### 2013\-03\-18 \- Release 3\.7\.16


> SQLite [version 3\.7\.16](releaselog/3_7_16.html) is a regularly scheduled release of SQLite.
>  This release contains several language enhancements and improvements
>  to the query optimizer. A list of the major enhancements and optimizations
>  can be see on the [change log](releaselog/3_7_16.html).
>  There was one important bug fix
>  (see [Ticket fc7bd6358f](https://www.sqlite.org/src/info/fc7bd6358f))
>  that addresses an incorrect query result that could have occurred in
>  a three\-way join where the join constraints compared INTEGER columns
>  to TEXT columns. This issue had been in the code for time out of mind
>  and had never before been reported, so we surmise that it is very obscure.
>  Nevertheless, all users are advised to upgrade to avoid any future problems
>  associated with this issue.



---

### 2013\-01\-09 \- Release 3\.7\.15\.2


> SQLite [version 3\.7\.15\.2](releaselog/3_7_15_2.html) is a patch release that fixes a single bug
>  that was introduced in version [version 3\.7\.15](releaselog/3_7_15.html). The fix is a 4\-character
>  edit to a single line of code. Other than this 4\-character change and
>  the update of the version number, nothing has changed from
>  [version 3\.7\.15\.1](releaselog/3_7_15_1.html).



---

### 2012\-12\-19 \- Release 3\.7\.15\.1


> SQLite [version 3\.7\.15\.1](releaselog/3_7_15_1.html) is a patch release that fixes a single bug
>  that was introduced in version [version 3\.7\.15](releaselog/3_7_15.html). The fix involved changing
>  two lines of code and adding a single assert(). This release also includes
>  some new test cases to prevent a regression of the bug, and the version
>  number is increased, of course. But otherwise, nothing has changed from
>  [version 3\.7\.15](releaselog/3_7_15.html).



---

### 2012\-12\-12 \- Release 3\.7\.15


> SQLite [version 3\.7\.15](releaselog/3_7_15.html) is a regularly schedule release of SQLite. This
>  release contains several improvements to the query planner and optimizer
>  and one important bug fix. This is the first release to officially
>  support Windows 8 Phone.
>  The important bug fix is a problem that can lead to segfaults when using
>  [shared cache mode](sharedcache.html) on a schema that contains a [COLLATE operator](lang_expr.html#collateop) within
>  a [CHECK constraint](lang_createtable.html#ckconst) or within a [view](lang_createview.html). Collating functions are associated
>  with individual database connections. But a pointer to the collating function
>  was also being cached within expressions. If an expression was part of the
>  schema and contained a cached collating function, it would point to the
>  collating function in the database connection that originally parsed the
>  schema. If that database connection closed while other database
>  connections using the same shared cache continued to operate, they other
>  database connections would try to use the deallocated collating function
>  in the database connection that closed. The fix in version 3\.7\.15 was to
>  not cache collating function pointers in the expression structure but
>  instead look them up each time a new statement is prepared.
> 
> 
>  This release also contains some important enhancements to the query planner
>  which should (we hope) make some queries run faster. The enhancements
>  include:
> 
> 
>  1. When doing a full\-table scan, try to use an index instead of
>  the original table, under the theory that indices contain less information
>  and are thus smaller and hence require less disk I/O to scan.
> 
> 
> 
>  - Enhance the [IN operator](lang_expr.html#in_op) to allow it to make use of
>  indices that have [numeric affinity](datatype3.html#affinity).
> 
> 
> 
>  - Do a better job of recognizing when an ORDER BY clause can be
>  implemented using indices \- especially in cases where the ORDER BY clause
>  contains terms from two or more tables in a join.



---

### 2012\-10\-04 \- Release 3\.7\.14\.1


> SQLite [version 3\.7\.14\.1](releaselog/3_7_14_1.html) is a patch release. Changes from the baseline
>  version 3\.7\.14 are minimal and are restricted to fixing three bugs.
>  One of the fixed bugs is a long\-standing issue with the TCL interface.
>  Another is an external compiler bug that SQLite merely works around and
>  that only comes up if you are using the VisualStudio\-2012 compiler to
>  generate WinRT applications on ARM with optimizations enabled. The
>  third problem is an SQLite core bug, introduced in version 3\.7\.14, that
>  can cause a segfault if a query contains a LEFT JOIN that contains an OR
>  in the ON clause.



---

### 2012\-09\-03 \- Release 3\.7\.14


> SQLite [version 3\.7\.14](releaselog/3_7_14.html) is a regularly scheduled maintenance release
>  of SQLite. The previous release continues to work well. Upgrading
>  is optional.
>  Version 3\.7\.14 drops native support for OS/2\. We are not aware of any
>  active projects that were using SQLite on OS/2 and since the SQLite
>  developers had no way of testing on OS/2 it seemed like it was time
>  to simply remove the OS/2 code from the SQLite tree. If there are
>  OS/2 projects out there that still need SQLite support, they can
>  continue to maintain their own private [VFS](vfs.html) which can be linked to
>  SQLite at start\-time using the [sqlite3\_vfs\_register()](c3ref/vfs_find.html) interface.
> 
> 
>  The [sqlite3\_close\_v2()](c3ref/close.html) interface has been added. The sqlite3\_close\_v2()
>  interface differs from sqlite3\_close() in that it is designed to work
>  better for host language that use a garbage collector. With the older
>  sqlite3\_close() interface, the associated [prepared statements](c3ref/stmt.html) and
>  [sqlite3\_backup](c3ref/backup.html) objects must be destroyed before the database connection.
>  With the newer sqlite3\_close\_v2() interface, the objects can be destroyed
>  in any order.
> 
> 
>  This release also includes performance improvements to the sort algorithm
>  that is used to implement ORDER BY and CREATE INDEX. And the query planner
>  has been enhanced to better use covering indices on queries that use OR
>  terms in the WHERE clause.



---

### 2012\-06\-11 \- Release 3\.7\.13


> SQLite [version 3\.7\.13](releaselog/3_7_13.html) adds support for WinRT and metro style
>  applications for Microsoft Windows 8\. The 3\.7\.13 release is
>  coming sooner than is usual after the previous release in order to get
>  this new capability into the hands of developers. To use SQLite in
>  a metro style application, compile with the \-DSQLITE\_OS\_WINRT flag.
>  Because of the increased application security and safety requirements
>  of WinRT, all database
>  filenames should be full pathnames. Note that SQLite is not capable
>  of accessing databases outside the installation directory and application
>  data directory. This restriction is another security and safety feature
>  of WinRT. Apart from these restrictions, SQLite should work exactly
>  the same on WinRT as it does on every other system.
>  Also in this release: when a database is opened using [URI filenames](uri.html)
>  and the [mode\=memory](uri.html#coreqp) query parameter
>  then the database is an in\-memory database, just as if it had
>  been named ":memory:". But, if shared cache mode is enabled, then
>  all other database connections that specify the same URI filename
>  will connect to the same in\-memory database. This allows two or more
>  database connections (in the same process) to share the same in\-memory
>  database.
> 
> 
>  This release also includes some corner\-case performance optimizations
>  that are obscure yet significant to an important subset of SQLite users.
>  Getting these performance optimizations into circulation quickly is
>  yet another reason for making this release so soon following the previous.
> 
> 
>  The next release of SQLite is scheduled to occur after the usual
>  2 or 3 month interval.



---

### 2012\-05\-22 \- Patch Release 3\.7\.12\.1


> SQLite [version 3\.7\.12\.1](releaselog/3_7_12_1.html) is a patch release for [version 3\.7\.12](releaselog/3_7_12.html) that
>  fixes a [bug](https://www.sqlite.org/src/info/c2ad16f997ee9c) that was
>  introduced in version 3\.7\.12 and that can
>  cause a segfault for certain obscure nested aggregate queries.
>  There are very few changes in 3\.7\.12\.1, and upgrading is only needed for
>  applications that do nested aggregate queries.



---

### 2012\-05\-14 \- Version 3\.7\.12


> SQLite [version 3\.7\.12](releaselog/3_7_12.html) is a regularly scheduled maintenance release.
>  This release contains several new optimizations and bug fixes and upgrading
>  is recommended. See the [change summary](releaselog/3_7_12.html) for details.



---

### 2012\-03\-20 \- Version 3\.7\.11


> SQLite [version 3\.7\.11](releaselog/3_7_11.html) is a regularly scheduled maintenance release
>  which was rushed out early due to a
>  [bug in the query optimizer](https://www.sqlite.org/src/info/b7c8682cc1)
>  introduced in the previous release. The bug is obscure \- it changes
>  a LEFT JOIN into an INNER JOIN in some cases when there is a 3\-way join
>  and OR terms in the WHERE clause. But it was considered serious enough to
>  rush out a fix. Apart from this one problem, SQLite [version 3\.7\.10](releaselog/3_7_10.html) has
>  not given any trouble. Upgrading to [version 3\.7\.11](releaselog/3_7_11.html) from versions
>  3\.7\.6\.3, 3\.7\.7, 3\.7\.7\.1, 3\.7\.8, or 3\.7\.9 is
>  optional. Upgrading from other releases, including the previous release
>  3\.7\.10, is recommended.
>  Other enhancements found in this release are enumerated in the
>  [change log](releaselog/3_7_11.html).



---

### 2012\-01\-16 \- Version 3\.7\.10


> SQLite [version 3\.7\.10](releaselog/3_7_10.html) is a regularly scheduled maintenance release.
>  Upgrading from version 3\.7\.6\.3, 3\.7\.7, 3\.7\.7\.1, 3\.7\.8, or 3\.7\.9 is
>  optional. Upgrading from other releases is recommended.
>  The [SQLITE\_CONFIG\_PCACHE](c3ref/c_config_covering_index_scan.html#sqliteconfigpcache) mechanism has been replaced with
>  [SQLITE\_CONFIG\_PCACHE2](c3ref/c_config_covering_index_scan.html#sqliteconfigpcache2). If you do not know what this mechanism
>  is (it is an extreme corner\-case and is seldom used) then this
>  change will not effect you in the least.
> 
> 
>  The default [schema format number](fileformat2.html#schemaformat) for new database files has changed
>  from 1 to 4\. SQLite has been able to generate and read database files
>  using schema format 4 for six years. But up unto now, the default
>  schema format has been 1 so that older versions of SQLite could read
>  and write databases generated by newer versions of SQLite. But those
>  older versions of SQLite have become so scarce now that it seems
>  reasonable to make the new format the default.
> 
> 
>  SQLite is changing some of the assumptions it makes above the behavior
>  of disk drives and flash memory devices during a sudden power loss.
>  This change is completely transparent to applications.
>  Read about the [powersafe overwrite](psow.html) property for additional information.
> 
> 
>  Lots of new interfaces have been added in this release:
>  * [sqlite3\_db\_release\_memory()](c3ref/db_release_memory.html)* [PRAGMA shrink\_memory](pragma.html#pragma_shrink_memory)* [sqlite3\_db\_filename()](c3ref/db_filename.html)* [sqlite3\_stmt\_busy()](c3ref/stmt_busy.html)* [sqlite3\_uri\_boolean()](c3ref/uri_boolean.html)* [sqlite3\_uri\_int64()](c3ref/uri_boolean.html)
> 
> 
> 
>  The [PRAGMA cache\_size](pragma.html#pragma_cache_size) statement has been enhanced. Formerly, you would
>  use this statement to tell SQLite how many pages of the database files it
>  should hold in its cache at once. The total memory requirement would
>  depend on the database page size. Now, if you give [PRAGMA cache\_size](pragma.html#pragma_cache_size)
>  a negative value \-N, it will allocate roughly N
>  [kibibytes](http://en.wikipedia.org/wiki/Kibibyte) of memory to cache,
>  divided up according to page size. This enhancement allows programs to
>  more easily control their memory usage.
> 
> 
>  There have been several obscure bug fixes. One noteworthy bug,
>  ticket [ff5be73dee](https://www.sqlite.org/src/info/ff5be73dee),
>  could in theory result in a corrupt database file if a power loss
>  occurred at just the wrong moment on an unusually cantankerous disk
>  drive. But that is mostly a theoretical concern and is very unlikely
>  to happen in practice. The bug was found during laboratory testing
>  and has never been observed to occur in the wild.



---

### 2011\-11\-01 \- Version 3\.7\.9


> SQLite [version 3\.7\.9](releaselog/3_7_9.html) is a regularly scheduled maintenance release.
>  Upgrading from version 3\.7\.6\.3, 3\.7\.7, 3\.7\.7\.1, and 3\.7\.8 is optional.
>  Upgrading from other versions is recommended.
>  The [SQLITE\_ENABLE\_STAT2](compile.html#enable_stat2) compile\-time option is now a no\-op. The enhanced
>  query\-planner functionality formerly available using SQLITE\_ENABLE\_STAT2
>  is now available through [SQLITE\_ENABLE\_STAT3](compile.html#enable_stat3). The enhanced query planning
>  is still disabled by default. However, future releases of SQLite might
>  convert STAT3 from an enable\-option to a disable\-option so that it is
>  available by default and is only omitted upon request.
> 
> 
>  The [FTS4](fts3.html#fts4) full\-text search engine has been enhanced such that tokens in
>  the search string that begin with "^" must be the first token in their
>  respective columns in order to match. Formerly, "^" characters in the
>  search string were simply ignored. Hence, if a legacy application was
>  including "^" characters in FTS4 search strings, thinking that they would
>  always be ignored, then those legacy applications might break with this
>  update. The fix is simply remove the "^" characters from the search
>  string.
> 
> 
>  See the [change summary](releaselog/3_7_9.html) for additional changes associated
>  with this release.



---

### 2011\-September\-19 \- Version 3\.7\.8


> SQLite [version 3\.7\.8](releaselog/3_7_8.html) is a quarterly maintenance release. Upgrading from
>  versions 3\.7\.6\.3, 3\.7\.7, or 3\.7\.7\.1 is optional. Upgrading from other
>  versions is recommended.
>  This release features a new "external merge sort" algorithm used to
>  implement ORDER BY and GROUP BY and also to presort the content of an
>  index for CREATE INDEX. The new algorithm does approximately the same
>  number of comparisons and I/Os as before, but the I/Os are much more
>  sequential and so runtimes are greatly reduced when the size of the
>  set being sorted is larger than the filesystem cache. The performance
>  improvement can be dramatic \- orders of magnitude faster
>  for large CREATE INDEX commands. On the other hand,
>  the code is slightly slower (1% or 2%)
>  for a small CREATE INDEX. Since CREATE INDEX is not an
>  operation that commonly occurs on a speed\-critical path, we feel that
>  this tradeoff is a good one. The slight slowdown for small CREATE INDEX
>  statements might be recovered in a future release. ORDER BY and GROUP BY
>  operations should now be faster for all cases, large and small.
> 
> 
>  The query planner has been enhanced to do a better job of handling
>  the DISTINCT keyword on SELECT statements.
> 
> 
>  There has been a lot of work on the default [VFSes](vfs.html). The Unix VFS has
>  been enhanced to include more overrideable system calls \- a feature requested
>  by Chromium to make it easier to build SQLite into a sandbox. The
>  windows VFS has been enhanced to be more resistant to interference from
>  anti\-virus software.
> 
> 
>  Every version of SQLite is better tested than the previous, and 3\.7\.8
>  is no exception to this rule. Version 3\.7\.8 has been used internally by
>  the SQLite team for mission critical functions and has performed flawlessly.
>  And, of course, it passes our rigorous [testing](testing.html) procedures with no
>  problems detected. Version 3\.7\.8 is recommended for all new development.



---

### 2011\-06\-28 \- Version 3\.7\.7\.1


> SQLite [version 3\.7\.7\.1](releaselog/3_7_7_1.html) adds a one\-line bug fix to 3\.7\.7 to fix
>  [a problem](https://www.sqlite.org/src/info/25ee812710)
>  causing [PRAGMA case\_sensitive\_like](pragma.html#pragma_case_sensitive_like) statements compiled using the legacy
>  [sqlite3\_prepare()](c3ref/prepare.html) interface to fail with an [SQLITE\_SCHEMA](rescode.html#schema) error. Because
>  [sqlite3\_exec()](c3ref/exec.html) uses sqlite3\_prepare() internally, the problem also affects
>  sqlite3\_exec().
>  Upgrading from 3\.7\.7 is only required for applications that use "PRAGMA
>  case\_sensitive\_like" and the sqlite3\_prepare() (or sqlite3\_exec()) interface.



---

### 2011\-06\-24 \- Version 3\.7\.7


> SQLite [version 3\.7\.7](releaselog/3_7_7.html) is a regularly scheduled bi\-monthly maintenance
>  release. Upgrading from version 3\.7\.6\.3 is optional. Upgrading from all
>  prior releases is recommended.
>  This release adds support for naming database files using [URI filenames](uri.html).
>  URI filenames are disabled by default (for backwards compatibility) but
>  applications are encouraged to enable them since incompatibilities are
>  likely to be exceedingly rare and the feature is useful. See the
>  [URI filename documentation](uri.html) for details.
> 
> 
>  Most of the other enhancements in this release involve
>  [virtual tables](vtab.html). The virtual table interface has been enhanced to
>  support [SAVEPOINT](lang_savepoint.html) and [ON CONFLICT](lang_conflict.html) clause processing, and the built\-in
>  [RTREE](rtree.html) and [FTS3/FTS4](fts3.html) have been augmented to take advantage of
>  the new capability. This means, for example, that it is now possible
>  to use the [REPLACE](lang_replace.html) command on [FTS3/FTS4](fts3.html) and [RTREE](rtree.html) tables.
> 
> 
>  The [FTS4](fts3.html#fts4) full\-text index extension has been enhanced to support
>  the [FTS4 prefix option](fts3.html#fts4prefix) and the [FTS4 order option](fts3.html#fts4order). These two enhancements
>  are provided in support of search\-as\-you\-type interfaces where search
>  results begin to appear after the first keystroke in the "search" box
>  and are refined with each subsequent keystroke. The way this is done is
>  to do a separate full\-text search after each key stroke, and add the
>  "\*" wildcard at the end of the word currently being typed. So, for
>  example, if the text typed so far is "fast da" and the next character
>  typed is "t", then the application does a full\-text search of the
>  pattern "fast dat\*" and displays the results. Such capability has
>  always existed. What is new is that the [FTS4 prefix option](fts3.html#fts4prefix) allows
>  the search to be very fast (a matter of milliseconds) even for difficult
>  cases such as "t\*" or "th\*".
> 
> 
>  There has been a fair amount of work done on the FTS4 module for this
>  release. But the core SQLite code has changed little and the previous
>  release has not given any problems, so we expect this to be a very
>  stable release.



---

### 2011\-05\-19 \- Version 3\.7\.6\.3


> SQLite [version 3\.7\.6\.3](releaselog/3_7_6_3.html) is a patch release that fixes a
>  [single bug](https://www.sqlite.org/src/info/2d1a5c67df)
>  associated with [WAL mode](wal.html). The bug has been in SQLite ever since WAL
>  was added, but the problem is very obscure and so nobody has noticed
>  before now. Nevertheless, all users are encouraged to upgrade to
>  version 3\.7\.6\.3 or later.
>  The bug is this:
>  If the [cache\_size](pragma.html#pragma_cache_size) is set very small (less than 10\) and SQLite comes
>  under memory pressure and if a multi\-statement transaction is started
>  in which the last statement prior to COMMIT is a SELECT statement and if
>  a [checkpoint](wal.html#ckpt) occurs right after the transaction commit, then
>  it might happen that the transaction will be silently rolled back instead
>  of being committed.
> 
> 
>  The default setting for [cache\_size](pragma.html#pragma_cache_size) is 2000\. So in most situations, this
>  bug will never appear. But sometimes programmers set [cache\_size](pragma.html#pragma_cache_size) to
>  very small values on gadgets and other low\-memory devices in order to
>  save memory space. Such applications are vulnerable.
>  Note that this bug does not cause database corruption. It is
>  as if [ROLLBACK](lang_transaction.html) were being run instead of [COMMIT](lang_transaction.html) in some cases.
> 
> 
>  **Bug Details**
> 
> 
>  Transactions commit in WAL mode by adding a record onto the end of
>  the WAL (the write\-ahead log) that contains a "commit" flag. So to
>  commit a transaction, SQLite takes all the pages that have changed
>  during that transaction, appends them to the WAL, and sets the commit
>  flag on the last page. Now, if SQLite comes under memory pressure, it
>  might try to free up memory space by writing changed pages to the WAL
>  prior to the commit. We call this "spilling" the cache to WAL. There
>  is nothing wrong with spilling cache to WAL. But if the
>  memory pressure is severe, it might be that by the time [COMMIT](lang_transaction.html) is run,
>  all changed pages for the transaction have already been spilled to WAL
>  and there are no pages left to be written to WAL.
>  And with no unwritten pages, there was nothing to put the commit flag
>  on. And without a commit flag, the transaction would end up being
>  rolled back.
> 
> 
>  The fix to this problem was that if all changed pages has already
>  been written to the WAL when the commit was started, then page 1 of
>  the database will be written to the WAL again, so that there will always
>  be a page available on which to set the commit flag.



---

### 2011\-04\-17 \- Version 3\.7\.6\.2


> SQLite [version 3\.7\.6\.2](releaselog/3_7_6_2.html) adds a one\-line bug fix to 3\.7\.6\.1 that enables
>  pthreads to work correctly on NetBSD. The problem was a faulty function
>  signature for the open system call. The problem does not appear to have
>  any adverse impact on any system other than NetBSD.
>  Upgrading from version 3\.7\.6\.1 is only needed on NetBSD.



---

### 2011\-04\-13 \- Version 3\.7\.6\.1


> SQLite [version 3\.7\.6\.1](releaselog/3_7_6_1.html) fixes a single bug in 3\.7\.6 that can cause a
>  segfault if [SQLITE\_FCNTL\_SIZE\_HINT](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlsizehint) is used on a Unix build that has
>  SQLITE\_ENABLE\_LOCKING\_MODE set to 0 and is compiled with
>  HAVE\_POSIX\_FALLOCATE.
>  Upgrading from 3\.7\.6 is only needed for users effected by the
>  configuration\-specific bug described above. There are no other changes
>  to the code.



---

### 2011\-04\-12 \- Version 3\.7\.6


> SQLite [version 3\.7\.6](releaselog/3_7_6.html) is a regularly scheduled bi\-monthly maintenance
>  release of SQLite. Upgrading from version 3\.7\.5 is optional. Upgrading
>  releases prior to 3\.7\.5 is recommended.



---

### 2011\-02\-01 \- Version 3\.7\.5


> SQLite [version 3\.7\.5](releaselog/3_7_5.html) is a regularly scheduled bi\-monthly maintenance
>  release of SQLite. Due to the discovery and fix of
>  [an obscure bug](https://www.sqlite.org/src/tktview?name=5d863f876e)
>  that could cause database corruption, upgrading from all prior
>  releases of SQLite is recommended. This bug was found during code
>  review and has not been observed in the wild.
>  This release adds new [opcodes](c3ref/c_dbstatus_options.html#sqlitedbstatuslookasidehit) for the
>  [sqlite3\_db\_status()](c3ref/db_status.html) interface that allow more precise measurement of
>  how the [lookaside memory allocator](malloc.html#lookaside) is performing, which can be useful
>  for tuning in applications with very tight memory constraints.
> 
> 
>  The [sqlite3\_vsnprintf()](c3ref/mprintf.html) interface was added. This routine is simply
>  a varargs version of the long\-standing [sqlite3\_snprintf()](c3ref/mprintf.html) interface.
> 
> 
>  The output from [sqlite3\_trace()](c3ref/profile.html) interface has been enhanced to work
>  better (and faster) in systems that use recursive extensions such as
>  [FTS3](fts3.html) or [RTREE](rtree.html).
> 
> 
>  Testing with Valgrind shows that this release of SQLite is about 1%
>  or 2% faster than the previous release for most operations.
> 
> 
>  A fork of the popular ADO.NET adaptor for SQLite known as System.Data.SQLite
>  is now available on <http://System.Data.SQLite.org/>. The originator
>  of System.Data.SQLite, Robert Simpson, is aware of this fork, has
>  expressed his approval, and has commit privileges on the new Fossil
>  repository. The SQLite development team intends to maintain
>  System.Data.SQLite moving forward.



---

### 2010\-12\-08 \- Version 3\.7\.4


> SQLite [version 3\.7\.4](releaselog/3_7_4.html) is a regularly scheduled bi\-monthly maintenance
>  release of SQLite. Upgrading from [version 3\.7\.2](releaselog/3_7_2.html) and [version 3\.7\.3](releaselog/3_7_3.html)
>  is optional. Upgrading from all other SQLite releases is recommended.
>  This release features [full\-text search](fts3.html) enhancements. The older
>  [FTS3](fts3.html) virtual table is still fully supported, and should also run
>  faster. In addition, the new [FTS4](fts3.html#fts4) virtual table is added. FTS4
>  follows the same syntax as FTS3 but holds additional metadata which
>  facilitates some performance improvements and more advanced
>  [matchinfo()](fts3.html#matchinfo) output. Look for further full\-text search enhancements
>  in subsequent releases.
> 
> 
>  Also in this release, the [EXPLAIN QUERY PLAN](eqp.html) output has been enhanced
>  and new documentation is provided so that application developers can
>  more easily understand how SQLite is performing their queries.
> 
> 
>  Thanks to an account from the folks at <http://www.devio.us/>, OpenBSD
>  has been added to the list of platforms upon which we
>  [test SQLite](testing.html) prior to every release. That list of platforms
>  now includes:
> 
> 
>  * Linux x86 \& x86\_64
>  * MacOS 10\.5 \& 10\.6
>  * MacOS 10\.2 PowerPC
>  * WinXP and Win7
>  * Android 2\.2
>  * OpenBSD 4\.7
> 
> 
> 
>  The previous release of SQLite ([version 3\.7\.3](releaselog/3_7_3.html)) has proven to be very
>  robust. The only serious issue discovered was
>  [ticket 80ba201079](https://www.sqlite.org/src/info/80ba201079) that
>  describes an incorrect query result that can occur under very
>  unusual circumstances. The ticket description contains details of the
>  problem. Suffice it to say here that the problem is very obscure and
>  is unlikely to effect most applications and so upgrading is optional.
>  The problem is fixed, of course, in this release.



---

### 2010\-October\-08 \- Version 3\.7\.3


> SQLite [version 3\.7\.3](releaselog/3_7_3.html) is a regularly scheduled bi\-monthly maintenance
>  release of SQLite. Upgrading from [version 3\.7\.2](releaselog/3_7_2.html) is optional.
>  Upgrading from all other releases is recommended.
>  This release adds two new interfaces (really just variations on existing
>  interfaces). The [sqlite3\_create\_function\_v2()](c3ref/create_function.html) interface adds a
>  destructor for the application\-data pointer. The new
>  [sqlite3\_soft\_heap\_limit64()](c3ref/hard_heap_limit64.html) interface allows the soft heap limit to
>  be set to a value greater than 231.
> 
> 
>  The [RTREE](rtree.html) extension has been enhanced with the ability to have an
>  [application\-defined query region](rtree.html#customquery). This might
>  be used, for example, to locate all objects within
>  the field of view of a camera.
> 
> 
>  The 3\.7\.3 release also includes some performance enhancements, including
>  query planner improvements, documentation updates,
>  and fixes to some very obscure bugs.



---

### 2010\-August\-24 \- Version 3\.7\.2


> SQLite [version 3\.7\.2](releaselog/3_7_2.html) fixes a long\-standing bug that can cause the
>  database [free\-page list](fileformat2.html#freelist) to go corrupt if [incremental\_vacuum](pragma.html#pragma_incremental_vacuum) is used
>  multiple times to
>  partially reduce the size of a database file that contains many hundreds
>  of unused database pages. The original bug reports together with links
>  to the patch that fixes it can be seen
>  [here](https://www.sqlite.org/src/info/5e10420e8d).
>  This bug has been in the code for at least a year and possibly longer.
>  The bug has nothing to do with the versions 3\.7\.1 or 3\.7\.0 or any other
>  recent release. The fact that the bug was discovered (and fixed)
>  within hours of the 3\.7\.1 release is purely a coincidence.
> 
> 
>  The bug is impossible to hit without using [incremental\_vacuum](pragma.html#pragma_incremental_vacuum) and is
>  very difficult to hit even with incremental\_vacuum. And the kind of
>  corruption that the bug causes can usually be fixed
>  simply by running [VACUUM](lang_vacuum.html). Nevertheless, because the bug can result
>  in database corruption, it is recommended that all SQLite users upgrade
>  to version 3\.7\.2 or later.



---

### 2010\-August\-23 \- Version 3\.7\.1


> SQLite [version 3\.7\.1](releaselog/3_7_1.html) is a stabilization release for the 3\.7\.x series.
>  Other than the filesize\-in\-header bug that was fixed in [version 3\.7\.0\.1](releaselog/3_7_0_1.html),
>  no major problems have been seen in 3\.7\.0\. Some minor corner\-case
>  performance regressions have been fixed. A typo in the OS/2 interface
>  has been repaired.
>  A biggest part of the 3\.7\.1 release is a cleanup and refactoring of
>  the pager module within SQLite. This refactoring should have no
>  application\-visible effects. The purpose was to reorganize the code
>  in ways that make it easier to prove correctness.
> 
> 
>  The 3\.7\.1 release adds new experimental methods for obtained more
>  detailed memory usage information and for controlling database file
>  fragmentation. And the query planner now does a better job of
>  optimizing the [LIKE](lang_expr.html#like) and [GLOB](lang_expr.html#glob) operators.
> 
> 
>  This release increases the maximum size of database pages from 32KiB to
>  64KiB. A database with 64KiB pages will not be readable or writable by
>  older versions of SQLite. Note that further increases in page size
>  are not feasible since the [file format](fileformat2.html) uses 16\-bit offsets to structures
>  within each page.



---

### 2010\-August\-04 \- Version 3\.7\.0\.1


> SQLite [version 3\.7\.0\.1](releaselog/3_7_0_1.html) is a patch release to fix a bug in the new
>  filesize\-in\-header feature of the [SQLite file format](fileformat2.html)
>  that could cause database corruption if the same database file is
>  written alternately with version 3\.7\.0 and version 3\.6\.23\.1 or earlier.
>  A performance regression was also fixed in this release.



---

### 2010\-07\-22 \- Version 3\.7\.0


> SQLite [version 3\.7\.0](releaselog/3_7_0.html) is a major release of SQLite that features
>  a new transaction control mechanism using a [write\-ahead log](wal.html) or [WAL](wal.html).
>  The traditional rollback\-journal is still used as the default so there
>  should be no visible change for legacy programs. But newer programs
>  can take advantage of improved performance and concurrency by enabling
>  the WAL journaling mode.
>  SQLite version 3\.7\.0 also contains some query planner enhancements and
>  a few obscure bug fixes, but the only really big change is the addition
>  of WAL mode.



---

### 2010\-03\-30 \- Version 3\.6\.23\.1


> SQLite [version 3\.6\.23\.1](releaselog/3_6_23_1.html) is a patch release to fix a bug in the
>  offsets() function of [FTS3](fts3.html) at the request of the Mozilla.



---

### 2010\-03\-09 \- Version 3\.6\.23


> SQLite [version 3\.6\.23](releaselog/3_6_23.html) is a regular bimonthly release of SQLite.
>  Upgrading from the prior release is purely optional.
>  This release contains new pragmas: the [secure\_delete pragma](pragma.html#pragma_secure_delete), and
>  the [compile\_options pragma](pragma.html#pragma_compile_options).
>  There are a new SQL functions: [sqlite\_compileoption\_used()](lang_corefunc.html#sqlite_compileoption_used)
>  and [sqlite\_compileoption\_get()](lang_corefunc.html#sqlite_compileoption_get).
>  New C/C\+\+ interfaces: [sqlite3\_compileoption\_used()](c3ref/compileoption_get.html),
>  [sqlite3\_compileoption\_get()](c3ref/compileoption_get.html), [SQLITE\_CONFIG\_LOG](c3ref/c_config_covering_index_scan.html#sqliteconfiglog), and
>  [sqlite3\_log()](c3ref/log.html).
> 
> 
>  This release also includes several minor bug fixes and performance
>  improvements. Support for [SQLITE\_OMIT\_FLOATING\_POINT](compile.html#omit_floating_point) is enhanced.
>  There are on\-going improvements to [FTS3](fts3.html).
> 
> 
>  The ".genfkey" command in the [Command Line Interface](cli.html) has been
>  removed. SQLite has supported standard SQL [foreign key constraints](foreignkeys.html)
>  since [version 3\.6\.19](releaselog/3_6_19.html) and so the ".genfkey" command was seen as
>  an anachronism.



---

### 2010\-01\-06 \- Version 3\.6\.22


> SQLite [version 3\.6\.22](releaselog/3_6_22.html) is a bug\-fix release. Two bugs have been fixed
>  that might cause incorrect query results.
>  * Ticket [31338dca7e](https://www.sqlite.org/src/info/31338dca7e)
>  describes a
>  problem with queries that have a WHERE clause of the form (x AND y) OR z
>  where x and z come from one table of a join and y comes from a different
>  table.
>  * Ticket [eb5548a849](https://www.sqlite.org/src/info/eb5548a849)
>  describes
>  a problem where the use of the CAST operator in the WHERE clause can lead
>  to incorrect results if the column being cast to a new datatype is also
>  used in the same WHERE clause without being cast.
> 
> 
>  Both bugs are obscure,
>  but because they could arise in an application after deployment, it is
>  recommended that all applications upgrade SQLite to version 3\.6\.22\.
>  This release also includes other minor bug fixes and performance
>  enhancements, especially in the [FTS3](fts3.html) extension.



---

### 2009\-12\-07 \- Version 3\.6\.21


> SQLite [version 3\.6\.21](releaselog/3_6_21.html) focuses on performance optimization. For
>  a certain set of traces, this version uses 12% fewer CPU instructions
>  than the previous release (as measured by Valgrind). In addition, the
>  [FTS3](fts3.html) extension has been through an extensive cleanup and rework and
>  the [sqlite3\_trace()](c3ref/profile.html) interface has been modified to insert
>  [bound parameter](lang_expr.html#varparam) values into its output.



---

### 2009\-11\-04 \- Version 3\.6\.20


> SQLite [version 3\.6\.20](releaselog/3_6_20.html) is a general maintenance release. The
>  query planner has been enhanced to work better with bound parameters
>  in LIKE and GLOB operators and in range constraints and various minor
>  bugs have been fixed. Upgrading from 3\.6\.19 is optional.



---

### 2009\-10\-14 \- Version 3\.6\.19


> SQLite [version 3\.6\.19](releaselog/3_6_19.html) adds native support for
>  [foreign key constraints](foreignkeys.html), including deferred constraints and
>  cascading deletes. Enforcement of foreign keys is disabled by
>  default for backwards compatibility and must be turned on using
>  the [foreign\_keys pragma](pragma.html#pragma_foreign_keys).
>  Version 3\.6\.19 also adds support for the
>  [IS and IS NOT operators](lang_expr.html#isisnot). Formerly, SQLite (as most
>  other SQL database engines) supported IS NULL and IS NOT NULL. The
>  IS and IS NOT operators are generalizations that allow the right\-hand
>  side to be an arbitrary expression. IS and IS NOT work the same as
>  \=\= (equals) and !\= (not equals) except that with IS and IS NOT the
>  NULL values compare equal to one another.



---

### 2009\-09\-11 \- Version 3\.6\.18


> Beginning with this release, the SQLite source code is tracked and
>  managed using the [Fossil](http://www.fossil-scm.org/)
>  distributed configuration management system. SQLite was previously
>  versioned using CVS. The entire CVS history has been imported into
>  Fossil. The older CVS repository remains on the website but is
>  read\-only.
>  There are two major enhancements in SQLite version 3\.6\.18\. The first
>  is a series or refinements to the query planner that help SQLite to
>  choose better plans for joins where in the past it was selecting suboptimal
>  query plans. The [SQLITE\_ENABLE\_STAT2](compile.html#enable_stat2) compile\-time option has been
>  added to cause SQLite to collect histogram data on indices when the
>  [ANALYZE](lang_analyze.html) command is run. The use of histograms improve the query
>  planning performance even more.
> 
> 
>  The second major enhancement is that SQLite now support recursive
>  triggers. The older non\-recursive behavior of triggers is still the
>  default behavior. Recursive triggers are activated using the
>  [recursive\_triggers pragma](pragma.html#pragma_recursive_triggers). In addition to allowing triggers to
>  call themselves (either directly or indirectly) the new capability
>  also fires DELETE triggers on rows that are removed from a table
>  as a result of [REPLACE](lang_conflict.html) conflict resolution processing.
> 
> 
>  Non\-recursive triggers are still the default behavior since this
>  is least likely to cause problems for existing applications. However,
>  we anticipate that triggers will become
>  recursive by default beginning with release 3\.7\.0\. At that point,
>  applications that want to continue using the older non\-recursive
>  trigger behavior will need to use the [recursive\_triggers pragma](pragma.html#pragma_recursive_triggers)
>  to disable recursive triggers.
> 
> 
>  This version of SQLite also contains bug fixes, though none of the
>  bugs are serious and all are obscure, so upgrading is optional.
> 
> 
>  The SQLite core continues to have [100% branch test coverage](testing.html#coverage)
>  and so despite the many changes in this release, the developers
>  believe that this version of SQLite is stable and ready for production
>  use.



---

### 2009\-08\-10 \- Version 3\.6\.17


> This is a monthly maintenance release with a focus of bug fixes,
>  performance improvements, and increased test coverage. This is the
>  first release of SQLite since [100% branch test coverage](testing.html#coverage)
>  was achieved on the SQLite core.
>  In addition, a new interface [sqlite3\_strnicmp()](c3ref/stricmp.html) is provided for the
>  convenience of extension writers.
> 
> 
>  None of the bugs fixed in this release are serious. All bugs are
>  obscure. Upgrading is optional.



---

### 2009\-07\-25 \- 100% Branch Test Coverage


> A subset of the [TH3](th3.html) test suite was measured by gcov to provide
>  [100% branch test coverage](testing.html#coverage) over the SQLite core
>  (exclusive of the VFS backend and of extensions such as FTS3 and RTREE)
>  when compiled for SuSE 10\.1 Linux on x86\. The SQLite developers pledge
>  to maintain branch test coverage at 100% in all future releases.
>  Ongoing work will strive for 100% branch test coverage on the
>  operating\-system backends and extensions as well.



---

### 2009\-06\-27 \- Version 3\.6\.16


> SQLite [version 3\.6\.16](releaselog/3_6_16.html) is another general maintenance release containing
>  performance and robustness enhancements. A single notable bug was fixed
>  (ticket \#3929\). This bug can cause INSERT or UPDATE statements to fail
>  on indexed tables that have AFTER triggers that modify the same table and
>  index.



---

### 2009\-06\-15 \- Version 3\.6\.15


> SQLite [version 3\.6\.15](releaselog/3_6_15.html) is a general maintenance release containing
>  performance and robustness enhancements and fixes for various obscure
>  bugs.



---

### 2009\-05\-25 \- Version 3\.6\.14\.2


> SQLite [version 3\.6\.14\.2](releaselog/3_6_14_2.html) fixes an obscure bug in the code generator
>  (ticket \#3879\)
>  section of SQLite which can potentially cause incorrect query results.
>  The changes from the prior release consist of only this one bug fix,
>  check\-in \[6676]
>  and a change to the version number text.
>  The bug was introduced in version 3\.6\.14\. It is recommended that
>  users of version 3\.6\.14 and 3\.6\.14\.1 upgrade to this release. Applications
>  are unlikely to hit this bug, but since it is difficult to predict which
>  applications might hit it and which might not, we recommend that all
>  users of 3\.6\.14 and 3\.5\.14\.1 upgrade to this release.



---

### 2009\-05\-19 \- Version 3\.6\.14\.1


> SQLite [version 3\.6\.14\.1](releaselog/3_6_14_1.html) is a patch release to [version 3\.6\.14](releaselog/3_6_14.html) with
>  minimal changes that fixes three bugs. Upgrading is only necessary
>  for users who are impacted by one or more of those bugs.



---

### 2009\-05\-07 \- Version 3\.6\.14


> SQLite [version 3\.6\.14](releaselog/3_6_14.html) provides new performance enhancements in
>  the btree and pager layers and in the query optimizer. Certain
>  workloads can be as much as twice as fast as the previous release,
>  though 10% faster is a more typical result.
>  Queries against [virtual tables](vtab.html) that contain OR and IN operators
>  in the WHERE clause are now able to use indexing.
> 
> 
>  A new optional [asynchronous I/O backend](asyncvfs.html) is available for
>  Unix and Windows. The asynchronous backend gives the illusion of faster
>  response time by pushing slow write operations into a background thread.
>  The tradeoff for faster response time is that more memory is required
>  (to hold the content of the pending writes) and if a power failure or
>  program crash occurs, some transactions that appeared to have committed
>  might end up being rolled back upon restart.
> 
> 
>  This release also contains many minor bug fixes, documentation enhancements,
>  new test cases, and cleanups and simplifications to the source code.
> 
> 
>  There is no compelling reason to upgrade from versions 3\.6\.12 or
>  3\.6\.13 if those prior versions are working. Though many users may
>  benefit from the improved performance.



---

### 2008\-12\-16 \- Version 3\.6\.7


> SQLite [version 3\.6\.7](releaselog/3_6_7.html) contains a major cleanup of the Unix driver,
>  and support for the new Proxy Locking mechanism on Mac OS X. Though
>  the Unix driver is reorganized, its functionality is the same and so
>  applications should not notice a difference.



---

### 2008\-11\-26 \- Version 3\.6\.6\.2


> This release fixes a bug that was introduced into SQLite [version 3\.6\.6](releaselog/3_6_6.html)
>  and which seems like it might be able to cause database corruption. This
>  bug was detected during stress testing. It has not been seen in the wild.
>  An analysis of the problem suggests that the bug might be able to cause
>  database corruption, however focused efforts to find a real\-world test
>  cases that actually causes database corruption have so far been unsuccessful.
>  Hence, the likelihood of this bug causing problems is low. Nevertheless,
>  we have decided to do an emergency branch release out of an abundance of
>  caution.
>  The [version 3\.6\.6\.2](releaselog/3_6_6_2.html) release also fixes an obscure memory leak that
>  can occur following a disk I/O error.



---

### 2008\-11\-22 \- Version 3\.6\.6\.1


> This release fixes a bug that was introduced into SQLite [version 3\.6\.4](releaselog/3_6_4.html)
>  and that can cause database corruption in obscure cases. This bug has
>  never been seen in the wild; it was first detected by internal stress
>  tests and required substantial analysis before it could be shown to
>  potentially lead to corruption. So we feel that SQLite versions 3\.6\.4,
>  3\.6\.5, and 3\.6\.6 are safe to use for development work. But upgrading
>  to this patch release or later is recommended prior to deploying
>  products that incorporate SQLite.
>  We have taken the unusual step of issuing a patch release in order to
>  get the fix for this bug into circulation quickly. SQLite version 3\.6\.7
>  will continue on its normal path of development with an anticipated
>  release in mid December.



---

### 2008\-11\-19 \- Version 3\.6\.6


> SQLite [version 3\.6\.5](releaselog/3_6_5.html) is released. This is a quick turn\-around release
>  that fixes a bug in virtual tables and FTS3 that snuck into
>  [version 3\.6\.5](releaselog/3_6_5.html). This release also adds the new
>  application\-defined page cache mechanism.



---

### 2008\-11\-12 \- Version 3\.6\.5


> SQLite [version 3\.6\.5](releaselog/3_6_5.html) is released. There are various minor feature
>  enhancements and numerous obscure bug fixes.
>  The [change log](releaselog/3_6_5.html) contains the details. Upgrading is
>  optional.



---

### 2008\-11\-01 \- Bloomberg Joins SQLite Consortium


> The SQLite developers are honored to announce that
>  [Bloomberg](http://www.bloomberg.com/) has joined the
>  [SQLite Consortium](consortium.html).



---

### 2008\-10\-15 \- Version 3\.6\.4


> SQLite version 3\.6\.4 adds new features designed to help applications
>  detect when indices are not being used on query. There are also some
>  important performance improvements. Upgrading is optional.



---

### 2008\-09\-22 \- Version 3\.6\.3


> SQLite version 3\.6\.3 fixes a bug in SELECT DISTINCT that was introduced
>  by the previous version. No new features are added. Upgrading is
>  recommended for all applications that make use of DISTINCT.



---

### 2008\-08\-30 \- Version 3\.6\.2


> SQLite version 3\.6\.2 contains rewrites of the page\-cache subsystem and
>  the procedures for matching identifiers to table columns in SQL statements.
>  These changes are designed to better modularize the code and make it more
>  maintainable and reliable moving forward. Nearly 5000 non\-comment lines
>  of core code (about 11\.3%) have changed
>  from the previous release. Nevertheless, there should be no
>  application\-visible changes, other than bug fixes.



---

### 2008\-08\-06 \- Version 3\.6\.1


> SQLite version 3\.6\.1 is a stabilization and performance enhancement
>  release.



---

### 2008\-07\-16 \- Version 3\.6\.0 beta


> Version 3\.6\.0 makes changes to the [VFS](c3ref/vfs.html) object in order
>  to make SQLite more easily portable to a wider variety of platforms.
>  There are potential incompatibilities with some legacy applications.
>  See the [35to36\.html](35to36.html) document for details.
>  Many new interfaces are introduced in version 3\.6\.0\. The code is
>  very well tested and is appropriate for use in stable systems. We
>  have attached the "beta" designation only so that we can make tweaks to
>  the new interfaces in the next release without having to declare an
>  incompatibility.



---

### 2008\-05\-12 \- Version 3\.5\.9


> Version 3\.5\.9 adds a new experimental [PRAGMA](pragma.html#syntax): [journal\_mode](pragma.html#pragma_journal_mode).
>  Setting the journal mode to PERSIST can provide performance improvement
>  on systems where deleting a file is expensive. The PERSIST journal
>  mode is still considered experimental and should be used with caution
>  pending further testing.
>  Version 3\.5\.9 is intended to be the last stable release prior to
>  version 3\.6\.0\. Version 3\.6\.0 will make incompatible changes to the
>  [sqlite3\_vfs](c3ref/vfs.html) VFS layer in order to address deficiencies in the original
>  design. These incompatibilities will only effect programmers who
>  write their own custom VFS layers (typically embedded device builders).
>  The planned VFS changes will be much smaller
>  than the changes that occurred on the
>  [3\.4\.2 to 3\.5\.0 transaction](34to35.html) that occurred last
>  September.
> 
> 
>  This release of SQLite is considered stable and ready for production use.



---

### 2008\-04\-16 \- Version 3\.5\.8


> Version 3\.5\.8 includes some important new performance optimizations
>  in the virtual machine code generator, including constant subexpression
>  factoring and common subexpression elimination. This release also
>  creates new public interfaces:
>  [sqlite3\_randomness()](c3ref/randomness.html) provides access to SQLite's internal
>  pseudo\-random number generator, [sqlite3\_limit()](c3ref/limit.html) allows size
>  limits to be set at run\-time on a per\-connection basis, and
>  [sqlite3\_context\_db\_handle()](c3ref/context_db_handle.html) is a convenience routine that allows
>  an application\-defined SQL function implementation to retrieve
>  its [database connection](c3ref/sqlite3.html) handle.
>  This release of SQLite is considered stable and ready for production use.



---

### 2008\-03\-17 \- Version 3\.5\.7


> Version 3\.5\.7 fixes several minor and obscure bugs, especially
>  in the autoconf\-generated makefile. Upgrading is optional.
>  This release of SQLite is considered stable and ready for production use.



---

### 2008\-02\-06 \- Version 3\.5\.6


> Version 3\.5\.6 fixes a minor regression in 3\.5\.5 \- a regression that
>  had nothing to do with the massive change of the virtual machine
>  to a register\-based design.
>  No problems have been reported with the new virtual machine. This
>  release of SQLite is considered stable and ready for production use.



---

### 2008\-01\-31 \- Version 3\.5\.5


> Version 3\.5\.5 changes over 8% of the core source code of SQLite in order
>  to convert the internal virtual machine from a stack\-based design into
>  a register\-based design. This change will allow future optimizations
>  and will avoid an entire class of stack overflow bugs that have caused
>  problems in the past. Even though this change is large, extensive testing
>  has found zero errors in the new virtual machine and so we believe this
>  to be a very stable release.



---

### 2007\-12\-14 \- Version 3\.5\.4


> Version 3\.5\.4 fixes a long\-standing but obscure bug in UPDATE and
>  DELETE which might cause database corruption. (See ticket \#2832\.)
>  Upgrading is recommended for all users.
>  This release also brings the processing of ORDER BY statements into
>  compliance with standard SQL. This could, in theory, cause problems
>  for existing applications that depend on the older, buggy behavior.
>  See ticket \#2822 for additional information.



---

### 2007\-12\-12 \- SQLite Consortium Announced


> The [SQLite Consortium](consortium.html) was launched
>  today with [Mozilla](http://www.mozilla.org/) and
>  [Symbian](http://www.symbian.com/) as charter members.
>  As noted in the [press release](pressrelease-20071212.html),
>  the Consortium's goal is to promote the continuing vitality and
>  independence of SQLite.



---

### 2007\-11\-27 \- Version 3\.5\.3


> This is an incremental release that fixes several minor problems.
>  Upgrading is optional. If Version 3\.5\.2 or 3\.5\.1 is working fine
>  for you, then there is no pressing need to change to 3\.5\.3\.
>  The prebuilt binaries and the amalgamation found on the
>  [download](download.html) page include the FTS3 fulltext
>  search extension module. We are doing this on an experimental
>  basis and are not promising to provide prebuilt binaries with
>  FTS3 in the future.



---

### 2007\-11\-05 \- Version 3\.5\.2


> This is an incremental release that fixes several minor problems,
>  adds some obscure features, and provides some performance tweaks.
>  Upgrading is optional.
>  The experimental compile\-time option
>  [SQLITE\_OMIT\_MEMORY\_ALLOCATION](compile.html#omitfeatures) is no longer supported. On the other
>  hand, it is now possible to compile SQLite so that it uses a static
>  array for all its dynamic memory allocation needs and never calls
>  malloc. Expect to see additional radical changes to the memory
>  allocation subsystem in future releases.



---

### 2007\-10\-04 \- Version 3\.5\.1


> Fix a long\-standing bug that might cause database corruption if a
>  disk\-full error occurs in the middle of a transaction and that
>  transaction is not rolled back.
>  Ticket \#2686\.
>  The new VFS layer is stable. However, we still reserve the right to
>  make tweaks to the interface definition of the VFS if necessary.



---

### 2007\-09\-04 \- Version 3\.5\.0 alpha


> The OS interface layer and the memory allocation subsystems in
>  SQLite have been reimplemented. The published API is largely unchanged
>  but the (unpublished) OS interface has been modified extensively.
>  Applications that implement their own OS interface will require
>  modification. See
>  [34to35\.html](34to35.html) for details.
>  This is a large change. Approximately 10% of the source code was
>  modified. We are calling this first release "alpha" in order to give
>  the user community time to test and evaluate the changes before we
>  freeze the new design.



---

### 2007\-08\-13 \- Version 3\.4\.2


> While stress\-testing the
>  [soft\_heap\_limit](c3ref/soft_heap_limit.html)
>  feature, a bug that could lead to
>  database corruption was discovered and fixed.
>  Though the consequences of this bug are severe, the chances of hitting
>  it in a typical application are remote. Upgrading is recommended
>  only if you use the
>  [sqlite3\_soft\_heap\_limit](c3ref/soft_heap_limit.html)
>  interface.



---

### 2007\-07\-20 \- Version 3\.4\.1


> This release fixes a bug in [VACUUM](lang_vacuum.html) that
>  can lead to database corruption. The bug was introduced in version
>  [3\.3\.14](changes.html#version_3_3_14).
>  Upgrading is recommended for all users. Also included are a slew of
>  other more routine
>  [enhancements and bug fixes](changes.html#version_3_4_1).



---

### 2007\-06\-18 \- Version 3\.4\.0


> This release fixes two separate bugs either of which
>  can lead to database corruption. Upgrading
>  is strongly recommended. If you must continue using an older version
>  of SQLite, please at least read about how to avoid these bugs
>  at CorruptionFollowingBusyError and ticket \#2418
>  
>  This release also adds explicit [limits](limits.html) on the
>  sizes and quantities of things SQLite will handle. The new limits might
>  causes compatibility problems for existing applications that
>  use excessively large strings, BLOBs, tables, or SQL statements.
>  The new limits can be increased at compile\-time to work around any problems
>  that arise. Nevertheless, the version number of this release is
>  3\.4\.0 instead of 3\.3\.18 in order to call attention to the possible
>  incompatibility.
>  
> 
> 
>  There are also new features, including
>  [incremental BLOB I/O](c3ref/blob_open.html) and
>  [incremental vacuum](pragma.html#pragma_incremental_vacuum).
>  See the [change log](changes.html#version_3_4_0)
>  for additional information.



---

### 2007\-04\-25 \- Version 3\.3\.17


> This version fixes a bug in the forwards\-compatibility logic of SQLite
>  that was causing a database to become unreadable when it should have
>  been read\-only. Upgrade from 3\.3\.16 only if you plan to deploy into
>  a product that might need to be upgraded in the future. For day to day
>  use, it probably does not matter.



---

### 2007\-04\-18 \- Version 3\.3\.16


> Performance improvements added in 3\.3\.14 but mistakenly turned off
>  in 3\.3\.15 have been reinstated. A bug has been fixed that prevented
>  VACUUM from running if a NULL value was in a UNIQUE column.



---

### 2007\-04\-09 \- Version 3\.3\.15


> An annoying bug introduced in 3\.3\.14 has been fixed. There are
>  also many enhancements to the test suite.



---

### 2007\-04\-02 \- Version 3\.3\.14


> This version focuses on performance improvements. If you recompile
>  the amalgamation using GCC option \-O3 (the precompiled binaries
>  use \-O2\) you may see performance
>  improvements of 35% or more over version 3\.3\.13 depending on your
>  workload. This version also
>  adds support for [exclusive access mode](pragma.html#pragma_locking_mode).



---

### 2007\-02\-13 \- Version 3\.3\.13


> This version fixes a subtle bug in the ORDER BY optimizer that can
>  occur when using joins. There are also a few minor enhancements.
>  Upgrading is recommended.



---

### 2007\-01\-27 \- Version 3\.3\.12


> The first published build of the previous version used the wrong
>  set of source files. Consequently, many people downloaded a build
>  that was labeled as "3\.3\.11" but was really 3\.3\.10\. Version 3\.3\.12
>  is released to clear up the ambiguity. A couple more bugs have
>  also been fixed and [PRAGMA integrity\_check](pragma.html#pragma_integrity_check) has been enhanced.



---

### 2007\-01\-22 \- Version 3\.3\.11


> Version 3\.3\.11 fixes for a few more problems in version 3\.3\.9 that
>  version 3\.3\.10 failed to catch. Upgrading is recommended.



---

### 2007\-01\-09 \- Version 3\.3\.10


> Version 3\.3\.10 fixes several bugs that were introduced by the previous
>  release. Upgrading is recommended.



---

### 2007\-01\-04 \- Version 3\.3\.9


> Version 3\.3\.9 fixes bugs that can lead to database corruption under
>  obscure and difficult to reproduce circumstances. See
>  DatabaseCorruption in the
>  wiki for details.
>  This release also adds the new
>  [sqlite3\_prepare\_v2()](c3ref/prepare.html)
>  API and includes important bug fixes in the command\-line
>  shell and enhancements to the query optimizer. Upgrading is
>  recommended.



---

### 2006\-10\-09 \- Version 3\.3\.8


> Version 3\.3\.8 adds support for full\-text search using the
>  FTS1 module. There are also minor bug fixes. Upgrade only if
>  you want to try out the new full\-text search capabilities or if
>  you are having problems with 3\.3\.7\.



---

### 2006\-08\-12 \- Version 3\.3\.7


> Version 3\.3\.7 includes support for loadable extensions and virtual
>  tables. But both features are still considered "beta" and their
>  APIs are subject to change in a future release. This release is
>  mostly to make available the minor bug fixes that have accumulated
>  since 3\.3\.6\. Upgrading is not necessary. Do so only if you encounter
>  one of the obscure bugs that have been fixed or if you want to try
>  out the new features.



---

### 2006\-06\-19 \- New Book About SQLite


> *[The Definitive Guide to SQLite](https://link.springer.com/book/10.1007/978-1-4302-3226-1)*,
>  a 2nd edition book by Mike Owens and Grant Allen,
>  is now available from [Apress](http://www.apress.com).
>  The books covers the latest SQLite internals as well as
>  the native C interface and bindings for PHP, Python,
>  Perl, Ruby, Tcl, and Java. Recommended.



---

### 2006\-06\-6 \- Version 3\.3\.6


> Changes include improved tolerance for Windows virus scanners
>  and faster :memory: databases. There are also fixes for several
>  obscure bugs. Upgrade if you are having problems.



---

### 2006\-04\-5 \- Version 3\.3\.5


> This release fixes many minor bugs and documentation typos and
>  provides some minor new features and performance enhancements.
>  Upgrade only if you are having problems or need one of the new features.



---

### 2006\-02\-11 \- Version 3\.3\.4


> This release fixes several bugs, including a
>  blunder that might cause a deadlock on multithreaded systems.
>  Anyone using SQLite in a multithreaded environment should probably upgrade.



---

### 2006\-01\-31 \- Version 3\.3\.3 stable


> There have been no major problems discovered in version 3\.3\.2, so
>  we hereby declare the new APIs and language features to be stable
>  and supported.



---

### 2006\-01\-24 \- Version 3\.3\.2 beta


> More bug fixes and performance improvements as we move closer to
>  a production\-ready version 3\.3\.x.



---

### 2006\-01\-16 \- Version 3\.3\.1 alpha


> Many bugs found in last week's alpha release have now been fixed and
>  the library is running much faster again.
>  Database connections can now be moved between threads as long as the
>  connection holds no locks at the time it is moved. Thus the common
>  paradigm of maintaining a pool of database connections and handing
>  them off to transient worker threads is now supported.
>  Please help test this new feature.
>  See the MultiThreading wiki page for additional
>  information.



---

### 2006\-01\-10 \- Version 3\.3\.0 alpha


> Version 3\.3\.0 adds support for CHECK constraints, DESC indices,
>  separate REAL and INTEGER column affinities, a new OS interface layer
>  design, and many other changes. The code passed a regression
>  test but should still be considered alpha. Please report any
>  problems.
>  The file format for version 3\.3\.0 has changed slightly to support
>  descending indices and
>  a more efficient encoding of boolean values. SQLite 3\.3\.0 will read and
>  write legacy databases created with any prior version of SQLite 3\. But
>  databases created by version 3\.3\.0 will not be readable or writable
>  by earlier versions of the SQLite. The older file format can be
>  specified at compile\-time for those rare cases where it is needed.



---

### 2005\-12\-19 \- Versions 3\.2\.8 and 2\.8\.17


> These versions contain one\-line changes to 3\.2\.7 and 2\.8\.16 to fix a bug
>  that has been present since March of 2002 and version 2\.4\.0\.
>  That bug might possibly cause database corruption if a large INSERT or
>  UPDATE statement within a multi\-statement transaction fails due to a
>  uniqueness constraint but the containing transaction commits.



---

### 2005\-09\-24 \- Version 3\.2\.7


> This version fixes several minor and obscure bugs.
>  Upgrade only if you are having problems.



---

### 2005\-09\-16 \- Version 3\.2\.6 \- Critical Bug Fix


> This version fixes a bug that can result in database
>  corruption if a VACUUM of a 1 gigabyte or larger database fails
>  (perhaps do to running out of disk space or an unexpected power loss)
>  and is later rolled back.
>  
>  Also in this release:
>  The ORDER BY and GROUP BY processing was rewritten to use less memory.
>  Support for COUNT(DISTINCT) was added. The LIKE operator can now be
>  used by the optimizer on columns with COLLATE NOCASE.



---

### 2005\-08\-27 \- Version 3\.2\.5


> This release fixes a few more lingering bugs in the new code.
>  We expect that this release will be stable and ready for production use.



---

### 2005\-08\-24 \- Version 3\.2\.4


> This release fixes a bug in the new optimizer that can lead to segfaults
>  when parsing very complex WHERE clauses.



---

### 2005\-08\-21 \- Version 3\.2\.3


> This release adds the [ANALYZE](lang_analyze.html) command,
>  the [CAST](lang_expr.html) operator, and many
>  very substantial improvements to the query optimizer. See the
>  [change log](changes.html#version_3_2_3) for additional
>  information.



---

### 2005\-08\-02 \- 2005 Open Source Award for SQLite


> SQLite and its primary author D. Richard Hipp have been honored with a
>  [2005 Open Source Award](https://developers.google.com/open-source/osa#2005-google-oreilly-open-source-award-winners)
>  from Google and O'Reilly.



---

### 2005\-06\-13 \- Version 3\.2\.2


> This release includes numerous minor bug fixes, speed improvements,
>  and code size reductions. There is no reason to upgrade unless you
>  are having problems or unless you just want to.



---

### 2005\-03\-29 \- Version 3\.2\.1


> This release fixes a memory allocation problem in the new
>  [ALTER TABLE ADD COLUMN](lang_altertable.html)
>  command.



---

### 2005\-03\-21 \- Version 3\.2\.0


> The primary purpose for version 3\.2\.0 is to add support for
>  [ALTER TABLE ADD COLUMN](lang_altertable.html).
>  The new ADD COLUMN capability is made
>  possible by AOL developers supporting and embracing great
>  open\-source software. Thanks, AOL!
>  Version 3\.2\.0 also fixes an obscure but serious bug that was discovered
>  just prior to release. If you have a multi\-statement transaction and
>  within that transaction an UPDATE or INSERT statement fails due to a
>  constraint, then you try to rollback the whole transaction, the rollback
>  might not work correctly. See
>  Ticket \#1171 for details. Upgrading is recommended for all users.



---

### 2005\-03\-16 \- Version 3\.1\.6


> Version 3\.1\.6 fixes a critical bug that can cause database corruption
>  when inserting rows into tables with around 125 columns. This bug was
>  introduced in version 3\.0\.0\. See
>  Ticket \#1163 for additional information.



---

### 2005\-03\-11 \- Versions 3\.1\.4 and 3\.1\.5 Released


> Version 3\.1\.4 fixes a critical bug that could cause database corruption
>  if the autovacuum mode of version 3\.1\.0 is turned on (it is off by
>  default) and a CREATE UNIQUE INDEX is executed within a transaction but
>  fails because the indexed columns are not unique. Anyone using the
>  autovacuum feature and unique indices should upgrade.
>  Version 3\.1\.5 adds the ability to disable
>  the F\_FULLFSYNC ioctl() in OS\-X by setting "PRAGMA synchronous\=on" instead
>  of the default "PRAGMA synchronous\=full". There was an attempt to add
>  this capability in 3\.1\.4 but it did not work due to a spelling error.



---

### 2005\-02\-19 \- Version 3\.1\.3 Released


> Version 3\.1\.3 cleans up some minor issues discovered in version 3\.1\.2\.



---

### 2005\-02\-15 \- Versions 2\.8\.16 and 3\.1\.2 Released


> A critical bug in the VACUUM command that can lead to database
>  corruption has been fixed in both the 2\.x branch and the main
>  3\.x line. This bug has existed in all prior versions of SQLite.
>  Even though it is unlikely you will ever encounter this bug,
>  it is suggested that all users upgrade. See
>  ticket \#1116 for additional information.
>  Version 3\.1\.2 is also the first stable release of the 3\.1
>  series. SQLite 3\.1 features added support for correlated
>  subqueries, autovacuum, autoincrement, ALTER TABLE, and
>  other enhancements. See the
>  [release notes
>  for version 3\.1\.0](releaselog/3_1_0.html) for a detailed description of the
>  changes available in the 3\.1 series.



---

### 2005\-02\-01 \- Version 3\.1\.1 (beta) Released


> Version 3\.1\.1 (beta) is now available on the
>  website. Version 3\.1\.1 is fully backwards compatible with the 3\.0 series
>  and features many new features including Autovacuum and correlated
>  subqueries. The
>  [release notes](releaselog/3_1_1.html)
>  From version 3\.1\.0 apply equally to this release beta. A stable release
>  is expected within a couple of weeks.



---

### 2005\-01\-21 \- Version 3\.1\.0 (alpha) Released


> Version 3\.1\.0 (alpha) is now available on the
>  website. Version 3\.1\.0 is fully backwards compatible with the 3\.0 series
>  and features many new features including Autovacuum and correlated
>  subqueries. See the
>  [release notes](releaselog/3_1_0.html)
>  for details.
>  This is an alpha release. A beta release is expected in about a week
>  with the first stable release to follow after two more weeks.



---

### 2004\-11\-09 \- SQLite at the 2004 International PHP Conference


> There was a talk on the architecture of SQLite and how to optimize
>  SQLite queries at the 2004 International PHP Conference in Frankfurt,
>  Germany.  
> 
>  Obsolete URL: https://www.sqlite.org/php2004/page\-001\.html   
> 
>  Slides from that talk are available.



---

### 2004\-10\-11 \- Version 3\.0\.8


> Version 3\.0\.8 of SQLite contains several code optimizations and minor
>  bug fixes and adds support for DEFERRED, IMMEDIATE, and EXCLUSIVE
>  transactions. This is an incremental release. There is no reason
>  to upgrade from version 3\.0\.7 if that version is working for you.



---

### 2004\-10\-10 \- SQLite at the 11th
Annual Tcl/Tk Conference


> There will be a talk on the use of SQLite in Tcl/Tk at the
>  11th Tcl/Tk Conference this week in
>  New Orleans. Visit [http://www.tcl\-lang.org/community/tcl2004/](http://www.tcl-lang.org/community/tcl2004/)
>  for details.  
> 
>  Obsolete URL: https://www.sqlite.org/tclconf2004/page\-001\.html   
> 
>  Slides from the talk are available.



---

### 2004\-09\-18 \- Version 3\.0\.7


> Version 3\.0 has now been in use by multiple projects for several
>  months with no major difficulties. We consider it stable and
>  ready for production use.



---

### 2004\-09\-02 \- Version 3\.0\.6 (beta)


> Because of some important changes to sqlite3\_step(),
>  we have decided to
>  do an additional beta release prior to the first "stable" release.
>  If no serious problems are discovered in this version, we will
>  release version 3\.0 "stable" in about a week.



---

### 2004\-08\-29 \- Version 3\.0\.5 (beta)


> The fourth beta release of SQLite version 3\.0 is now available.
>  The next release is expected to be called "stable".



---

### 2004\-08\-08 \- Version 3\.0\.4 (beta)


> The third beta release of SQLite version 3\.0 is now available.
>  This new beta fixes several bugs including a database corruption
>  problem that can occur when doing a DELETE while a SELECT is pending.
>  Expect at least one more beta before version 3\.0 goes final.



---

### 2004\-07\-22 \- Version 3\.0\.3 (beta)


> The second beta release of SQLite version 3\.0 is now available.
>  This new beta fixes many bugs and adds support for databases with
>  varying page sizes. The next 3\.0 release will probably be called
>  a final or stable release.
>  Version 3\.0 adds support for internationalization and a new
>  more compact file format.
>  [Details.](version3.html)
>  The API and file format have been fixed since 3\.0\.2\. All
>  regression tests pass (over 100000 tests) and the test suite
>  exercises over 95% of the code.
> 
> 
>  SQLite version 3\.0 is made possible in part by AOL
>  developers supporting and embracing great Open\-Source Software.



---

### 2004\-07\-22 \- Version 2\.8\.15


> SQLite version 2\.8\.15 is a maintenance release for the version 2\.8
>  series. Version 2\.8 continues to be maintained with bug fixes, but
>  no new features will be added to version 2\.8\. All the changes in
>  this release are minor. If you are not having problems, there is
>  there is no reason to upgrade.



---

### 2004\-06\-30 \- Version 3\.0\.2 (beta) Released


> The first beta release of SQLite version 3\.0 is now available.
>  Version 3\.0 adds support for internationalization and a new
>  more compact file format.
>  [Details.](version3.html)
>  As of this release, the API and file format are frozen. All
>  regression tests pass (over 100000 tests) and the test suite
>  exercises over 95% of the code.
>  SQLite version 3\.0 is made possible in part by AOL
>  developers supporting and embracing great Open\-Source Software.



---

### 2004\-06\-25 \- Website hacked


> The www.sqlite.org website was hacked sometime around 2004\-06\-22
>  because the lead SQLite developer failed to properly patch CVS.
>  Evidence suggests that the attacker was unable to elevate privileges
>  above user "cvs". Nevertheless, as a precaution the entire website
>  has been reconstructed from scratch on a fresh machine. All services
>  should be back to normal as of 2004\-06\-28\.



---

### 2004\-06\-18 \- Version 3\.0\.0 (alpha) Released


> The first alpha release of SQLite version 3\.0 is available for
>  public review and comment. Version 3\.0 enhances internationalization support
>  through the use of UTF\-16 and user\-defined text collating sequences.
>  BLOBs can now be stored directly, without encoding.
>  A new file format results in databases that are 25% smaller (depending
>  on content). The code is also a little faster. In spite of the many
>  new features, the library footprint is still less than 240KB
>  (x86, gcc \-O1\).
>  [Additional information](version3.html).
>  Our intent is to freeze the file format and API on 2004\-07\-01\.
>  Users are encouraged to review and evaluate this alpha release carefully
>  and submit any feedback prior to that date.
> 
> 
>  The 2\.8 series of SQLite will continue to be supported with bug
>  fixes for the foreseeable future.



---

### 2004\-06\-09 \- Version 2\.8\.14 Released


> SQLite version 2\.8\.14 is a patch release to the stable 2\.8 series.
>  There is no reason to upgrade if 2\.8\.13 is working ok for you.
>  This is only a bug\-fix release. Most development effort is
>  going into version 3\.0\.0 which is due out soon.



---

### 2004\-05\-31 \- CVS Access Temporarily Disabled


> Anonymous access to the CVS repository will be suspended
>  for 2 weeks beginning on 2004\-06\-04\. Everyone will still
>  be able to download
>  prepackaged source bundles, create or modify trouble tickets, or view
>  change logs during the CVS service interruption. Full open access to the
>  CVS repository will be restored on 2004\-06\-18\.



---

### 2004\-04\-23 \- Work Begins On SQLite Version 3


> Work has begun on version 3 of SQLite. Version 3 is a major
>  changes to both the C\-language API and the underlying file format
>  that will enable SQLite to better support internationalization.
>  The first beta is schedule for release on 2004\-07\-01\.
>  Plans are to continue to support SQLite version 2\.8 with
>  bug fixes. But all new development will occur in version 3\.0\.



---


*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


