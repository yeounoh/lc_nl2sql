




TH3




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










TH3


►
Table Of Contents
[1\. Overview](#overview)
[1\.1\. History](#history)
[2\. Operation](#operation)
[3\. Generating A Test Program](#generating_a_test_program)
[3\.1\. Test Automation Scripts](#test_automation_scripts)
[4\. Test Coverage](#test_coverage)
[5\. Mutation Testing](#mutation_testing)
[6\. TH3 License](#th3_license)




# 1\. Overview


SQLite Test Harness \#3 (hereafter "TH3") is one of
[three test harnesses](testing.html#harnesses) used for testing SQLite.
TH3 meets the following objectives:


* TH3 is able to run on embedded platforms that lack the support
 infrastructure of workstations.
* TH3 tests SQLite in an as\-deployed configuration using only
 published and documented interfaces.
 In other words, TH3 tests the compiled object code, not
 the source code, thus verifying that no problems were introduced
 by compiler bugs. "Test what you fly and fly what you test."
* TH3 checks SQLite's response to out\-of\-memory errors, disk I/O
 errors, and power loss during transaction commit.
* TH3 exercises SQLite in a variety of run\-time configurations
 (UTF8 vs UTF16, different pages sizes, varying journal modes, etc.)
* TH3 achieves 100% branch test coverage (and 100% 
 [MC/DC](https://en.wikipedia.org/wiki/Modified_condition/decision_coverage))
 over the SQLite core.
 (Test coverage of extensions such as FTS and RTREE is less than 100%).


TH3 was originally written for validation testing only, but has
subsequently been used for development testing and debugging
as well, and has proven very helpful in those roles. A full\-coverage
test takes less than five minutes on a workstation and hence
serves as a fast regression test during day\-to\-day maintenance
of the SQLite code base.


## 1\.1\. History


TH3 originated from an effort to test SQLite on 
[SymbianOS](https://en.wikipedia.org/wiki/Symbian).
Prior to TH3, all SQLite tests were run using the
[TCL](http://www.tcl.tk/) script language, but TCL would not (easily)
compile on SymbianOS which made testing difficult. The first attempt
to remedy this problem was the "TH1" (Test Harness \#1\) scripting 
language \- a reimplementation of parts of the TCL language in a 
more portable form that would compile and run on SymbianOS, and 
that was sufficient to run the SQLite tests. TH1
did not survive as a standard testing tool for SQLite,
but it did find continued service as a
scripting language used to customize the 
[Fossil](http://www.fossil-scm.org/) version control system.
There was also a "Test Harness \#2" which was an attempt to
create a simple scripting language using operator prefix notation
to drive tests. TH3 was the third attempt.



At about that same time, some avionics manufacturers were
expressing interest in SQLite, which prompted the SQLite developers
to design TH3 to support the rigorous testing standards of
[DO\-178B](https://en.wikipedia.org/wiki/DO-178B).



The first code for TH3 was laid down on 2008\-09\-25\.
An intense effort over the next 10 months resulted in TH3 achieving
100% MC/DC on 2009\-07\-25\. The TH3 code continues to be improved and
expanded.



As of 2018\-05\-19, the TH3 source tree consists 
and well over 500,000 lines of source code in 1709 separate files.



# 2\. Operation


TH3 is a test program generator. The output of TH3 is a program
implemented in C\-code and intended to be
linked against the SQLite library under test. The generated test
program is compiled and run on the target platform in order to verify
correct operation of SQLite on that platform.


The inputs to TH3 are test modules written in C or SQL and
small configuration
files that determine how to initialize SQLite. The
TH3 package includes 1,444 test
modules and more than 47 configurations (as of 2018\-05\-19\).
New modules and configurations
can be added to customize TH3 for specialized applications.
Each time TH3 is run, it reads
a subset of the available test modules and configuration files to generate
a custom C program that performs all of the specified tests under all
specified configurations. A complete test of SQLite normally involves running
TH3 multiple times to generate multiple test programs covering different
aspects of SQLite's operation, then linking all test programs against
a common SQLite library and running them separately on the target platform.



There are no arbitrary limits in TH3\. One could generate a
single test program that contained all test modules and all configuration files.
However, such a test program might be too large to deploy on embedded
platforms. (As of 2018\-05\-19, a full\-up TH3 test is over 850,000 lines and
58MB of C code.) TH3 provides the ability to break the library of test
modules up into smaller, more easily digested pieces.


Each individual test module might contain dozens, hundreds, or thousands
of separate tests. The test modules can be written in C or as scripts of
SQL or a mixture of the two. About two\-thirds of the existing test modules are
written in pure SQL with the remainder either in pure C or a combination 
of C and SQL.



Each test module file contains a header which describes the circumstances
under which the test is valid. For a particular configuration, only those
modules that are compatible with the configuration are run. 


# 3\. Generating A Test Program


The TH3 program generator is a TCL script named "mkth3\.tcl".
To generate a test program, one has merely to run this script and supply
the names of files containing test modules and configurations on the
command line. Test modules are files that use the ".test" suffix
and configurations are files that use the ".cfg" suffix. A
typical invocation of mkth3\.tcl might look something like the following:



```
tclsh mkth3.tcl *.test *.cfg >testprog1.c

```

The output from the mkth3\.tcl script is a C program that contains
everything needed to run the tests \- everything that is except for
the SQLite library itself. The generated test program contains 
implementations for all of the support interfaces used by the test
modules and it contains the main() routine that drives the
tests. To convert the test program into a working executable, simply
compile it against SQLite:



```
cc -o testprog1 testprog1.c sqlite3.c

```

The compilation step shown immediately above is merely representative.
In a working installation, one would normally want
to specify optimization parameters and compile\-time switches on the
compiler command line.


For testing on embedded systems, the mkth3\.tcl script and the compiler
steps shown above are performed on an ordinary workstation using
a cross\-compiler, then the resulting test program is
transferred onto the device to be run.


Once the test program is generated, it is run with no arguments to
perform the tests. Progress information as well as error diagnostics
appear on standard output. (Alternative output arrangements can be made
using a compile\-time option for embedded devices that lack a standard
output channel.) The program returns zero if there are no
errors and non\-zero if any problems were detected.


Typical output from a single TH3 test program run looks like this:




```
With SQLite 3.8.11 2015-05-15 04:13:15 56ef98a04765c34c1c2f3ed7a6f03a732f3b886e
-DSQLITE_COVERAGE_TEST
-DSQLITE_NO_SYNC
-DSQLITE_SYSTEM_MALLOC
-DSQLITE_THREADSAFE=1
Config-begin c1.
Begin c1.pager08
End c1.pager08
Begin c1.build33
End c1.build33
Begin c1.orderby01
End c1.orderby01
... 15014 lines of output omitted ....
Begin 64k.syscall01
End 64k.syscall01
Begin 64k.build01
End 64k.build01
Begin 64k.auth01
End 64k.auth01
Config-end 64k. TH3 memory used: 6373738
Config-begin wal1.
Begin wal1.wal37
End wal1.wal37
Config-end wal1. TH3 memory used: 100961
All 226 VDBE coverage points reached
th3: 0 errors out of 1442264 tests in 213.741 seconds. 64-bit little-endian
th3: SQLite 3.8.11 2015-05-15 04:13:15 56ef98a04765c34c1c2f3ed7a6f03a732f3b886e

```

The output begins with a report of the [SQLITE\_SOURCE\_ID](c3ref/c_source_id.html)
(cross\-checked again [sqlite3\_sourceid()](c3ref/libversion.html)) for the
SQLite under test and the compile\-time options used as reported
by [sqlite3\_compileoption\_get()](c3ref/compileoption_get.html). The output concludes with a summary
of the test results and a repeat of the [SQLITE\_SOURCE\_ID](c3ref/c_source_id.html). If any
errors are detected, additional lines detail the problem. The error
reporting lines always begin with a single space character so that they
can be quickly extracted from large output files using:




```
grep "^ "

```

The default output shows the beginning and end of each configuration
and test module combination. In the example above "c1" and "64k" are
configurations and "pager08", "build33", "orderby01", etc. are test modules.
Compile\-time and run\-time options are available to increase or decrease
the amount of output.
The output can be increased by showing each test case within each
test module. The output can be decreased
by degrees: omitting test modules starts and stops,
omitting configuration starts and stops, and finally by omitting all output.



## 3\.1\. Test Automation Scripts


TH3 comes with additional TCL scripts that help automate the testing
process on workstations. The "th3make" script automatically runs "mkth3\.tcl"
and "gcc" and then runs the resulting test program and checks the results.
Arguments to th3make include all of the "\*.test" test modules and 
"\*.cfg" configurations that are to be included in the test. Additional
options to th3make can cause the test program to be compiled using different
compilers (GCC, Clang, MSVC), to use different output verbosity levels, to
run the test program under valgrind, to check the output for coverage using
gcov, and so forth. The th3make script also accepts "\*.rc" filenames as
arguments. These \*.rc files are just collections of other arguments that
are commonly used together for a single purpose. For example, the "quick.rc"
file contains a set of eight arguments to th3make that run a fast (3\-minute)
full\-coverage test. This allows the operator to type "./th3make quick.rc" as
a short\-cut to typing out all of the required command\-line options. The
following are a few of the more than 40 available \*.rc files:



* **alignment***N***.rc** \- 
 These files contain \-D options to the compiler that are used by
 various notable downstreams.
* **cov.rc** \- Options for measuring test coverage
* **extensions.rc** \- Options to enable [FTS4](fts3.html#fts4), [R\-Trees](rtree.html),
 and [STAT4](fileformat2.html#stat4tab).
* **fast.rc** \- Run most tests, including those not needed for
 coverage, skipping only soak tests, using delivery compiler options
 (ex: \-O3\)
* **memdebug.rc** \- like test.rc but also enable
 [\-DSQLITE\_MEMDEBUG](compile.html#memdebug).
* **min.rc** \- Run the minimum set of tests needed for 100% coverage.
* **quick.rc** \- Run all tests required for 100% coverage tests
 using \-Os and [\-DSQLITE\_DEBUG](compile.html#debug).
* **test.rc** \- Run the same tests as in fast.rc but without
 compiler optimization and enabling options like
 [\-DSQLITE\_DEBUG](compile.html#debug) and
 \-DSQLITE\_ENABLE\_EXPENSIVE\_ASSERT.
* **test\-ex.rc** \- long\-running soak tests.


The TH3 repository also includes the "multitest.tcl" script, another
TCL script used to automate TH3 testing on workstations. Multitest.tcl
automatically compiles SQLite, then
runs ./th3make repeatedly with a variety of alignments, and captures
the output in a succinct summary screen. A typical multitest.tcl run
generates output that looks like this:




```
./multitest.tcl -q --jobs 3
start-time: 2018-05-19 03:17:12 UTC
file mkdir sqlite3bld
cd sqlite3bld
exec sh /ramdisk/sqlite/configure
file copy -force config.h ../config.h
exec make clean sqlite3.c
file rename sqlite3.c ../sqlite3.c
file rename sqlite3.h ../sqlite3.h
exec make clean sqlite3.c OPTS=-DSQLITE_ENABLE_UPDATE_DELETE_LIMIT=1
file rename sqlite3.c ../sqlite3udl.c
exec make clean sqlite3.c OPTS=-DSQLITE_SMALL_STACK=1
file rename sqlite3.c ../sqlite3ss.c
cd ..
*******************************************************************************
t01: cov.rc.................................................... Ok   (00:03:42)
t02: cov.rc ++STAT4 ++DESERIALIZE -D_HAVE_SQLITE_CONFIG_H...... Ok   (00:04:45)
t03: vfs-cov.rc................................................ Ok   (00:03:59)
t04: demo.rc................................................... Ok   (00:00:05)
t07: test.rc ../th3private/*.test.............................. Ok   (00:00:21)
t08: test.rc ../th3private/*.test ++STAT4...................... Ok   (00:01:41)
t05: quick.rc.................................................. Ok   (00:04:26)
t09: quick.rc ~TEST_REALLOC_STRESS -funsigned-char............. Ok   (00:05:39)
t10: quick.rc ~THREADSAFE=0 -DLONGDOUBLE_TYPE=double........... Ok   (00:03:24)
t06: quick.rc extensions.rc -D_HAVE_SQLITE_CONFIG_H............ Ok   (00:09:03)
t11: quick.rc sqlite3ss.c ~MAX_ATTACHED=125.................... Ok   (00:04:39)
t12: quick.rc ~BYTEORDER=0 ++RTREE............................. Ok   (00:07:28)
t13: quick.rc ~DISABLE_INTRINSIC ++RTREE....................... Ok   (00:07:31)
t16: quick.rc ~TRACE_SIZE_LIMIT=15 cov1/main16.test............ Ok   (00:00:22)
t14: quick.rc ~DIRECT_OVERFLOW_READ -fsigned-char.............. Ok   (00:04:35)
t15: quick.rc ~UNTESTABLE ~EXTRA_IFNULLROW..................... Ok   (00:01:44)
t17: quick.rc ~MAX_MMAP_SIZE=0................................. Ok   (00:04:46)
t18: quick.rc ++NULL_TRIM ++OFFSET_SQL_FUNC.................... Ok   (00:04:47)
t19: quick.rc ++BATCH_ATOMIC_WRITE ++DESERIALIZE............... Ok   (00:05:41)
t20: lean1.rc quick.rc......................................... Ok   (00:03:09)
t22: test.rc alignment2.rc sqlite3udl.c........................ Ok   (00:44:22)
t21: test.rc alignment1.rc..................................... Ok   (01:02:32)
t23: memdebug1.rc extensions.rc................................ Ok   (01:49:58)
t25: valgrind1.rc -O3 extensions.rc............................ Ok   (00:56:08)
t24: memdebug2.rc extensions.rc................................ Ok   (01:43:34)
t27: test-ex1.rc............................................... Ok   (00:45:00)
t26: valgrind2.rc -O3 extensions.rc............................ Ok   (01:02:52)
t29: test-ex3.rc............................................... Ok   (00:31:48)
t28: test-ex2.rc............................................... Ok   (01:12:03)
t30: test-ex4.rc............................................... Ok   (01:09:47)
t32: test.rc alignment4.rc -m32 CC=clang....................... Ok   (00:48:31)
t31: test.rc alignment3.rc sqlite3udl.c........................ Ok   (01:22:29)
t34: test.rc alignment6.rc..................................... Ok   (00:35:31)
t33: test.rc alignment5.rc extensions.rc....................... Ok   (00:59:33)
t35: test.rc alignment7.rc..................................... Ok   (00:44:10)
t40: fast.rc alignment2.rc sqlite3udl.c........................ Ok   (00:15:46)
t39: fast.rc alignment1.rc extensions.rc -m32.................. Ok   (00:33:19)
t36: test.rc ~MUTATION_TEST.................................... Ok   (00:35:45)
t42: fast.rc alignment4.rc..................................... Ok   (00:13:03)
t43: fast.rc alignment5.rc..................................... Ok   (00:13:32)
t44: fast.rc alignment6.rc..................................... Ok   (00:11:41)
t41: fast.rc alignment3.rc sqlite3udl.c........................ Ok   (00:26:31)
t45: fast.rc alignment7.rc..................................... Ok   (00:12:57)
t46: fast.rc -fsanitize=undefined.............................. Ok   (00:38:18)
*******************************************************************************
0 failures on 44 th3makes and 198583082 tests in (07:16:01) 3 cores on bella
SQLite 3.24.0 2018-05-18 17:58:33 c6071ac99cfa4b6272ac4d739fc61a85acb544f6c1c2a

```

As can be seen above, a single run
of multitest.tcl invokes th3make dozens of times and takes between 12 and 24
CPU hours. The middle section of the output shows the arguments to each
individual th3make run and the result and elapse time for that th3make.
All build products and output for the separate th3make runs are
captures in subdirectories for post\-test analysis.
The two\-line summary at the bottom shows the total number of errors and tests
over all th3make runs and the total elapse time, together with the 
[SQLITE\_SOURCE\_ID](c3ref/c_source_id.html) information for the version of SQLite that was
tested. This summary information is recorded in the
[release
checklist](https://www.sqlite.org/checklists) during final testing.



Abbreviations are applied in the multitest.tcl output so that
each th3make invocation will fit on a single 80\-column output line.
The initial "th3make" verb is omitted.
"\~" is shorthand for "\-DSQLITE\_" and "\+\+" is stands for
"\-DSQLITE\_ENABLE". Hence, multitest.tcl output line




```
quick.rc ~DISABLE_INTRINSIC ++RTREE

```

Really means




```
th3make quick.rc -DSQLITE_DISABLE_INTRINSIC -DSQLITE_ENABLE_RTREE

```

# 4\. Test Coverage


Using one particular subset of the available TH3 test modules (the "cov1"
tests) SQLite obtained 
[100% branch test coverage](testing.html#coverage) and 100% [MC/DC](testing.html#mcdc) as measured
by [gcov](http://gcc.gnu.org/onlinedocs/gcc/Gcov.html)
on Linux x86 and x86\_64 hardware. All releases of SQLite since
[version 3\.6\.17](releaselog/3_6_17.html) (2009\-08\-10\) have been tested to this standard. 
The SQLite developers 
are committed to maintaining 100% branch coverage and MC/DC for all 
future releases of SQLite.


The cov1 test set used to obtain 100% branch test coverage are only a
subset of the tests currently implemented using TH3\. New test modules are
added on a regular basis.



# 5\. Mutation Testing


The TH3 source tree contains a scripted name
"mutation\-test.tcl" that automates the process of
[mutation testing](testing.html#mutationtests).



The mutation\-test.tcl script takes care of all of the details for
running a mutation test:



1. The script compiles the TH3 test harness into machine code ("th3\.o") if
 necessary.
2. The script compiles the sqlite3\.c source file into assembly language
 ("sqlite3\.s") if necessary.
3. The script loops through instructions in the assembly language file
 to locate branch operations.
	1. The script makes a copy of the original sqlite3\.s file.
	2. The copy is edited to change the branch instruction into either
	 a no\-op or an unconditional jump.
	3. The copy of sqlite3\.s is assembled into sqlite3\.o then linked
	 again th3\.o to generate the "th3" executable.
	4. The "th3" binary is run and the output checked for errors.
4. The script shows progress for each cycle of the previous step then
 displays a summary of "survivors" at the end. A "survivor" is a
 mutation that was not detected by TH3\.


Mutation testing can be slow, since each test can take up to 5
minutes on a fast workstation, and there are two tests for each
branch instructions, and over 20,000 branch instructions. Efforts are
made to expedite operation. For example, TH3 is compiled in such a
way that it exits as soon as it finds the first error, and as many
of the mutations are easily detected, many cycles happen in only
a few seconds. Nevertheless, the mutation\-test.tcl script includes
command\-line options to limit the range of code lines tested so that
mutation testing only needs to be performed on blocks of code that
have recently changed.



# 6\. TH3 License


SQLite itself is in the [public domain](copyright.html) and
can be used for any purpose. But TH3 is proprietary and requires a license.



Even though open\-source users do not have direct access to TH3, all
users of SQLite benefit from TH3 indirectly since each version of SQLite is
validated running TH3 on multiple platforms (Linux, Windows, WinRT, Mac,
OpenBSD) prior to release. So anyone using an official release
of SQLite can deploy their application with the confidence of knowing that
it has been tested using TH3\. They simply cannot rerun those tests
themselves without purchasing a TH3 license.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


