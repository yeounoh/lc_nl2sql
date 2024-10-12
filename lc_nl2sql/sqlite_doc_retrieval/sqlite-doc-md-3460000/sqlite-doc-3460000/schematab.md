




The Schema Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Schema Table


►
Table Of Contents
[1\. Introduction](#introduction)
[2\. Alternative Names](#alternative_names)
[3\. Interpretation Of The Schema Table](#interpretation_of_the_schema_table)
[4\. Creation and Modification Of The Schema Table](#creation_and_modification_of_the_schema_table)




# 1\. Introduction


Every SQLite database contains a single "schema table" that stores the
schema for that database. The schema for a database is a description of
all of the other tables, indexes, triggers, and views that are
contained within the database. The schema table looks like this:




> ```
> 
> CREATE TABLE sqlite_schema(
>   type text,
>   name text,
>   tbl_name text,
>   rootpage integer,
>   sql text
> );
> 
> ```


The sqlite\_schema table contains one row for each table, index, view,
and trigger (collectively "objects") in the schema, except there
is no entry for the sqlite\_schema table itself. See the
[schema storage](fileformat2.html#ffschema) subsection of the [file format](fileformat2.html) documentation for
additional information on how SQLite uses the sqlite\_schema table
internally.



# 2\. Alternative Names


The schema table can always be referenced using the name "sqlite\_schema",
especially if qualifed by the schema name like 
"main.sqlite\_schema" or "temp.sqlite\_schema". But for historical
compatibility, some alternative names are also recognized, including:



1. sqlite\_master
2. sqlite\_temp\_schema
3. sqlite\_temp\_master



Alternatives (2\) and (3\) only work for the TEMP database associated
with each database connection, but alternative (1\) works anywhere.
For historical reasons, callbacks from the [sqlite3\_set\_authorizer()](c3ref/set_authorizer.html)
interface always refer to the schema table using names (1\) or (3\).



# 3\. Interpretation Of The Schema Table


The meanings of the fields of the schema table are as follows:




**type**

The sqlite\_schema.type column will be one
of the following text strings: 'table', 'index', 'view', or 'trigger'
according to the type of object defined. The 'table' string is used
for both ordinary and [virtual tables](vtab.html).



**name**

The sqlite\_schema.name column will hold the name of the object.
[UNIQUE](lang_createtable.html#uniqueconst) and [PRIMARY KEY](lang_createtable.html#primkeyconst) constraints on tables cause SQLite to create
[internal indexes](fileformat2.html#intschema) with names of the form "sqlite\_autoindex\_TABLE\_N"
where TABLE is replaced by the name of the table that contains the
constraint and N is an integer beginning with 1 and increasing by one
with each constraint seen in the table definition.
In a [WITHOUT ROWID](withoutrowid.html) table, there is no sqlite\_schema entry for the
PRIMARY KEY, but the "sqlite\_autoindex\_TABLE\_N" name is set aside
for the PRIMARY KEY as if the sqlite\_schema entry did exist. This
will affect the numbering of subsequent UNIQUE constraints.
The "sqlite\_autoindex\_TABLE\_N" name is never allocated for an
[INTEGER PRIMARY KEY](lang_createtable.html#rowid), either in rowid tables or WITHOUT ROWID tables.




**tbl\_name**

The sqlite\_schema.tbl\_name column holds the name of a table or view
that the object is associated with. For a table or view, the
tbl\_name column is a copy of the name column. For an index, the tbl\_name
is the name of the table that is indexed. For a trigger, the tbl\_name
column stores the name of the table or view that causes the trigger 
to fire.



**rootpage**

The sqlite\_schema.rootpage column stores the page number of the root
b\-tree page for tables and indexes. For rows that define views, triggers,
and virtual tables, the rootpage column is 0 or NULL.



**sql**

The sqlite\_schema.sql column stores SQL text that describes the
object. This SQL text is a [CREATE TABLE](lang_createtable.html), [CREATE VIRTUAL TABLE](lang_createvtab.html),
[CREATE INDEX](lang_createindex.html),
[CREATE VIEW](lang_createview.html), or [CREATE TRIGGER](lang_createtrigger.html) statement that if evaluated against
the database file when it is the main database of a [database connection](c3ref/sqlite3.html)
would recreate the object. The text is usually a copy of the original
statement used to create the object but with normalizations applied so
that the text conforms to the following rules:



* The CREATE, TABLE, VIEW, TRIGGER, and INDEX keywords at the beginning
of the statement are converted to all upper case letters.
* The TEMP or TEMPORARY keyword is removed if it occurs after the 
initial CREATE keyword.
* Any database name qualifier that occurs prior to the name of the
object being created is removed.
* Leading spaces are removed.
* All spaces following the first two keywords are converted into a single
space.


The text in the sqlite\_schema.sql column is a copy of the original
CREATE statement text that created the object, except normalized as
described above and as modified by subsequent [ALTER TABLE](lang_altertable.html) statements.
The sqlite\_schema.sql is NULL for the [internal indexes](fileformat2.html#intschema) that are
automatically created by [UNIQUE](lang_createtable.html#uniqueconst) or [PRIMARY KEY](lang_createtable.html#primkeyconst) constraints.




# 4\. Creation and Modification Of The Schema Table


SQLite creates the schema table upon database creation and modifies
its content as SQLite users submit DDL statements for execution. There
is no need for users to modify it under normal circumstances, and they
bear the risk of [database corruption](howtocorrupt.html#cfgerr) if they do modify it.



