




Flags for sqlite3changeset\_start\_v2




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Flags for sqlite3changeset\_start\_v2


> ```
> #define SQLITE_CHANGESETSTART_INVERT        0x0002
> 
> ```


The following flags may passed via the 4th parameter to
[sqlite3changeset\_start\_v2](../session/sqlite3changeset_start.html) and [sqlite3changeset\_start\_v2\_strm](../session/sqlite3changegroup_add_strm.html):


SQLITE\_CHANGESETAPPLY\_INVERT 
 Invert the changeset while iterating through it. This is equivalent to
 inverting a changeset using sqlite3changeset\_invert() before applying it.
 It is an error to specify this flag with a patchset.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


