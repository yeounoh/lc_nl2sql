




SQLite: Single File Database




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







## Single\-file Cross\-platform Database



A database in SQLite is a single disk file¹.
Furthermore, the [file format](fileformat2.html) is cross\-platform.
A database that is created on one machine can be
copied and used on a different machine with
a different architecture. SQLite databases
are portable across 32\-bit and 64\-bit machines
and between 
[big\-endian](http://en.wikipedia.org/wiki/Endianness) and 
[little\-endian](http://en.wikipedia.org/wiki/Endianness)
architectures.




The SQLite database file format is also stable.
All releases of SQLite version 3 can read and write database
files created by the very first SQLite 3 release (version 3\.0\.0\)
going back to 2004\-06\-18\. This is "backwards compatibility".
The developers promise to maintain backwards compatibility of
the database file format for all future releases of SQLite 3\.
"Forwards compatibility" means that older releases
of SQLite can also read and write databases created by newer
releases. SQLite is usually, but not completely forwards
compatible. 




The stability of the SQLite database file format and the fact
that the file format is cross\-platform combine to make SQLite
database files an excellent choice as an 
[Application File Format](appfileformat.html).
The US Library Of Congress acknowledges this by listing SQLite
as a [recommended storage format](locrsf.html) for long\-term preservation of
digital content.






---



Notes:
1. Temporary journal files are created as part of transaction control,
but those extra files are not part of the steady\-state database.





*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


