




Automatic Undo/Redo With SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# Automatic Undo/Redo Using SQLite



This page demonstrates how to use triggers to implement undo/redo 
logic for an application that uses SQLite as its 
[application file format](appfileformat.html).

## Object\-Oriented Design



This design note considers the database to be a collection of objects.
Each SQL table is a class.
Each row is an instance of that class.
There are, of course, other ways to interpret an SQL database schema,
and the techniques described here work equally well under alternative
interpretations, but an object\-oriented view seems be more natural
to most contemporary programmers.

## Capture Changes Using Triggers



The core idea is to create a special table (named "UNDOLOG" in the example)
that holds information needed to undo/redo changes to the database. 
For each class (table) in the database that wants to participate in 
the undo/redo, triggers are created that cause entries to be made in 
the UNDOLOG table for each DELETE, INSERT, and UPDATE of the participating
class.
The UNDOLOG entries consist of ordinary SQL statements the can be
played back to reverse the changes.


For example, suppose you wanted undo/redo on a class (table)
that looks like this:


> ```
> 
> CREATE TABLE ex1(a,b,c);
> 
> ```



Triggers to record changes to table EX1 might look like this:


> ```
> 
> CREATE TEMP TRIGGER ex1_it AFTER INSERT ON ex1 BEGIN
>   INSERT INTO undolog VALUES(NULL,'DELETE FROM ex1 WHERE rowid='||new.rowid);
> END;
> CREATE TEMP TRIGGER ex1_ut AFTER UPDATE ON ex1 BEGIN
>   INSERT INTO undolog VALUES(NULL,'UPDATE ex1
>      SET a='||quote(old.a)||',b='||quote(old.b)||',c='||quote(old.c)||'
>    WHERE rowid='||old.rowid);
> END;
> CREATE TEMP TRIGGER ex1_dt BEFORE DELETE ON ex1 BEGIN
>   INSERT INTO undolog VALUES(NULL,'INSERT INTO ex1(rowid,a,b,c)
>     VALUES('||old.rowid||','||quote(old.a)||','||quote(old.b)||
>            ','||quote(old.c)||')');
> END;
> 
> ```



After each INSERT on ex1, the ex1\_it trigger constructs text of a 
DELETE statement that will undo the INSERT. The ex1\_ut trigger constructs 
an UPDATE statement that will undo the effects of an UPDATE. 
And the ex1\_dt trigger constructs a statement that will undo the 
effects of a DELETE.


Note the use of the [quote() SQL function](lang_corefunc.html#quote) in these triggers.
The quote() function converts its argument into a form 
that is appropriate for inclusion in an SQL statement. Numeric values 
come through unchanged. Single quotes are added before and after 
strings and any internal single quotes are escaped. BLOB values
are rendered using SQL\-standard hexadecimal BLOB notation. The
use of the quote() function ensures that the SQL statements used to
undo and redo are always safe from SQL injection.

## Automatic Creation Of Triggers



Triggers such as the above could be entered manually, but that is tedious.
An important feature of the technique demonstrated below is 
that the triggers are generated automatically.


The implementation language for the example code is 
[TCL](http://www.tcl-lang.org), though you can easily do the same thing 
in another programming language.
Remember that the code here is a demonstration of the technique,
not a drop\-in module that will automatically do everything for you.
The demonstration code shown below is derived from actual code 
in production use. But you will need to make changes to tailor it 
to your application.


To activate the undo/redo logic, invoke the undo::activate command 
with all classes (tables) that are to participate in the undo/redo 
as arguments. Use undo::deactivate, undo::freeze, and undo::unfreeze 
to control the state of the undo/redo mechanism.


The undo::activate command creates temporary triggers in the database
that record all changes made to the tables named in the arguments.

## Application Interface



After a sequence of changes that define a single undo/redo step, 
invoke the undo::barrier command to define the limit of that step. 
In an interactive program, you can call undo::event after any change 
and undo::barrier will be called automatically as an idle callback.


When the user presses the Undo button, invoke undo::undo. 
Invoke undo::redo when the user presses the Redo button.


On each call to undo::undo or undo::redo, the undo/redo module 
automatically invokes methods status\_refresh and reload\_all in 
all toplevel namespaces. These methods should be defined to 
reconstruct the display or otherwise update the state of the 
program based on the undone/redone changes to the database.


The demonstration code below includes a status\_refresh method 
that grays\-out or activates the Undo and Redo buttons and menu 
entries depending on whether or not there is anything to be 
undone or redone. You will need to redefine this method to 
control the Undo and Redo buttons in your application.


The demonstration code assumes that the SQLite database is 
opened used as a database object named "db".

## Example Code



> ```
> 
> # Everything goes in a private namespace
> namespace eval ::undo {
> 
> # proc:  ::undo::activate TABLE ...
> # title: Start up the undo/redo system
> #
> # Arguments should be one or more database tables (in the database associated
> # with the handle "db") whose changes are to be recorded for undo/redo
> # purposes.
> #
> proc activate {args} {
>   variable _undo
>   if {$_undo(active)} return
>   eval _create_triggers db $args
>   set _undo(undostack) {}
>   set _undo(redostack) {}
>   set _undo(active) 1
>   set _undo(freeze) -1
>   _start_interval
> }
> 
> # proc:  ::undo::deactivate
> # title: Halt the undo/redo system and delete the undo/redo stacks
> #
> proc deactivate {} {
>   variable _undo
>   if {!$_undo(active)} return
>   _drop_triggers db
>   set _undo(undostack) {}
>   set _undo(redostack) {}
>   set _undo(active) 0
>   set _undo(freeze) -1
> }
> 
> # proc:  ::undo::freeze
> # title: Stop accepting database changes into the undo stack
> #
> # From the point when this routine is called up until the next unfreeze,
> # new database changes are rejected from the undo stack.
> #
> proc freeze {} {
>   variable _undo
>   if {![info exists _undo(freeze)]} return
>   if {$_undo(freeze)>=0} {error "recursive call to ::undo::freeze"}
>   set _undo(freeze) [db one {SELECT coalesce(max(seq),0) FROM undolog}]
> }
> 
> # proc:  ::undo::unfreeze
> # title: Begin accepting undo actions again.
> #
> proc unfreeze {} {
>   variable _undo
>   if {![info exists _undo(freeze)]} return
>   if {$_undo(freeze)<0} {error "called ::undo::unfreeze while not frozen"}
>   db eval "DELETE FROM undolog WHERE seq>$_undo(freeze)"
>   set _undo(freeze) -1
> }
> 
> # proc:  ::undo::event
> # title: Something undoable has happened
> #
> # This routine is called whenever an undoable action occurs.  Arrangements
> # are made to invoke ::undo::barrier no later than the next idle moment.
> #
> proc event {} {
>   variable _undo
>   if {$_undo(pending)==""} {
>     set _undo(pending) [after idle ::undo::barrier]
>   }
> }
> 
> # proc:  ::undo::barrier
> # title: Create an undo barrier right now.
> #
> proc barrier {} {
>   variable _undo
>   catch {after cancel $_undo(pending)}
>   set _undo(pending) {}
>   if {!$_undo(active)} {
>     refresh
>     return
>   }
>   set end [db one {SELECT coalesce(max(seq),0) FROM undolog}]
>   if {$_undo(freeze)>=0 && $end>$_undo(freeze)} {set end $_undo(freeze)}
>   set begin $_undo(firstlog)
>   _start_interval
>   if {$begin==$_undo(firstlog)} {
>     refresh
>     return
>   }
>   lappend _undo(undostack) [list $begin $end]
>   set _undo(redostack) {}
>   refresh
> }
> 
> # proc:  ::undo::undo
> # title: Do a single step of undo
> #
> proc undo {} {
>   _step undostack redostack
> }
> 
> # proc:  ::undo::redo
> # title: Redo a single step
> #
> proc redo {} {
>   _step redostack undostack
> }
> 
> # proc:   ::undo::refresh
> # title:  Update the status of controls after a database change
> #
> # The undo module calls this routine after any undo/redo in order to
> # cause controls gray out appropriately depending on the current state
> # of the database.  This routine works by invoking the status_refresh
> # module in all top-level namespaces.
> #
> proc refresh {} {
>   set body {}
>   foreach ns [namespace children ::] {
>     if {[info proc ${ns}::status_refresh]==""} continue
>     append body ${ns}::status_refresh\n
>   }
>   proc ::undo::refresh {} $body
>   refresh
> }
> 
> # proc:   ::undo::reload_all
> # title:  Redraw everything based on the current database
> #
> # The undo module calls this routine after any undo/redo in order to
> # cause the screen to be completely redrawn based on the current database
> # contents.  This is accomplished by calling the "reload" module in
> # every top-level namespace other than ::undo.
> #
> proc reload_all {} {
>   set body {}
>   foreach ns [namespace children ::] {
>     if {[info proc ${ns}::reload]==""} continue
>     append body ${ns}::reload\n
>   }
>   proc ::undo::reload_all {} $body
>   reload_all
> }
> 
> ##############################################################################
> # The public interface to this module is above.  Routines and variables that
> # follow (and whose names begin with "_") are private to this module.
> ##############################################################################
> 
> # state information
> #
> set _undo(active) 0
> set _undo(undostack) {}
> set _undo(redostack) {}
> set _undo(pending) {}
> set _undo(firstlog) 1
> set _undo(startstate) {}
> 
> 
> # proc:  ::undo::status_refresh
> # title: Enable and/or disable menu options a buttons
> #
> proc status_refresh {} {
>   variable _undo
>   if {!$_undo(active) || [llength $_undo(undostack)]==0} {
>     .mb.edit entryconfig Undo -state disabled
>     .bb.undo config -state disabled
>   } else {
>     .mb.edit entryconfig Undo -state normal
>     .bb.undo config -state normal
>   }
>   if {!$_undo(active) || [llength $_undo(redostack)]==0} {
>     .mb.edit entryconfig Redo -state disabled
>     .bb.redo config -state disabled
>   } else {
>     .mb.edit entryconfig Redo -state normal
>     .bb.redo config -state normal
>   }
> }
> 
> # xproc:  ::undo::_create_triggers DB TABLE1 TABLE2 ...
> # title:  Create change recording triggers for all tables listed
> #
> # Create a temporary table in the database named "undolog".  Create
> # triggers that fire on any insert, delete, or update of TABLE1, TABLE2, ....
> # When those triggers fire, insert records in undolog that contain
> # SQL text for statements that will undo the insert, delete, or update.
> #
> proc _create_triggers {db args} {
>   catch {$db eval {DROP TABLE undolog}}
>   $db eval {CREATE TEMP TABLE undolog(seq integer primary key, sql text)}
>   foreach tbl $args {
>     set collist [$db eval "pragma table_info($tbl)"]
>     set sql "CREATE TEMP TRIGGER _${tbl}_it AFTER INSERT ON $tbl BEGIN\n"
>     append sql "  INSERT INTO undolog VALUES(NULL,"
>     append sql "'DELETE FROM $tbl WHERE rowid='||new.rowid);\nEND;\n"
> 
>     append sql "CREATE TEMP TRIGGER _${tbl}_ut AFTER UPDATE ON $tbl BEGIN\n"
>     append sql "  INSERT INTO undolog VALUES(NULL,"
>     append sql "'UPDATE $tbl "
>     set sep "SET "
>     foreach {x1 name x2 x3 x4 x5} $collist {
>       append sql "$sep$name='||quote(old.$name)||'"
>       set sep ","
>     }
>     append sql " WHERE rowid='||old.rowid);\nEND;\n"
> 
>     append sql "CREATE TEMP TRIGGER _${tbl}_dt BEFORE DELETE ON $tbl BEGIN\n"
>     append sql "  INSERT INTO undolog VALUES(NULL,"
>     append sql "'INSERT INTO ${tbl}(rowid"
>     foreach {x1 name x2 x3 x4 x5} $collist {append sql ,$name}
>     append sql ") VALUES('||old.rowid||'"
>     foreach {x1 name x2 x3 x4 x5} $collist {append sql ,'||quote(old.$name)||'}
>     append sql ")');\nEND;\n"
> 
>     $db eval $sql
>   }
> }
> 
> # xproc:  ::undo::_drop_triggers DB
> # title:  Drop all of the triggers that _create_triggers created
> #
> proc _drop_triggers {db} {
>   set tlist [$db eval {SELECT name FROM sqlite_temp_schema
>                        WHERE type='trigger'}]
>   foreach trigger $tlist {
>     if {![regexp {_.*_(i|u|d)t$} $trigger]} continue
>     $db eval "DROP TRIGGER $trigger;"
>   }
>   catch {$db eval {DROP TABLE undolog}}
> }
> 
> # xproc: ::undo::_start_interval
> # title: Record the starting conditions of an undo interval
> #
> proc _start_interval {} {
>   variable _undo
>   set _undo(firstlog) [db one {SELECT coalesce(max(seq),0)+1 FROM undolog}]
> }
> 
> # xproc: ::undo::_step V1 V2
> # title: Do a single step of undo or redo
> #
> # For an undo V1=="undostack" and V2=="redostack".  For a redo,
> # V1=="redostack" and V2=="undostack".
> #
> proc _step {v1 v2} {
>   variable _undo
>   set op [lindex $_undo($v1) end]
>   set _undo($v1) [lrange $_undo($v1) 0 end-1]
>   foreach {begin end} $op break
>   db eval BEGIN
>   set q1 "SELECT sql FROM undolog WHERE seq>=$begin AND seq<=$end
>           ORDER BY seq DESC"
>   set sqllist [db eval $q1]
>   db eval "DELETE FROM undolog WHERE seq>=$begin AND seq<=$end"
>   set _undo(firstlog) [db one {SELECT coalesce(max(seq),0)+1 FROM undolog}]
>   foreach sql $sqllist {
>     db eval $sql
>   }
>   db eval COMMIT
>   reload_all
> 
>   set end [db one {SELECT coalesce(max(seq),0) FROM undolog}]
>   set begin $_undo(firstlog)
>   lappend _undo($v2) [list $begin $end]
>   _start_interval
>   refresh
> }
> 
> 
> # End of the ::undo namespace
> }
> 
> ```


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


































