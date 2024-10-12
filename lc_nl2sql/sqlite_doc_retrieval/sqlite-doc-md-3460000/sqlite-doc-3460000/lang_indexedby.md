




The INDEXED BY Clause




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The INDEXED BY Clause


# 1\. How INDEXED BY Works


The INDEXED BY phrase forces the [SQLite query planner](optoverview.html) to use a
particular named index on a [DELETE](lang_delete.html), [SELECT](lang_select.html), or [UPDATE](lang_update.html) statement.
The INDEXED BY phrase is an SQLite extension and
is not portable to other SQL database engines.


**[qualified\-table\-name:](syntax/qualified-table-name.html)**
hide








schema\-name



.



table\-name



AS



alias









INDEXED



BY



index\-name

NOT



INDEXED




















The "INDEXED BY index\-name" phrase specifies 
that the named index
must be used in order to look up values on the preceding table.
If index\-name does not exist or cannot be used 
for the query, then the preparation of the SQL statement fails.
The "NOT INDEXED" clause specifies that no index shall be used when
accessing the preceding table, including implied indices create by
UNIQUE and PRIMARY KEY constraints. However, the [rowid](lang_createtable.html#rowid)
can still be used to look up entries even when "NOT INDEXED" is specified.


Some SQL database engines provide non\-standard "hint" mechanisms which
can be used to give the query optimizer clues about what indices it should
use for a particular statement. The INDEXED BY clause of SQLite is 
*not* a hinting mechanism and it should not be used as such.
The INDEXED BY clause does not give the optimizer hints about which index
to use; it gives the optimizer a requirement of which index to use.
If the query optimizer is unable to use the index specified by the
INDEXED BY clause, then the query will fail with an error.


The INDEXED BY clause is *not* intended for use in tuning
the performance of a query. The intent of the INDEXED BY clause is
to raise a run\-time error if a schema change, such as dropping or
creating an index, causes the query plan for a time\-sensitive query
to change. The INDEXED BY clause is designed to help detect
undesirable query plan changes during regression testing.
Application 
developers are admonished to omit all use of INDEXED BY during
application design, implementation, testing, and tuning. If
INDEXED BY is to be used at all, it should be inserted at the very
end of the development process when "locking down" a design.


# 2\. See Also


1. The [query planner checklist](queryplanner-ng.html#howtofix) describes steps that application
developers should following to help resolve query planner problems.
Notice the that the use of INDEXED BY is a last resort, to be used only
when all other measures fail.
2. [The unary "\+" operator](optoverview.html#uplus)
can be used to disqualify terms in the WHERE clause from use by indices.
Careful use of unary \+ can sometimes help prevent the query planner from
choosing a poor index without restricting it to using one specific index.
Careful placement of unary \+ operators is a better method for controlling 
which indices are used by a query.
3. The [sqlite3\_stmt\_status()](c3ref/stmt_status.html) C/C\+\+ interface together with the
[SQLITE\_STMTSTATUS\_FULLSCAN\_STEP](c3ref/c_stmtstatus_counter.html#sqlitestmtstatusfullscanstep) and [SQLITE\_STMTSTATUS\_SORT](c3ref/c_stmtstatus_counter.html#sqlitestmtstatussort) verbs
can be used to detect at run\-time when an SQL statement is not
making effective use of indices. Many applications may prefer to
use the [sqlite3\_stmt\_status()](c3ref/stmt_status.html) interface to detect index misuse
rather than the INDEXED BY phrase described here.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


