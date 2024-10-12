




Experimental Interfaces




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## SQLite C Interface](../c3ref/intro.html)
## Experimental And Deprecated Interfaces


SQLite interfaces can be subdivided into three categories:


1. Stable
2. Experimental
3. Deprecated


Stable interfaces will be maintained indefinitely in a backwards
compatible way. An application that uses only stable interfaces
should always be able to relink against a newer version of SQLite
without any changes.


Experimental interfaces are subject to change.
Applications that use experimental interfaces
may need to be modified when upgrading to a newer SQLite release, though
this is rare.
When new interfaces are added to SQLite, they generally begin
as experimental interfaces. After an interface has been in use for
a while and the developers are confident that the design of the interface
is sound and worthy of long\-term support, the interface is marked
as stable.


Deprecated interfaces have been superceded by better methods of
accomplishing the same thing and should be avoided in new applications.
Deprecated interfaces continue to be supported for the sake of
backwards compatibility. At some point in the future, it is possible
that deprecated interfaces may be removed.


Key points:


* Experimental interfaces are subject to change and/or removal
at any time.
* Deprecated interfaces should not be used in new code and might
be removed in some future release.


