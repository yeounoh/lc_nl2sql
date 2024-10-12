




Virtual Table Indexing Information




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Virtual Table Indexing Information




> ```
> 
> struct sqlite3_index_info {
>   /* Inputs */
>   int nConstraint;           /* Number of entries in aConstraint */
>   struct sqlite3_index_constraint {
>      int iColumn;              /* Column constrained.  -1 for ROWID */
>      unsigned char op;         /* Constraint operator */
>      unsigned char usable;     /* True if this constraint is usable */
>      int iTermOffset;          /* Used internally - xBestIndex should ignore */
>   } *aConstraint;            /* Table of WHERE clause constraints */
>   int nOrderBy;              /* Number of terms in the ORDER BY clause */
>   struct sqlite3_index_orderby {
>      int iColumn;              /* Column number */
>      unsigned char desc;       /* True for DESC.  False for ASC. */
>   } *aOrderBy;               /* The ORDER BY clause */
>   /* Outputs */
>   struct sqlite3_index_constraint_usage {
>     int argvIndex;           /* if >0, constraint is part of argv to xFilter */
>     unsigned char omit;      /* Do not code a test for this constraint */
>   } *aConstraintUsage;
>   int idxNum;                /* Number used to identify the index */
>   char *idxStr;              /* String, possibly obtained from sqlite3_malloc */
>   int needToFreeIdxStr;      /* Free idxStr using sqlite3_free() if true */
>   int orderByConsumed;       /* True if output is already ordered */
>   double estimatedCost;           /* Estimated cost of using this index */
>   /* Fields below are only available in SQLite 3.8.2 and later */
>   sqlite3_int64 estimatedRows;    /* Estimated number of rows returned */
>   /* Fields below are only available in SQLite 3.9.0 and later */
>   int idxFlags;              /* Mask of SQLITE_INDEX_SCAN_* flags */
>   /* Fields below are only available in SQLite 3.10.0 and later */
>   sqlite3_uint64 colUsed;    /* Input: Mask of columns used by statement */
> };
> 
> ```



The sqlite3\_index\_info structure and its substructures is used as part
of the [virtual table](../vtab.html) interface to
pass information into and receive the reply from the [xBestIndex](../vtab.html#xbestindex)
method of a [virtual table module](../c3ref/module.html). The fields under \*\*Inputs\*\* are the
inputs to xBestIndex and are read\-only. xBestIndex inserts its
results into the \*\*Outputs\*\* fields.


The aConstraint\[] array records WHERE clause constraints of the form:



> column OP expr




where OP is \=, \<, \<\=, \>, or \>\=. The particular operator is
stored in aConstraint\[].op using one of the
[SQLITE\_INDEX\_CONSTRAINT\_ values](../c3ref/c_index_constraint_eq.html).
The index of the column is stored in
aConstraint\[].iColumn. aConstraint\[].usable is TRUE if the
expr on the right\-hand side can be evaluated (and thus the constraint
is usable) and false if it cannot.


The optimizer automatically inverts terms of the form "expr OP column"
and makes other simplifications to the WHERE clause in an attempt to
get as many WHERE clause terms into the form shown above as possible.
The aConstraint\[] array only reports WHERE clause terms that are
relevant to the particular virtual table being queried.


Information about the ORDER BY clause is stored in aOrderBy\[].
Each term of aOrderBy records a column of the ORDER BY clause.


The colUsed field indicates which columns of the virtual table may be
required by the current scan. Virtual table columns are numbered from
zero in the order in which they appear within the CREATE TABLE statement
passed to sqlite3\_declare\_vtab(). For the first 63 columns (columns 0\-62\),
the corresponding bit is set within the colUsed mask if the column may be
required by SQLite. If the table has at least 64 columns and any column
to the right of the first 63 is required, then bit 63 of colUsed is also
set. In other words, column iCol may be required if the expression
(colUsed \& ((sqlite3\_uint64\)1 \<\< (iCol\>\=63 ? 63 : iCol))) evaluates to
non\-zero.


The [xBestIndex](../vtab.html#xbestindex) method must fill aConstraintUsage\[] with information
about what parameters to pass to xFilter. If argvIndex\>0 then
the right\-hand side of the corresponding aConstraint\[] is evaluated
and becomes the argvIndex\-th entry in argv. If aConstraintUsage\[].omit
is true, then the constraint is assumed to be fully handled by the
virtual table and might not be checked again by the byte code. The
aConstraintUsage\[].omit flag is an optimization hint. When the omit flag
is left in its default setting of false, the constraint will always be
checked separately in byte code. If the omit flag is change to true, then
the constraint may or may not be checked in byte code. In other words,
when the omit flag is true there is no guarantee that the constraint will
not be checked again using byte code.


The idxNum and idxStr values are recorded and passed into the
[xFilter](../vtab.html#xfilter) method.
[sqlite3\_free()](../c3ref/free.html) is used to free idxStr if and only if
needToFreeIdxStr is true.


The orderByConsumed means that output from [xFilter](../vtab.html#xfilter)/[xNext](../vtab.html#xnext) will occur in
the correct order to satisfy the ORDER BY clause so that no separate
sorting step is required.


The estimatedCost value is an estimate of the cost of a particular
strategy. A cost of N indicates that the cost of the strategy is similar
to a linear scan of an SQLite table with N rows. A cost of log(N)
indicates that the expense of the operation is similar to that of a
binary search on a unique indexed field of an SQLite table with N rows.


The estimatedRows value is an estimate of the number of rows that
will be returned by the strategy.


The xBestIndex method may optionally populate the idxFlags field with a
mask of SQLITE\_INDEX\_SCAN\_\* flags. Currently there is only one such flag \-
SQLITE\_INDEX\_SCAN\_UNIQUE. If the xBestIndex method sets this flag, SQLite
assumes that the strategy may visit at most one row.


Additionally, if xBestIndex sets the SQLITE\_INDEX\_SCAN\_UNIQUE flag, then
SQLite also assumes that if a call to the xUpdate() method is made as
part of the same statement to delete or update a virtual table row and the
implementation returns SQLITE\_CONSTRAINT, then there is no need to rollback
any database changes. In other words, if the xUpdate() returns
SQLITE\_CONSTRAINT, the database contents must be exactly as they were
before xUpdate was called. By contrast, if SQLITE\_INDEX\_SCAN\_UNIQUE is not
set and xUpdate returns SQLITE\_CONSTRAINT, any database changes made by
the xUpdate method are automatically rolled back by SQLite.


IMPORTANT: The estimatedRows field was added to the sqlite3\_index\_info
structure for SQLite [version 3\.8\.2](../releaselog/3_8_2.html) (2013\-12\-06\).
If a virtual table extension is
used with an SQLite version earlier than 3\.8\.2, the results of attempting
to read or write the estimatedRows field are undefined (but are likely
to include crashing the application). The estimatedRows field should
therefore only be used if [sqlite3\_libversion\_number()](../c3ref/libversion.html) returns a
value greater than or equal to 3008002\. Similarly, the idxFlags field
was added for [version 3\.9\.0](../releaselog/3_9_0.html) (2015\-10\-14\).
It may therefore only be used if
sqlite3\_libversion\_number() returns a value greater than or equal to
3009000\.


3 Methods using this object:
 [sqlite3\_vtab\_collation()](../c3ref/vtab_collation.html),
[sqlite3\_vtab\_distinct()](../c3ref/vtab_distinct.html),
[sqlite3\_vtab\_rhs\_value()](../c3ref/vtab_rhs_value.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


