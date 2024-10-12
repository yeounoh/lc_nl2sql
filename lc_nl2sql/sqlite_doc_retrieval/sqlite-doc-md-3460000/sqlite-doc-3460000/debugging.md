




Hints for Debugging SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# Debugging Hints



The following is a random assortment of techniques used by the
SQLite developers to trace, examine, and understand the behavior of the
core SQLite library.


These techniques are designed to aid in understanding the
core SQLite library itself, not applications that merely use SQLite.

1. **Use the ".eqp full" option on the [command\-line shell](cli.html)**
When you have a SQL script that you are debugging or trying
to understand, it is often useful to run it in the [command\-line shell](cli.html)
with the ".eqp full" setting. When ".eqp" is set to FULL, the shell
automatically shows the [EXPLAIN](lang_explain.html) and [EXPLAIN QUERY PLAN](eqp.html) output for
each command prior to actually running that command.

For added readability, also set ".echo on" so that the output contains
the original SQL text.

The newer ".eqp trace" command does everything that ".eqp full" does
and also turns on [VDBE tracing](pragma.html#pragma_vdbe_trace).
2. **Use compile\-time options to enable debugging features.**
Suggested compile\-time options include:

	* [\-DSQLITE\_DEBUG](compile.html#debug)* [\-DSQLITE\_ENABLE\_EXPLAIN\_COMMENTS](compile.html#enable_explain_comments)* \-DSQLITE\_ENABLE\_TREETRACE
	* \-DSQLITE\_ENABLE\_WHERETRACE
The SQLITE\_ENABLE\_TREETRACE and SQLITE\_ENABLE\_WHERETRACE options
are not documented in [compile\-time options](compile.html) document because they
are not officially supported. What they do is activate the
".treetrace" and ".wheretrace" dot\-commands in the command\-line
shell, which provide low\-level tracing output for the logic that
generates code for SELECT and DML statements and WHERE clauses, respectively.

- **Call sqlite3ShowExpr() and similar from the debugger.**
When compiled with [SQLITE\_DEBUG](compile.html#debug), SQLite includes routines that will
print out various internal abstract syntax tree structures as ASCII\-art graphs.
This can be very useful in a debugging in order to understand the variables
that SQLite is working with. The following routines are available:


	* void sqlite3ShowExpr(const Expr\*);
	* void sqlite3ShowExprList(const ExprList\*);
	* void sqlite3ShowIdList(const IdList\*);
	* void sqlite3ShowSrcList(const SrcList\*);
	* void sqlite3ShowSelect(const Select\*);
	* void sqlite3ShowWith(const With\*);
	* void sqlite3ShowUpsert(const Upsert\*);
	* void sqlite3ShowTrigger(const Trigger\*);
	* void sqlite3ShowTriggerList(const Trigger\*);
	* void sqlite3ShowTriggerStep(const TriggerStep\*);
	* void sqlite3ShowTriggerStepList(const TriggerStep\*);
	* void sqlite3ShowWindow(const Window\*);
	* void sqlite3ShowWinFunc(const Window\*);
These routines are not APIs and are subject to change. They are
for interactive debugging use only.

- **Breakpoints on test\_addoptrace**
When debugging the [bytecode](opcode.html) generator, it is often useful to know
where a particular opcode is being generated. To find this easily,
run the script in a debugger. Set a breakpoint on the "test\_addoptrace"
routine. Then run the "PRAGMA vdbe\_addoptrace\=ON;" followed by the
SQL statement in question. Each opcode will be displayed as it is
appended to the VDBE program, and the breakpoint will fire immediately
thereafter. Step until reaching the opcode then look backwards
in the stack to see where and how it was generated.

This only works when compiled with [SQLITE\_DEBUG](compile.html#debug).

- **Using the ".treetrace" and ".wheretrace" shell commands**
When the command\-line shell and the core SQLite library are
both compiled with [SQLITE\_DEBUG](compile.html#debug) and
SQLITE\_ENABLE\_TREETRACE and SQLITE\_ENABLE\_WHERETRACE, then the
shell has two commands used to turn on debugging facilities for the
most intricate parts of the code generator \- the logic dealing with
SELECT statements and WHERE clauses, respectively.
The ".treetrace" and ".wheretrace" commands each take a numeric
argument which can be expressed in hexadecimal. Each bit turns on
various parts of debugging. Values of "0xfff" and "0xff" are commonly
used. Use an argument of "0" to turn all tracing output back off.

- **Using the ".breakpoint" shell command**
The ".breakpoint" command in the CLI does nothing but invoke the
procedure named "test\_breakpoint()", which is a no\-op.

If you have a script and you want to start debugging at some point
half\-way through that script, simply set a breakpoint in gdb (or whatever
debugger you are using) on the test\_breakpoint() function, and add a
".breakpoint" command where you want to stop. When you reach that first
breakpoint, set whatever additional breakpoints are variable traces you
need.

- **Disable the [lookaside memory allocator](malloc.html#lookaside)**
When looking for memory allocation problems (memory leaks, use\-after\-free
errors, buffer overflows, etc) it is sometimes useful to disable the
[lookaside memory allocator](malloc.html#lookaside) then run the test under valgrind or MSAN or
some other heap memory debugging tool.
The lookaside memory allocator can 
be disabled at start\-time using the [SQLITE\_CONFIG\_LOOKASIDE](c3ref/c_config_covering_index_scan.html#sqliteconfiglookaside)
interface. The [command\-line shell](cli.html) will use that interface to
disable lookaside if it is started with the "\-\-lookaside 0 0"
command line option.




*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 






