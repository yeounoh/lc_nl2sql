




SQLite Download Page




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







## SQLite Download Page








---




### Build Product Names and Info



Build products are named using one of the following templates:

1. **sqlite\-**product**\-**version**.zip**- **sqlite\-**product**\-**version**.tar.gz**- **sqlite\-**product**\-**os**\-**cpu**\-**version**.zip**- **sqlite\-**product**\-**date**.zip**


Templates (1\) and (2\) are used for source\-code products. Template (1\) is
used for generic source\-code products and templates (2\) is used for source\-code
products that are generally only useful on unix\-like platforms. Template (3\)
is used for precompiled binaries products. Template (4\) is used for
unofficial pre\-release "snapshots" of source code.

The *version* is encoded so that filenames sort in order of
increasing version number when viewed using "ls". For version 3\.X.Y the
filename encoding is 3XXYY00\. For branch version 3\.X.Y.Z, the encoding is
3XXYYZZ.

The *date* in template (4\) is of the form: YYYYMMDDHHMM

For convenient, script\-driven extraction of the downloadable
file URLs and associated information, an HTML comment is embedded
in this page's source. Its first line (sans leading tag) reads:

> **Download product data for scripts to read**


Its subsequent lines comprise a CSV table with this column header:

> **PRODUCT,VERSION,RELATIVE\-URL,SIZE\-IN\-BYTES,SHA3\-HASH**


The column header and following data lines have no leading space.
The PRODUCT column is a constant value ("PRODUCT") for convenient
regular expression matching. Other columns are self\-explanatory.
This format will remain stable except for possible new columns
appended to the right of older columns.




### Source Code Repositories



The SQLite source code is maintained in three geographically\-dispersed
self\-synchronizing
[Fossil](https://www.fossil-scm.org/) repositories that are
available for anonymous read\-only access. Anyone can
view the repository contents and download historical versions
of individual files or ZIP archives of historical check\-ins.
You can also [clone the entire repository](getthecode.html#clone).


See the [How To Compile SQLite](howtocompile.html) page for additional information
on how to use the raw SQLite source code.
Note that a recent version of [Tcl](https://www.tcl-lang.org/)
is required in order to build from the repository sources.
The [amalgamation](amalgamation.html) source code files
(the "sqlite3\.c" and "sqlite3\.h" files) build products and are
not contained in raw source code tree.



> <https://www.sqlite.org/cgi/src> (Dallas)  
> 
> [https://www2\.sqlite.org/cgi/src](https://www2.sqlite.org/cgi/src) (Newark)  
> 
> [https://www3\.sqlite.org/cgi/src](https://www3.sqlite.org/cgi/src) (San Francisco)


There is a GitHub mirror at


> [https://github.com/sqlite/sqlite/](https://github.com/sqlite/sqlite)


The documentation is maintained in separate
[Fossil](https://www.fossil-scm.org/) repositories located
at:



> <https://www.sqlite.org/cgi/docsrc> (Dallas)  
> 
> [https://www2\.sqlite.org/cgi/docsrc](https://www2.sqlite.org/cgi/docsrc) (Newark)  
> 
> [https://www3\.sqlite.org/cgi/docsrc](https://www3.sqlite.org/cgi/docsrc) (San Francisco)















