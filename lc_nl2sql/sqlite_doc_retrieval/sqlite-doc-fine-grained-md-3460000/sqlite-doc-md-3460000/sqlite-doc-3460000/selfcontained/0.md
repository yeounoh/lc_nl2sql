




SQLite is a Self Contained System




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










SQLite is a Self Contained System



SQLite is "stand\-alone" or "self\-contained" in the sense that it
has very few dependencies. It runs on any operating system, even
stripped\-down bare\-bones embedded operating systems. SQLite uses
no external libraries or interfaces (other than a few standard C\-library 
calls described below). The entire SQLite library is
encapsulated in a [single source code file](amalgamation.html) that requires
no special facilities or tools to build.




A minimal build of SQLite requires just these routines from the
standard C library:


* memcmp()
* memcpy()
* memmove()
* memset()
* strcmp()
* strlen()
* strncmp()



Most builds also use the system memory allocation routines:


* malloc()
* realloc()
* free()


But those routines are optional and can be omitted
using a [compile\-time option](compile.html#zero_malloc).




Default builds of SQLite contain appropriate [VFS objects](vfs.html) for talking
to underlying operating system, and those VFS objects will contain
operating system calls such as open(), read(), write(), fsync(), and
so forth. All of these interfaces are readily available on most platforms,
and custom VFSes can be designed to run SQLite on even the most
austere embedded devices.


*This page last modified on [2022\-08\-10 18:45:48](https://sqlite.org/docsrc/honeypot) UTC* 


