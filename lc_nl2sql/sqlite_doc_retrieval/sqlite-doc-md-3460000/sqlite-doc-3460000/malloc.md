




Dynamic Memory Allocation In SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Dynamic Memory Allocation In SQLite


►
Table Of Contents
[1\. Features](#_features)
[2\. Testing](#_testing)
[2\.1\. Use of reallocarray()](#_use_of_reallocarray_)
[3\. Configuration](#_configuration)
[3\.1\. Alternative low\-level memory allocators](#_alternative_low_level_memory_allocators)
[3\.1\.1\. The default memory allocator](#the_default_memory_allocator)
[3\.1\.2\. The debugging memory allocator](#the_debugging_memory_allocator)
[3\.1\.3\. The Win32 native memory allocator](#the_win32_native_memory_allocator)
[3\.1\.4\. Zero\-malloc memory allocator](#zero_malloc_memory_allocator)
[3\.1\.5\. Experimental memory allocators](#experimental_memory_allocators)
[3\.1\.6\. Application\-defined memory allocators](#application_defined_memory_allocators)
[3\.1\.7\. Memory allocator overlays](#memory_allocator_overlays)
[3\.1\.8\. No\-op memory allocator stub](#no_op_memory_allocator_stub)
[3\.2\. Page cache memory](#_page_cache_memory)
[3\.3\. Lookaside memory allocator](#_lookaside_memory_allocator)
[3\.3\.1\. Two\-Size Lookaside](#two_size_lookaside)
[3\.4\. Memory status](#_memory_status)
[3\.5\. Setting memory usage limits](#_setting_memory_usage_limits)
[4\. Mathematical Guarantees Against Memory Allocation Failures](#_mathematical_guarantees_against_memory_allocation_failures)
[4\.1\. Computing and controlling parameters M and n](#_computing_and_controlling_parameters_m_and_n)
[4\.2\. Ductile failure](#_ductile_failure)
[5\. Stability Of Memory Interfaces](#_stability_of_memory_interfaces)




# Overview


SQLite uses dynamic memory allocation to obtain
memory for storing various objects
(ex: [database connections](c3ref/sqlite3.html) and [prepared statements](c3ref/stmt.html)) and to build
a memory cache of the database file and to hold the results of queries.
Much effort has gone into making the dynamic memory allocation subsystem
of SQLite reliable, predictable, robust, secure, and efficient.


This document provides an overview of dynamic memory allocation within 
SQLite. The target audience is software engineers who are tuning their
use of SQLite for peak performance in demanding environments.
Nothing in this document is required knowledge for using SQLite. The
default settings and configuration for SQLite will work well in most
applications. However, the information contained in this document may
be useful to engineers who are tuning SQLite to comply with special
requirements or to run under unusual circumstances.



# 1\.  Features


The SQLite core and its memory allocation subsystem provides the 
following capabilities:


* **Robust against allocation failures.**
If a memory allocation ever fails (that is to say, 
if malloc() or realloc() ever return NULL)
then SQLite will recover gracefully. SQLite will first attempt
to free memory from unpinned cache pages then retry the allocation
request. 
Failing that, SQLite will either stop what
it is doing and return the
[SQLITE\_NOMEM](rescode.html#nomem) error code back up to the application or it will
make do without the requested memory.
* **No memory leaks.**
The application is responsible for destroying any objects it allocates.
(For example, the application must use [sqlite3\_finalize()](c3ref/finalize.html) on 
every [prepared statement](c3ref/stmt.html) and [sqlite3\_close()](c3ref/close.html) on every 
[database connection](c3ref/sqlite3.html).) But as long as
the application cooperates, SQLite will never leak memory. This is
true even in the face of memory allocation failures or other system
errors.
* **Memory usage limits.**
The [sqlite3\_soft\_heap\_limit64()](c3ref/hard_heap_limit64.html) mechanism allows the application to
set a memory usage limit that SQLite strives to stay below. SQLite
will attempt to reuse memory from its caches rather than allocating new
memory as it approaches the soft limit.
* **Zero\-malloc option.**
The application can optionally provide SQLite with several buffers of bulk memory
at startup and SQLite will then use those provided buffers for all of
its memory allocation needs and never call system malloc() or free().
* **Application\-supplied memory allocators.**
The application can provide SQLite with pointers to alternative 
memory allocators at start\-time. The alternative memory allocator
will be used in place of system malloc() and free().
* **Proof against breakdown and fragmentation.**
SQLite can be configured so that, subject to certain usage constraints
detailed below, it is guaranteed to never fail a memory allocation
or fragment the heap.
This property is important to long\-running, high\-reliability
embedded systems where a memory allocation error could contribute
to an overall system failure.
* **Memory usage statistics.**
Applications can see how much memory they are using and detect when
memory usage is approaching or exceeding design boundaries.
* **Plays well with memory debuggers.**
Memory allocation in SQLite is structured so that standard
third\-party memory debuggers (such as [dmalloc](http://dmalloc.com) or 
[valgrind](http://valgrind.org)) can be used to verify correct
memory allocation behavior.
* **Minimal calls to the allocator.**
The system malloc() and free() implementations are inefficient
on many systems. SQLite strives to reduce overall processing time
by minimizing its use of malloc() and free().
* **Open access.**
Pluggable SQLite extensions or even the application itself can 
access to the same underlying memory allocation
routines used by SQLite through the
[sqlite3\_malloc()](c3ref/free.html), [sqlite3\_realloc()](c3ref/free.html), and [sqlite3\_free()](c3ref/free.html) interfaces.



# 2\.  Testing


Most of the code in the SQLite source tree is devoted purely to 
[testing and verification](testing.html). Reliability is important to SQLite.
Among the tasks of the test infrastructure is to ensure that
SQLite does not misuse dynamically allocated memory, that SQLite
does not leak memory, and that SQLite responds
correctly to a dynamic memory allocation failure.


The test infrastructure verifies that SQLite does not misuse
dynamically allocated memory by using a specially instrumented
memory allocator. The instrumented memory allocator is enabled
at compile\-time using the [SQLITE\_MEMDEBUG](compile.html#memdebug) option. The instrumented
memory allocator is much slower than the default memory allocator and
so its use is not recommended in production. But when
enabled during testing, 
the instrumented memory allocator performs the following checks:


* **Bounds checking.**
The instrumented memory allocator places sentinel values at both ends
of each memory allocation to verify that nothing within SQLite writes
outside the bounds of the allocation.
* **Use of memory after freeing.**
When each block of memory is freed, every byte is overwritten with a
nonsense bit pattern. This helps to ensure that no memory is ever
used after having been freed.
* **Freeing memory not obtained from malloc.**
Each memory allocation from the instrumented memory allocator contains
sentinels used to verify that every allocation freed came
from prior malloc.
* **Uninitialized memory.**
The instrumented memory allocator initializes each memory allocation
to a nonsense bit pattern to help ensure that the user makes no
assumptions about the content of allocation memory.


Regardless of whether or not the instrumented memory allocator is
used, SQLite keeps track of how much memory is currently checked out.
There are hundreds of test scripts used for testing SQLite. At the
end of each script, all objects are destroyed and a test is made to
ensure that all memory has been freed. This is how memory
leaks are detected. Notice that memory leak detection is in force at
all times, during test builds and during production builds. Whenever
one of the developers runs any individual test script, memory leak
detection is active. Hence memory leaks that do arise during development
are quickly detected and fixed.



The response of SQLite to out\-of\-memory (OOM) errors is tested using
a specialized memory allocator overlay that can simulate memory failures.
The overlay is a layer that is inserted in between the memory allocator
and the rest of SQLite. The overlay passes most memory allocation
requests straight through to the underlying allocator and passes the
results back up to the requester. But the overlay can be set to 
cause the Nth memory allocation to fail. To run an OOM test, the overlay
is first set to fail on the first allocation attempt. Then some test
script is run and verification that the allocation was correctly caught
and handled is made. Then the overlay is set to fail on the second
allocation and the test repeats. The failure point continues to advance
one allocation at a time until the entire test procedure runs to
completion without hitting a memory allocation error. This whole
test sequence run twice. On the first pass, the
overlay is set to fail only the Nth allocation. On the second pass,
the overlay is set to fail the Nth and all subsequent allocations.


Note that the memory leak detection logic continues to work even
when the OOM overlay is being used. This verifies that SQLite
does not leak memory even when it encounters memory allocation errors.
Note also that the OOM overlay can work with any underlying memory
allocator, including the instrumented memory allocator that checks
for memory allocation misuse. In this way it is verified that 
OOM errors do not induce other kinds of memory usage errors.


Finally, we observe that the instrumented memory allocator and the
memory leak detector both work over the entire SQLite test suite and
the [TCL test suite](testing.html#tcl) provides over 99% statement test coverage and that
the [TH3](th3.html) test harness provides [100% branch test coverage](testing.html#coverage)
with no leak leaks. This is
strong evidence that dynamic memory allocation is used correctly
everywhere within SQLite.



## 2\.1\.  Use of reallocarray()


The reallocarray() interface is a recent innovation (circa 2014\)
from the OpenBSD community that grow out of efforts to prevent the
next ["heartbleed" bug](http://heartbleed.com) by avoiding 32\-bit integer
arithmetic overflow on memory allocation size computations. The
reallocarray() function has both unit\-size and count parameters.
To allocate memory sufficient to hold an array of N elements each X\-bytes
in size, one calls "reallocarray(0,X,N)". This is preferred over
the traditional technique of invoking "malloc(X\*N)" as reallocarray()
eliminates the risk that the X\*N multiplication will overflow and
cause malloc() to return a buffer that is a different size from what
the application expected.


SQLite does not use reallocarray(). The reason is that reallocarray()
is not useful to SQLite. It turns out that SQLite never does memory
allocations that are the simple product of two integers. Instead, SQLite
does allocations of the form "X\+C" or "N\*X\+C" or "M\*N\*X\+C" or
"N\*X\+M\*Y\+C", and so forth. The reallocarray() interface is not helpful
in avoiding integer overflow in those cases.


Nevertheless, integer overflow in the computation of memory allocation
sizes is a concern that SQLite would like to deal with. To prevent
problems, all SQLite internal memory allocations occur using thin wrapper
functions that take a signed 64\-bit integer size parameter. The SQLite 
source code is audited to ensure that all size computations are carried 
out using 64\-bit signed integers as well. SQLite will
refuse to allocate more than about 2GB of memory at one go. (In common
use, SQLite seldom ever allocates more than about 8KB of memory at a time
so a 2GB allocation limit is not a burden.) So the 64\-bit size parameter
provides lots of headroom for detecting overflows. The same audit that
verifies that all size computations are done as 64\-bit signed integers
also verifies that it is impossible to overflow a 64\-bit integer
during the computation.


The code audits used to ensure that memory allocation size computations
do not overflow in SQLite are repeated prior to every SQLite release.



# 3\.  Configuration


The default memory allocation settings in SQLite are appropriate
for most applications. However, applications with unusual or particularly
strict requirements may want to adjust the configuration to more closely
align SQLite to their needs.
Both compile\-time and start\-time configuration options are available.



## 3\.1\.  Alternative low\-level memory allocators


The SQLite source code includes several different memory allocation
modules that can be selected at compile\-time, or to a limited extent
at start\-time.



### 3\.1\.1\. The default memory allocator


By default, SQLite uses the malloc(), realloc(), and free() routines
from the standard C library for its memory allocation needs. These routines
are surrounded by a thin wrapper that also provides a "memsize()" function
that will return the size of an existing allocation. The memsize() function
is needed to keep an accurate count of the number of bytes of outstanding
memory; memsize() determines how many bytes to remove from the outstanding
count when an allocation is freed. The default allocator implements
memsize() by always allocating 8 extra bytes on each malloc() request and
storing the size of the allocation in that 8\-byte header.


The default memory allocator is recommended for most applications.
If you do not have a compelling need to use an alternative memory
allocator, then use the default.



### 3\.1\.2\. The debugging memory allocator


If SQLite is compiled with the [SQLITE\_MEMDEBUG](compile.html#memdebug) compile\-time option,
then a different, heavy wrapper is used around system malloc(), realloc(), 
and free().
The heavy wrapper allocates around 100 bytes of extra space
with each allocation. The extra space is used to place sentinel values 
at both ends of the allocation returned to the SQLite core. When an
allocation is freed,
these sentinels are checked to make sure the SQLite core did not overrun
the buffer in either direction. When the system library is GLIBC, the 
heavy wrapper also makes use of the GNU backtrace() function to examine
the stack and record the ancestor functions of the malloc() call. When
running the SQLite test suite, the heavy wrapper also records the name of
the current test case. These latter two features are useful for
tracking down the source of memory leaks detected by the test suite.


The heavy wrapper that is used when [SQLITE\_MEMDEBUG](compile.html#memdebug) is set also
makes sure each new allocation is filled with nonsense data prior to
returning the allocation to the caller. And as soon as an allocation
is free, it is again filled with nonsense data. These two actions help
to ensure that the SQLite core does not make assumptions about the state
of newly allocated memory and that memory allocations are not used after
they have been freed.


The heavy wrapper employed by [SQLITE\_MEMDEBUG](compile.html#memdebug) is intended for use
only during testing, analysis, and debugging of SQLite. The heavy wrapper
has a significant performance and memory overhead and probably should not
be used in production.



### 3\.1\.3\. The Win32 native memory allocator


If SQLite is compiled for Windows with the [SQLITE\_WIN32\_MALLOC](compile.html#win32_malloc)
compile\-time option, then a different, thin wrapper is used around
HeapAlloc(), HeapReAlloc(), and HeapFree(). The thin wrapper uses the
configured SQLite heap, which will be different from the default process
heap if the [SQLITE\_WIN32\_HEAP\_CREATE](compile.html#win32_heap_create) compile\-time option is used. In
addition, when an allocation is made or freed, HeapValidate() will be
called if SQLite is compiled with assert() enabled and the
[SQLITE\_WIN32\_MALLOC\_VALIDATE](compile.html#win32_malloc_validate) compile\-time option.



### 3\.1\.4\. Zero\-malloc memory allocator


When SQLite is compiled with the [SQLITE\_ENABLE\_MEMSYS5](compile.html#enable_memsys5) option, an
alternative memory allocator that does not use malloc() is included in the
build. The SQLite developers refer to this alternative memory allocator
as "memsys5". Even when it is included in the build, memsys5 is 
disabled by default.
To enable memsys5, the application must invoke the following SQLite 
interface at start\-time:



> ```
> 
> [sqlite3_config](c3ref/config.html)([SQLITE_CONFIG_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap), pBuf, szBuf, mnReq);
> 
> ```


In the call above, pBuf is a pointer to a large, contiguous chunk
of memory space that SQLite will use to satisfy all of its memory
allocation needs. pBuf might point to a static array or it might
be memory obtained from some other application\-specific mechanism.
szBuf is an integer that is the number of bytes of memory space
pointed to by pBuf. mnReq is another integer that is the
minimum size of an allocation. Any call to [sqlite3\_malloc(N)](c3ref/free.html) where
N is less than mnReq will be rounded up to mnReq. mnReq must be
a power of two. We shall see later that the mnReq parameter is
important in reducing the value of **n** and hence the minimum memory
size requirement in the [Robson proof](malloc.html#nofrag).


The memsys5 allocator is designed for use on embedded systems, 
though there is nothing to prevent its use on workstations.
The szBuf is typically between a few hundred kilobytes up to a few
dozen megabytes, depending on system requirements and memory budget.


The algorithm used by memsys5 can be called "power\-of\-two,
first\-fit". The sizes of all memory allocation 
requests are rounded up to a power of two and the request is satisfied
by the first free slot in pBuf that is large enough. Adjacent freed
allocations are coalesced using a buddy system. When used appropriately,
this algorithm provides mathematical guarantees against fragmentation and
breakdown, as described further [below](#nofrag).



### 3\.1\.5\. Experimental memory allocators


The name "memsys5" used for the zero\-malloc memory allocator implies
that there are several additional memory allocators available, and indeed
there are. The default memory allocator is "memsys1". The debugging
memory allocator is "memsys2". Those have already been covered.


If SQLite is compiled with [SQLITE\_ENABLE\_MEMSYS3](compile.html#enable_memsys3) then another
zero\-malloc memory allocator, similar to memsys5, is included in the
source tree. The memsys3 allocator, like memsys5, must be activated
by a call to [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap),...). Memsys3
uses the memory buffer supplied as its source for all memory allocations.
The difference between memsys3 and memsys5 is that memsys3 uses a
different memory allocation algorithm that seems to work well in
practice, but which does not provide mathematical
guarantees against memory fragmentation and breakdown. Memsys3 was
a predecessor to memsys5\. The SQLite developers now believe that 
memsys5 is superior to
memsys3 and that all applications that need a zero\-malloc memory
allocator should use memsys5 in preference to memsys3\. Memsys3 is
considered both experimental and deprecated and will likely be removed 
from the source tree in a future release of SQLite.


Memsys4 and memsys6 were experimental memory allocators
introduced in around 2007 and subsequently removed from the
source tree in around 2008, after it became clear that they
added no new value.


Other experimental memory allocators might be added in future releases
of SQLite. One may anticipate that these will be called memsys7, memsys8,
and so forth.



### 3\.1\.6\. Application\-defined memory allocators


New memory allocators do not have to be part of the SQLite source tree
nor included in the sqlite3\.c [amalgamation](amalgamation.html). Individual applications can
supply their own memory allocators to SQLite at start\-time.


To cause SQLite to use a new memory allocator, the application
simply calls:



> ```
> 
> [sqlite3_config](c3ref/config.html)([SQLITE_CONFIG_MALLOC](c3ref/c_config_covering_index_scan.html#sqliteconfigmalloc), pMem);
> 
> ```


In the call above, pMem is a pointer to an [sqlite3\_mem\_methods](c3ref/mem_methods.html) object
that defines the interface to the application\-specific memory allocator.
The [sqlite3\_mem\_methods](c3ref/mem_methods.html) object is really just a structure containing
pointers to functions to implement the various memory allocation primitives.



In a multi\-threaded application, access to the [sqlite3\_mem\_methods](c3ref/mem_methods.html)
is serialized if and only if [SQLITE\_CONFIG\_MEMSTATUS](c3ref/c_config_covering_index_scan.html#sqliteconfigmemstatus) is enabled.
If [SQLITE\_CONFIG\_MEMSTATUS](c3ref/c_config_covering_index_scan.html#sqliteconfigmemstatus) is disabled then the methods in
[sqlite3\_mem\_methods](c3ref/mem_methods.html) must take care of their own serialization needs.



### 3\.1\.7\. Memory allocator overlays


An application can insert layers or "overlays" in between the
SQLite core and the underlying memory allocator.
For example, the [out\-of\-memory test logic](#oomtesting)
for SQLite uses an overlay that can simulate memory allocation
failures.


An overlay can be created by using the



> ```
> 
> [sqlite3_config](c3ref/config.html)([SQLITE_CONFIG_GETMALLOC](c3ref/c_config_covering_index_scan.html#sqliteconfiggetmalloc), pOldMem);
> 
> ```


interface to obtain pointers to the existing memory allocator.
The existing allocator is saved by the overlay and is used as
a fallback to do real memory allocation. Then the overlay is
inserted in place of the existing memory allocator using
the [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_MALLOC](c3ref/c_config_covering_index_scan.html#sqliteconfigmalloc),...) as described
[above](#appalloc).




### 3\.1\.8\. No\-op memory allocator stub


If SQLite is compiled with the [SQLITE\_ZERO\_MALLOC](compile.html#zero_malloc) option, then
the [default memory allocator](malloc.html#defaultalloc) is omitted and replaced by a stub
memory allocator that never allocates any memory. Any calls to the
stub memory allocator will report back that no memory is available.


The no\-op memory allocator is not useful by itself. It exists only
as a placeholder so that SQLite has a memory allocator to link against
on systems that may not have malloc(), free(), or realloc() in their
standard library.
An application that is compiled with [SQLITE\_ZERO\_MALLOC](compile.html#zero_malloc) will need to
use [sqlite3\_config()](c3ref/config.html) together with [SQLITE\_CONFIG\_MALLOC](c3ref/c_config_covering_index_scan.html#sqliteconfigmalloc) or
[SQLITE\_CONFIG\_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap) to specify a new alternative memory allocator
before beginning to use SQLite.



## 3\.2\.  Page cache memory


In most applications, the database page cache subsystem within 
SQLite uses more dynamically allocated memory than all other parts
of SQLite combined. It is not unusual to see the database page cache
consume over 10 times more memory than the rest of SQLite combined.


SQLite can be configured to make page cache memory allocations from
a separate and distinct memory pool of fixed\-size
slots. This can have two advantages:


* Because allocations are all the same size, the memory allocator can
operate much faster. The allocator need not bother with coalescing 
adjacent free slots or searching for a slot
of an appropriate size. All unallocated memory slots can be stored on
a linked list. Allocating consists of removing the first entry from the
list. Deallocating is simply adding an entry to the beginning of the list.
* With a single allocation size, the **n** parameter in the
[Robson proof](malloc.html#nofrag) is 1, and the total memory space required by the allocator
(**N**) is exactly equal to maximum memory used (**M**). 
No additional memory is required to cover fragmentation overhead, thus 
reducing memory requirements. This is particularly important for the
page cache memory since the page cache constitutes the largest component
of the memory needs of SQLite.


The page\-cache memory allocator is disabled by default.
An application can enable it at start\-time as follows:



> ```
> 
> [sqlite3_config](c3ref/config.html)([SQLITE_CONFIG_PAGECACHE](c3ref/c_config_covering_index_scan.html#sqliteconfigpagecache), pBuf, sz, N);
> 
> ```


The pBuf parameter is a pointer to a contiguous range of bytes that
SQLite will use for page\-cache memory allocations. The buffer must be
at least sz\*N bytes in size. The "sz" parameter
is the size of each page\-cache allocation. N is the maximum 
number of available allocations.


If SQLite needs a page\-cache entry that is larger than "sz" bytes or
if it needs more than N entries, it falls back to using the
general\-purpose memory allocator.



## 3\.3\.  Lookaside memory allocator


SQLite [database connections](c3ref/sqlite3.html) make many
small and short\-lived memory allocations.
This occurs most commonly when compiling SQL statements using
[sqlite3\_prepare\_v2()](c3ref/prepare.html) but also to a lesser extent when running
[prepared statements](c3ref/stmt.html) using [sqlite3\_step()](c3ref/step.html). These small memory
allocations are used to hold things such as the names of tables
and columns, parse tree nodes, individual query results values,
and B\-Tree cursor objects. There are consequently
many calls to malloc() and free() \- so many calls that malloc() and
free() end up using a significant fraction of the CPU time assigned
to SQLite.


SQLite [version 3\.6\.1](releaselog/3_6_1.html) (2008\-08\-06\)
introduced the lookaside memory allocator to
help reduce the memory allocation load. In the lookaside allocator,
each [database connection](c3ref/sqlite3.html) preallocates a single large chunk of memory
(typically in the range of 60 to 120 kilobytes) and divides that chunk
up into small fixed\-size "slots" of around 100 to 1000 byte each. This
becomes the lookaside memory pool. Thereafter, memory allocations
associated with the [database connection](c3ref/sqlite3.html) and that are not too large
are satisfied using one of the lookaside pool slots rather than by calling
the general\-purpose memory allocator. Larger allocations continue to
use the general\-purpose memory allocator, as do allocations that occur
when the lookaside pool slots are all checked out. 
But in many cases, the memory
allocations are small enough and there are few enough outstanding that
the new memory requests can be satisfied from the lookaside
pool.


Because lookaside allocations are always the same size, the allocation
and deallocation algorithms are very quick. There is no
need to coalesce adjacent free slots or search for a slot
of a particular size. Each [database connection](c3ref/sqlite3.html) maintains a singly\-linked
list of unused slots. Allocation requests simply pull the first
element of this list. Deallocations simply push the element back onto
the front of the list.
Furthermore, each [database connection](c3ref/sqlite3.html) is assumed to already be
running in a single thread (there are mutexes already in
place to enforce this) so no additional mutexing is required to 
serialize access to the lookaside slot freelist.
Consequently, lookaside memory
allocations and deallocations are very fast. In speed tests on
Linux and Mac OS X workstations, SQLite has shown overall performance
improvements as high as 10% and 15%, depending on the workload how
and lookaside is configured.


The size of the lookaside memory pool has a global default value
but can also be configured on a connection\-by\-connection basis.
To change the default size of the lookaside memory pool at
compile\-time, use the 
[\-DSQLITE\_DEFAULT\_LOOKASIDE\=*SZ,N*](compile.html#default_lookaside)
option.
To change the default size of the lookaside memory pool at
start\-time, use the [sqlite3\_config()](c3ref/config.html) interface:



> ```
> 
> [sqlite3_config](c3ref/config.html)([SQLITE_CONFIG_LOOKASIDE](c3ref/c_config_covering_index_scan.html#sqliteconfiglookaside), sz, cnt);
> 
> ```


The "sz" parameter is the size in bytes of each lookaside slot.
The "cnt" parameter is
the total number of lookaside memory slots per database connection.
The total amount
of lookaside memory allocated to each [database connection](c3ref/sqlite3.html) is
sz\*cnt bytes. 



The lookaside pool can be changed for an individual
[database connection](c3ref/sqlite3.html) "db" using this call:



> ```
> 
> [sqlite3_db_config](c3ref/db_config.html)(db, [SQLITE_DBCONFIG_LOOKASIDE](c3ref/c_dbconfig_defensive.html#sqlitedbconfiglookaside), pBuf, sz, cnt);
> 
> ```


The "pBuf" parameter is a pointer to memory space that will be
used for the lookaside memory pool. If pBuf is NULL, then SQLite
will obtain its own space for the memory pool using [sqlite3\_malloc()](c3ref/free.html).
The "sz" and "cnt" parameters are the size of each lookaside slot
and the number of slots, respectively. If pBuf is not NULL, then it
must point to at least sz\*cnt bytes of memory.


The lookaside configuration can only be changed while there are
no outstanding lookaside allocations for the database connection.
Hence, the configuration should be set immediately after creating the 
database connection using [sqlite3\_open()](c3ref/open.html) (or equivalent) and before
evaluating any SQL statements on the connection.


### 3\.3\.1\. Two\-Size Lookaside



Beginning with SQLite version 3\.31\.0 (2020\-01\-22\),
lookaside supports two memory pools, each with a different size
slot. The small\-slot pool uses 128\-byte slots and the large\-slot
pool uses whatever size is specified by [SQLITE\_DBCONFIG\_LOOKASIDE](c3ref/c_dbconfig_defensive.html#sqlitedbconfiglookaside)
(defaulting to 1200 bytes). Splitting the pool in two like this
allows memory allocations to be covered by lookaside more often
while at the same time reducing per\-database\-connection heap usage
from 120KB down to 48KB.




Configuration continues to use the SQLITE\_DBCONFIG\_LOOKASIDE or
SQLITE\_CONFIG\_LOOKASIDE configuration options, as described above,
with parameters "sz" and "cnt". The total heap space used for
lookaside continues to be sz\*cnt bytes. But the space is allocated
between the small\-slot lookaside and big\-slot lookaside, with
preference given to small\-slot lookaside. The total number of
slots will usually exceed "cnt", since "sz" is typically much
larger than the small\-slot size of 128 bytes.




The default lookaside configuration has changed from 100 slots
of 1200 bytes each (120KB) to be 40 slots of 1200 bytes each
(48KB). This space ends up being allocated as 93 slots of
128 bytes each and 30 slots of 1200 bytes each. So more lookaside
slots are available but much less heap space is used.




The default lookaside configuration, the size of the small\-slots,
and the details of how heap space is allocated between small\-slots
and big\-slots, are all subject to change from one release to the
next.





## 3\.4\.  Memory status


By default, SQLite keeps statistics on its memory usage. These
statistics are useful in helping to determine how much memory an
application really needs. The statistics can also be used in
high\-reliability system to determine
if the memory usage is coming close to or exceeding the limits 
of the [Robson proof](malloc.html#nofrag) and hence that the memory allocation subsystem is 
liable to breakdown.


Most memory statistics are global, and therefore the tracking of
statistics must be serialized with a mutex. Statistics are turned 
on by default, but an option exists to disable them. By disabling 
memory statistics,
SQLite avoids entering and leaving a mutex on each memory allocation
and deallocation. That savings can be noticeable on systems where
mutex operations are expensive. To disable memory statistics, the
following interface is used at start\-time:



> ```
> 
> [sqlite3_config](c3ref/config.html)([SQLITE_CONFIG_MEMSTATUS](c3ref/c_config_covering_index_scan.html#sqliteconfigmemstatus), onoff);
> 
> ```


The "onoff" parameter is true to enable the tracking of memory
statistics and false to disable statistics tracking.


Assuming statistics are enabled, the following routine can be used
to access them:



> ```
> 
> [sqlite3_status](c3ref/status.html)([verb](c3ref/c_status_malloc_count.html#sqlitestatusmemoryused), &current, &highwater, resetflag);
> 
> ```


The "verb" argument determines what statistic is accessed.
There are [various verbs](c3ref/c_status_malloc_count.html#sqlitestatusmemoryused) defined. The
list is expected to grow as the [sqlite3\_status()](c3ref/status.html) interface matures.
The current value the selected parameter is written into integer 
"current" and the highest historical value
is written into integer "highwater". If resetflag is true, then
the high\-water mark is reset down to the current value after the call
returns.


A different interface is used to find statistics associated with a
single [database connection](c3ref/sqlite3.html):



> ```
> 
> [sqlite3_db_status](c3ref/db_status.html)(db, [verb](c3ref/c_dbstatus_options.html#sqlitedbstatuslookasideused), &current, &highwater, resetflag);
> 
> ```


This interface is similar except that it takes a pointer to
a [database connection](c3ref/sqlite3.html) as its first argument and returns statistics about
that one object rather than about the entire SQLite library.
The [sqlite3\_db\_status()](c3ref/db_status.html) interface currently only recognizes a
single verb [SQLITE\_DBSTATUS\_LOOKASIDE\_USED](c3ref/c_dbstatus_options.html#sqlitedbstatuslookasideused), though additional verbs
may be added in the future.


The per\-connection statistics do not use global variables and hence
do not require mutexes to update or access. Consequently the
per\-connection statistics continue to function even if
[SQLITE\_CONFIG\_MEMSTATUS](c3ref/c_config_covering_index_scan.html#sqliteconfigmemstatus) is turned off.



## 3\.5\.  Setting memory usage limits


The [sqlite3\_soft\_heap\_limit64()](c3ref/hard_heap_limit64.html) interface can be used to set an
upper bound on the total amount of outstanding memory that the
general\-purpose memory allocator for SQLite will allow to be outstanding
at one time. If attempts are made to allocate more memory than specified
by the soft heap limit, then SQLite will first attempt to free cache
memory before continuing with the allocation request. The soft heap
limit mechanism only works if [memory statistics](malloc.html#memstatus) are enabled and
it works best
if the SQLite library is compiled with the [SQLITE\_ENABLE\_MEMORY\_MANAGEMENT](compile.html#enable_memory_management)
compile\-time option.


The soft heap limit is "soft" in this sense: If SQLite is not able
to free up enough auxiliary memory to stay below the limit, it goes
ahead and allocates the extra memory and exceeds its limit. This occurs
under the theory that it is better to use additional memory than to fail
outright.


As of SQLite [version 3\.6\.1](releaselog/3_6_1.html) (2008\-08\-06\), 
the soft heap limit only applies to the
general\-purpose memory allocator. The soft heap limit does not know
about or interact with
the [pagecache memory allocator](malloc.html#pagecache) or the [lookaside memory allocator](malloc.html#lookaside).
This deficiency will likely be addressed in a future release.



# 4\.  Mathematical Guarantees Against Memory Allocation Failures


The problem of dynamic memory allocation, and specifically the
problem of a memory allocator breakdown, has been studied by
J. M. Robson and the results published as:



> J. M. Robson. "Bounds for Some Functions Concerning Dynamic
> Storage Allocation". *Journal of the Association for
> Computing Machinery*, Volume 21, Number 8, July 1974,
> pages 491\-499\.


Let us use the following notation (similar but not identical to
Robson's notation):



> | **N** | The amount of raw memory needed by the memory allocation system in order to guarantee that no memory allocation will ever fail. |
> | --- | --- |
> | **M** | The maximum amount of memory that the application ever has checked out at any point in time. |
> | **n** | The ratio of the largest memory allocation to the smallest. We assume that every memory allocation size is an integer multiple of the smallest memory allocation size. |


Robson proves the following result:



> **N** \= **M**\*(1 \+ (log2 **n**)/2\) \- **n** \+ 1


Colloquially, the Robson proof shows that in order to guarantee
breakdown\-free operation, any memory allocator must use a memory pool
of size **N** which exceeds the maximum amount of memory ever
used **M** by a multiplier that depends on **n**, 
the ratio of the largest to the smallest allocation size. In other
words, unless all memory allocations are of exactly the same size
(**n**\=1\) then the system needs access to more memory than it will
ever use at one time. Furthermore, we see that the amount of surplus
memory required grows rapidly as the ratio of largest to smallest
allocations increases, and so there is strong incentive to keep all
allocations as near to the same size as possible.


Robson's proof is constructive. 
He provides an algorithm for computing a sequence of allocation
and deallocation operations that will lead to an allocation failure due to
memory fragmentation if available memory is as much as one byte
less than **N**.
And, Robson shows that a power\-of\-two first\-fit memory allocator
(such as implemented by [memsys5](malloc.html#memsys5)) will never fail a memory allocation
provided that available memory is **N** or more bytes.


The values **M** and **n** are properties of the application.
If an application is constructed in such a way that both **M** and
**n** are known, or at least have known upper bounds, and if the
application uses
the [memsys5](malloc.html#memsys5) memory allocator and is provided with **N** bytes of
available memory space using [SQLITE\_CONFIG\_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap)
then Robson proves that no memory allocation request will ever fail
within the application.
To put this another way, the application developer can select a value
for **N** that will guarantee that no call to any SQLite interface
will ever return [SQLITE\_NOMEM](rescode.html#nomem). The memory pool will never become
so fragmented that a new memory allocation request cannot be satisfied.
This is an important property for
applications where a software fault could cause injury, physical harm, or
loss of irreplaceable data.


## 4\.1\.  Computing and controlling parameters **M** and **n**


The Robson proof applies separately to each of the memory allocators
used by SQLite:


* The general\-purpose memory allocator ([memsys5](malloc.html#memsys5)).
* The [pagecache memory allocator](malloc.html#pagecache).
* The [lookaside memory allocator](malloc.html#lookaside).


For allocators other than [memsys5](malloc.html#memsys5),
all memory allocations are of the same size. Hence, **n**\=1
and therefore **N**\=**M**. In other words, the memory pool need
be no larger than the largest amount of memory in use at any given moment.


The usage of pagecache memory is somewhat harder to control in
SQLite version 3\.6\.1, though mechanisms are planned for subsequent
releases that will make controlling pagecache memory much easier.
Prior to the introduction of these new mechanisms, the only way
to control pagecache memory is using the [cache\_size pragma](pragma.html#pragma_cache_size).


Safety\-critical applications will usually want to modify the
default lookaside memory configuration so that when the initial
lookaside memory buffer is allocated during [sqlite3\_open()](c3ref/open.html) the
resulting memory allocation is not so large as to force the **n**
parameter to be too large. In order to keep **n** under control,
it is best to try to keep the largest memory allocation below 2 or 4
kilobytes. Hence, a reasonable default setup for the lookaside
memory allocator might any one of the following:



> ```
> 
> sqlite3_config(SQLITE_CONFIG_LOOKASIDE, 32, 32);  /* 1K */
> sqlite3_config(SQLITE_CONFIG_LOOKASIDE, 64, 32);  /* 2K */
> sqlite3_config(SQLITE_CONFIG_LOOKASIDE, 32, 64);  /* 2K */
> sqlite3_config(SQLITE_CONFIG_LOOKASIDE, 64, 64);  /* 4K */
> 
> ```


Another approach is to initially disable the lookaside memory
allocator:



> ```
> 
> sqlite3_config(SQLITE_CONFIG_LOOKASIDE, 0, 0);
> 
> ```


Then let the application maintain a separate pool of larger
lookaside memory buffers that it can distribute to [database connections](c3ref/sqlite3.html)
as they are created. In the common case, the application will only
have a single [database connection](c3ref/sqlite3.html) and so the lookaside memory pool
can consist of a single large buffer.



> ```
> 
> sqlite3_db_config(db, SQLITE_DBCONFIG_LOOKASIDE, aStatic, 256, 500);
> 
> ```


The lookaside memory allocator is really intended as performance
optimization, not as a method for assuring breakdown\-free memory allocation,
so it is not unreasonable to completely disable the lookaside memory
allocator for safety\-critical operations.


The general purpose memory allocator is the most difficult memory pool
to manage because it supports allocations of varying sizes. Since 
**n** is a multiplier on **M** we want to keep **n** as small
as possible. This argues for keeping the minimum allocation size for
[memsys5](malloc.html#memsys5) as large as possible. In most applications, the
[lookaside memory allocator](malloc.html#lookaside) is able to handle small allocations. So
it is reasonable to set the minimum allocation size for [memsys5](malloc.html#memsys5) to
2, 4 or even 8 times the maximum size of a lookaside allocation. 
A minimum allocation size of 512 is a reasonable setting.


Further to keeping **n** small, one desires to keep the size of
the largest memory allocations under control.
Large requests to the general\-purpose memory allocator
might come from several sources:


1. SQL table rows that contain large strings or BLOBs.
2. Complex SQL queries that compile down to large [prepared statements](c3ref/stmt.html).
3. SQL parser objects used internally by [sqlite3\_prepare\_v2()](c3ref/prepare.html).
4. Storage space for [database connection](c3ref/sqlite3.html) objects.
5. Page cache memory allocations that overflow into the general\-purpose
 memory allocator.
6. Lookaside buffer allocations for new [database connections](c3ref/sqlite3.html).


The last two allocations can be controlled and/or eliminated by
configuring the [pagecache memory allocator](malloc.html#pagecache),
and [lookaside memory allocator](malloc.html#lookaside) appropriately, as described above.
The storage space required for [database connection](c3ref/sqlite3.html) objects depends
to some extent on the length of the filename of the database file, but
rarely exceeds 2KB on 32\-bit systems. (More space is required on
64\-bit systems due to the increased size of pointers.)
Each parser object uses about 1\.6KB of memory. Thus, elements 3 through 6
above can easily be controlled to keep the maximum memory allocation
size below 2KB.


If the application is designed to manage data in small pieces,
then the database should never contain any large strings or BLOBs
and hence element 1 above should not be a factor. If the database
does contain large strings or BLOBs, they should be read using
[incremental BLOB I/O](c3ref/blob.html) and rows that contain the
large strings or BLOBs should never be update by any means other
than [incremental BLOB I/O](c3ref/blob.html). Otherwise, the 
[sqlite3\_step()](c3ref/step.html) routine will need to read the entire row into
contiguous memory at some point, and that will involve at least
one large memory allocation.


The final source of large memory allocations is the space to hold
the [prepared statements](c3ref/stmt.html) that result from compiling complex SQL
operations. Ongoing work by the SQLite developers is reducing the
amount of space required here. But large and complex queries might
still require [prepared statements](c3ref/stmt.html) that are several kilobytes in
size. The only workaround at the moment is for the application to
break complex SQL operations up into two or more smaller and simpler 
operations contained in separate [prepared statements](c3ref/stmt.html).


All things considered, applications should normally be able to
hold their maximum memory allocation size below 2K or 4K. This
gives a value for log2(**n**) of 2 or 3\. This will
limit **N** to between 2 and 2\.5 times **M**.


The maximum amount of general\-purpose memory needed by the application
is determined by such factors as how many simultaneous open 
[database connection](c3ref/sqlite3.html) and [prepared statement](c3ref/stmt.html) objects the application
uses, and on the complexity of the [prepared statements](c3ref/stmt.html). For any
given application, these factors are normally fixed and can be
determined experimentally using [SQLITE\_STATUS\_MEMORY\_USED](c3ref/c_status_malloc_count.html#sqlitestatusmemoryused).
A typical application might only use about 40KB of general\-purpose
memory. This gives a value of **N** of around 100KB.


## 4\.2\.  Ductile failure


If the memory allocation subsystems within SQLite are configured
for breakdown\-free operation but the actual memory usage exceeds
design limits set by the [Robson proof](malloc.html#nofrag), SQLite will usually continue 
to operate normally.
The [pagecache memory allocator](malloc.html#pagecache)
and the [lookaside memory allocator](malloc.html#lookaside) automatically failover
to the [memsys5](malloc.html#memsys5) general\-purpose memory allocator. And it is usually the
case that the [memsys5](malloc.html#memsys5) memory allocator will continue to function
without fragmentation even if **M** and/or **n** exceeds the limits
imposed by the [Robson proof](malloc.html#nofrag). The [Robson proof](malloc.html#nofrag) shows that it is 
possible for a memory allocation to break down and fail in this 
circumstance, but such a failure requires an especially
despicable sequence of allocations and deallocations \- a sequence that
SQLite has never been observed to follow. So in practice it is usually
the case that the limits imposed by Robson can be exceeded by a
considerable margin with no ill effect.


Nevertheless, application developers are admonished to monitor
the state of the memory allocation subsystems and raise alarms when
memory usage approaches or exceeds Robson limits. In this way,
the application will provide operators with abundant warning well
in advance of failure.
The [memory statistics](malloc.html#memstatus) interfaces of SQLite provide the application with
all the mechanism necessary to complete the monitoring portion of
this task.



# 5\.  Stability Of Memory Interfaces


**Update:** As of SQLite version 3\.7\.0 (2010\-07\-21\), 
all of SQLite memory allocation interfaces
are considered stable and will be supported in future releases.


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


