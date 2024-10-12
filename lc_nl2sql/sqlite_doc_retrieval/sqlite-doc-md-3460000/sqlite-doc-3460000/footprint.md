




SQLite Library Footprint




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# Size Of The SQLite Library



As of 2023\-07\-04, the size of SQLite library is generally less than
1 megabyte. The size varies by compiler, operating system,
CPU architecture, compile\-time options, and other factors. When
compiling using \-Os (optimize for size) and with no other compile
time\-options specified, here are a few examples from commonly used
platforms:


* gcc 10\.2\.1 on Raspberry PI 4 64\-bit ARM: **590 KB**.
* clang 14\.0\.0 on MacOS M1: **750 KB**.
* gcc 5\.4\.0 on Ubuntu 16\.04\.7 x64: **650 KB**
* gcc 9\.4\.0 on Ubuntu 20\.04\.5 x64: **650 KB**



Your mileage may vary.


Library size will likely be larger
when including optional features such as full\-text search or r\-tree indexes,
or when using more aggressive compiler options such as \-O3\.


This document is intended only as a general guideline to the
compiled size of the SQLite library. If you need exact numbers, please
make your own measurements using your specific combination of SQLite
source code version, compiler, target platform, and compile\-time options.
*This page last modified on [2023\-07\-30 10:50:18](https://sqlite.org/docsrc/honeypot) UTC* 










