




Long Term Support




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Long Term Support



The intent of the developers is to support SQLite through
the year 2050\.




At this writing, 2050 is still 34 years in the future.
Nobody knows what will happen in that time, and we cannot
absolutely promise that SQLite will be viable or useful that
far out.
But we can promise this: we plan as if we will be
supporting SQLite until 2050\.
That long\-term outlook affects our
decisions in important ways.



* **Cross\-platform Code** →
SQLite runs on any platform with an 8\-bit byte,
two's complement 32\-bit and 64\-bit integers, 
and a C compiler. It is actively
tested on all currently popular CPUs and operating
systems.
The extreme portability of the SQLite code and file
format will help it remain viable on future platforms.
* **Stable, Cross\-platform Database Files** →
SQLite [database files](fileformat2.html) are bit\-for\-bit identical on
32\-bit, 64\-bit, big\-endian, and little\-endian platforms. You
can copy an SQLite database file from one system to another
without having to translate or convert the database.
Furthermore, the file format is well documented and stable.
Database files created today will be readable and writable by
future versions of SQLite decades in the future.
* **[Aviation\-grade testing](testing.html)** →
Every machine\-code branch instruction is tested in both
directions. Multiple times. On multiple platforms and with
multiple compilers. This helps make the code robust for
future migrations. The intense testing also means that new
developers can make experimental enhancements to SQLite and,
assuming legacy tests all pass, be reasonably sure that the
enhancement does not break legacy.
* **Extensive, detailed documentation** →
SQLite has candid, developer\-friendly,
and open\-source documentation. Docs are written by and
for programmers.
(A few examples:
[\[1]](./arch.html)
[\[2]](./fileformat.html)
[\[3]](./queryplanner.html)
[\[4]](./opcode.html)
[\[5]](./compile.html)
[\[6]](./malloc.html)
[\[7]](./debugging.html)
[\[8]](./howtocorrupt.html))
The extensive documentation helps new developers
come up to speed on SQLite very quickly.
* **Heavily commented source code** →
The SQLite source code is over 35% comment. Not boiler\-plate
comments, but useful comments that explain the meaning of variables
and objects and the intent of methods and procedures. 
The code is designed
to be accessible to new programmers and maintainable over a span
of decades.
* **Disaster planning** →
Every byte of source\-code history for SQLite is cryptographically
protected and is automatically replicated to multiple
geographically separated servers, in datacenters 
owned by different companies.
Thousands of additional clones exist on private servers around the
world.
The primary developers of SQLite live in different regions of the world.
SQLite can survive a continental catastrophe.
* **Old school** →
Nobody is completely immune to trends and fads, but the SQLite
developers work hard to avoid being sucked into the latest programming
fashion. Our aim is to produce timeless code that will be
readable, understandable, and maintainable by programmers 
who have not yet been born.



In addition to "supporting" SQLite through the year 2050, the developers
also promise to keep the SQLite 
[C\-language API](cintro.html) and [on\-disk format](fileformat2.html) 
fully backwards compatible.
This means that application written to use SQLite today should be able to
link against and use future versions of SQLite released decades in the
future.




Our goal is to make the content you store in SQLite today as 
easily accessible to your grandchildren as it is to you.




**Update on 2018\-05\-31:**
Our goal of supporting SQLite long\-term have apparently come to the
notice of the preservationist at the 
[US Library Of Congress](https://www.loc.gov) who have identified
SQLite as a [recommended storage format](locrsf.html) for the preservation of
digital content.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


