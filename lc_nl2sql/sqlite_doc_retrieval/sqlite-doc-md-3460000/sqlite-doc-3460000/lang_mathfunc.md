




Built\-In Mathematical SQL Functions




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Built\-In Mathematical SQL Functions


# 1\. Overview


The math functions shown below are a subgroup of
[scalar functions](lang_corefunc.html) that are built into the
[SQLite amalgamation source file](amalgamation.html) but are only active
if the amalgamation is compiled using the
[\-DSQLITE\_ENABLE\_MATH\_FUNCTIONS](compile.html#enable_math_functions) compile\-time option.



The arguments to math functions can be integers, floating\-point numbers,
or strings or blobs that look like integers or real numbers. If any argument
is NULL or is a string or blob that is not readily converted into a number,
then the function will return NULL.
These functions also return NULL for domain errors, such as trying to
take the square root of a negative number, or compute the arccosine of a
value greater than 1\.0 or less than \-1\.0\.



The values returned by these functions are often approximations.
For example, the [pi()](lang_mathfunc.html#pi) function returns 
3\.141592653589793115997963468544185161590576171875 which 
is about 1\.22465e\-16 too small, but it is the closest approximation available
for IEEE754 doubles.



* [acos(X)](lang_mathfunc.html#acos)
* [acosh(X)](lang_mathfunc.html#acosh)
* [asin(X)](lang_mathfunc.html#asin)
* [asinh(X)](lang_mathfunc.html#asinh)
* [atan(X)](lang_mathfunc.html#atan)
* [atan2(Y,X)](lang_mathfunc.html#atan2)
* [atanh(X)](lang_mathfunc.html#atanh)
* [ceil(X)](lang_mathfunc.html#ceil)
* [ceiling(X)](lang_mathfunc.html#ceil)
* [cos(X)](lang_mathfunc.html#cos)
* [cosh(X)](lang_mathfunc.html#cosh)
* [degrees(X)](lang_mathfunc.html#degrees)
* [exp(X)](lang_mathfunc.html#exp)
* [floor(X)](lang_mathfunc.html#floor)
* [ln(X)](lang_mathfunc.html#ln)
* [log(B,X)](lang_mathfunc.html#log)
* [log(X)](lang_mathfunc.html#log)
* [log10(X)](lang_mathfunc.html#log)
* [log2(X)](lang_mathfunc.html#log2)
* [mod(X,Y)](lang_mathfunc.html#mod)
* [pi()](lang_mathfunc.html#pi)
* [pow(X,Y)](lang_mathfunc.html#pow)
* [power(X,Y)](lang_mathfunc.html#pow)
* [radians(X)](lang_mathfunc.html#radians)
* [sin(X)](lang_mathfunc.html#sin)
* [sinh(X)](lang_mathfunc.html#sinh)
* [sqrt(X)](lang_mathfunc.html#sqrt)
* [tan(X)](lang_mathfunc.html#tan)
* [tanh(X)](lang_mathfunc.html#tanh)
* [trunc(X)](lang_mathfunc.html#trunc)





# 2\. Descriptions of built\-in scalar SQL math functions




**acos(*X*)**


 Return the arccosine of X. The result is in radians.




**acosh(*X*)**


 Return the hyperbolic arccosine of X.




**asin(*X*)**


 Return the arcsine of X. The result is in radians.




**asinh(*X*)**


 Return the hyperbolic arcsine of X.




**atan(*X*)**


 Return the arctangent of X. The result is in radians.




**atan2(*Y*,*X*)**


 Return the arctangent of Y/X. The result is in radians. The
 result is placed into correct quadrant depending on the signs
 of X and Y.




**atanh(*X*)**


 Return the hyperbolic arctangent of X.




**ceil(*X*)**


 Return the first representable integer value greater than or equal to X.
 For positive values of X, this routine rounds away from zero.
 For negative values of X, this routine rounds toward zero.




**cos(*X*)**


 Return the cosine of X. X is in radians.




**cosh(*X*)**


 Return the hyperbolic cosine of X.




**degrees(*X*)**


 Convert value X from radians into degrees.




**exp(*X*)**


 Compute *e* (Euler's number, approximately 2\.71828182845905\) raised
 to the power X.




**floor(*X*)**


 Return the first representable integer value less than or equal to X.
 For positive numbers, this function rounds toward zero.
 For negative numbers, this function rounds away from zero.




**ln(*X*)**


 Return the natural logarithm of X.




**log(*X*)  
log10(*X*)  
log(*B*,*X*)**


 Return the base\-10 logarithm for X. Or, for the two\-argument version,
 return the base\-B logarithm of X.
 
 Compatibility note: SQLite works like PostgreSQL in that the log() function
 computes a base\-10 logarithm. Most other SQL database engines compute a
 natural logarithm for log(). In the two\-argument version of log(B,X), the
 first argument is the base and the second argument is the operand. This is
 the same as in PostgreSQL and MySQL, but is reversed from SQL Server which
 uses the second argument as the base and the first argument as the operand.






**log2(*X*)**


 Return the logarithm base\-2 for the number X.




**mod(*X*,*Y*)**


 Return the remainder after dividing X by Y. This is similar to the '%'
 operator, except that it works for non\-integer arguments.




**pi()**


 Return an approximation for π.




**pow(*X*,*Y*)  
power(*X*,*Y*)**


 Compute X raised to the power Y.




**radians(*X*)**


 Convert X from degrees into radians.




**sin(*X*)**


 Return the sine of X. X is in radians.




**sinh(*X*)**


 Return the hyperbolic sine of X.




**sqrt(*X*)**


 Return the square root of X. NULL is returned if X is negative.




**tan(*X*)**


 Return the tangent of X. X is in radians.




**tanh(*X*)**


 Return the hyperbolic tangent of X.




**trunc(*X*)**


 Return the representable integer in between X and 0 (inclusive)
 that is furthest away from zero. Or, in other words, return the
 integer part of X, rounding toward zero.
 The trunc() function is similar to [ceiling(X)](lang_mathfunc.html#ceil) and [floor(X)](lang_mathfunc.html#floor) except
 that it always rounds toward zero whereas ceiling(X) and floor(X) round
 up and down, respectively.




*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 




