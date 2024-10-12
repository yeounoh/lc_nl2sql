




Memory Allocation Subsystem




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Memory Allocation Subsystem




> ```
> 
> void *sqlite3_malloc(int);
> void *sqlite3_malloc64(sqlite3_uint64);
> void *sqlite3_realloc(void*, int);
> void *sqlite3_realloc64(void*, sqlite3_uint64);
> void sqlite3_free(void*);
> sqlite3_uint64 sqlite3_msize(void*);
> 
> ```



The SQLite core uses these three routines for all of its own
internal memory allocation needs. "Core" in the previous sentence
does not include operating\-system specific [VFS](../vfs.html) implementation. The
Windows VFS uses native malloc() and free() for some operations.


The sqlite3\_malloc() routine returns a pointer to a block
of memory at least N bytes in length, where N is the parameter.
If sqlite3\_malloc() is unable to obtain sufficient free
memory, it returns a NULL pointer. If the parameter N to
sqlite3\_malloc() is zero or negative then sqlite3\_malloc() returns
a NULL pointer.


The sqlite3\_malloc64(N) routine works just like
sqlite3\_malloc(N) except that N is an unsigned 64\-bit integer instead
of a signed 32\-bit integer.


Calling sqlite3\_free() with a pointer previously returned
by sqlite3\_malloc() or sqlite3\_realloc() releases that memory so
that it might be reused. The sqlite3\_free() routine is
a no\-op if is called with a NULL pointer. Passing a NULL pointer
to sqlite3\_free() is harmless. After being freed, memory
should neither be read nor written. Even reading previously freed
memory might result in a segmentation fault or other severe error.
Memory corruption, a segmentation fault, or other severe error
might result if sqlite3\_free() is called with a non\-NULL pointer that
was not obtained from sqlite3\_malloc() or sqlite3\_realloc().


The sqlite3\_realloc(X,N) interface attempts to resize a
prior memory allocation X to be at least N bytes.
If the X parameter to sqlite3\_realloc(X,N)
is a NULL pointer then its behavior is identical to calling
sqlite3\_malloc(N).
If the N parameter to sqlite3\_realloc(X,N) is zero or
negative then the behavior is exactly the same as calling
sqlite3\_free(X).
sqlite3\_realloc(X,N) returns a pointer to a memory allocation
of at least N bytes in size or NULL if insufficient memory is available.
If M is the size of the prior allocation, then min(N,M) bytes
of the prior allocation are copied into the beginning of buffer returned
by sqlite3\_realloc(X,N) and the prior allocation is freed.
If sqlite3\_realloc(X,N) returns NULL and N is positive, then the
prior allocation is not freed.


The sqlite3\_realloc64(X,N) interfaces works the same as
sqlite3\_realloc(X,N) except that N is a 64\-bit unsigned integer instead
of a 32\-bit signed integer.


If X is a memory allocation previously obtained from sqlite3\_malloc(),
sqlite3\_malloc64(), sqlite3\_realloc(), or sqlite3\_realloc64(), then
sqlite3\_msize(X) returns the size of that memory allocation in bytes.
The value returned by sqlite3\_msize(X) might be larger than the number
of bytes requested when X was allocated. If X is a NULL pointer then
sqlite3\_msize(X) returns zero. If X points to something that is not
the beginning of memory allocation, or if it points to a formerly
valid memory allocation that has now been freed, then the behavior
of sqlite3\_msize(X) is undefined and possibly harmful.


The memory returned by sqlite3\_malloc(), sqlite3\_realloc(),
sqlite3\_malloc64(), and sqlite3\_realloc64()
is always aligned to at least an 8 byte boundary, or to a
4 byte boundary if the [SQLITE\_4\_BYTE\_ALIGNED\_MALLOC](../compile.html#4_byte_aligned_malloc) compile\-time
option is used.


The pointer arguments to [sqlite3\_free()](../c3ref/free.html) and [sqlite3\_realloc()](../c3ref/free.html)
must be either NULL or else pointers obtained from a prior
invocation of [sqlite3\_malloc()](../c3ref/free.html) or [sqlite3\_realloc()](../c3ref/free.html) that have
not yet been released.


The application must not read or write any part of
a block of memory after it has been released using
[sqlite3\_free()](../c3ref/free.html) or [sqlite3\_realloc()](../c3ref/free.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


