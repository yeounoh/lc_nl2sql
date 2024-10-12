




Invalid UTF Policy




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Invalid UTF Policy


# 1\. Garbage In, Garbage Out



With regard to invalid UTF, SQLite follows a policy of
Garbage\-In, Garbage\-Out (GIGO). If you insert invalid UTF
into an SQLite database, then try to query that data, what you get back out
might not be exactly what you put in. If you put garbage in, then you
may not complain if you get different garbage back out.




For the purposes of this discussion, "invalid UTF" can mean any of
the following circumstances:



* Invalid surrogate pairs in UTF\-16\.
* Invalid multi\-byte sequences in UTF\-8\.
* Using more bytes of UTF\-8 than necessary to represent a single
code point. (Example: encoding 'A' as the two\-byte sequence
0xc1, 0x01 instead of just a single 0x41 byte.)
* NUL characters (U\+0000\) embedded in strings.
* Invalid sequences of combining characters.
* UTF\-8 or UTF\-16 bytes sequences that encode numbers that are not
defined Unicode characters.


## 1\.1\. Invalid UTF will never cause memory errors



If you insert invalid UTF into an SQLite database, then SQLite makes
no guarantees about what text you might get back out. But it does
promise that invalid UTF will never cause memory errors
(array overruns, reads or writes of uninitialized memory, etc), at
least for the built\-in processing of SQLite.
In other words, invalid UTF will not cause SQLite to crash.




This promise only applies to the core SQLite components, not
application\-provided extensions, of course.
If an application adds new application\-defined SQL functions or
virtual tables or collating sequences or other extensions, and a
database contains invalid UTF, then invalid UTF might get passed
into those extensions. If the invalid UTF causes one of those
extensions to crash, then that is a problem with the extension,
not with SQLite.



# 2\. No enforcement of text formatting rules



SQLite does not try to enforce UTF formatting rules. You can
insert invalid UTF into a TEXT field and SQLite will not complain
about this. It stores the invalid TEXT as best it can. SQLite
sees its role in the world as a storage engine, not a text format
validation engine.



# 3\. Best effort to preserve text



SQLite does not promise to always preserve invalid UTF, but it does
make an effort. Generally speaking, if you insert invalid UTF into
SQLite, you will get the exact same byte sequence back out, as long
as you do not ask SQLite to transform the text in any way.




For example, if you insert some UTF\-16LE with invalid surrogates into
a TEXT column of a table of a database that has [PRAGMA encoding\=UTF16LE](pragma.html#pragma_encoding),
then later query that column using [sqlite3\_column\_text16()](c3ref/column_blob.html), you will 
probably get back the same exact invalid UTF\-16\. But if you insert the
same invalid UTF\-16LE content in a [PRAGMA encoding\=UTF8](pragma.html#pragma_encoding) database,
the content must be converted into UTF8 when it is stored, which could
cause irreversible changes to the content. Or if you insert that
same invalid UTF\-16LE content into a [PRAGMA encoding\=UTF16LE](pragma.html#pragma_encoding) database
but then read it out using [sqlite3\_column\_text()](c3ref/column_blob.html), then a UTF16 to
UTF8 conversion must occur during the read\-out and that conversion might
introduce irreversible changes.




Or, suppose you are doing everything using UTF\-8 (the most common case).
Invalid UTF\-8 will normally pass through the database without any change
in its byte sequence. However, if you try to transform the invalid
UTF\-8 with SQL function like [substr()](lang_corefunc.html#substr) or [replace()](lang_corefunc.html#replace)
or if you try to do string matching with the [LIKE](lang_expr.html#like) operator, then
you might get unexpected results.




So, in other words, SQLite does not actively try to subvert your
invalid text. But when you ask SQLite to make transformations of invalid
UTF, there are no guarantees that those transformations will be reversible
or even sensible.



# 4\. Invalid UTF in the database schema



If a database schema contains names (table names, column names, index
names, and so forth) that are invalid UTF, SQLite will continue to
operate normally. As far as SQLite is concerned, those names are just
byte sequences. SQLite does not care whether they are valid UTF or not.




When generating error messages (using, for example, [sqlite3\_errmsg()](c3ref/errcode.html)),
sometimes SQLite will embedded parts of the database schema into the
error message. If those embedded schema elements
are invalid UTF, then the resulting error message might also be
invalid UTF.
Similarly, the output from the [PRAGMA integrity\_check](pragma.html#pragma_integrity_check) and similar
statements will sometimes embed the names of schema elements. If those
schema element names are invalid UTF, then the output of the command
will also be invalid UTF.


*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


