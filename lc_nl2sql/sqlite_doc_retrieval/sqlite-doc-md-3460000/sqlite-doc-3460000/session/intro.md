




Introduction




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







These pages define the C\-language interface for the SQLite
[session extension](../sessionintro.html).
This is not a tutorial. These pages are designed to be precise, not
easy to read. A tutorial is [available separately](../sessionintro.html).

This version of the C\-language interface reference is
broken down into small pages for easy viewing. The
same content is also available as a
[single large HTML file](../session.html)
for those who prefer that format.


The content on these pages is extracted from comments
in the source code.


The interface is broken down into three categories:


1. [**List Of Objects.**](../session/objlist.html)
 This is a list of the three abstract objects used by the SQLite session
 module.

- [**List Of Constants.**](../session/constlist.html)
 This is a list of numeric constants used by the SQLite session module
 and represented by \#defines in the sqlite3session.h header file. There
 are constants passed to conflict handler callbacks to indicate the type
 of conflict, and constants returned by the conflict handler to indicate
 how the conflict should be resolved.

- [**List Of Functions.**](../session/funclist.html)
 This is a list of all SQLite session module functions.




