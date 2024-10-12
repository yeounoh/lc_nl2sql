




35% Faster Than The Filesystem




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










35% Faster Than The Filesystem


►
Table Of Contents
[1\. Summary](#summary)
[1\.1\. Caveats](#caveats)
[1\.2\. Related Studies](#related_studies)
[2\. How These Measurements Are Made](#how_these_measurements_are_made)
[2\.1\. Read Performance Measurements](#read_performance_measurements)
[2\.2\. Write Performance Measurements](#write_performance_measurements)
[2\.3\. Variations](#variations)
[3\. General Findings](#general_findings)
[4\. Additional Notes](#additional_notes)
[4\.1\. Compiling And Testing on Android](#compiling_and_testing_on_android)




# 1\. Summary


SQLite reads and writes small blobs (for example, thumbnail images)
[35% faster¹](#approx) than the same blobs
can be read from or written to individual files on disk using
fread() or fwrite().



Furthermore, a single SQLite database holding
10\-kilobyte blobs uses about 20% less disk space than
storing the blobs in individual files.



The performance difference arises (we believe) because when
working from an SQLite database, the open() and close() system calls
are invoked only once, whereas
open() and close() are invoked once for each blob
when using blobs stored in individual files. It appears that the
overhead of calling open() and close() is greater than the overhead
of using the database. The size reduction arises from the fact that
individual files are padded out to the next multiple of the filesystem
block size, whereas the blobs are packed more tightly into an SQLite
database.




The measurements in this article were made during the week of 2017\-06\-05
using a version of SQLite in between 3\.19\.2 and 3\.20\.0\. You may expect
future versions of SQLite to perform even better.



## 1\.1\. Caveats




¹The 35% figure above is approximate. Actual timings vary
depending on hardware, operating system, and the
details of the experiment, and due to random performance fluctuations
on real\-world hardware. See the text below for more detail.
Try the experiments yourself. Report significant deviations on
the [SQLite forum](support.html#fx).




The 35% figure is based on running tests on every machine
that the author has easily at hand.
Some reviewers of this article report that SQLite has higher 
latency than direct I/O on their systems. We do not yet understand
the difference. We also see indications that SQLite does not
perform as well as direct I/O when experiments are run using
a cold filesystem cache.




So let your take\-away be this: read/write latency for
SQLite is competitive with read/write latency of individual files on
disk. Often SQLite is faster. Sometimes SQLite is almost
as fast. Either way, this article disproves the common
assumption that a relational database must be slower than direct
filesystem I/O.



## 1\.2\. Related Studies



A [2022 study](https://golangexample.com/an-unscientific-benchmark-of-sqlite-vs-the-file-system-btrfs/)
([alternative link on GitHub](https://github.com/chrisdavies/dbench)) found that
SQLite is *roughly* twice as fast at real\-world workloads compared to Btrfs and Ext4 on Linux.




[Jim Gray](https://www.microsoft.com/en-us/research/people/gray/)
and others studied the read performance of BLOBs
versus file I/O for Microsoft SQL Server and found that reading BLOBs 
out of the 
database was faster for BLOB sizes less than between 250KiB and 1MiB.
([Paper](https://www.microsoft.com/en-us/research/publication/to-blob-or-not-to-blob-large-object-storage-in-a-database-or-a-filesystem/)).
In that study, the database still stores the filename of the content even
if the content is held in a separate file. So the database is consulted
for every BLOB, even if it is only to extract the filename. In this
article, the key for the BLOB is the filename, so no preliminary database
access is required. Because the database is never used at all when
reading content from individual files in this article, the threshold
at which direct file I/O becomes faster is smaller than it is in Gray's
paper.




The [Internal Versus External BLOBs](intern-v-extern-blob.html) article on this website is an
earlier investigation (circa 2011\) that uses the same approach as the
Jim Gray paper — storing the blob filenames as entries in the
database — but for SQLite instead of SQL Server.





# 2\. How These Measurements Are Made


I/O performance is measured using the
[kvtest.c](https://www.sqlite.org/src/file/test/kvtest.c) program
from the SQLite source tree.
To compile this test program, first gather the kvtest.c source file
into a directory with the [SQLite amalgamation](amalgamation.html) source
files "sqlite3\.c" and "sqlite3\.h". Then on unix, run a command like
the following:




```
gcc -Os -I. -DSQLITE_DIRECT_OVERFLOW_READ \
  kvtest.c sqlite3.c -o kvtest -ldl -lpthread

```

Or on Windows with MSVC:




```
cl -I. -DSQLITE_DIRECT_OVERFLOW_READ kvtest.c sqlite3.c

```

Instructions for compiling for Android
are [shown below](#compile-android).




Use the resulting "kvtest" program to
generate a test database with 100,000 random uncompressible
blobs, each with a random
size between 8,000 and 12,000 bytes
using a command like this:




```
./kvtest init test1.db --count 100k --size 10k --variance 2k

```


If desired, you can verify the new database by running this command:




```
./kvtest stat test1.db

```


Next, make copies of all the blobs into individual files in a directory
using a command like this:




```
./kvtest export test1.db test1.dir

```


At this point, you can measure the amount of disk space used by
the test1\.db database and the space used by the test1\.dir directory
and all of its content. On a standard Ubuntu Linux desktop, the
database file will be 1,024,512,000 bytes in size and the test1\.dir
directory will use 1,228,800,000 bytes of space (according to "du \-k"),
about 20% more than the database.




The "test1\.dir" directory created above puts all the blobs into a single
folder. It was conjectured that some operating systems would perform 
poorly when a single directory contains 100,000 objects. To test this,
the kvtest program can also store the blobs in a hierarchy of folders with no
more than 100 files and/or subdirectories per folder. The alternative
on\-disk representation of the blobs can be created using the \-\-tree
command\-line option to the "export" command, like this:




```
./kvtest export test1.db test1.tree --tree

```


The test1\.dir directory will contain 100,000 files
with names like "000000", "000001", "000002" and so forth but the
test1\.tree directory will contain the same files in subdirectories like
"00/00/00", "00/00/01", and so on. The test1\.dir and test1\.test
directories take up approximately the same amount of space, though
test1\.test is very slightly larger due to the extra directory entries.




All of the experiments that follow operate the same with either 
"test1\.dir" or "test1\.tree". Very little performance difference is
measured in either case, regardless of operating system.




Measure the performance for reading blobs from the database and from
individual files using these commands:




```
./kvtest run test1.db --count 100k --blob-api
./kvtest run test1.dir --count 100k --blob-api
./kvtest run test1.tree --count 100k --blob-api

```


Depending on your hardware and operating system, you should see that reads 
from the test1\.db database file are about 35% faster than reads from 
individual files in the test1\.dir or test1\.tree folders. Results can vary
significantly from one run to the next due to caching, so it is advisable
to run tests multiple times and take an average or a worst case or a best
case, depending on your requirements.



The \-\-blob\-api option on the database read test causes kvtest to use
the [sqlite3\_blob\_read()](c3ref/blob_read.html) feature of SQLite to load the content of the
blobs, rather than running pure SQL statements. This helps SQLite to run
a little faster on read tests. You can omit that option to compare the
performance of SQLite running SQL statements.
In that case, the SQLite still out\-performs direct reads, though
by not as much as when using [sqlite3\_blob\_read()](c3ref/blob_read.html).
The \-\-blob\-api option is ignored for tests that read from individual disk
files.




Measure write performance by adding the \-\-update option. This causes
the blobs are overwritten in place with another random blob of
exactly the same size.




```
./kvtest run test1.db --count 100k --update
./kvtest run test1.dir --count 100k --update
./kvtest run test1.tree --count 100k --update

```


The writing test above is not completely fair, since SQLite is doing
[power\-safe transactions](transactional.html) whereas the direct\-to\-disk writing is not.
To put the tests on a more equal footing, add either the \-\-nosync
option to the SQLite writes to disable calling fsync() or
FlushFileBuffers() to force content to disk, or using the \-\-fsync option
for the direct\-to\-disk tests to force them to invoke fsync() or
FlushFileBuffers() when updating disk files.




By default, kvtest runs the database I/O measurements all within
a single transaction. Use the \-\-multitrans option to run each blob
read or write in a separate transaction. The \-\-multitrans option makes
SQLite much slower, and uncompetitive with direct disk I/O. This
option proves, yet again, that to get the most performance out of
SQLite, you should group as much database interaction as possible within
a single transaction.




There are many other testing options, which can be seen by running
the command:




```
./kvtest help

```

## 2\.1\. Read Performance Measurements


The chart below shows data collected using 
[kvtest.c](https://www.sqlite.org/src/file/test/kvtest.c) on five different
systems:



* **Win7**: A circa\-2009 Dell Inspiron laptop, Pentium dual\-core
 at 2\.30GHz, 4GiB RAM, Windows7\.
* **Win10**: A 2016 Lenovo YOGA 910, Intel i7\-7500 at 2\.70GHz,
 16GiB RAM, Windows10\.
* **Mac**: A 2015 MacBook Pro, 3\.1GHz intel Core i7, 16GiB RAM,
 MacOS 10\.12\.5
* **Ubuntu**: Desktop built from Intel i7\-4770K at 3\.50GHz, 32GiB RAM,
 Ubuntu 16\.04\.2 LTS
* **Android**: Galaxy S3, ARMv7, 2GiB RAM


All machines use SSD except Win7 which has a
hard\-drive. The test database is 100K blobs with sizes uniformly
distributed between 8K and 12K, for a total of about 1 gigabyte
of content. The database page size
is 4KiB. The \-DSQLITE\_DIRECT\_OVERFLOW\_READ compile\-time option was
used for all of these tests.
Tests were run multiple times.
The first run was used to warm up the cache and its timings were discarded.




The chart below shows average time to read a blob directly from the
filesystem versus the time needed to read the same blob from the SQLite 
database.
The actual timings vary considerably from one system to another 
(the Ubuntu desktop is much
faster than the Galaxy S3 phone, for example). 
This chart shows the ratio of the
times needed to read blobs from a file divided by the time needed to
from the database. The left\-most column in the chart is the normalized
time to read from the database, for reference.




In this chart, an SQL statement ("SELECT v FROM kv WHERE k\=?1") 
is prepared once. Then for each blob, the blob key value is bound 
to the ?1 parameter and the statement is evaluated to extract the
blob content.




The chart shows that on Windows10, content can be read from the SQLite
database about 5 times faster than it can be read directly from disk.
On Android, SQLite is only about 35% faster than reading from disk.





![](images/faster-read-sql.jpg)

  

Chart 1: SQLite read latency relative to direct filesystem reads.  

100K blobs, avg 10KB each, random order using SQL


The performance can be improved slightly by bypassing the SQL layer
and reading the blob content directly using the
[sqlite3\_blob\_read()](c3ref/blob_read.html) interface, as shown in the next chart:





![](images/faster-read-blobapi.jpg)

  

Chart 2: SQLite read latency relative to direct filesystem reads.  

100K blobs, avg size 10KB, random order  

using sqlite3\_blob\_read().


Further performance improves can be made by using the
[memory\-mapped I/O](mmap.html) feature of SQLite. In the next chart, the
entire 1GB database file is memory mapped and blobs are read
(in random order) using the [sqlite3\_blob\_read()](c3ref/blob_read.html) interface.
With these optimizations, SQLite is twice as fast as Android
or MacOS\-X and over 10 times faster than Windows.





![](images/faster-read-mmap.jpg)

  

Chart 3: SQLite read latency relative to direct filesystem reads.  

100K blobs, avg size 10KB, random order  

using sqlite3\_blob\_read() from a memory\-mapped database.


The third chart shows that reading blob content out of SQLite can be
twice as fast as reading from individual files on disk for Mac and
Android, and an amazing ten times faster for Windows.



## 2\.2\. Write Performance Measurements



Writes are slower.
On all systems, using both direct I/O and SQLite, write performance is
between 5 and 15 times slower than reads.




Write performance measurements were made by replacing (overwriting)
an entire blob with a different blob. All of the blobs in these
experiment are random and incompressible. Because writes are so much
slower than reads, only 10,000 of the 100,000 blobs in the database
are replaced. The blobs to be replaced are selected at random and
are in no particular order.




The direct\-to\-disk writes are accomplished using fopen()/fwrite()/fclose().
By default, and in all the results shown below, the OS filesystem buffers are
never flushed to persistent storage using fsync() or
FlushFileBuffers(). In other words, there is no attempt to make the
direct\-to\-disk writes transactional or power\-safe.
We found that invoking fsync() or FlushFileBuffers() on each file
written causes direct\-to\-disk storage
to be about 10 times or more slower than writes to SQLite.




The next chart compares SQLite database updates in [WAL mode](wal.html)
against raw direct\-to\-disk overwrites of separate files on disk.
The [PRAGMA synchronous](pragma.html#pragma_synchronous) setting is NORMAL.
All database writes are in a single transaction.
The timer for the database writes is stopped after the transaction
commits, but before a [checkpoint](wal.html#ckpt) is run.
Note that the SQLite writes, unlike the direct\-to\-disk writes,
are [transactional](transactional.html) and [power\-safe](transactional.html), though because the synchronous
setting is NORMAL instead of FULL, the transactions are not durable.





![](images/faster-write-safe.jpg)

  

Chart 4: SQLite write latency relative to direct filesystem writes.  

10K blobs, avg size 10KB, random order,  

WAL mode with synchronous NORMAL,  

exclusive of checkpoint time


The android performance numbers for the write experiments are omitted
because the performance tests on the Galaxy S3 are so random. Two
consecutive runs of the exact same experiment would give wildly different
times. And, to be fair, the performance of SQLite on android is slightly
slower than writing directly to disk.




The next chart shows the performance of SQLite versus direct\-to\-disk
when transactions are disabled ([PRAGMA journal\_mode\=OFF](pragma.html#pragma_journal_mode))
and [PRAGMA synchronous](pragma.html#pragma_synchronous) is set to OFF. These settings put SQLite on an
equal footing with direct\-to\-disk writes, which is to say they make the
data prone to corruption due to system crashes and power failures.





![](images/faster-write-unsafe.jpg)

  

Chart 5: SQLite write latency relative to direct filesystem writes.  

10K blobs, avg size 10KB, random order,  

journaling disabled, synchronous OFF.


In all of the write tests, it is important to disable anti\-virus software
prior to running the direct\-to\-disk performance tests. We found that
anti\-virus software slows down direct\-to\-disk by an order of magnitude
whereas it impacts SQLite writes very little. This is probably due to the
fact that direct\-to\-disk changes thousands of separate files which all need
to be checked by anti\-virus, whereas SQLite writes only changes the single
database file.



## 2\.3\. Variations


The [\-DSQLITE\_DIRECT\_OVERFLOW\_READ](compile.html#direct_overflow_read) compile\-time option causes SQLite
to bypass its page cache when reading content from overflow pages. This
helps database reads of 10K blobs run a little faster, but not all that much
faster. SQLite still holds a speed advantage over direct filesystem reads
without the SQLITE\_DIRECT\_OVERFLOW\_READ compile\-time option.



Other compile\-time options such as using \-O3 instead of \-Os or
using [\-DSQLITE\_THREADSAFE\=0](compile.html#threadsafe) and/or some of the other
[recommended compile\-time options](compile.html#rcmd) might help SQLite to run even faster
relative to direct filesystem reads.



The size of the blobs in the test data affects performance.
The filesystem will generally be faster for larger blobs, since
the overhead of open() and close() is amortized over more bytes of I/O,
whereas the database will be more efficient in both speed and space
as the average blob size decreases.




# 3\. General Findings


1. SQLite is competitive with, and usually faster than, blobs stored in
separate files on disk, for both reading and writing.
2. SQLite is much faster than direct writes to disk on Windows
when anti\-virus protection is turned on. Since anti\-virus software
is and should be on by default in Windows, that means that SQLite
is generally much faster than direct disk writes on Windows.
3. Reading is about an order of magnitude faster than writing, for all
systems and for both SQLite and direct\-to\-disk I/O.
4. I/O performance varies widely depending on operating system and hardware.
Make your own measurements before drawing conclusions.
5. Some other SQL database engines advise developers to store blobs in separate
files and then store the filename in the database. In that case, where
the database must first be consulted to find the filename before opening
and reading the file, simply storing the entire blob in the database
gives much faster read and write performance with SQLite.
See the [Internal Versus External BLOBs](intern-v-extern-blob.html) article for more information.


# 4\. Additional Notes



## 4\.1\. Compiling And Testing on Android



The kvtest program is compiled and run on Android as follows.
First install the Android SDK and NDK. Then prepare a script
named "android\-gcc" that looks approximately like this:




```
#!/bin/sh
#
NDK=/home/drh/Android/Sdk/ndk-bundle
SYSROOT=$NDK/platforms/android-16/arch-arm
ABIN=$NDK/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin
GCC=$ABIN/arm-linux-androideabi-gcc
$GCC --sysroot=$SYSROOT -fPIC -pie $*

```

Make that script executable and put it on your $PATH. Then
compile the kvtest program as follows:




```
android-gcc -Os -I. kvtest.c sqlite3.c -o kvtest-android

```

Next, move the resulting kvtest\-android executable to the Android
device:




```
adb push kvtest-android /data/local/tmp

```

Finally use "adb shell" to get a shell prompt on the Android device,
cd into the /data/local/tmp directory, and begin running the tests
as with any other unix host.


*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


