




SQLite Is Transactional




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







## SQLite is Transactional


A transactional database is one in which all changes and queries
appear to be
Atomic, Consistent, Isolated, and Durable
([ACID](http://en.wikipedia.org/wiki/ACID)).
SQLite implements 
[serializable](http://en.wikipedia.org/wiki/Serializability)
transactions that are atomic, consistent, isolated, and durable,
even if the transaction is interrupted by a program crash, an
operating system crash, or a power failure to the computer.




We here restate and amplify the previous sentence for emphasis:
All changes within a single transaction in SQLite either occur
completely or not at all, even if the act of writing the change
out to the disk is interrupted by
* a program crash,
* an operating system crash, or
* a power failure.




The claim of the previous paragraph is extensively checked in the
SQLite regression test suite using a special test harness that 
simulates the effects on a database file of operating system crashes 
and power failures.




[Additional information](atomiccommit.html)



*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 






