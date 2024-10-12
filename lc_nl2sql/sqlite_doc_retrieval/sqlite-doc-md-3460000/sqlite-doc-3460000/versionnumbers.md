




Version Numbers in SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Version Numbers in SQLite


# 1\. SQLite Version Numbers



Beginning with [version 3\.9\.0](releaselog/3_9_0.html) (2015\-10\-14\) SQLite uses 
[semantic versioning](http://semver.org).
Prior to that time, SQLite employed a version identifier that
contained between two and four numbers.



## 1\.1\. The New Version Numbering System (After 2015\-10\-14\)



All SQLite releases starting with 3\.9\.0 use a three\-number
"[semantic version](http://semver.org)" of the form X.Y.Z.
The first number X is only increased when there is a change that
breaks backward compatibility. The
current value for X is 3, and the SQLite developers plan to support
the current SQLite database file format, SQL syntax, and C interface
through [at least the year 2050](lts.html). Hence, one
can expect that all future versions of SQLite for the next several
decades will begin with "3\.".




The second number Y is incremented for any change that breaks forward
compatibility by adding new features.
Most future SQLite releases are expected
to increment the second number Y. The Z is reset to zero whenever Y
is increased.




The third number Z is incremented for releases consisting of only
small changes that implement performance enhancements and/or bug fixes.




The rate of enhancement for SQLite over the previous five years
(2010\-2015\) is approximately 6 increments of Y per year. The
numbering format used by for [SQLITE\_VERSION\_NUMBER](c3ref/c_source_id.html) and
[sqlite3\_libversion\_number()](c3ref/libversion.html) allows versions up to 3\.999\.999, which is
more than enough for the planned end\-of\-support date for SQLite
in 2050\. However, the current tarball naming conventions only
reserve two digits for the Y and so the naming format for downloads
will need to be revised in about 2030\.



## 1\.2\. The Historical Numbering System (Before 2015\-10\-14\)


This historical version numbering system used a two\-, three\-,
or four\-number version: W.X, W.X.Y, or W.X.Y.Z.
W was the file format: 1 or 2 or 3\.
X was the major version.
Y was the minor version.
Z was used only for patch releases to fix bugs.




There have been three historical file formats for SQLite.
SQLite 1\.0 through 1\.0\.32 used the
[gdbm](https://www.gnu.org/software/gdbm/gdbm.html) library as its storage
engine.
SQLite 2\.0\.0 through 2\.8\.17 used a custom b\-tree storage engine that
supported only text keys and data.
All modern versions of SQLite (3\.0\.0 to present) use a b\-tree storage
engine that has full support for binary data and Unicode.




This major version number X was historically incremented only for
large and important changes to the code. What constituted "large
and important" was subjective. The 3\.6\.23 to 3\.7\.0 change
was a result of adding support for [WAL mode](wal.html).
The 3\.7\.17 to 3\.8\.0 change was a result of rewrite known as the
[next generation query planner](queryplanner-ng.html).




The minor version number Y was historically incremented for new
features and/or new interfaces that did not significantly change
the structure of the code. The addition of [common table expressions](lang_with.html),
[partial indexes](partialindex.html), and [indexes on expressions](expridx.html) are all examples of
"minor" changes. Again, the distinction between "major" and "minor"
is subjective.




The patch level Z was historically only used for bug\-fix releases
that changed only a small number of code lines.



## 1\.3\. Version History


* [Chronology](chronology.html)
* [Change log](changes.html)


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


