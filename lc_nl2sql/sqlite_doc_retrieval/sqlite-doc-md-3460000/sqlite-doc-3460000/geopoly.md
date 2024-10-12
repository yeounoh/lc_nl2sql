




The Geopoly Interface To The SQLite R\*Tree Module




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Geopoly Interface To The SQLite R\*Tree Module


►
Table Of Contents
[1\. Overview](#overview)
[1\.1\. GeoJSON](#geojson)
[1\.2\. Binary storage format](#binary_storage_format)
[2\. Using The Geopoly Extension](#using_the_geopoly_extension)
[2\.1\. Queries](#queries)
[3\. Special Functions](#special_functions)
[3\.1\. The geopoly\_overlap(P1,P2\) Function](#the_geopoly_overlap_p1_p2_function)
[3\.2\. The geopoly\_within(P1,P2\) Function](#the_geopoly_within_p1_p2_function)
[3\.3\. The geopoly\_area(P) Function](#the_geopoly_area_p_function)
[3\.4\. The geopoly\_blob(P) Function](#the_geopoly_blob_p_function)
[3\.5\. The geopoly\_json(P) Function](#the_geopoly_json_p_function)
[3\.6\. The geopoly\_svg(P,...) Function](#the_geopoly_svg_p_function)
[3\.7\. The geopoly\_bbox(P) and geopoly\_group\_bbox(P) Functions](#the_geopoly_bbox_p_and_geopoly_group_bbox_p_functions)
[3\.8\. The geopoly\_contains\_point(P,X,Y) Function](#the_geopoly_contains_point_p_x_y_function)
[3\.9\. The geopoly\_xform(P,A,B,C,D,E,F) Function](#the_geopoly_xform_p_a_b_c_d_e_f_function)
[3\.10\. The geopoly\_regular(X,Y,R,N) Function](#the_geopoly_regular_x_y_r_n_function)
[3\.11\. The geopoly\_ccw(J) Function](#the_geopoly_ccw_j_function)
[4\. Implementation Details](#implementation_details)
[4\.1\. Binary Encoding of Polygons](#binary_encoding_of_polygons)
[4\.2\. Shadow Tables](#shadow_tables)




# 1\. Overview



The Geopoly module is an alternative interface to the [R\-Tree extension](rtree.html) that uses
the [GeoJSON](http://geojson.org) notation
([RFC\-7946](https://tools.ietf.org/html/rfc7946)) to describe two\-dimensional
polygons. Geopoly includes functions for detecting when one polygon is
contained within or overlaps with another, for computing the
area enclosed by a polygon, for doing linear transformations of polygons,
for rendering polygons as
[SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics), and other
similar operations.




The source code for Geopoly is included in the [amalgamation](amalgamation.html). However,
depending on configuration options and the a particular version of SQLite
you are using, the Geopoly extension may or may not be enabled by default.
To ensure that Geopoly is enabled for your build, 
add the [\-DSQLITE\_ENABLE\_GEOPOLY\=1](compile.html#enable_geopoly) compile\-time option.




Geopoly operates on "simple" polygons \- that is, polygons for which
the boundary does not intersect itself. Geopoly thus extends the capabilities
of the [R\-Tree extension](rtree.html) which can only deal with rectangular areas.
On the other hand, the [R\-Tree extension](rtree.html) is
able to handle between 1 and 5 coordinate dimensions, whereas Geopoly is restricted
to 2\-dimensional shapes only.




Each polygon in the Geopoly module can be associated with an arbitrary
number of auxiliary data fields.



## 1\.1\. GeoJSON


The [GeoJSON standard](https://tools.ietf.org/html/rfc7946) is syntax for
exchanging geospatial information using JSON. GeoJSON is a rich standard
that can describe nearly any kind of geospatial content.



The Geopoly module only understands
a small subset of GeoJSON, but a critical subset. 
In particular, GeoJSON understands
the JSON array of vertexes that describes a simple polygon.



A polygon is defined by its vertexes.
Each vertex is a JSON array of two numeric values which are the
X and Y coordinates of the vertex.
A polygon is a JSON array of at least four of these vertexes, 
and hence is an array of arrays.
The first and last vertex in the array must be the same.
The polygon follows the right\-hand rule: When tracing a line from
one vertex to the next, the area to the right of the line is outside
of the polygon and the area to the left is inside the polygon.
In other words, the net rotation of the vertexes is counter\-clockwise.




For example, the following JSON describes an isosceles triangle, sitting
on the X axis and with an area of 0\.5:




```
[[0,0],[1,0],[0.5,1],[0,0]]

```


A triangle has three vertexes, but the GeoJSON description of the triangle
has 4 vertexes because the first and last vertex are duplicates.



## 1\.2\. Binary storage format



Internally, Geopoly stores polygons in a binary format \- an SQL BLOB.
Details of the binary format are given below.
All of the Geopoly interfaces are able to accept polygons in either the
GeoJSON format or in the binary format.



# 2\. Using The Geopoly Extension



A geopoly table is created as follows:




```
CREATE VIRTUAL TABLE newtab USING geopoly(a,b,c);

```


The statement above creates a new geopoly table named "newtab".
Every geopoly table contains a built\-in integer "rowid" column
and a "\_shape" column that contains
the polygon associated with that row of the table.
The example above also defines three auxiliary data columns 
named "a", "b", and "c" that can store whatever additional
information the application needs to associate
with each polygon. If there is no need to store auxiliary
information, the list of auxiliary columns can be omitted.




Store new polygons in the table using ordinary INSERT statements:




```
INSERT INTO newtab(_shape) VALUES('[[0,0],[1,0],[0.5,1],[0,0]]');

```


UPDATE and DELETE statements work similarly.



## 2\.1\. Queries



To query the geopoly table using an indexed geospatial search, 
use one of the functions geopoly\_overlap()
or geopoly\_within() as a boolean function in the WHERE clause,
with the "\_shape" column as the first argument to the function.
For example:




```
SELECT * FROM newtab WHERE geopoly_overlap(_shape, $query_polygon);

```


The previous example will return every row for which the \_shape
overlaps the polygon in the $query\_polygon parameter. The
geopoly\_within() function works similarly, but only returns rows for
which the \_shape is completely contained within $query\_polygon.




Queries (and also DELETE and UPDATE statements) in which the WHERE
clause contains a bare geopoly\_overlap() or geopoly\_within() function
make use of the underlying R\*Tree data structures for a fast lookup that
only has to examine a subset of the rows in the table. The number of
rows examines depends, of course, on the size of the $query\_polygon.
Large $query\_polygons will normally need to look at more rows than small
ones.




Queries against the rowid of a geopoly table are also very quick, even
for tables with a vast number of rows.
However, none of the auxiliary data columns are indexes, and so queries
against the auxiliary data columns will involve a full table scan.



# 3\. Special Functions



The geopoly module defines several new SQL functions that are useful for
dealing with polygons. All polygon arguments to these functions can be
either the GeoJSON format or the internal binary format.




## 3\.1\. The geopoly\_overlap(P1,P2\) Function



If P1 and P2 are both polygons, then the geopoly\_overlap(P1,P2\) function returns
a non\-zero integer if there is any overlap between P1 and P2, or it returns
zero if P1 and P2 completely disjoint.
If either P1 or P2 is not a polygon, this routine returns NULL.




The geopoly\_overlap(P1,P2\) function is special in that the geopoly virtual
table knows how to use R\*Tree indexes to optimize queries in which the 
WHERE clause uses geopoly\_overlap() as a boolean function. Only the
geopoly\_overlap(P1,P2\) and geopoly\_within(P1,P2\) functions have this
capability.




## 3\.2\. The geopoly\_within(P1,P2\) Function



If P1 and P2 are both polygons, then the geopoly\_within(P1,P2\) function returns
a non\-zero integer if P1 is completely contained within P2, or it returns zero
if any part of P1 is outside of P2\. If P1 and P2 are the same polygon, this routine
returns non\-zero.
If either P1 or P2 is not a polygon, this routine returns NULL.




The geopoly\_within(P1,P2\) function is special in that the geopoly virtual
table knows how to use R\*Tree indexes to optimize queries in which the 
WHERE clause uses geopoly\_within() as a boolean function. Only the
geopoly\_within(P1,P2\) and geopoly\_overlap(P1,P2\) functions have this
capability.




## 3\.3\. The geopoly\_area(P) Function



If P is a polygon, then geopoly\_area(P) returns the area enclosed by
that polygon. If P is not a polygon, geopoly\_area(P) returns NULL.




## 3\.4\. The geopoly\_blob(P) Function



If P is a polygon, then geopoly\_blob(P) returns the binary encoding
of that polygon as a BLOB.
If P is not a polygon, geopoly\_blob(P) returns NULL.




## 3\.5\. The geopoly\_json(P) Function



If P is a polygon, then geopoly\_json(P) returns the GeoJSON representation
of that polygon as a TEXT string.
If P is not a polygon, geopoly\_json(P) returns NULL.




## 3\.6\. The geopoly\_svg(P,...) Function



If P is a polygon, then geopoly\_svg(P,...) returns a text string which is a
[Scalable Vector Graphics (SVG)](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics)
representation of that polygon. If there is more one argument, then second
and subsequent arguments are added as attributes to each SVG glyph. For example:




```
SELECT geopoly_svg($polygon,'class="poly"','style="fill:blue;"');

```


If P is not a polygon, geopoly\_svg(P,...) returns NULL.




Note that geopoly uses a traditional right\-handed cartesian coordinate system
with the origin at the lower left, whereas SVG uses a left\-handed coordinate
system with the origin at the upper left. The geopoly\_svg() routine makes no
attempt to transform the coordinate system, so the displayed images are shown
in mirror image and rotated. If that is undesirable, the geopoly\_xform() routine
can be used to transform the output from cartesian to SVG coordinates prior to
passing the polygons into geopoly\_svg().




## 3\.7\. The geopoly\_bbox(P) and geopoly\_group\_bbox(P) Functions



If P is a polygon, then geopoly\_bbox(P) returns a new polygon that is
the smallest (axis\-aligned) rectangle completely enclosing P.
If P is not a polygon, geopoly\_bbox(P) returns NULL.




The geopoly\_group\_bbox(P) function is an aggregate version of geopoly\_bbox(P).
The geopoly\_group\_bbox(P) function returns the smallest rectangle that will
enclose all P values seen during aggregation.




## 3\.8\. The geopoly\_contains\_point(P,X,Y) Function



If P is a polygon, then geopoly\_contains\_point(P,X,Y) returns a 
non\-zero integer if and only
if the coordinate X,Y is inside or on the boundary of the polygon P.
If P is not a polygon, geopoly\_contains\_point(P,X,Y) returns NULL.




## 3\.9\. The geopoly\_xform(P,A,B,C,D,E,F) Function



The geopoly\_xform(P,A,B,C,D,E,F) function returns a new polygon that is an
affine transformation of the polygon P and where the transformation
is defined by values A,B,C,D,E,F. If P is not a valid polygon, this
routine returns NULL.




The transformation converts each vertex of the polygon according to the
following formula:




```
x1 = A*x0 + B*y0 + E
y1 = C*x0 + D*y0 + F

```


So, for example, to move a polygon by some amount DX, DY without changing
its shape, use:




```
geopoly_xform($polygon, 1, 0, 0, 1, $DX, $DY)

```


To rotate a polygon by R radians around the point 0, 0:




```
geopoly_xform($polygon, cos($R), sin($R), -sin($R), cos($R), 0, 0)

```


Note that a transformation that flips the polygon might cause the
order of vertexes to be reversed. In other words, the transformation
might cause the vertexes to circulate in clockwise order instead of
counter\-clockwise. This can be corrected by sending the result
through the [geopoly\_ccw()](geopoly.html#ccw) function after transformation.





## 3\.10\. The geopoly\_regular(X,Y,R,N) Function



The geopoly\_regular(X,Y,R,N) function returns a convex, simple, regular,
equilateral, equiangular polygon with N sides, centered at X,Y, and with
a circumradius of R. Or, if R is negative or if N is less than 3, the
function returns NULL. The N value is capped at 1000 so that the routine
will never render a polygon with more than 1000 sides even if the N value
is larger than 1000\.




As an example, the following graphic:




> 3
>  4
>  5
>  6
>  7
>  8
>  10
>  12
>  16
>  20


Was generated by this script:




```
SELECT '<svg width="600" height="300">';
WITH t1(x,y,n,color) AS (VALUES
   (100,100,3,'red'),
   (200,100,4,'orange'),
   (300,100,5,'green'),
   (400,100,6,'blue'),
   (500,100,7,'purple'),
   (100,200,8,'red'),
   (200,200,10,'orange'),
   (300,200,12,'green'),
   (400,200,16,'blue'),
   (500,200,20,'purple')
)
SELECT
   geopoly_svg(geopoly_regular(x,y,40,n),
        printf('style="fill:none;stroke:%s;stroke-width:2"',color))
   || printf(' <text x="%d" y="%d" alignment-baseline="central" text-anchor="middle">%d</text>',x,y+6,n)
  FROM t1;
SELECT '</svg>';

```


## 3\.11\. The geopoly\_ccw(J) Function


The geopoly\_ccw(J) function returns the polygon J with counter\-clockwise (CCW) rotation.




[RFC\-7946](https://tools.ietf.org/html/rfc7946) requires that polygons use CCW rotation.
But the spec also observes that many legacy GeoJSON files do not following the spec and
contain polygons with clockwise (CW) rotation. The geopoly\_ccw() function is useful for
applications that are reading legacy GeoJSON scripts. If the input to geopoly\_ccw() is
a correctly\-formatted polygon, then no changes are made. However, if the circulation of
the input polygon is backwards, then geopoly\_ccw() reverses the circulation order so that
it conforms to the spec and so that it will work correctly with the Geopoly module.





# 4\. Implementation Details


The geopoly module is an extension to the [R\-Tree extension](rtree.html). Geopoly
uses the same underlying logic and shadow tables as the [R\-Tree extension](rtree.html).
Geopoly merely presents a different interface, and provides some extra logic
to compute polygon decoding, overlap, and containment.



## 4\.1\. Binary Encoding of Polygons



Geopoly stores all polygons internally using a binary format. A binary
polygon consists of a 4\-byte header following by an array of coordinate
pairs in which each dimension of each coordinate is a 32\-bit floating point
number.




The first byte of the header is a flag byte. The least significant bit
of the flag byte determines whether the coordinate pairs that follow the
header are stored big\-endian or little\-endian. A value of 0 for the least
significant bit means big\-endian and a value of 1 means little endian.
Other bits of the first byte in the header are reserved for future expansion.




The next three bytes in the header record the number of vertexes in the polygon
as a big\-endian integer. Thus there is an upper bound of about 16 million
vertexes per polygon.




Following the header is the array of coordinate pairs. Each coordinate is
a 32\-bit floating point number. The use of 32\-bit floating point values for
coordinates means that any point on the earth's surface can be mapped with
a resolution of approximately 2\.5 meters. Higher resolutions are of course
possible if the map is restricted to a single continent or country.
Note that the resolution of coordinates in the geopoly module is similar
in magnitude to daily movement of points on the earth's surface due to
tidal forces.




The list of coordinates in the binary format contains no redundancy. 
The last coordinate is not a repeat of the first as it is with GeoJSON. 
Hence, there is always one fewer coordinate pair in the binary representation of
a polygon compared to the GeoJSON representation.



## 4\.2\. Shadow Tables



The geopoly module is built on top of the [R\-Tree extension](rtree.html) and uses the
same underlying shadow tables and algorithms. For indexing purposes, each
polygon is represented in the shadow tables as a rectangular bounding box.
The underlying R\-Tree implementation uses bounding boxes to limit the search
space. Then the geoploy\_overlap() and/or geopoly\_within() routines further
refine the search to the exact answer.


*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


