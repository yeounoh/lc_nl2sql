




JSON Functions And Operators




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










JSON Functions And Operators


►
Table Of Contents
[1\. Overview](#overview)
[2\. Compiling in JSON Support](#compiling_in_json_support)
[3\. Interface Overview](#interface_overview)
[3\.1\. JSON arguments](#json_arguments)
[3\.2\. JSONB](#jsonb)
[3\.2\.1\. The JSONB format](#the_jsonb_format)
[3\.2\.2\. Handling of malformed JSONB](#handling_of_malformed_jsonb)
[3\.3\. PATH arguments](#path_arguments)
[3\.4\. VALUE arguments](#value_arguments)
[3\.5\. Compatibility](#compatibility)
[3\.6\. JSON5 Extensions](#json5_extensions)
[3\.7\. Performance Considerations](#performance_considerations)
[3\.8\. The JSON BLOB Input Bug](#the_json_blob_input_bug)
[4\. Function Details](#function_details)
[4\.1\. The json() function](#the_json_function)
[4\.2\. The jsonb() function](#the_jsonb_function)
[4\.3\. The json\_array() function](#the_json_array_function)
[4\.4\. The jsonb\_array() function](#the_jsonb_array_function)
[4\.5\. The json\_array\_length() function](#the_json_array_length_function)
[4\.6\. The json\_error\_position() function](#the_json_error_position_function)
[4\.7\. The json\_extract() function](#the_json_extract_function)
[4\.8\. The jsonb\_extract() function](#the_jsonb_extract_function)
[4\.9\. The \-\> and \-\>\> operators](#the_and_operators)
[4\.10\. The json\_insert(), json\_replace, and json\_set() functions](#the_json_insert_json_replace_and_json_set_functions)
[4\.11\. The jsonb\_insert(), jsonb\_replace, and jsonb\_set() functions](#the_jsonb_insert_jsonb_replace_and_jsonb_set_functions)
[4\.12\. The json\_object() function](#the_json_object_function)
[4\.13\. The jsonb\_object() function](#the_jsonb_object_function)
[4\.14\. The json\_patch() function](#the_json_patch_function)
[4\.15\. The jsonb\_patch() function](#the_jsonb_patch_function)
[4\.16\. The json\_pretty() function](#the_json_pretty_function)
[4\.17\. The json\_remove() function](#the_json_remove_function)
[4\.18\. The jsonb\_remove() function](#the_jsonb_remove_function)
[4\.19\. The json\_type() function](#the_json_type_function)
[4\.20\. The json\_valid() function](#the_json_valid_function)
[4\.21\. The json\_quote() function](#the_json_quote_function)
[4\.22\. Array and object aggregate functions](#array_and_object_aggregate_functions)
[4\.23\. The json\_each() and json\_tree() table\-valued functions](#the_json_each_and_json_tree_table_valued_functions)
[4\.23\.1\. Examples using json\_each() and json\_tree()](#examples_using_json_each_and_json_tree_)




# 1\. Overview



By default, SQLite supports thirty functions and two operators for
dealing with JSON values. There are also two [table\-valued functions](vtab.html#tabfunc2)
that can be used to decompose a JSON string.




There are twenty\-six scalar functions and operators:



1. [json](#jmini)(*json*)
2. [jsonb](#jminib)(*json*)
3. [json\_array](#jarray)(*value1*,*value2*,...)
4. [jsonb\_array](#jarrayb)(*value1*,*value2*,...)
5. [json\_array\_length](#jarraylen)(*json*)  
[json\_array\_length](#jarraylen)(*json*,*path*)
6. [json\_error\_position](#jerr)(*json*)
7. [json\_extract](#jex)(*json*,*path*,...)
8. [jsonb\_extract](#jexb)(*json*,*path*,...)
9. *json* [\-\>](#jptr) *path*
10. *json* [\-\>\>](#jptr) *path*
11. [json\_insert](#jins)(*json*,*path*,*value*,...)
12. [jsonb\_insert](#jinsb)(*json*,*path*,*value*,...)
13. [json\_object](#jobj)(*label1*,*value1*,...)
14. [jsonb\_object](#jobjb)(*label1*,*value1*,...)
15. [json\_patch](#jpatch)(*json*1,json2\)
16. [jsonb\_patch](#jpatchb)(*json*1,json2\)
17. [json\_pretty](#jpretty)(*json*)
18. [json\_remove](#jrm)(*json*,*path*,...)
19. [jsonb\_remove](#jrmb)(*json*,*path*,...)
20. [json\_replace](#jrepl)(*json*,*path*,*value*,...)
21. [jsonb\_replace](#jreplb)(*json*,*path*,*value*,...)
22. [json\_set](#jset)(*json*,*path*,*value*,...)
23. [jsonb\_set](#jsetb)(*json*,*path*,*value*,...)
24. [json\_type](#jtype)(*json*)  
[json\_type](#jtype)(*json*,*path*)
25. [json\_valid](#jvalid)(*json*)  
[json\_valid](#jvalid)(*json*,flags)
26. [json\_quote](#jquote)(*value*)


There are four [aggregate SQL functions](lang_aggfunc.html):



1. [json\_group\_array](#jgrouparray)(*value*)
2. [jsonb\_group\_array](#jgrouparrayb)(*value*)
3. [json\_group\_object](#jgroupobject)(*label*,*value*)
4. [jsonb\_group\_object](#jgroupobjectb)(name,*value*)


The two [table\-valued functions](vtab.html#tabfunc2) are:



1. [json\_each](#jeach)(*json*)  
[json\_each](#jeach)(*json*,*path*)
2. [json\_tree](#jtree)(*json*)  
[json\_tree](#jtree)(*json*,*path*)




# 2\. Compiling in JSON Support



The JSON functions and operators are built into SQLite by default,
as of SQLite version 3\.38\.0 (2022\-02\-22\). They can be omitted
by adding the \-DSQLITE\_OMIT\_JSON compile\-time option. Prior to
version 3\.38\.0, the JSON functions were an extension that would only
be included in builds if the \-DSQLITE\_ENABLE\_JSON1 compile\-time option
was included. In other words, the JSON functions went from being
opt\-in with SQLite version 3\.37\.2 and earlier to opt\-out with
SQLite version 3\.38\.0 and later.



# 3\. Interface Overview



SQLite stores JSON as ordinary text.
Backwards compatibility constraints mean that SQLite is only able to
store values that are NULL, integers, floating\-point numbers, text,
and BLOBs. It is not possible to add a new "JSON" type.




## 3\.1\. JSON arguments



For functions that accept JSON as their first argument, that argument
can be a JSON object, array, number, string, or null. SQLite numeric
values and NULL values are interpreted as JSON numbers and nulls, respectively.
SQLite text values can be understood as JSON objects, arrays, or strings.
If an SQLite text value that is not a well\-formed JSON object, array, or
string is passed into JSON function, that function will usually throw
an error. (Exceptions to this rule are [json\_valid()](json1.html#jvalid),
[json\_quote()](json1.html#jquote), and [json\_error\_position()](json1.html#jerr).)




These routines understand all
[rfc\-8259 JSON syntax](https://www.rfc-editor.org/rfc/rfc8259.txt)
and also [JSON5 extensions](https://spec.json5.org/). JSON text
generated by these routines always strictly conforms to the
[canonical JSON definition](https://json.org) and does not contain any JSON5
or other extensions. The ability to read and understand JSON5 was added in
version 3\.42\.0 (2023\-05\-16\).
Prior versions of SQLite would only read canonical JSON.




## 3\.2\. JSONB



Beginning with version 3\.45\.0 (2024\-01\-15\), SQLite allows its
internal "parse tree" representation of JSON to be stored on disk,
as a BLOB, in a format that we call "JSONB". By storing SQLite's internal
binary representation of JSON directly in the database, applications
can bypass the overhead of parsing and rendering JSON when reading and
updating JSON values. The internal JSONB format also uses slightly
less disk space then text JSON.




Any SQL function parameter that accepts text JSON as an input will also
accept a BLOB in the JSONB format. The function will operate the
same in either case, except that it will run faster when
the input is JSONB, since it does not need to run the JSON parser.




Most SQL functions that return JSON text have a corresponding function
that returns the equivalent JSONB. The functions that return JSON
in the text format begin with "json\_" and functions that
return the binary JSONB format begin with "jsonb\_".



### 3\.2\.1\. The JSONB format



JSONB is a binary representation of JSON used by SQLite and
is intended for internal use by SQLite only. Applications
should not use JSONB outside of SQLite nor try to reverse\-engineer the
JSONB format.




The "JSONB" name is inspired by [PostgreSQL](https://postgresql.org), but the
on\-disk format for SQLite's JSONB is not the same as PostgreSQL's.
The two formats have the same name, but are not binary compatible.
The PostgreSQL JSONB format claims to offer O(1\)
lookup of elements in objects and arrays. SQLite's JSONB format makes no
such claim. SQLite's JSONB has O(N) time complexity for
most operations in SQLite, just like text JSON. The advantage of JSONB in
SQLite is that it is smaller and faster than text JSON \- potentially several
times faster. There is space in the
on\-disk JSONB format to add enhancements and future versions of SQLite might
include options to provide O(1\) lookup of elements in JSONB, but no such
capability is currently available.



### 3\.2\.2\. Handling of malformed JSONB



The JSONB that is generated by SQLite will always be well\-formed. If you
follow recommended practice and
treat JSONB as an opaque BLOB, then you will not have any problems. But
JSONB is just a BLOB, so a mischievous programmer could devise BLOBs
that are similar to JSONB but that are technically malformed. When
misformatted JSONB is feed into JSON functions, any of the following
might happen:



* The SQL statement might abort with a "malformed JSON" error.
* The correct answer might be returned, if the malformed parts of
the JSONB blob do not impact the answer.
* A goofy or nonsensical answer might be returned.



The way in which SQLite handles invalid JSONB might change
from one version of SQLite to the next. The system follows
the garbage\-in/garbage\-out rule: If you feed the JSON functions invalid
JSONB, you get back an invalid answer. If you are in doubt about the
validity of our JSONB, use the [json\_valid()](json1.html#jvalid) function to verify it.




We do make this one promise:
Malformed JSONB will never cause a memory
error or similar problem that might lead to a vulnerability.
Invalid JSONB might lead to crazy answers,
or it might cause queries to abort, but it won't cause a crash.




## 3\.3\. PATH arguments



For functions that accept PATH arguments, that PATH must be well\-formed or
else the function will throw an error.
A well\-formed PATH is a text value that begins with exactly one
'$' character followed by zero or more instances
of ".*objectlabel*" or "\[*arrayindex*]".




The *arrayindex* is usually a non\-negative integer *N*. In
that case, the array element selected is the *N*\-th element
of the array, starting with zero on the left.
The *arrayindex* can also be of the form "**\#\-***N*"
in which case the element selected is the *N*\-th from the
right. The last element of the array is "**\#\-1**". Think of
the "\#" characters as the "number of elements in the array". Then
the expression "\#\-1" evaluates to the integer that corresponds to 
the last entry in the array. It is sometimes useful for the array
index to be just the **\#** character, for example when appending
a value to an existing JSON array:

* json\_set('\[0,1,2]','$\[\#]','new')
→ '\[0,1,2,"new"]'





## 3\.4\. VALUE arguments



For functions that accept "*value*" arguments (also shown as
"*value1*" and "*value2*"),
those arguments are usually understood
to be literal strings that are quoted and become JSON string values
in the result. Even if the input *value* strings look like 
well\-formed JSON, they are still interpreted as literal strings in the
result.




However, if a *value* argument comes directly from the result of another
JSON function or from [the \-\> operator](json1.html#jptr) (but not [the \-\>\> operator](json1.html#jptr)),
then the argument is understood to be actual JSON and
the complete JSON is inserted rather than a quoted string.




For example, in the following call to json\_object(), the *value*
argument looks like a well\-formed JSON array. However, because it is just
ordinary SQL text, it is interpreted as a literal string and added to the
result as a quoted string:

* json\_object('ex','\[52,3\.14159]')
→ '{"ex":"\[52,3\.14159]"}'
* json\_object('ex',('\[52,3\.14159]'\-\>\>'$'))
→ '{"ex":"\[52,3\.14159]"}'





But if the *value* argument in the outer json\_object() call is the
result of another JSON function like [json()](json1.html#jmini) or [json\_array()](json1.html#jarray), then
the value is understood to be actual JSON and is inserted as such:

* json\_object('ex',json('\[52,3\.14159]'))
→ '{"ex":\[52,3\.14159]}'
* json\_object('ex',json\_array(52,3\.14159\))
→ '{"ex":\[52,3\.14159]}'
* json\_object('ex','\[52,3\.14159]'\-\>'$')
→ '{"ex":\[52,3\.14159]}'





To be clear: "*json*" arguments are always interpreted as JSON
regardless of where the value for that argument comes from. But
"*value*" arguments are only interpreted as JSON if those arguments
come directly from another JSON function or [the \-\> operator](json1.html#jptr).




Within JSON value arguments interpreted as JSON strings, Unicode escape
sequences are not treated as equivalent to the characters or escaped
control characters represented by the expressed Unicode code point.
Such escape sequences are not translated or specially treated; they
are treated as plain text by SQLite's JSON functions.



## 3\.5\. Compatibility



The current implementation of this JSON library uses a recursive descent
parser. In order to avoid using excess stack space, any JSON input that has
more than 1000 levels of nesting is considered invalid. Limits on nesting
depth are allowed for compatible implementations of JSON by
[RFC\-8259 section 9](https://tools.ietf.org/html/rfc8259#section-9).




## 3\.6\. JSON5 Extensions



Beginning in version 3\.42\.0 (2023\-05\-16\), these routines will
read and interpret input JSON text that includes
[JSON5](https://spec.json5.org/) extensions. However, JSON text generated
by these routines will always be strictly conforming to the 
[canonical definition of JSON](https://json.org).




Here is a synopsis of JSON5 extensions (adapted from the
[JSON5 specification](https://spec.json5.org/#introduction)):



* Object keys may be unquoted identifiers.
* Objects may have a single trailing comma.
* Arrays may have a single trailing comma.
* Strings may be single quoted.
* Strings may span multiple lines by escaping new line characters.
* Strings may include new character escapes.
* Numbers may be hexadecimal.
* Numbers may have a leading or trailing decimal point.
* Numbers may be "Infinity", "\-Infinity", and "NaN".
* Numbers may begin with an explicit plus sign.
* Single (//...) and multi\-line (/\*...\*/) comments are allowed.
* Additional white space characters are allowed.



To convert string X from JSON5 into canonical JSON, invoke
"[json(X)](json1.html#jmini)". The output of the "[json()](json1.html#jmini)" function will be canonical
JSON regardless of any JSON5 extensions that are present in the input.
For backwards compatibility, the [json\_valid(X)](json1.html#jvalid) function without a
"flags" argument continues
to report false for inputs that are not canonical JSON, even if the
input is JSON5 that the function is able to understand. To determine
whether or not an input string is valid JSON5, include the 0x02 bit
in the "flags" argument to json\_valid: "json\_valid(X,2\)".




These routines understand all of JSON5, plus a little more.
SQLite extends the JSON5 syntax in these two ways:



1. Strict JSON5 requires that
unquoted object keys must be ECMAScript 5\.1 IdentifierNames. But large
unicode tables and lots of code is required in order to determine whether or
not a key is an ECMAScript 5\.1 IdentifierName. For this reason,
SQLite allows object keys to include any unicode characters
greater than U\+007f that are not whitespace characters. This relaxed
definition of "identifier" greatly simplifies the implementation and allows
the JSON parser to be smaller and run faster.
2. JSON5 allows floating\-point infinities to be expressed as
"Infinity", "\-Infinity", or "\+Infinity"
in exactly that case \- the initial "I" is capitalized and all other
characters are lower case. SQLite also allows the abbreviation "Inf"
to be used in place of "Infinity" and it allows both keywords
to appear in any combination of upper and lower case letters.
Similarly,
JSON5 allows "NaN" for not\-a\-number. SQLite extends this to also allow
"QNaN" and "SNaN" in any combination of upper and lower case letters.
Note that SQLite interprets NaN, QNaN, and SNaN as just an alternative
spellings for "null".
This extension has been added because (we are told) there exists a lot
of JSON in the wild that includes these non\-standard representations
for infinity and not\-a\-number.


## 3\.7\. Performance Considerations



Most JSON functions do their internal processing using JSONB. So if the
input is text, they first most translate the input text into JSONB.
If the input is already in the JSONB format, no translation is needed,
that step can be skipped, and performance is faster.




For that reason,
when an argument to one JSON function is supplied by another
JSON function, it is usually more efficient to use the "jsonb\_"
variant for the function used as the argument. 



* ... json\_insert(A,'$.b',json(C)) ...
   ← Less efficient.
* ... json\_insert(A,'$.b',jsonb(C)) ...
   ← More efficient.



The [aggregate JSON SQL functions](json1.html#jgroupobjectb) are an exception to this rule. Those
functions all do their processing using text instead of JSONB. So for the
aggregate JSON SQL functions, it is more efficient for the arguments
to be supplied using "json\_" functions than "jsonb\_"
functions.



* ... json\_group\_array(json(A))) ...
   ← More efficient.
* ... json\_group\_array(jsonb(A))) ...
   ← Less efficient.



## 3\.8\. The JSON BLOB Input Bug


If a JSON input is a BLOB that is not JSONB and that looks like
text JSON when cast to text, then it is accepted as text JSON.
This is actually a long\-standing bug in the original implementation
that the SQLite developers were unaware of. The documentation stated
that a BLOB input to a JSON function should raise an error. But in the
actual implementation, the input would be accepted as long
as the BLOB content was a valid JSON string in the text encoding of
the database.



This JSON BLOB input bug was accidentally fixed when the JSON routines
were reimplemented for the 3\.45\.0 release (2024\-01\-15\).
That caused breakage in applications that had come to depend on the old
behavior. (In defense of those applications: they were often lured into
using BLOBs as JSON by the [readfile()](cli.html#fileio) SQL function
available in the [CLI](cli.html). Readfile() was used to read JSON from disk files,
but readfile() returns a BLOB. And that worked for them, so why not just
do it?)



For backwards compatibility,
the (formerly incorrect) legacy behavior of interpreting BLOBs as text JSON
if no other interpretation works
is hereby documented and is be officially supported in 
version 3\.45\.1 (2024\-01\-30\) and all subsequent releases.



# 4\. Function Details


The following sections provide additional detail on the operation of
the various JSON functions and operators:




## 4\.1\. The json() function


The json(X) function verifies that its argument X is a valid
JSON string or JSONB blob and returns a minified version of that JSON string
with all unnecessary whitespace removed. If X is not a well\-formed
JSON string or JSONB blob, then this routine throws an error.



If the input is JSON5 text, then it is converted into canonical
RFC\-8259 text prior to being returned.



If the argument X to json(X) contains JSON objects with duplicate
labels, then it is undefined whether or not the duplicates are
preserved. The current implementation preserves duplicates.
However, future enhancements
to this routine may choose to silently remove duplicates.




Example:

* json(' { "this" : "is", "a": \[ "test" ] } ')
→ '{"this":"is","a":\["test"]}'





## 4\.2\. The jsonb() function


The jsonb(X) function returns the binary JSONB representation
of the JSON provided as argument X. An error is raised if X is
TEXT that does not have valid JSON syntax.



If X is a BLOB and appears to be JSONB,
then this routine simply returns a copy of X.
Only the outer\-most element of the JSONB input is examined, however.
The deep structure of the JSONB is not validated.




## 4\.3\. The json\_array() function


The json\_array() SQL function accepts zero or more arguments and
returns a well\-formed JSON array that is composed from those arguments.
If any argument to json\_array() is a BLOB then an error is thrown.



An argument with SQL type TEXT is normally converted into a quoted 
JSON string. However, if the argument is the output from another json1
function, then it is stored as JSON. This allows calls to json\_array()
and [json\_object()](json1.html#jobj) to be nested. The [json()](json1.html#jmini) function can also
be used to force strings to be recognized as JSON.



Examples:

* json\_array(1,2,'3',4\)
→ '\[1,2,"3",4]'
* json\_array('\[1,2]')
→ '\["\[1,2]"]'
* json\_array(json\_array(1,2\))
→ '\[\[1,2]]'
* json\_array(1,null,'3','\[4,5]','{"six":7\.7}')
→ '\[1,null,"3","\[4,5]","{\\"six\\":7\.7}"]'
* json\_array(1,null,'3',json('\[4,5]'),json('{"six":7\.7}'))
→ '\[1,null,"3",\[4,5],{"six":7\.7}]'





## 4\.4\. The jsonb\_array() function


The jsonb\_array() SQL function works just like the [json\_array()](json1.html#jarray)
function except that it returns the constructed JSON array in the
SQLite's private JSONB format rather than in the standard
RFC 8259 text format.




## 4\.5\. The json\_array\_length() function


The json\_array\_length(X) function returns the number of elements
in the JSON array X, or 0 if X is some kind of JSON value other
than an array. The json\_array\_length(X,P) locates the array at path P
within X and returns the length of that array, or 0 if path P locates
an element in X that is not a JSON array, and NULL if path P does not
locate any element of X. Errors are thrown if either X is not 
well\-formed JSON or if P is not a well\-formed path.



Examples:

* json\_array\_length('\[1,2,3,4]')
→ 4
* json\_array\_length('\[1,2,3,4]', '$')
→ 4
* json\_array\_length('\[1,2,3,4]', '$\[2]')
→ 0
* json\_array\_length('{"one":\[1,2,3]}')
→ 0
* json\_array\_length('{"one":\[1,2,3]}', '$.one')
→ 3
* json\_array\_length('{"one":\[1,2,3]}', '$.two')
→ NULL





## 4\.6\. The json\_error\_position() function


The json\_error\_position(X) function returns 0 if the input X is a
well\-formed JSON or JSON5 string. If the input X contains one or more
syntax errors, then this function returns the character position of the
first syntax error. The left\-most character is position 1\.



If the input X is a BLOB, then this routine returns 0 if X is
a well\-formed JSONB blob. If the return value is positive, then it
represents the *approximate* 1\-based position in the BLOB of the
first detected error.




The json\_error\_position() function was added with
SQLite version 3\.42\.0 (2023\-05\-16\).





## 4\.7\. The json\_extract() function


The json\_extract(X,P1,P2,...) extracts and returns one or more 
values from the
well\-formed JSON at X. If only a single path P1 is provided, then the
SQL datatype of the result is NULL for a JSON null, INTEGER or REAL
for a JSON numeric value, an INTEGER zero for a JSON false value,
an INTEGER one for a JSON true value, the dequoted text for a 
JSON string value, and a text representation for JSON object and array values.
If there are multiple path arguments (P1, P2, and so forth) then this
routine returns SQLite text which is a well\-formed JSON array holding
the various values.



Examples:

* json\_extract('{"a":2,"c":\[4,5,{"f":7}]}', '$')
→ '{"a":2,"c":\[4,5,{"f":7}]}'
* json\_extract('{"a":2,"c":\[4,5,{"f":7}]}', '$.c')
→ '\[4,5,{"f":7}]'
* json\_extract('{"a":2,"c":\[4,5,{"f":7}]}', '$.c\[2]')
→ '{"f":7}'
* json\_extract('{"a":2,"c":\[4,5,{"f":7}]}', '$.c\[2].f')
→ 7
* json\_extract('{"a":2,"c":\[4,5],"f":7}','$.c','$.a')
→ '\[\[4,5],2]'
* json\_extract('{"a":2,"c":\[4,5],"f":7}','$.c\[\#\-1]')
→ 5
* json\_extract('{"a":2,"c":\[4,5,{"f":7}]}', '$.x')
→ NULL
* json\_extract('{"a":2,"c":\[4,5,{"f":7}]}', '$.x', '$.a')
→ '\[null,2]'
* json\_extract('{"a":"xyz"}', '$.a')
→ 'xyz'
* json\_extract('{"a":null}', '$.a')
→ NULL




There is a subtle incompatibility between the json\_extract() function
in SQLite and the json\_extract() function in MySQL. The MySQL version
of json\_extract() always returns JSON. The SQLite version of
json\_extract() only returns JSON if there are two or more PATH arguments
(because the result is then a JSON array) or if the single PATH argument
references an array or object. In SQLite, if json\_extract() has only
a single PATH argument and that PATH references a JSON null or a string
or a numeric value, then json\_extract() returns the corresponding SQL
NULL, TEXT, INTEGER, or REAL value.



The difference between MySQL json\_extract() and SQLite json\_extract()
really only stands out when accessing individual values within the JSON
that are strings or NULLs. The following table demonstrates the difference:






| Operation | SQLite Result | MySQL Result |
| --- | --- | --- |
| json\_extract('{"a":null,"b":"xyz"}','$.a') | NULL | 'null' |
| json\_extract('{"a":null,"b":"xyz"}','$.b') | 'xyz' | '"xyz"' |



## 4\.8\. The jsonb\_extract() function



The jsonb\_extract() function works the same as the [json\_extract()](json1.html#jex) function,
except in cases where json\_extract() would normally return a text
JSON array object, this routine returns the array or object in the
JSONB format. For the common case where a text, numeric, null, or
boolean JSON element is returned, this routine works exactly the same
as json\_extract().





## 4\.9\. The \-\> and \-\>\> operators


Beginning with SQLite version 3\.38\.0 (2022\-02\-22\), the \-\>
and \-\>\> operators are available for extracting subcomponents of JSON.
The SQLite implementation of \-\> and \-\>\> strives to be
compatible with both MySQL and PostgreSQL.
The \-\> and \-\>\> operators take a JSON string or JSONB blob
as their left operand and a PATH expression or object field
label or array index as their right operand. The \-\> operator
returns a text JSON representation of the selected subcomponent or
NULL if that subcomponent does not exist. The \-\>\> operator returns
an SQL TEXT, INTEGER, REAL, or NULL value that represents the selected
subcomponent, or NULL if the subcomponent does not exist.



Both the \-\> and \-\>\> operators select the same subcomponent
of the JSON to their left. The difference is that \-\> always returns a
JSON representation of that subcomponent and the \-\>\> operator always
returns an SQL representation of that subcomponent. Thus, these operators
are subtly different from a two\-argument [json\_extract()](json1.html#jex) function call.
A call to json\_extract() with two arguments will return a JSON representation
of the subcomponent if and only if the subcomponent is a JSON array or
object, and will return an SQL representation of the subcomponent if the
subcomponent is a JSON null, string, or numeric value.



When the \-\> operator returns JSON, it always returns the
RFC 8565 text representation of that JSON, not JSONB. Use the
[jsonb\_extract()](json1.html#jexb) function if you need a subcomponent in the
JSONB format.



The right\-hand operand to the \-\> and \-\>\> operators can
be a well\-formed JSON path expression. This is the form used by MySQL.
For compatibility with PostgreSQL,
the \-\> and \-\>\> operators also accept a text object label or
integer array index as their right\-hand operand.
If the right operand is a text
label X, then it is interpreted as the JSON path '$.X'. If the right
operand is an integer value N, then it is interpreted as the JSON path '$\[N]'.



Examples:

* '{"a":2,"c":\[4,5,{"f":7}]}' \-\> '$'
→ '{"a":2,"c":\[4,5,{"f":7}]}'
* '{"a":2,"c":\[4,5,{"f":7}]}' \-\> '$.c'
→ '\[4,5,{"f":7}]'
* '{"a":2,"c":\[4,5,{"f":7}]}' \-\> 'c'
→ '\[4,5,{"f":7}]'
* '{"a":2,"c":\[4,5,{"f":7}]}' \-\> '$.c\[2]'
→ '{"f":7}'
* '{"a":2,"c":\[4,5,{"f":7}]}' \-\> '$.c\[2].f'
→ '7'
* '{"a":2,"c":\[4,5,{"f":7}]}' \-\>\> '$.c\[2].f'
→ 7
* '{"a":2,"c":\[4,5,{"f":7}]}' \-\> 'c' \-\> 2 \-\>\> 'f'
→ 7
* '{"a":2,"c":\[4,5],"f":7}' \-\> '$.c\[\#\-1]'
→ '5'
* '{"a":2,"c":\[4,5,{"f":7}]}' \-\> '$.x'
→ NULL
* '\[11,22,33,44]' \-\> 3
→ '44'
* '\[11,22,33,44]' \-\>\> 3
→ 44
* '{"a":"xyz"}' \-\> '$.a'
→ '"xyz"'
* '{"a":"xyz"}' \-\>\> '$.a'
→ 'xyz'
* '{"a":null}' \-\> '$.a'
→ 'null'
* '{"a":null}' \-\>\> '$.a'
→ NULL







## 4\.10\. The json\_insert(), json\_replace, and json\_set() functions


The json\_insert(), json\_replace, and json\_set() functions all take
a single JSON value as their first argument followed by zero or more
pairs of path and value arguments, and return a new JSON string formed
by updating the input JSON by the path/value pairs. The functions
differ only in how they deal with creating new values and overwriting
preexisting values.






| Function | Overwrite if already exists? | Create if does not exist? |
| --- | --- | --- |
| json\_insert() | No | Yes |
| json\_replace() | Yes | No |
| json\_set() | Yes | Yes |


The json\_insert(), json\_replace(), and json\_set() functions always
take an odd number of arguments. The first argument is always the original
JSON to be edited. Subsequent arguments occur in pairs with the first
element of each pair being a path and the second element being the value
to insert or replace or set on that path.



Edits occur sequentially from left to right. Changes caused by
prior edits can affect the path search for subsequent edits.



If the value of a path/value pair is an SQLite TEXT value, then it
is normally inserted as a quoted JSON string, even if the string looks
like valid JSON. However, if the value is the result of another
json function (such as [json()](json1.html#jmini) or [json\_array()](json1.html#jarray) or [json\_object()](json1.html#jobj))
or if it is the result of [the \-\> operator](json1.html#jptr),
then it is interpreted as JSON and is inserted as JSON retaining all
of its substructure. Values that are the result of [the \-\>\> operator](json1.html#jptr)
are always interpreted as TEXT and are inserted as a JSON string even
if they look like valid JSON.



These routines throw an error if the first JSON argument is not
well\-formed or if any PATH argument is not well\-formed or if any
argument is a BLOB.



To append an element onto the end of an array, using json\_insert()
with an array index of "\#". Examples:

* json\_insert('\[1,2,3,4]','$\[\#]',99\)
→ '\[1,2,3,4,99]'
* json\_insert('\[1,\[2,3],4]','$\[1]\[\#]',99\)
→ '\[1,\[2,3,99],4]'




Other examples:

* json\_insert('{"a":2,"c":4}', '$.a', 99\)
→ '{"a":2,"c":4}'
* json\_insert('{"a":2,"c":4}', '$.e', 99\)
→ '{"a":2,"c":4,"e":99}'
* json\_replace('{"a":2,"c":4}', '$.a', 99\)
→ '{"a":99,"c":4}'
* json\_replace('{"a":2,"c":4}', '$.e', 99\)
→ '{"a":2,"c":4}'
* json\_set('{"a":2,"c":4}', '$.a', 99\)
→ '{"a":99,"c":4}'
* json\_set('{"a":2,"c":4}', '$.e', 99\)
→ '{"a":2,"c":4,"e":99}'
* json\_set('{"a":2,"c":4}', '$.c', '\[97,96]')
→ '{"a":2,"c":"\[97,96]"}'
* json\_set('{"a":2,"c":4}', '$.c', json('\[97,96]'))
→ '{"a":2,"c":\[97,96]}'
* json\_set('{"a":2,"c":4}', '$.c', json\_array(97,96\))
→ '{"a":2,"c":\[97,96]}'







## 4\.11\. The jsonb\_insert(), jsonb\_replace, and jsonb\_set() functions


The jsonb\_insert(), jsonb\_replace(), and jsonb\_set() functions work the
same as [json\_insert()](json1.html#jins), [json\_replace()](json1.html#jrepl), and [json\_set()](json1.html#jset), respectively,
except that "jsonb\_" versions return their result in the binary
JSONB format.




## 4\.12\. The json\_object() function


The json\_object() SQL function accepts zero or more pairs of arguments
and returns a well\-formed JSON object that is composed from those arguments.
The first argument of each pair is the label and the second argument of
each pair is the value.
If any argument to json\_object() is a BLOB then an error is thrown.



The json\_object() function currently allows duplicate labels without
complaint, though this might change in a future enhancement.



An argument with SQL type TEXT it is normally converted into a quoted 
JSON string even if the input text is well\-formed JSON. 
However, if the argument is the direct result from another JSON
function or [the \-\> operator](json1.html#jptr) (but not [the \-\>\> operator](json1.html#jptr)), 
then it is treated as JSON and all of its JSON type information
and substructure is preserved. This allows calls to json\_object()
and [json\_array()](json1.html#jarray) to be nested. The [json()](json1.html#jmini) function can also
be used to force strings to be recognized as JSON.



Examples:

* json\_object('a',2,'c',4\)
→ '{"a":2,"c":4}'
* json\_object('a',2,'c','{e:5}')
→ '{"a":2,"c":"{e:5}"}'
* json\_object('a',2,'c',json\_object('e',5\))
→ '{"a":2,"c":{"e":5}}'





## 4\.13\. The jsonb\_object() function



The jsonb\_object() function works just like the [json\_object()](json1.html#jobj) function
except that the generated object is returned in the binary JSONB format.




## 4\.14\. The json\_patch() function


The json\_patch(T,P) SQL function runs the
[RFC\-7396](https://tools.ietf.org/html/rfc7396) MergePatch algorithm
to apply patch P against input T. The patched copy of T is returned.



MergePatch can add, modify, or delete elements of a JSON Object,
and so for JSON Objects, the json\_patch() routine is a generalized
replacement for [json\_set()](json1.html#jset) and [json\_remove()](json1.html#jrm). However, MergePatch
treats JSON Array objects as atomic. MergePatch cannot append to an
Array nor modify individual elements of an Array. It can only insert,
replace, or delete the whole Array as a single unit. Hence, json\_patch()
is not as useful when dealing with JSON that includes Arrays,
especially Arrays with lots of substructure.



Examples:

* json\_patch('{"a":1,"b":2}','{"c":3,"d":4}')
→ '{"a":1,"b":2,"c":3,"d":4}'
* json\_patch('{"a":\[1,2],"b":2}','{"a":9}')
→ '{"a":9,"b":2}'
* json\_patch('{"a":\[1,2],"b":2}','{"a":null}')
→ '{"b":2}'
* json\_patch('{"a":1,"b":2}','{"a":9,"b":null,"c":8}')
→ '{"a":9,"c":8}'
* json\_patch('{"a":{"x":1,"y":2},"b":3}','{"a":{"y":9},"c":8}')
→ '{"a":{"x":1,"y":9},"b":3,"c":8}'





## 4\.15\. The jsonb\_patch() function



The jsonb\_patch() function works just like the [json\_patch()](json1.html#jpatch) function
except that the patched JSON is returned in the binary JSONB format.




## 4\.16\. The json\_pretty() function



The json\_pretty() function works like [json()](json1.html#jmini) except that it adds
extra whitespace to make the JSON result easier for humans to read.
The first argument is the JSON or JSONB that is to be pretty\-printed.
The optional second argument is a text string that is used for indentation.
If the second argument is omitted or is NULL, then indentation is four
spaces per level.



The json\_pretty() function was added with SQLite version 3\.46\.0 
(2024\-05\-23\).




## 4\.17\. The json\_remove() function


The json\_remove(X,P,...) function takes a single JSON value as its
first argument followed by zero or more path arguments.
The json\_remove(X,P,...) function returns
a copy of the X parameter with all the elements 
identified by path arguments removed. Paths that select elements
not found in X are silently ignored.



Removals occurs sequentially from left to right. Changes caused by
prior removals can affect the path search for subsequent arguments.



If the json\_remove(X) function is called with no path arguments,
then it returns the input X reformatted, with excess whitespace
removed.



The json\_remove() function throws an error if the first argument
is not well\-formed JSON or if any later argument is not a well\-formed
path.



Examples:

* json\_remove('\[0,1,2,3,4]','$\[2]')
→ '\[0,1,3,4]'
* json\_remove('\[0,1,2,3,4]','$\[2]','$\[0]')
→ '\[1,3,4]'
* json\_remove('\[0,1,2,3,4]','$\[0]','$\[2]')
→ '\[1,2,4]'
* json\_remove('\[0,1,2,3,4]','$\[\#\-1]','$\[0]')
→ '\[1,2,3]'
* json\_remove('{"x":25,"y":42}')
→ '{"x":25,"y":42}'
* json\_remove('{"x":25,"y":42}','$.z')
→ '{"x":25,"y":42}'
* json\_remove('{"x":25,"y":42}','$.y')
→ '{"x":25}'
* json\_remove('{"x":25,"y":42}','$')
→ NULL





## 4\.18\. The jsonb\_remove() function



The jsonb\_remove() function works just like the [json\_remove()](json1.html#jrm) function
except that the edited JSON result is returned in the binary JSONB format.




## 4\.19\. The json\_type() function


The json\_type(X) function returns the "type" of the outermost element
of X. The json\_type(X,P) function returns the "type" of the element
in X that is selected by path P. The "type" returned by json\_type() is
one of the following SQL text values:
'null', 'true', 'false', 'integer', 'real', 'text', 'array', or 'object'.
If the path P in json\_type(X,P) selects an element that does not exist
in X, then this function returns NULL.



The json\_type() function throws an error if its first argument is
not well\-formed JSON or JSONB or if its second argument is not a well\-formed
JSON path.



Examples:

* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}')
→ 'object'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$')
→ 'object'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a')
→ 'array'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a\[0]')
→ 'integer'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a\[1]')
→ 'real'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a\[2]')
→ 'true'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a\[3]')
→ 'false'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a\[4]')
→ 'null'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a\[5]')
→ 'text'
* json\_type('{"a":\[2,3\.5,true,false,null,"x"]}','$.a\[6]')
→ NULL





## 4\.20\. The json\_valid() function


The json\_valid(X,Y) function return 1 if the argument X is well\-formed
JSON, or returns 0 if X is not well\-formed. The Y parameter is an integer
bitmask that defines what is meant by "well\-formed". The following bits
of Y are currently defined:



* **0x01** →
The input is text that strictly complies with canonical RFC\-8259 JSON,
without any extensions.
* **0x02** →
The input is text that is JSON with [JSON5](json1.html#json5) extensions described above.
* **0x04** →
The input is a BLOB that superficially appears to be [JSONB](json1.html#jsonbx).
* **0x08** →
The input is a BLOB that strictly conforms to the internal [JSONB](json1.html#jsonbx) format.


By combining bits, the following useful values of Y can be derived:



* **1** → X is RFC\-8259 JSON text
* **2** → X is [JSON5](json1.html#json5) text
* **4** → X is probably [JSONB](json1.html#jsonbx)
* **5** → X is RFC\-8259 JSON text or [JSONB](json1.html#jsonbx)
* **6** → X is [JSON5](json1.html#json5) text or [JSONB](json1.html#jsonbx)
 ← *This is probably the value you want*
* **8** → X is strictly conforming [JSONB](json1.html#jsonbx)
* **9** → X is RFC\-8259 or strictly conforming [JSONB](json1.html#jsonbx)
* **10** → X is JSON5 or strictly conforming [JSONB](json1.html#jsonbx)


The Y parameter is optional. If omitted, it defaults to 1, which means
that the default behavior is to return true only if the input X is
strictly conforming RFC\-8259 JSON text without any extensions. This
makes the one\-argument version of json\_valid() compatible with older
versions of SQLite, prior to the addition of support for
[JSON5](json1.html#json5) and [JSONB](json1.html#jsonbx).



The difference between 0x04 and 0x08 bits in the Y parameter is that
0x04 only examines the outer wrapper of the BLOB to see if it superficially
looks like [JSONB](json1.html#jsonbx). This is sufficient for must purposes and is very fast.
The 0x08 bit does a thorough examination of all internal details of the BLOB.
The 0x08 bit takes time that is linear in the size of the X input and is much
slower. The 0x04 bit is recommended for most purposes.



If you just want to know if a value is a plausible input to one of
the other JSON functions, a Y value of 6 is probably what you want to use.



Any Y value less than 1 or greater than 15 raises an error, for the
latest version of json\_valid(). However, future versions of json\_valid()
might be enhanced to accept flag values outside of this range, having new
meanings that we have not yet thought of.



If either X or Y inputs to json\_valid() are NULL, then the function
returns NULL.



Examples:

* json\_valid('{"x":35}')
→ 1
* json\_valid('{x:35}')
→ 0
* json\_valid('{x:35}',6\)
→ 1
* json\_valid('{"x":35')
→ 0
* json\_valid(NULL)
→ NULL





## 4\.21\. The json\_quote() function


The json\_quote(X) function converts the SQL value X (a number or a
string) into its corresponding JSON representation. If X is a JSON value
returned by another JSON function, then this function is a no\-op.



Examples:

* json\_quote(3\.14159\)
→ 3\.14159
* json\_quote('verdant')
→ '"verdant"'
* json\_quote('\[1]')
→ '"\[1]"'
* json\_quote(json('\[1]'))
→ '\[1]'
* json\_quote('\[1,')
→ '"\[1,"'








## 4\.22\. Array and object aggregate functions


The json\_group\_array(X) function is an
[aggregate SQL function](lang_aggfunc.html) that returns a JSON array
comprised of all X values in the aggregation.
Similarly, the json\_group\_object(NAME,VALUE) function returns a JSON object
comprised of all NAME/VALUE pairs in the aggregation.
The "jsonb\_" variants are the same except that they return their
result in the binary [JSONB](json1.html#jsonbx) format.





## 4\.23\. The json\_each() and json\_tree() table\-valued functions


The json\_each(X) and json\_tree(X) [table\-valued functions](vtab.html#tabfunc2) walk the
JSON value provided as their first argument and return one row for each
element. The json\_each(X) function only walks the immediate children
of the top\-level array or object,
or just the top\-level element itself if the top\-level
element is a primitive value.
The json\_tree(X) function recursively walks through the
JSON substructure starting with the top\-level element. 



The json\_each(X,P) and json\_tree(X,P) functions work just like
their one\-argument counterparts except that they treat the element
identified by path P as the top\-level element.



The schema for the table returned by json\_each() and json\_tree() is
as follows:




> ```
> 
> CREATE TABLE json_tree(
>     key ANY,             -- key for current element relative to its parent
>     value ANY,           -- value for the current element
>     type TEXT,           -- 'object','array','string','integer', etc.
>     atom ANY,            -- value for primitive types, null for array & object
>     id INTEGER,          -- integer ID for this element
>     parent INTEGER,      -- integer ID for the parent of this element
>     fullkey TEXT,        -- full path describing the current element
>     path TEXT,           -- path to the container of the current row
>     json JSON HIDDEN,    -- 1st input parameter: the raw JSON
>     root TEXT HIDDEN     -- 2nd input parameter: the PATH at which to start
> );
> 
> ```



The "key" column is the integer array index for elements of a JSON array 
and the text label for elements of a JSON object. The key column is
NULL in all other cases.




The "atom" column is the SQL value corresponding to primitive elements \- 
elements other than JSON arrays and objects. The "atom" column is NULL
for a JSON array or object. The "value" column is the same as the
"atom" column for primitive JSON elements but takes on the text JSON value
for arrays and objects.




The "type" column is an SQL text value taken from ('null', 'true', 'false',
'integer', 'real', 'text', 'array', 'object') according to the type of
the current JSON element.




The "id" column is an integer that identifies a specific JSON element
within the complete JSON string. The "id" integer is an internal housekeeping
number, the computation of which might change in future releases. The
only guarantee is that the "id" column will be different for every row.




The "parent" column is always NULL for json\_each().
For json\_tree(),
the "parent" column is the "id" integer for the parent of the current
element, or NULL for the top\-level JSON element or the element identified
by the root path in the second argument.




The "fullkey" column is a text path that uniquely identifies the current
row element within the original JSON string. The complete key to the
true top\-level element is returned even if an alternative starting point
is provided by the "root" argument.




The "path" column is the path to the array or object container that holds 
the current row, or the path to the current row in the case where the 
iteration starts on a primitive type and thus only provides a single
row of output.



### 4\.23\.1\. Examples using json\_each() and json\_tree()


Suppose the table "CREATE TABLE user(name,phone)" stores zero or
more phone numbers as a JSON array object in the user.phone field.
To find all users who have any phone number with a 704 area code:




> ```
> 
> SELECT DISTINCT user.name
>   FROM user, json_each(user.phone)
>  WHERE json_each.value LIKE '704-%';
> 
> ```


Now suppose the user.phone field contains plain text if the user
has only a single phone number and a JSON array if the user has multiple
phone numbers. The same question is posed: "Which users have a phone number
in the 704 area code?" But now the json\_each() function can only be called
for those users that have two or more phone numbers since json\_each()
requires well\-formed JSON as its first argument:




> ```
> 
> SELECT name FROM user WHERE phone LIKE '704-%'
> UNION
> SELECT user.name
>   FROM user, json_each(user.phone)
>  WHERE json_valid(user.phone)
>    AND json_each.value LIKE '704-%';
> 
> ```


Consider a different database with "CREATE TABLE big(json JSON)".
To see a complete line\-by\-line decomposition of the data:




> ```
> 
> SELECT big.rowid, fullkey, value
>   FROM big, json_tree(big.json)
>  WHERE json_tree.type NOT IN ('object','array');
> 
> ```


In the previous, the "type NOT IN ('object','array')" term of the
WHERE clause suppresses containers and only lets through leaf elements.
The same effect could be achieved this way:




> ```
> 
> SELECT big.rowid, fullkey, atom
>   FROM big, json_tree(big.json)
>  WHERE atom IS NOT NULL;
> 
> ```


Suppose each entry in the BIG table is a JSON object 
with a '$.id' field that is a unique identifier
and a '$.partlist' field that can be a deeply nested object.
You want to find the id of every entry that contains one
or more references to uuid '6fa5181e\-5721\-11e5\-a04e\-57f3d7b32808' anywhere
in its '$.partlist'.




> ```
> 
> SELECT DISTINCT json_extract(big.json,'$.id')
>   FROM big, json_tree(big.json, '$.partlist')
>  WHERE json_tree.key='uuid'
>    AND json_tree.value='6fa5181e-5721-11e5-a04e-57f3d7b32808';
> 
> ```


*This page last modified on [2024\-05\-05 15:23:53](https://sqlite.org/docsrc/honeypot) UTC* 


