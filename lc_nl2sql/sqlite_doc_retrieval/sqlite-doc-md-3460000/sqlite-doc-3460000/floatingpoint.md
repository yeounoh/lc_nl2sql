




Floating Point Numbers




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Floating Point Numbers


►
Table Of Contents
[1\. How SQLite Stores Numbers](#how_sqlite_stores_numbers)
[1\.1\. Floating\-Point Accuracy](#floating_point_accuracy)
[1\.2\. Floating Point Numbers](#floating_point_numbers)
[1\.2\.1\. Unrepresentable numbers](#unrepresentable_numbers)
[1\.2\.2\. Is it close enough?](#is_it_close_enough_)
[2\. Extensions For Dealing With Floating Point Numbers](#extensions_for_dealing_with_floating_point_numbers)
[2\.1\. The ieee754\.c Extension](#the_ieee754_c_extension)
[2\.1\.1\. The ieee754() function](#the_ieee754_function)
[2\.1\.2\. The ieee754\_mantissa() and ieee754\_exponent() functions](#the_ieee754_mantissa_and_ieee754_exponent_functions)
[2\.1\.3\. The ieee754\_from\_blob() and ieee754\_to\_blob() functions](#the_ieee754_from_blob_and_ieee754_to_blob_functions)
[2\.2\. The decimal.c Extension](#the_decimal_c_extension)




# 1\. How SQLite Stores Numbers



SQLite stores integer values in the 64\-bit 
[twos\-complement](https://en.wikipedia.org/wiki/Two%27s_complement)
format\&sup1\.
This gives a storage range of \-9223372036854775808 to \+9223372036854775807,
inclusive. Integers within this range are exact.





So\-called "REAL" or floating point values are stored in the
[IEEE 754](https://en.wikipedia.org/wiki/IEEE_754)
[Binary\-64](https://en.wikipedia.org/wiki/Double-precision_floating-point_format)
format\&sup1\.
This gives a range of positive values between approximately
1\.7976931348623157e\+308 and 4\.9406564584124654e\-324 with an equivalent
range of negative values. A binary64 can also be 0\.0 (and \-0\.0\), positive
and negative infinity and "NaN" or "Not\-a\-Number". Floating point
values are approximate.




Pay close attention to the last sentence in the previous paragraph:



> **Floating point values are approximate.**



If you need an exact answer, you should not use binary64 floating\-point
values, in SQLite or in any other product. This is not an SQLite limitation.
It is a mathematical limitation inherent in the design of floating\-point numbers.



—  
¹
Exception: The [R\-Tree extension](rtree.html) stores information as 32\-bit floating
point or integer values.



## 1\.1\. Floating\-Point Accuracy



SQLite promises to preserve the 15 most significant digits of a floating
point value. However, it makes no guarantees about the accuracy of
computations on floating point values, as no such guarantees are possible.
Performing math on floating\-point values introduces error.
For example, consider what happens if you attempt to subtract two floating\-point
numbers of similar magnitude:




> | 1152693165\.1106291898 |
> | --- |
> | \-1152693165\.1106280772 |
> | --- |
> | 0\.0000011126 |


The result shown above (0\.0000011126\) is the correct answer. But if you
do this computation using binary64 floating\-point, the answer you get is
0\.00000095367431640625 \- an error of about 14%. If you do many similar
computations as part of your program, the errors add up so that your final
result might be completely meaningless.



The error arises because only about the first 15 significant digits of
each number are stored accurately, and the first difference between the two numbers
being subtracted is in the 16th digit. 



## 1\.2\. Floating Point Numbers



The binary64 floating\-point format uses 64 bits per number. Hence there
are 1\.845e\+19 different possible floating point values. On the other hand
there are infinitely many real numbers in the range of 
1\.7977e\+308 and 4\.9407e\-324\. It follows then that binary64 cannot possibly
represent all possible real numbers within that range. Approximations are
required.




An IEEE 754 floating\-point value is an integer multiplied by a power
of two:




> M × 2E


The M value is the "mantissa" and E is the "exponent". Both
M and E are integers.



For Binary64, M is a 53\-bit integer and E is an 11\-bit integer that is
offset so that represents a range of values between \-1074 and \+972, inclusive.



*(NB: The usual description of IEEE 754 is more complex, and it is important
to understand the added complexity if you really want to appreciate the details,
merits, and limitations of IEEE 754\. However, the integer description shown
here, while not exactly right, is easier to understand and is sufficient for
the purposes of this article.)*


### 1\.2\.1\. Unrepresentable numbers


Not every decimal number with fewer than 16 significant digits can be
represented exactly as a binary64 number. In fact, most decimal numbers
with digits to the right of the decimal point lack an exact binary64
equivalent. For example, if you have a database column that is intended
to hold an item price in dollars and cents, the only cents value that
can be exactly represented are 0\.00, 0\.25, 0\.50, and 0\.75\. Any other
numbers to the right of the decimal point result in an approximation.
If you provide a "price" value of 47\.49, that number will be represented
in binary64 as:




> 6683623321994527 × 2\-47


Which works out to be:




> 47\.49000000000000198951966012828052043914794921875


That number is very close to 47\.49, but it is not exact. It is a little
too big. If we reduce M by one to 6683623321994526 so that we have the
next smaller possible binary64 value, we get:




> 47\.4899999999999948840923025272786617279052734375



This second number is too small.
The first number is closer to the desired value of 47\.49, so that is the
one that gets used. But it is not exact. Most decimal values work this
way in IEEE 754\. Remember the key point we made above:




> **Floating point values are approximate.**


If you remember nothing else about floating\-point values, 
please don't forget this one key idea.



### 1\.2\.2\. Is it close enough?


The precision provided by IEEE 754 Binary64 is sufficient for most computations.
For example, if "47\.49" represents a price and inflation is running
at 2% per year, then the price is going up by about 0\.0000000301 dollars per
second. The error in the recorded value of 47\.49 represents about 66 nanoseconds
worth of inflation. So if the 47\.49 price is exact
when you enter it, then the effects of inflation will cause the true value to
exactly equal the value actually stored
(47\.4900000000000019895196601282805204391479492187\) in less than 
one ten\-millionth of a second.
Surely that level of precision is sufficient for most purposes?



# 2\. Extensions For Dealing With Floating Point Numbers



## 2\.1\. The ieee754\.c Extension


The ieee754 extension converts a floating point number between its
binary64 representation and the M×2E format.
In other words in the expression:




> F \= M × 2E


The ieee754 extension converts between F and (M,E) and back again.



The ieee754 extension is not part of the [amalgamation](amalgamation.html), but it is included
by default in the [CLI](cli.html). If you want to include the ieee754 extension in your
application, you will need to compile and load it separately.




### 2\.1\.1\. The ieee754() function


The ieee754(F) SQL function takes a single floating\-point argument
as its input and returns a string that looks like this:




> 'ieee754(M,E)'


Except that the M and E are replaced by the mantissa and exponent of the
floating point number. For example:




```
sqlite> .mode box
sqlite> SELECT ieee754(47.49) AS x;
┌───────────────────────────────┐
│               x               │
├───────────────────────────────┤
│ ieee754(6683623321994527,-47) │
└───────────────────────────────┘

```


Going in the other direction, the 2\-argument version of ieee754() takes
the M and E values and converts them into the corresponding F value:




```
sqlite> select ieee754(6683623321994527,-47) as x;
┌───────┐
│   x   │
├───────┤
│ 47.49 │
└───────┘

```


### 2\.1\.2\. The ieee754\_mantissa() and ieee754\_exponent() functions


The text output of the one\-argument form of ieee754() is great for human
readability, but it is awkward to use as part of a larger expression. Hence
the ieee754\_mantissa() and ieee754\_exponent() routines were added to return
the M and E values corresponding to their single argument F
value.
For example:




```
sqlite> .mode box
sqlite> SELECT ieee754_mantissa(47.49) AS M, ieee754_exponent(47.49) AS E;
┌──────────────────┬─────┐
│        M         │  E  │
├──────────────────┼─────┤
│ 6683623321994527 │ -47 │
└──────────────────┴─────┘

```


### 2\.1\.3\. The ieee754\_from\_blob() and ieee754\_to\_blob() functions


The ieee754\_to\_blob(F) SQL function converts the floating point number F
into an 8\-byte BLOB that is the big\-endian binary64 encoding of that number.
The ieee754\_from\_blob(B) function goes the other way, converting an 8\-byte
blob into the floating\-point value that the binary64 encoding represents.



So, for example, if you read
[on
Wikipedia](https://en.wikipedia.org/wiki/Double-precision_floating-point_format) that the encoding for the minimum positive binary64 value is
0x0000000000000001, then you can find the corresponding floating point value
like this:




```
sqlite> .mode box
sqlite> SELECT ieee754_from_blob(x'0000000000000001') AS F;
┌───────────────────────┐
│           F           │
├───────────────────────┤
│ 4.94065645841247e-324 │
└───────────────────────┘

```

Or go the other way:




```
sqlite> .mode box
sqlite> SELECT quote(ieee754_to_blob(4.94065645841247e-324)) AS binary64;
┌─────────────────────┐
│      binary64       │
├─────────────────────┤
│ X'0000000000000001' │
└─────────────────────┘

```


## 2\.2\. The decimal.c Extension


The decimal extension provides arbitrary\-precision decimal arithmetic on
numbers stored as text strings. Because the numbers are stored to arbitrary
precision and as text, no approximations are needed. Computations can be
done exactly.



The decimal extension is not (currently) part of the SQLite [amalgamation](amalgamation.html).
However, it is included in the [CLI](cli.html).



There are three math functions available:






* decimal\_add(A,B)
* decimal\_sub(A,B)
* decimal\_mul(A,B)
* decimal\_pow2(N)


The first three functions respectively add, subtract, and multiply their arguments
and return a new text string that is the decimal representation of the result. The
argument is interpreted as text.
There is no division operator because decimal division often does not generate
a finite decimal result.



The decimal\_pow2(N) function returns 2\.0 raised to the N\-th power where N is an
integer between \-20000 and \+20000\.



Use the decimal\_cmp(A,B) to compare two decimal values. The result will
be negative, zero, or positive if A is less than, equal to, or greater than B,
respectively.



The decimal\_sum(X) function is an aggregate, like the built\-in
[sum() aggregate function](lang_aggfunc.html#sumunc), except that decimal\_sum() computes its result
to arbitrary precision and is therefore precise.



The decimal extension provides the "decimal" collating sequences
that compares decimal text strings in numeric order.



The decimal(X) and decimal\_exp(X) generate a decimal representation for input X.
The decimal\_exp(X) function returns the result in exponential notation (with a "e\+NN"
at the end) and decimal(X) returns a pure decimal (without the "e\+NN"). If the input
X is a floating point value, it is expanded to its exact decimal equivalent. For
example:




```
sqlite> .mode qbox
sqlite> select decimal(47.49);
┌──────────────────────────────────────────────────────┐
│                    decimal(47.49)                    │
├──────────────────────────────────────────────────────┤
│ '47.49000000000000198951966012828052043914794921875' │
└──────────────────────────────────────────────────────┘

```

