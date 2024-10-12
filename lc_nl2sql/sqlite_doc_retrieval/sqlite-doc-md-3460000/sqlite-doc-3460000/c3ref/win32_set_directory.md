




Win32 Specific Interface




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Win32 Specific Interface




> ```
> 
> int sqlite3_win32_set_directory(
>   unsigned long type, /* Identifier for directory being set or reset */
>   void *zValue        /* New value for directory being set or reset */
> );
> int sqlite3_win32_set_directory8(unsigned long type, const char *zValue);
> int sqlite3_win32_set_directory16(unsigned long type, const void *zValue);
> 
> ```



These interfaces are available only on Windows. The
[sqlite3\_win32\_set\_directory](../c3ref/win32_set_directory.html) interface is used to set the value associated
with the [sqlite3\_temp\_directory](../c3ref/temp_directory.html) or [sqlite3\_data\_directory](../c3ref/data_directory.html) variable, to
zValue, depending on the value of the type parameter. The zValue parameter
should be NULL to cause the previous value to be freed via [sqlite3\_free](../c3ref/free.html);
a non\-NULL value will be copied into memory obtained from [sqlite3\_malloc](../c3ref/free.html)
prior to being used. The [sqlite3\_win32\_set\_directory](../c3ref/win32_set_directory.html) interface returns
[SQLITE\_OK](../rescode.html#ok) to indicate success, [SQLITE\_ERROR](../rescode.html#error) if the type is unsupported,
or [SQLITE\_NOMEM](../rescode.html#nomem) if memory could not be allocated. The value of the
[sqlite3\_data\_directory](../c3ref/data_directory.html) variable is intended to act as a replacement for
the current directory on the sub\-platforms of Win32 where that concept is
not present, e.g. WinRT and UWP. The [sqlite3\_win32\_set\_directory8](../c3ref/win32_set_directory.html) and
[sqlite3\_win32\_set\_directory16](../c3ref/win32_set_directory.html) interfaces behave exactly the same as the
sqlite3\_win32\_set\_directory interface except the string parameter must be
UTF\-8 or UTF\-16, respectively.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


