




Load An Extension




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Load An Extension




> ```
> 
> int sqlite3_load_extension(
>   sqlite3 *db,          /* Load the extension into this database connection */
>   const char *zFile,    /* Name of the shared library containing extension */
>   const char *zProc,    /* Entry point.  Derived from zFile if 0 */
>   char **pzErrMsg       /* Put error message here if not 0 */
> );
> 
> ```



This interface loads an SQLite extension library from the named file.


The sqlite3\_load\_extension() interface attempts to load an
[SQLite extension](../loadext.html) library contained in the file zFile. If
the file cannot be loaded directly, attempts are made to load
with various operating\-system specific extensions added.
So for example, if "samplelib" cannot be loaded, then names like
"samplelib.so" or "samplelib.dylib" or "samplelib.dll" might
be tried also.


The entry point is zProc.
zProc may be 0, in which case SQLite will try to come up with an
entry point name on its own. It first tries "sqlite3\_extension\_init".
If that does not work, it constructs a name "sqlite3\_X\_init" where the
X is consists of the lower\-case equivalent of all ASCII alphabetic
characters in the filename from the last "/" to the first following
"." and omitting any initial "lib".
The sqlite3\_load\_extension() interface returns
[SQLITE\_OK](../rescode.html#ok) on success and [SQLITE\_ERROR](../rescode.html#error) if something goes wrong.
If an error occurs and pzErrMsg is not 0, then the
[sqlite3\_load\_extension()](../c3ref/load_extension.html) interface shall attempt to
fill \*pzErrMsg with error message text stored in memory
obtained from [sqlite3\_malloc()](../c3ref/free.html). The calling function
should free this memory by calling [sqlite3\_free()](../c3ref/free.html).


Extension loading must be enabled using
[sqlite3\_enable\_load\_extension()](../c3ref/enable_load_extension.html) or
[sqlite3\_db\_config](../c3ref/db_config.html)(db,[SQLITE\_DBCONFIG\_ENABLE\_LOAD\_EXTENSION](../c3ref/c_dbconfig_defensive.html#sqlitedbconfigenableloadextension),1,NULL)
prior to calling this API,
otherwise an error will be returned.


**Security warning:** It is recommended that the
[SQLITE\_DBCONFIG\_ENABLE\_LOAD\_EXTENSION](../c3ref/c_dbconfig_defensive.html#sqlitedbconfigenableloadextension) method be used to enable only this
interface. The use of the [sqlite3\_enable\_load\_extension()](../c3ref/enable_load_extension.html) interface
should be avoided. This will keep the SQL function [load\_extension()](../lang_corefunc.html#load_extension)
disabled and prevent SQL injections from giving attackers
access to extension loading capabilities.


See also the [load\_extension() SQL function](../lang_corefunc.html#load_extension).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


