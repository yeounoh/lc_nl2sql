




The COMPLETION() Table\-Valued Function




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The COMPLETION() Table\-Valued Function


# 1\. Overview


The COMPLETION extension implements a [table\-valued function](vtab.html#tabfunc2) named
"completion" that can be used to suggest completions of partially entered
words during interactive SQL input. The completion table can be
used to help implement tab\-completion, for example.



# 2\. Details


The designed query interface is:




```
SELECT DISTINCT candidate COLLATE nocase
  FROM completion($prefix, $wholeline)
 ORDER BY 1;

```

The query above will return suggestions for the whole input word that
begins with $prefix. The $wholeline parameter is all text from the beginning
of the line up to the insertion point. The $wholeline parameter is used
for context.



The $prefix parameter may be NULL, in which case the prefix is deduced
from $wholeline. Or, the $wholeline parameter may be NULL or omitted if 
context information is unavailable or if context\-aware completion is not
desired.



The completion table might return the same candidate more than once, and
it will return candidates in an arbitrary order. The DISTINCT keyword and
the ORDER BY in the sample query above are added to make the answers unique
and in lexicographical order.



## 2\.1\. Example Usage


The completion table is used to implement tab\-completion in the
[command\-line shell](cli.html) in conjunction with either the readline or linenoise
input line editing packages for unix. See the
<https://sqlite.org/src/file/src/shell.c.in> source file for example
code. Search for "FROM completion" to find the relevant code sections.



Because the completion table is built into the command\-line shell in order
to provide for tab\-completions, you can run test queries against the
completion table directly in the command\-line shell. Simply type a
query such as the example shown above, filling in appropriate values
for $prefix and $wholeline, and observe the output.



# 3\. Limitations


The completion table is designed for interactive use. It will return
answers at a speed appropriate for human typing. No effort is made to
be unusually efficient, so long as the response time is nearly instantaneous
in a user interface.



As of this writing (2017\-07\-13\), the completion virtual table only
looks for SQL keywords, and schema, table, and column names. The
context contained in $wholeline is completely ignored. Future enhancements
will try to return new completions taken from function and pragma names
and other sources, as well as consider more context. The completion
table should be considered a work\-in\-progress.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


