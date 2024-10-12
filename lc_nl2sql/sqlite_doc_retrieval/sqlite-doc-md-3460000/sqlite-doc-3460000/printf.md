




SQLite's Built\-in printf()




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










SQLite's Built\-in printf()


►
Table Of Contents
[1\. Overview](#overview)
[1\.1\. Advantages](#advantages)
[1\.2\. Disadvantages](#disadvantages)
[2\. Formatting Details](#formatting_details)
[2\.1\. Substitution Types](#substitution_types)
[2\.2\. The Optional Length Field](#the_optional_length_field)
[2\.3\. The Optional Width Field](#the_optional_width_field)
[2\.4\. The Optional Precision Field](#the_optional_precision_field)
[2\.5\. The Options Flags Field](#the_options_flags_field)
[3\. Implementation And History](#implementation_and_history)




# 1\. Overview


SQLite contains its own implementation of the string formatting routine "printf()",
accessible via the following interfaces:



* [format()](lang_corefunc.html#format) → an SQL function returning the formatted string
* [sqlite3\_mprintf()](c3ref/mprintf.html) → Store the formatted string in memory obtained
 [sqlite3\_malloc64()](c3ref/free.html).
* [sqlite3\_snprintf()](c3ref/mprintf.html) → Store the formatted string in a static buffer
* [sqlite3\_str\_appendf()](c3ref/str_append.html) → Append formatted text to a dynamic string
* [sqlite3\_vmprintf()](c3ref/mprintf.html) → Varargs version of sqlite3\_mprintf()
* [sqlite3\_vsnprintf()](c3ref/mprintf.html) → Varargs version of sqlite3\_snprintf()
* [sqlite3\_str\_vappendf()](c3ref/str_append.html) → Varargs version of sqlite3\_str\_appendf()


The same core string formatter is also used internally by SQLite.



## 1\.1\. Advantages


Why does SQLite have its own private built\-in printf() implementation?
Why not use the printf() implementation from the standard C library?
Several reasons:






1. By using its own built\-in implementation, SQLite guarantees that the
output will be the same on all platforms and in all LOCALEs.
This is important for consistency and for testing. It would be problematic
if one machine gave an answer of "5\.25e\+08" and another gave an answer
of "5\.250e\+008". Both answers are correct, but it is better when SQLite
always gives the same answer.
2. We know of no way to use the standard library printf() C interface to
implement the [format() SQL function](lang_corefunc.html#format) feature of SQLite. The built\-in
printf() implementation can be easily adapted to that task, however.
3. The printf() in SQLite supports new non\-standard substitution
types ([%q](printf.html#percentq), [%Q](printf.html#percentq), [%w](printf.html#percentw), and [%z](printf.html#percentz)), and enhanced substitution
behavior (%s and [%z](printf.html#percentz)) that are useful both internally to SQLite
and to applications using SQLite.
Standard library printf()s cannot normally be extended in this way.
4. Via the [sqlite3\_mprintf()](c3ref/mprintf.html) and [sqlite3\_vmprintf()](c3ref/mprintf.html) interfaces,
the built\-in printf() implementation supports the ability to render an
arbitrary\-length string into a memory buffer obtained from [sqlite3\_malloc64()](c3ref/free.html).
This is safer and less error prone than trying to precompute an upper size
limit on the result string, allocate an appropriately sized buffer, and
then calling snprintf().
5. The SQLite\-specific printf() supports a new flag (!) called the
"alternate\-form\-2" flag. The alternate\-form\-2 flag changes the processing
of floating\-point conversions in subtle ways so that the output is always
an SQL\-compatible text representation of a floating\-point number \- something
that is not possible to achieve with standard\-library printf(). For
string substitutions, the alternate\-form\-2 flag causes the width and
precision to be measured in characters instead of bytes, which simplifies
processing of strings containing multi\-byte UTF8 characters.
6. The built\-in SQLite has compile\-time options such as
SQLITE\_PRINTF\_PRECISION\_LIMIT that provide defense against 
denial\-of\-service attacks for application that expose the
printf() functionality to untrusted users.
7. Using a built\-in printf() implementation means that SQLite has one
fewer dependency on the host environment, making it more portable.


## 1\.2\. Disadvantages



In fairness, having a built\-in implementation of printf() also comes with
some disadvantages. To wit:



1. The built\-in printf() implementation uses extra code space 
(about 7800 bytes on GCC 5\.4 with \-Os).
2. The floating\-point to text conversion subfunction for the built\-in printf()
is limited in precision to 16 significant digits or 26 significant digits
if the "!" alternate\-form\-2 flag is used.
Every IEEE\-754 double can be represented *exactly* as a decimal
value, but for many doubles the exact decimal representation requires
more than 16 or 26 significant digits.
The SQLite printf() function only renders the first 16 or 26 significant digits
because that can be done efficient and because 16 decimal digits it is sufficient
to distinguish every possible double value. Use the [decimal extension](floatingpoint.html#decext) to get
the exact decimal equivalent of double value for the rare cases where that is
required.
3. The order of the buffer pointer and buffer size parameters in the built\-in
snprintf() implementation is reversed from the order used in standard\-library
implementations.
4. The built\-in printf() implementation does not handle posix positional referencing
modifiers that allow the order of arguments to printf() to be different from the
order of the %\-substitutions. In the built\-in printf(), the order of the arguments
must exactly match the order of the %\-substitutions.



In spite of the disadvantages, the developers believe that having a built\-in
printf() implementation inside of SQLite is a net positive.



# 2\. Formatting Details


The format string for printf() is a template for the generated
string. Substitutions are made whenever a "%" character appears in
the format string. The "%" is followed by one or more additional
characters that describe the substitution. Each substitution has
the following format:




> **%***\[flags]\[width]\[***.***precision]\[length]type*


All substitutions begin with a single "%" and end with a single type character.
The other elements of the substitution are optional.



To include a single "%" character in the output, put two consecutive
"%" characters in the template.



## 2\.1\. Substitution Types


The following chart shows the substitution types supported by SQLite:






| Substitution Type | Meaning |
| --- | --- |
| % | Two "%" characters in a row are translated into a single "%" in the output,  without substituting any values. |
| d, i | The argument is a signed integer which is displayed in decimal. |
| u | The argument is an unsigned integer which is displayed in decimal. |
| f | The argument is a double which is displayed in decimal. |
| e, E | The argument is a double which is displayed in exponential notation.  The exponent character is 'e' or 'E' depending on the type. |
| g, G | The argument is a double which is displayed in either normal decimal  notation or if the exponent is not close to zero, in exponential  notation. |
| x, X | The argument is an integer which is displayed in hexadecimal.  Lower\-case hexadecimal is used for %x and upper\-case is used  for %X |
| o | The argument is an integer which is displayed in octal. |
| s, z | The argument is either a zero\-terminated string that is displayed,  or a null pointer which is treated as an empty string. For  the %z type in C\-language interfaces, [sqlite3\_free()](c3ref/free.html) is invoked  on the string after it has been copied into the output. The %s and %z  substitutions are identical for the SQL printf() function, with  a NULL argument treated as an empty string.  The %s substitution is universal among printf functions, but  the %z substitution and safe treatment of null pointers  are SQLite enhancements, not found in other  printf() implementations. |
| c | For the C\-language interfaces, the argument is an integer which  is interpreted as a character. For the [format() SQL function](lang_corefunc.html#format) the  argument is a string from which the first character is extracted and  displayed. |
| p | The argument is a pointer which is displayed as a hexadecimal address.  Since the SQL language has no concept of a pointer, the %p substitution  for the [format() SQL function](lang_corefunc.html#format) works like %x. |
| n | The argument is a pointer to an integer. Nothing is displayed for  this substitution type. Instead, the integer to which the argument  points is overwritten with the number of characters in the generated  string that result from all format symbols to the left of the %n. |
| q, Q | The argument is a zero\-terminated string. The string is printed with  all single quote (') characters doubled so that the string can safely  appear inside an SQL string literal. The %Q substitution type also  puts single\-quotes on both ends of the substituted string.  If the argument  to %Q is a null pointer then the output is an unquoted "NULL". In other  words, a null pointer generates an SQL NULL, and a non\-null pointer generates  a valid SQL string literal. If the argument to %q is a null pointer  then no output is generated. Thus a null\-pointer to %q is the same as  an empty string.  For these substitutions, the precision is the number of bytes or  characters taken from the argument, not the number of bytes or characters that  are written into the output.    The %q and %Q substitutions are SQLite enhancements, not found in  most other printf() implementations. |
| w | This substitution works like %q except that it doubles all double\-quote  characters (") instead of single\-quotes, making the result suitable for  using with a double\-quoted identifier name in an SQL statement.    The %w substitution is an SQLite enhancements, not found in  most other printf() implementations. |



## 2\.2\. The Optional Length Field


The length of the argument value can be specified by one or more letters
that occur just prior to the substitution type letter. In SQLite, the
length only matter for integer types. The length is ignored for the
[format() SQL function](lang_corefunc.html#format) which always uses 64\-bit values. The following
table shows the length specifiers allowed by SQLite:






| Length Specifier | Meaning |
| --- | --- |
| *(default)* | An "int" or "unsigned int". 32\-bits on all modern systems. |
| l | A "long int" or "long unsigned int". Also 32\-bits on all modern systems. |
| ll | A "long long int" or "long long unsigned" or an "sqlite3\_int64" or  "sqlite3\_uint64" value. These are 64\-bit integers on all modern systems. |



Only the "ll" length modifier ever makes a difference for SQLite. And
it only makes a difference when using the C\-language interfaces.



## 2\.3\. The Optional Width Field


The width field specifies the minimum width of the substituted value in
the output. If the string or number that is written into the output is shorter
than the width, then the value is padded. Padding is on the left (the
value is right\-justified) by default. If the "\-" flag is used, then the
padding is on the right and the value is left\-justified.



The width is measured in bytes by default. However, if the "!" flag is
present then the width is in characters. This only makes a difference for
multi\-byte utf\-8 characters, and those only occur on string substitutions.



If the width is a single "\*" character instead of a number, then the
actual width value is read as an integer from the argument list. If the
value read is negative, then the absolute value is used for the width and
the value is left\-justified as if the "\-" flag were present.



If the value being substituted is larger than the width, then full value
is added to the output. In other words, the width is the minimum width of
the value as it is rendered in the output.



## 2\.4\. The Optional Precision Field


The precision field, if it is present, must follow the width separated
by a single "." character. If there is no width, then the "." that introduces
the precision immediately follows either the flags (if there are any) or
the initial "%".



For string substitutions %s, %z, %q, %Q, or %w the precision is the number
of byte or character used from the argument. The number is bytes by default but
is characters if the "!" flag is present. If there is no precision, then the
entire string is substituted. Examples: "%.3s" substitutes the first 3 bytes
of the argument string. "%!.3s" substitutes the first three characters of the
argument string.



For integer substitutions %d, %i, %x, %X, %o, and %p the precision specifies
minimum number of digits to display. Leading zeros are added if necessary, to
expand the output to the minimum number of digits.



For floating\-point substitutions %e, %E, and %f the precision specifies 
the number of digits to display to the right of the decimal point. With
the %g and %G, the precision is the total number of significant digits, rounded
up to 1 if the specified precision is 0\.



For the character substitution %c a precision N greater than 1 causes the
character to be repeated N times. This is a non\-standard extension found only
in SQLite.



If the precision is a single "\*" character instead of a number, then the
actual precision value is read as an integer from the argument list.



## 2\.5\. The Options Flags Field


Flags consist of zero or more characters that immediately follow the
"%" that introduces the substitution. The various flags and their meanings
are as follows:






| Flag | Meaning |
| --- | --- |
| **\-** | Left\-justify the value in the output. The default is to right\-justify. If the width is zero or is otherwise less than the length of the value being substituted, then there is no padding and the "\-" flag is a no\-op. |
| **\+** | For signed numeric substitutions, include a "\+" sign before positive numbers. A "\-" sign always appears before negative numbers regardless of flag settings. |
| *(space)* | For signed numeric substitutions, prepend a single space before positive numbers. |
| **0** | (The zero\-padding option) Prepend as many "0" characters to numeric substitutions as necessary to expand the value out to the specified width. If the width field is omitted, then this flag is a no\-op. Infinity and NaN (Not\-A\-Number) floating point values are normally rendered as "Inf" and "NaN", respectively, but with the zero\-padding option enabled they are rendered as "9\.0e\+999" and "null". In other words, with the zero\-padding option, floating\-point Infinity and NaN are rendered as valid SQL and JSON literals. |
| **\#** | This is the "alternate\-form\-1" flag. For %g and %G substitutions, this causes trailing zeros to be removed. This flag forces a decimal point to appear for all floating\-point substitutions. For %o, %x, and %X substitutions, the alternate\-form\-1 flag cause the value to be prepended with "0", "0x", or "0X", respectively. |
| **,** | The comma option causes comma separators to be added to the output of numeric substitutions (%d, %f, and similar) before every 3rd digits to the left of the decimal point. No commas are added for digits to the right of the decimal point. This can help humans to more easily discern the magnitude of large integer values. For example, the value 2147483647 would be rendered as "2147483647" using "%d" but would appear as "2,147,483,647" with "%,d". This flag is a non\-standard extension. |
| **!** | This is the "alternate\-form\-2 flag. For string substitutions, this flag causes the width and precision to be understand in terms of characters rather than bytes. For floating point substitutions, the alternate\-form\-2 flag increases the  maximum number of significant digits displayed from 16 to 26, forces the display of the decimal point and causes at least one digit to appear after the decimal point. The alternate\-form\-2 flag is a non\-standard extension that appears in no other printf() implementations, as far as we know. |



# 3\. Implementation And History



The core string formatting routine is the sqlite3VXPrintf() function found in the
[printf.c](https://sqlite.org/src/file/src/printf.c) source file. All the
various interfaces invoke (sometimes indirectly) this one core function.
The sqlite3VXPrintf() function began as code written by the first author
of SQLite ([Hipp](crew.html)) when he was a graduate student at Duke University in the
late 1980s. Hipp kept this printf() implementation in his personal toolbox until
he started working on SQLite in 2000\. The code was incorporated into the
SQLite source tree on [2000\-10\-08](https://sqlite.org/src/timeline?c=f9372072a6)
for SQLite version 1\.0\.9\.




The [Fossil Version Control System](https://www.fossil-scm.org/) uses its own
printf() implementation that is derived from an early version of the SQLite
printf() implementation, but those two implementations have since diverged.




The [sqlite3\_snprintf()](c3ref/mprintf.html) function has its buffer pointer and buffer size
arguments reversed from what is found in the standard C library snprintf()
routine. This is because there was no snprintf() routine in the
standard C library
when Hipp was first implementing his version, and he chose a different order
than the designers of the standard C library.



