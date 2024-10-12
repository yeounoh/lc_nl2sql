




Using SQLite In Multi\-Threaded Applications




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Using SQLite In Multi\-Threaded Applications


# 1\. Overview


SQLite supports three different threading modes:


1. **Single\-thread**.
In this mode, all mutexes are disabled and SQLite is unsafe to use in
more than a single thread at once.
2. **Multi\-thread**.
In this mode, SQLite can be safely used by multiple threads provided that
no single [database connection](c3ref/sqlite3.html) nor any object derived from database connection,
such as a [prepared statement](c3ref/stmt.html),
is used in two or more threads at the same time.
3. **Serialized**.
In serialized mode, API calls to affect or use any SQLite [database connection](c3ref/sqlite3.html)
or any object derived from such a database connection
can be made safely from multiple threads.
The effect on an individual object is the same as if the API calls had all
been made in the same order from a single thread. The name "serialized"
arises from the fact that SQLite uses mutexes to serialize access to each
object.



The threading mode can be selected at compile\-time (when the SQLite
library is being compiled from source code) or at start\-time (when the
application that intends to use SQLite is initializing) or at
run\-time (when a new SQLite database connection is being created).
Generally speaking, run\-time overrides start\-time and start\-time
overrides compile\-time. Except, single\-thread mode cannot be
overridden once selected.




The default mode is serialized.



# 2\. Compile\-time selection of threading mode



Use the [SQLITE\_THREADSAFE](compile.html#threadsafe) compile\-time parameter to select the
threading mode. If no [SQLITE\_THREADSAFE](compile.html#threadsafe) compile\-time parameter is
present, then serialized mode is used.
This can be made explicit with 
[\-DSQLITE\_THREADSAFE\=1](compile.html#threadsafe).
With
[\-DSQLITE\_THREADSAFE\=0](compile.html#threadsafe) the threading mode is
single\-thread. With
[\-DSQLITE\_THREADSAFE\=2](compile.html#threadsafe) the threading mode is
multi\-thread.




The return value of the [sqlite3\_threadsafe()](c3ref/threadsafe.html) interface is the value
of SQLITE\_THREADSAFE set at compile\-time. It does not reflect changes
to the threading mode made at runtime via the [sqlite3\_config()](c3ref/config.html)
interface or by flags given as the third argument to [sqlite3\_open\_v2()](c3ref/open.html).




If single\-thread mode is selected at compile\-time, then critical
mutexing logic is omitted from the build and it is impossible to
enable either multi\-thread or serialized modes at start\-time or
run\-time.



# 3\. Start\-time selection of threading mode



Assuming that the compile\-time threading mode is not single\-thread, then
the threading mode can be changed during initialization using the
[sqlite3\_config()](c3ref/config.html) interface. The [SQLITE\_CONFIG\_SINGLETHREAD](c3ref/c_config_covering_index_scan.html#sqliteconfigsinglethread) verb
puts SQLite into single\-thread mode, the [SQLITE\_CONFIG\_MULTITHREAD](c3ref/c_config_covering_index_scan.html#sqliteconfigmultithread)
verb sets multi\-thread mode, and the [SQLITE\_CONFIG\_SERIALIZED](c3ref/c_config_covering_index_scan.html#sqliteconfigserialized) verb
sets serialized mode.



# 4\. Run\-time selection of threading mode


If single\-thread mode has not been selected at compile\-time or start\-time,
then individual database connections can be created as either multi\-thread
or serialized. It is not possible to downgrade an individual database
connection to single\-thread mode. Nor is it possible to escalate an
individual database connection if the compile\-time or start\-time mode
is single\-thread.


The threading mode for an individual database connection is determined
by flags given as the third argument to [sqlite3\_open\_v2()](c3ref/open.html). The
[SQLITE\_OPEN\_NOMUTEX](c3ref/c_open_autoproxy.html) flag causes the database connection to be in the
multi\-thread mode and the [SQLITE\_OPEN\_FULLMUTEX](c3ref/c_open_autoproxy.html) flag causes the connection
to be in serialized mode. If neither flag is specified or if
[sqlite3\_open()](c3ref/open.html) or [sqlite3\_open16()](c3ref/open.html) are used instead of 
[sqlite3\_open\_v2()](c3ref/open.html), then the default
mode determined by the compile\-time and start\-time settings is used.



*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


