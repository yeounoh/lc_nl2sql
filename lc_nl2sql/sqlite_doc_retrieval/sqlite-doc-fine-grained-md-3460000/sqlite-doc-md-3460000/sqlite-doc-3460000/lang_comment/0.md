




SQL Comment Syntax




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










SQL Comment Syntax


**[comment\-syntax:](syntax/comment-syntax.html)**
hide










\-\-



anything\-except\-newline









newline

end\-of\-input









/\*






anything\-except\-\*/

\*/











Comments are not SQL commands, but can occur within the text of
SQL queries passed to [sqlite3\_prepare\_v2()](c3ref/prepare.html) and related interfaces.
Comments are treated as whitespace by the parser.
Comments can begin anywhere whitespace 
can be found, including inside expressions that span multiple lines.



SQL comments begin with two consecutive "\-" characters (ASCII 0x2d)
and extend up to and including the next newline character (ASCII 0x0a)
or until the end of input, whichever comes first.


C\-style comments begin
with "/\*" and extend up to and including the next "\*/" character pair
or until the end of input, whichever comes first. C\-style comments
can span multiple lines. 


Comments can appear anywhere whitespace can occur,
including inside expressions and in the middle of other SQL statements.
Comments do not nest.



*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


