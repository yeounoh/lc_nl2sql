




String LIKE Matching




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## String LIKE Matching




> ```
> 
> int sqlite3_strlike(const char *zGlob, const char *zStr, unsigned int cEsc);
> 
> ```


The [sqlite3\_strlike(P,X,E)](../c3ref/strlike.html) interface returns zero if and only if
string X matches the [LIKE](../lang_expr.html#like) pattern P with escape character E.
The definition of [LIKE](../lang_expr.html#like) pattern matching used in
[sqlite3\_strlike(P,X,E)](../c3ref/strlike.html) is the same as for the "X LIKE P ESCAPE E"
operator in the SQL dialect understood by SQLite. For "X LIKE P" without
the ESCAPE clause, set the E parameter of [sqlite3\_strlike(P,X,E)](../c3ref/strlike.html) to 0\.
As with the LIKE operator, the [sqlite3\_strlike(P,X,E)](../c3ref/strlike.html) function is case
insensitive \- equivalent upper and lower case ASCII characters match
one another.


The [sqlite3\_strlike(P,X,E)](../c3ref/strlike.html) function matches Unicode characters, though
only ASCII characters are case folded.


Note that this routine returns zero on a match and non\-zero if the strings
do not match, the same as [sqlite3\_stricmp()](../c3ref/stricmp.html) and [sqlite3\_strnicmp()](../c3ref/stricmp.html).


See also: [sqlite3\_strglob()](../c3ref/strglob.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


