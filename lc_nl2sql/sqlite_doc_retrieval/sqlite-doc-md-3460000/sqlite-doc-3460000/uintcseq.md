




The UINT Collating Sequence




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The UINT Collating Sequence


# 1\. Overview


 The UINT collating sequences is a [loadable extension](loadext.html) for
SQLite that implements a new collating sequence that compares text
containing unsigned integers in numeric order.



 The UINT collating sequence is not a standard part of SQLite.
It must be loaded as a separate extension. The source code to
UINT is in the [uint.c source file](https://sqlite.org/src/file/ext/misc/uint.c)
in the [ext/misc/ folder](https://sqlite.org/src/file/ext/misc) of the
SQLite source tree.



 The UINT collating sequence is not included in standard builds of
the SQLite library, but it is loaded by default in the [CLI](cli.html). This
is typical of the [CLI](cli.html) which loads various extensions above and beyond
what are available in the standard SQLite library.



 The UINT collating sequence works just like the default
BINARY collating sequence for text, except that embedded strings
of digits compare in numeric order.



* Leading zeros are handled properly, in the sense that
they do not mess of the maginitude comparison of embedded
strings of digits. "x00123y" is equal to "x123y".
* Only unsigned integers are recognized. Plus and minus
signs are ignored. Decimal points and exponential notation
are ignored.
* Embedded integers can be of arbitrary length. Comparison
is not limited to integers that can be expressed as a
64\-bit machine integer.


# 2\. Example:



> | COLLATE binary | COLLATE uint |
> | --- | --- |
> | ```  '0000123457' '123456' 'abc0000000010xyz' 'abc0010xyy' 'abc10xzz' 'abc674xyz' 'abc87xyz' 'abc9xyz' ``` | ```  '123456' '0000123457' 'abc9xyz' 'abc0010xyy' 'abc0000000010xyz' 'abc10xzz' 'abc87xyz' 'abc674xyz' ``` |


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


