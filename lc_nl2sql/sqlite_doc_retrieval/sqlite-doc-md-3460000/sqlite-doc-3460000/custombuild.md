




Custom Builds Of SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# Custom Builds Of SQLite
or
Porting SQLite To New Operating Systems


## 1\.0 Introduction


For most applications, the recommended method for building
SQLite is to use [the amalgamation](amalgamation.html) code
file, **sqlite3\.c**, and its corresponding header file
**sqlite3\.h**. The sqlite3\.c code file should compile and
run on any Unix, Windows system without any changes
or special compiler options. Most applications can simply include
the sqlite3\.c file together with the other C code files that make
up the application, compile them all together, and have working
and well configured version of SQLite.



> *Most applications work great with SQLite in its
> default configuration and with no special compile\-time configuration.
> Most developers should be able to completely ignore this document
> and simply build SQLite from
> [the amalgamation](amalgamation.html) without any
> special knowledge and without taking any special actions.*


However, highly tuned and specialized
applications may want or need to replace some of
SQLite's built\-in system interfaces with alternative implementations
more suitable for the needs of the application. SQLite is designed
to be easily reconfigured at compile\-time to meet the specific
needs of individual projects. Among the compile\-time configuration
options for SQLite are these:


* Replace the built\-in mutex subsystem with an alternative
 implementation.
* Completely disable all mutexing for use in single\-threaded
 applications.
* Reconfigure the memory allocation subsystem to use a memory
 allocator other the malloc() implementation from the standard
 library.
* Realign the memory allocation subsystem so that it never calls
 malloc() at all but instead satisfies all memory requests using
 a fixed\-size memory buffer assigned to SQLite at startup.
* Replace the interface to the file system with an alternative
 design. In other words, override all of the system calls that
 SQLite makes in order to talk to the disk with a completely different
 set of system calls.
* Override other operating system interfaces such as calls to obtain
 Zulu or local time.


Generally speaking, there are three separate subsystems within
SQLite that can be modified or overridden at compile\-time. The
mutex subsystem is used to serialize access to SQLite resources that
are shared among threads. The memory allocation subsystem is used
to allocate memory required by SQLite objects and for the database
cache. Finally, the [Virtual File System](c3ref/vfs.html) subsystem is
used to provide a portable interface between SQLite and the underlying
operating system and especially the file system. We call these three
subsystems the "interface" subsystems of SQLite.


We emphasis that most applications are well\-served by the 
built\-in default implementations of the SQLite interface subsystems.
Developers are encouraged to use the
default built\-in implementations whenever possible
and to build SQLite without any special compile\-time options or parameters.
However, some highly specialized applications may benefit from
substituting or modifying one or more of these built\-in SQLite
interface subsystems.
Or, if SQLite is used on an operating system other than
Unix (Linux or Mac OS X), Windows (Win32 or WinCE), or OS/2 then none
of the interface subsystems that come built into SQLite will work
and the application will need to provide alternative implementations
suitable for the target platform.


## 2\.0 Configuring Or Replacing The Mutex Subsystem


In a multithreaded environment, SQLite uses mutexes to serialize
access to shared resources.
The mutex subsystem is only required for applications that access
SQLite from multiple threads. For single\-threaded applications, or
applications which only call SQLite from a single thread, the mutex
subsystem can be completely disabled by recompiling with the following
option:



> ```
> 
> -DSQLITE_THREADSAFE=0
> 
> ```


Mutexes are cheap but they are not free, so performance will be better
when mutexes are completely disabled. The resulting library footprint
will also be a little smaller. Disabling the mutexes at compile\-time
is a recommended optimization for applications where it makes sense.


When using SQLite as a shared library, an application can test to see
whether or not mutexes have been disabled using the
[sqlite3\_threadsafe()](c3ref/threadsafe.html) API. Applications that link against SQLite at
run\-time and use SQLite from multiple threads should probably check this
API to make sure they did not accidentally get linked against a version of
the SQLite library that has its mutexes disabled. Single\-threaded
applications will, of course, work correctly regardless of whether or
not SQLite is configured to be threadsafe, though they will be a little
bit faster when using versions of SQLite with mutexes disabled.


SQLite mutexes can also be disabled at run\-time using the
[sqlite3\_config()](c3ref/config.html) interface. To completely disable all mutexing,
the application can invoke:



> ```
> 
> sqlite3_config(SQLITE_CONFIG_SINGLETHREAD);
> 
> ```


Disabling mutexes at run\-time is not as effective as disabling them
at compile\-time since SQLite still must do a test of a boolean variable
to see if mutexes are enabled or disabled at each point where a mutex
might be required. But there is still a performance advantage for
disabling mutexes at run\-time.


For multi\-threaded applications that are careful about how they
manage threads, SQLite supports an alternative run\-time configuration
that is half way between not using any mutexes and the default situation
of mutexing everything in sight. This in\-the\-middle mutex alignment can
be established as follows:



> ```
> 
> sqlite3_config(SQLITE_CONFIG_MULTITHREAD);
> sqlite3_config(SQLITE_CONFIG_MEMSTATUS, 0);
> 
> ```


There are two separate configuration changes here which can
be used either together or separately. The
[SQLITE\_CONFIG\_MULTITHREAD](c3ref/c_config_covering_index_scan.html#sqliteconfigmultithread) setting disables the mutexes that
serialize access to [database connection](c3ref/sqlite3.html) objects and 
[prepared statement](c3ref/stmt.html) objects. With this setting, the application
is free to use SQLite from multiple threads, but it must make sure
than no two threads try to access the same [database connection](c3ref/sqlite3.html)
or any [prepared statements](c3ref/stmt.html) associated with the same 
[database connection](c3ref/sqlite3.html) at the same time. Two threads can use SQLite
at the same time, but they must use separate [database connections](c3ref/sqlite3.html).
The second [SQLITE\_CONFIG\_MEMSTATUS](c3ref/c_config_covering_index_scan.html#sqliteconfigmemstatus) setting disables the mechanism
in SQLite that tracks the total size of all outstanding memory
allocation requests. This omits the need to mutex each call
to [sqlite3\_malloc()](c3ref/free.html) and [sqlite3\_free()](c3ref/free.html), which saves a huge
number of mutex operations. But a consequence of disabling the
memory statistics mechanism is that the 
[sqlite3\_memory\_used()](c3ref/memory_highwater.html), [sqlite3\_memory\_highwater()](c3ref/memory_highwater.html), and
[sqlite3\_soft\_heap\_limit64()](c3ref/hard_heap_limit64.html) interfaces cease to work.



SQLite uses pthreads for its mutex implementation on Unix and
SQLite requires a recursive mutex. Most modern pthread implementations
support recursive mutexes, but not all do. For systems that do not
support recursive mutexes, it is recommended that applications operate
in single\-threaded mode only. If this is not possible, SQLite provides
an alternative recursive mutex implementation built on top of the
standard "fast" mutexes of pthreads. This alternative
implementation should work correctly as long as pthread\_equal() is
atomic and the processor has a coherent data cache. The alternative
recursive mutex implementation is enabled by the following
compiler command\-line switch:



> ```
> 
> -DSQLITE_HOMEGROWN_RECURSIVE_MUTEX=1
> 
> ```


When porting SQLite to a new operating system, it is usually necessary
to completely replace the built\-in mutex subsystem with an alternative
built around the mutex primitives of the new operating system. This
is accomplished by compiling SQLite with the following option:



> ```
> 
> -DSQLITE_MUTEX_APPDEF=1
> 
> ```


When SQLite is compiled with the SQLITE\_MUTEX\_APPDEF\=1 option, it
completely omits the implementation of its 
[mutex primitive functions](c3ref/mutex_alloc.html). But the SQLite
library still attempts to call these functions where necessary, so the
application must itself implement the
[mutex primitive functions](c3ref/mutex_alloc.html) and link them together
with SQLite.


## 3\.0 Configuring Or Replacing The Memory Allocation Subsystem


By default, SQLite obtains the memory it needs for objects and
cache from the malloc()/free() implementation of the standard library.
There is also on\-going work with experimental memory allocators that
satisfy all memory requests from a single fixed memory buffer handed
to SQLite at application start. Additional information on these
experimental memory allocators will be provided in a future revision
of this document.


SQLite supports the ability of an application to specify an alternative
memory allocator at run\-time by filling in an instance of the
[sqlite3\_mem\_methods](c3ref/mem_methods.html) object with pointers to the routines of the
alternative implementation then registering the new alternative
implementation using the [sqlite3\_config()](c3ref/config.html) interface.
For example:



> ```
> 
> sqlite3_config(SQLITE_CONFIG_MALLOC, &my_malloc_implementation);
> 
> ```


SQLite makes a copy of the content of the [sqlite3\_mem\_methods](c3ref/mem_methods.html) object
so the object can be modified after the [sqlite3\_config()](c3ref/config.html) call returns.


## 4\.0 Adding New Virtual File Systems


Since [version 3\.5\.0](releaselog/3_5_0.html) (2007\-09\-04\), 
SQLite has supported an interface called the
[virtual file system](c3ref/vfs.html) or "VFS".
This object is somewhat misnamed since it
is really an interface to the whole underlying operating system, not
just the filesystem.


 One of the interesting features
of the VFS interface is that SQLite can support multiple VFSes at the
same time. Each [database connection](c3ref/sqlite3.html) has to choose a single VFS for its
use when the connection is first opened using [sqlite3\_open\_v2()](c3ref/open.html).
But if a process contains multiple [database connections](c3ref/sqlite3.html) each can choose
a different VFS. VFSes can be added at run\-time using the
[sqlite3\_vfs\_register()](c3ref/vfs_find.html) interface.


The default builds for SQLite on Unix, Windows, and OS/2 include 
a VFS appropriate for the target platform. SQLite builds for other
operating systems do not contain a VFS by default, but the application
can register one or more at run\-time.


## 5\.0 Porting SQLite To A New Operating System


In order to port SQLite to a new operating system \- an operating
system not supported by default \- the application
must provide...


* a working mutex subsystem (but only if it is multithreaded),
* a working memory allocation subsystem (assuming it lacks malloc()
in its standard library), and
* a working VFS implementation.


All of these things can be provided in a single auxiliary C code file
and then linked with the stock "sqlite3\.c" code file to generate a working
SQLite build for the target operating system. In addition to the
alternative mutex and memory allocation subsystems and the new VFS,
the auxiliary C code file should contain implementations for the
following two routines:


* [sqlite3\_os\_init()](c3ref/initialize.html)
* [sqlite3\_os\_end()](c3ref/initialize.html)


The "sqlite3\.c" code file contains default implementations of a VFS
and of the [sqlite3\_initialize()](c3ref/initialize.html) and [sqlite3\_shutdown()](c3ref/initialize.html) functions that
are appropriate for Unix, Windows, and OS/2\.
To prevent one of these default components from being loaded when sqlite3\.c
is compiled, it is necessary to add the following compile\-time
option:



> ```
> 
> -DSQLITE_OS_OTHER=1
> 
> ```


The SQLite core will call [sqlite3\_initialize()](c3ref/initialize.html) early. The auxiliary
C code file can contain an implementation of sqlite3\_initialize() that
registers an appropriate VFS and also perhaps initializes an alternative
mutex system (if mutexes are required) or does any memory allocation
subsystem initialization that is required.
The SQLite core never calls [sqlite3\_shutdown()](c3ref/initialize.html) but it is part of the
official SQLite API and is not otherwise provided when compiled with
\-DSQLITE\_OS\_OTHER\=1, so the auxiliary C code file should probably provide
it for completeness.


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


