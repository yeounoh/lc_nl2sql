




Count The Number Of Rows Modified




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Count The Number Of Rows Modified




> ```
> 
> int sqlite3_changes(sqlite3*);
> sqlite3_int64 sqlite3_changes64(sqlite3*);
> 
> ```



These functions return the number of rows modified, inserted or
deleted by the most recently completed INSERT, UPDATE or DELETE
statement on the database connection specified by the only parameter.
The two functions are identical except for the type of the return value
and that if the number of rows modified by the most recent INSERT, UPDATE
or DELETE is greater than the maximum value supported by type "int", then
the return value of sqlite3\_changes() is undefined. Executing any other
type of SQL statement does not modify the value returned by these functions.


Only changes made directly by the INSERT, UPDATE or DELETE statement are
considered \- auxiliary changes caused by [triggers](../lang_createtrigger.html),
[foreign key actions](../foreignkeys.html#fk_actions) or [REPLACE](../lang_replace.html) constraint resolution are not counted.


Changes to a view that are intercepted by
[INSTEAD OF triggers](../lang_createtrigger.html#instead_of_trigger) are not counted. The value
returned by sqlite3\_changes() immediately after an INSERT, UPDATE or
DELETE statement run on a view is always zero. Only changes made to real
tables are counted.


Things are more complicated if the sqlite3\_changes() function is
executed while a trigger program is running. This may happen if the
program uses the [changes() SQL function](../lang_corefunc.html#changes), or if some other callback
function invokes sqlite3\_changes() directly. Essentially:


* Before entering a trigger program the value returned by
sqlite3\_changes() function is saved. After the trigger program
has finished, the original value is restored.



- Within a trigger program each INSERT, UPDATE and DELETE
statement sets the value returned by sqlite3\_changes()
upon completion as normal. Of course, this value will not include
any changes performed by sub\-triggers, as the sqlite3\_changes()
value will be saved and restored after each sub\-trigger has run.



This means that if the changes() SQL function (or similar) is used
by the first INSERT, UPDATE or DELETE statement within a trigger, it
returns the value as set when the calling statement began executing.
If it is used by the second or subsequent such statement within a trigger
program, the value returned reflects the number of rows modified by the
previous INSERT, UPDATE or DELETE statement within the same trigger.


If a separate thread makes changes on the same database connection
while [sqlite3\_changes()](../c3ref/changes.html) is running then the value returned
is unpredictable and not meaningful.


See also:
* the [sqlite3\_total\_changes()](../c3ref/total_changes.html) interface
* the [count\_changes pragma](../pragma.html#pragma_count_changes)* the [changes() SQL function](../lang_corefunc.html#changes)* the [data\_version pragma](../pragma.html#pragma_data_version)




See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


