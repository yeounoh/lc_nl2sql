




The SQLite Query Optimizer Overview




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The SQLite Query Optimizer Overview


►
Table Of Contents
[1\. Introduction](#introduction)
[2\. WHERE Clause Analysis](#where_clause_analysis)
[2\.1\. Index Term Usage Examples](#index_term_usage_examples)
[3\. The BETWEEN Optimization](#the_between_optimization)
[4\. OR Optimizations](#or_optimizations)
[4\.1\. Converting OR\-connected constraint into an IN operator](#converting_or_connected_constraint_into_an_in_operator)
[4\.2\. Evaluating OR constraints separately and taking the UNION of the result](#evaluating_or_constraints_separately_and_taking_the_union_of_the_result)
[5\. The LIKE Optimization](#the_like_optimization)
[6\. The Skip\-Scan Optimization](#the_skip_scan_optimization)
[7\. Joins](#joins)
[7\.1\. Manual Control Of Join Order](#manual_control_of_join_order)
[7\.1\.1\. Manual Control Of Query Plans Using SQLITE\_STAT Tables](#manual_control_of_query_plans_using_sqlite_stat_tables)
[7\.1\.2\. Manual Control of Query Plans using CROSS JOIN](#manual_control_of_query_plans_using_cross_join)
[8\. Choosing Between Multiple Indexes](#choosing_between_multiple_indexes)
[8\.1\. Disqualifying WHERE Clause Terms using Unary\-"\+"](#disqualifying_where_clause_terms_using_unary_)
[8\.2\. Range Queries](#range_queries)
[9\. Covering Indexes](#covering_indexes)
[10\. ORDER BY Optimizations](#order_by_optimizations)
[10\.1\. Partial ORDER BY via Index](#partial_order_by_via_index)
[11\. Subquery Flattening](#subquery_flattening)
[12\. Subquery Co\-routines](#subquery_co_routines)
[12\.1\. Using Co\-routines to Defer Work until after the Sorting](#using_co_routines_to_defer_work_until_after_the_sorting)
[13\. The MIN/MAX Optimization](#the_min_max_optimization)
[14\. Automatic Query\-Time Indexes](#automatic_query_time_indexes)
[14\.1\. Hash Joins](#hash_joins)
[15\. The WHERE\-Clause Push\-Down Optimization](#the_where_clause_push_down_optimization)
[16\. The OUTER JOIN Strength Reduction Optimization](#the_outer_join_strength_reduction_optimization)
[17\. The Omit OUTER JOIN Optimization](#the_omit_outer_join_optimization)
[18\. The Constant Propagation Optimization](#the_constant_propagation_optimization)




# 1\. Introduction



 This document provides an overview of how the query planner and optimizer
 for SQLite works.





 Given a single SQL statement, there might be dozens, hundreds, or even
 thousands of ways to implement that statement, depending on the complexity
 of the statement itself and of the underlying database schema. The 
 task of the query planner is to select the algorithm that minimizes
 disk I/O and CPU overhead.





 Additional background information is available in the
 [indexing tutorial](queryplanner.html) document.
 The [Next Generation Query Planner](queryplanner-ng.html) document provides more detail on
 how the [join order](optoverview.html#joins) is chosen.






# 2\. WHERE Clause Analysis



 Prior to analysis, the following transformations are made
 to shift all join constraints into the WHERE clause:






* All NATURAL joins are converted into joins with a USING clause.
* All USING clauses (including ones created by the previous step)
 are converted into equivalent ON clauses.
* All ON clauses (include ones created by the previous step)
 are added as new conjuncts (AND\-connected terms) in the WHERE clause.



 SQLite makes no distinction between join constraints that occur in the
 WHERE clause and constraints in the ON clause of an inner join, since that
 distinction does not affect the outcome. However, there is
 a difference between ON clause constraints and WHERE clause constraints for
 outer joins. Therefore, when SQLite moves an ON clause constraint from an
 outer join over to the WHERE clause it adds special tags to the Abstract
 Syntax Tree (AST) to indicate that the constraint came from an outer join
 and from which outer join it came. There is no way to add those tags in
 pure SQL text. Hence, the SQL input must use ON clauses on outer joins.
 But in the internal AST, all constraints are part of the WHERE clause,
 because having everything in one place simplifies processing.




 After all constraints have been shifted into the WHERE clause,
 The WHERE clause is broken up into conjuncts (hereafter called
 "terms"). In other words, the WHERE clause is broken up into pieces
 separated from the others by an AND operator.
 If the WHERE clause is composed of constraints separated by the OR
 operator (disjuncts) then the entire clause is considered to be a single "term"
 to which the [OR\-clause optimization](#or_opt) is applied.




 All terms of the WHERE clause are analyzed to see if they can be
 satisfied using indexes.
 To be usable by an index a term must usually be of one of the following
 forms:


> ```
> 
>   column = expression
>   column IS expression
>   column > expression
>   column >= expression
>   column < expression
>   column <= expression
>   expression = column
>   expression IS column
>   expression > column
>   expression >= column
>   expression < column
>   expression <= column
>   column IN (expression-list)
>   column IN (subquery)
>   column IS NULL
>   column LIKE pattern
>   column GLOB pattern
> 
> ```





 If an index is created using a statement like this:




```
CREATE INDEX idx_ex1 ON ex1(a,b,c,d,e,...,y,z);

```


 Then the index might be used if the initial columns of the index
 (columns a, b, and so forth) appear in WHERE clause terms.
 The initial columns of the index must be used with
 the **\=** or **IN** or **IS** operators. 
 The right\-most column that is used can employ inequalities. 
 For the right\-most
 column of an index that is used, there can be up to two inequalities
 that must sandwich the allowed values of the column between two extremes.




 It is not necessary for every column of an index to appear in a
 WHERE clause term in order for that index to be used. 
 However, there cannot be gaps in the columns of the index that are used.
 Thus for the example index above, if there is no WHERE clause term
 that constrains column c, then terms that constrain columns a and b can
 be used with the index but not terms that constrain columns d through z.
 Similarly, index columns will not normally be used (for indexing purposes)
 if they are to the right of a 
 column that is constrained only by inequalities.
 (See the [skip\-scan optimization](optoverview.html#skipscan) below for the exception.)




 In the case of [indexes on expressions](expridx.html), whenever the word "column" is
 used in the foregoing text, one can substitute "indexed expression"
 (meaning a copy of the expression that appears in the [CREATE INDEX](lang_createindex.html)
 statement) and everything will work the same.
 




## 2\.1\. Index Term Usage Examples



 For the index above and WHERE clause like this:




```
... WHERE a=5 AND b IN (1,2,3) AND c IS NULL AND d='hello'

```


 The first four columns a, b, c, and d of the index would be usable since
 those four columns form a prefix of the index and are all bound by
 equality constraints.




 For the index above and WHERE clause like this:




```
... WHERE a=5 AND b IN (1,2,3) AND c>12 AND d='hello'

```


 Only columns a, b, and c of the index would be usable. The d column
 would not be usable because it occurs to the right of c and c is
 constrained only by inequalities.




 For the index above and WHERE clause like this:




```
... WHERE a=5 AND b IN (1,2,3) AND d='hello'

```


 Only columns a and b of the index would be usable. The d column
 would not be usable because column c is not constrained and there can
 be no gaps in the set of columns that usable by the index.




 For the index above and WHERE clause like this:




```
... WHERE b IN (1,2,3) AND c NOT NULL AND d='hello'

```


 The index is not usable at all because the left\-most column of the
 index (column "a") is not constrained. Assuming there are no other
 indexes, the query above would result in a full table scan.




 For the index above and WHERE clause like this:




```
... WHERE a=5 OR b IN (1,2,3) OR c NOT NULL OR d='hello'

```


 The index is not usable because the WHERE clause terms are connected
 by OR instead of AND. This query would result in a full table scan.
 However, if three additional indexes where added that contained columns
 b, c, and d as their left\-most columns, then the
 [OR\-clause optimization](#or_opt) might apply.





# 3\. The BETWEEN Optimization



 If a term of the WHERE clause is of the following form:


> ```
> 
>   expr1 BETWEEN expr2 AND expr3
> 
> ```





 Then two "virtual" terms are added as follows:


> ```
> 
>   expr1 >= expr2 AND expr1 <= expr3
> 
> ```





 Virtual terms are used for analysis only and do not cause any byte\-code
 to be generated.
 If both virtual terms end up being used as constraints on an index,
 then the original BETWEEN term is omitted and the corresponding test
 is not performed on input rows.
 Thus if the BETWEEN term ends up being used as an index constraint
 no tests are ever performed on that term.
 On the other hand, the
 virtual terms themselves never causes tests to be performed on
 input rows.
 Thus if the BETWEEN term is not used as an index constraint and
 instead must be used to test input rows, the *expr1* expression is
 only evaluated once.




# 4\. OR Optimizations



 WHERE clause constraints that are connected by OR instead of AND can
 be handled in two different ways.



## 4\.1\. Converting OR\-connected constraint into an IN operator



 If a term consists of multiple subterms containing a common column
 name and separated by OR, like this:


> ```
> 
>   column = expr1 OR column = expr2 OR column = expr3 OR ...
> 
> ```





 Then that term is rewritten as follows:


> ```
> 
>   column IN (expr1,expr2,expr3,...)
> 
> ```





 The rewritten term then might go on to constrain an index using the
 normal rules for **IN** operators. Note that *column* must be
 the same column in every OR\-connected subterm,
 although the column can occur on either the left or the right side of
 the **\=** operator.



## 4\.2\. Evaluating OR constraints separately and taking the UNION of the result



 If and only if the previously described conversion of OR to an IN operator
 does not work, the second OR\-clause optimization is attempted.
 Suppose the OR clause consists of multiple subterms as follows:


> ```
> 
>   expr1 OR expr2 OR expr3
> 
> ```





 Individual subterms might be a single comparison expression like
 **a\=5** or **x\>y** or they can be 
 LIKE or BETWEEN expressions, or a subterm
 can be a parenthesized list of AND\-connected sub\-subterms.
 Each subterm is analyzed as if it were itself the entire WHERE clause
 in order to see if the subterm is indexable by itself.
 If every subterm of an OR clause is separately indexable
 then the OR clause might be coded such that a separate index is used
 to evaluate each term of the OR clause. One way to think about how
 SQLite uses separate indexes for each OR clause term is to imagine
 that the WHERE clause where rewritten as follows:


> ```
> 
>   rowid IN (SELECT rowid FROM table WHERE expr1
>             UNION SELECT rowid FROM table WHERE expr2
>             UNION SELECT rowid FROM table WHERE expr3)
> 
> ```





 The rewritten expression above is conceptual; WHERE clauses containing
 OR are not really rewritten this way.
 The actual implementation of the OR clause uses a mechanism that is
 more efficient and that works even for [WITHOUT ROWID](withoutrowid.html) tables or 
 tables in which the "rowid" is inaccessible. Nevertheless,
 the essence of the implementation is captured by the statement
 above: Separate indexes are used to find candidate result rows
 from each OR clause term and the final result is the union of
 those rows.




 Note that in most cases, SQLite will only use a single index for each
 table in the FROM clause of a query. The second OR\-clause optimization
 described here is the exception to that rule. With an OR\-clause,
 a different index might be used for each subterm in the OR\-clause.




 For any given query, the fact that the OR\-clause optimization described
 here can be used does not guarantee that it will be used.
 SQLite uses a cost\-based query planner that estimates the CPU and
 disk I/O costs of various competing query plans and chooses the plan
 that it thinks will be the fastest. If there are many OR terms in
 the WHERE clause or if some of the indexes on individual OR\-clause 
 subterms are not very selective, then SQLite might decide that it is
 faster to use a different query algorithm, or even a full\-table scan.
 Application developers can use the
 [EXPLAIN QUERY PLAN](lang_explain.html) prefix on a statement to get a
 high\-level overview of the chosen query strategy.




# 5\. The LIKE Optimization



 A WHERE\-clause term that uses the [LIKE](lang_expr.html#like) or [GLOB](lang_expr.html#glob) operator
 can sometimes be used with an index to do a range search, 
 almost as if the LIKE or GLOB were an alternative to a [BETWEEN](lang_expr.html#between)
 operator.
 There are many conditions on this optimization:






1. The right\-hand side of the LIKE or GLOB must be either a string literal
 or a [parameter](lang_expr.html#varparam) bound to a string literal
 that does not begin with a wildcard character.
2. It must not be possible to make the LIKE or GLOB operator true by
 having a numeric value (instead of a string or blob) on the
 left\-hand side. This means that either:
	1. the left\-hand side of the LIKE or GLOB operator is the name
	 of an indexed column with [TEXT affinity](datatype3.html#affinity), or
	2. the right\-hand side pattern argument does not begin with a
	 minus sign ("\-") or a digit.
 This constraint arises from the fact that numbers do not sort in
 lexicographical order. For example: 9\<10 but '9'\>'10'.
3. The built\-in functions used to implement LIKE and GLOB must not
 have been overloaded using the [sqlite3\_create\_function()](c3ref/create_function.html) API.
4. For the GLOB operator, the column must be indexed using the 
 built\-in BINARY collating sequence.
5. For the LIKE operator, if [case\_sensitive\_like](pragma.html#pragma_case_sensitive_like) mode is enabled then
 the column must indexed using BINARY collating sequence, or if
 [case\_sensitive\_like](pragma.html#pragma_case_sensitive_like) mode is disabled then the column must indexed
 using built\-in NOCASE collating sequence.
6. If the ESCAPE option is used, the ESCAPE character must be ASCII,
 or a single\-byte character in UTF\-8\.



 The LIKE operator has two modes that can be set by a
 [pragma](pragma.html#pragma_case_sensitive_like). The
 default mode is for LIKE comparisons to be insensitive to differences
 of case for latin1 characters. Thus, by default, the following
 expression is true:




```
'a' LIKE 'A'

```


 If the case\_sensitive\_like pragma is enabled as follows:




```
PRAGMA case_sensitive_like=ON;

```


 Then the LIKE operator pays attention to case and the example above would
 evaluate to false. Note that case insensitivity only applies to
 latin1 characters \- basically the upper and lower case letters of English
 in the lower 127 byte codes of ASCII. International character sets
 are case sensitive in SQLite unless an application\-defined
 [collating sequence](datatype3.html#collation) and [like() SQL function](lang_corefunc.html#like) are provided that
 take non\-ASCII characters into account.
 If an application\-defined collating sequence and/or like() SQL
 function are provided, the LIKE optimization described here will never
 be taken.




 The LIKE operator is case insensitive by default because this is what
 the SQL standard requires. You can change the default behavior at
 compile time by using the [SQLITE\_CASE\_SENSITIVE\_LIKE](compile.html#case_sensitive_like) command\-line option
 to the compiler.




 The LIKE optimization might occur if the column named on the left of the
 operator is indexed using the built\-in BINARY collating sequence and
 case\_sensitive\_like is turned on. Or the optimization might occur if
 the column is indexed using the built\-in NOCASE collating sequence and the 
 case\_sensitive\_like mode is off. These are the only two combinations
 under which LIKE operators will be optimized.




 The GLOB operator is always case sensitive. The column on the left side
 of the GLOB operator must always use the built\-in BINARY collating sequence
 or no attempt will be made to optimize that operator with indexes.




 The LIKE optimization will only be attempted if
 the right\-hand side of the GLOB or LIKE operator is either
 literal string or a [parameter](lang_expr.html#varparam) that has been [bound](c3ref/bind_blob.html)
 to a string literal. The string literal must not
 begin with a wildcard; if the right\-hand side begins with a wildcard
 character then this optimization is not attempted. If the right\-hand side 
 is a [parameter](lang_expr.html#varparam) that is bound to a string, then this optimization is
 only attempted if the [prepared statement](c3ref/stmt.html) containing the expression
 was compiled with [sqlite3\_prepare\_v2()](c3ref/prepare.html) or [sqlite3\_prepare16\_v2()](c3ref/prepare.html).
 The LIKE optimization is not attempted if the
 right\-hand side is a [parameter](lang_expr.html#varparam) and the statement was prepared using
 [sqlite3\_prepare()](c3ref/prepare.html) or [sqlite3\_prepare16()](c3ref/prepare.html).




 Suppose the initial sequence of non\-wildcard characters on the right\-hand
 side of the LIKE or GLOB operator is *x*. We are using a single 
 character to denote this non\-wildcard prefix but the reader should
 understand that the prefix can consist of more than 1 character.
 Let *y* be the smallest string that is the same length as /x/ but which
 compares greater than *x*. For example, if *x* is
 'hello' then
 *y* would be 'hellp'.
 The LIKE and GLOB optimizations consist of adding two virtual terms
 like this:


> ```
> 
>   column >= x AND column < y
> 
> ```





 Under most circumstances, the original LIKE or GLOB operator is still
 tested against each input row even if the virtual terms are used to
 constrain an index. This is because we do not know what additional
 constraints may be imposed by characters to the right
 of the *x* prefix. However, if there is only a single
 global wildcard to the right of *x*, then the original LIKE or 
 GLOB test is disabled.
 In other words, if the pattern is like this:


> ```
> 
>   column LIKE x%
>   column GLOB x*
> 
> ```





 then the original LIKE or GLOB tests are disabled when the virtual
 terms constrain an index because in that case we know that all of the
 rows selected by the index will pass the LIKE or GLOB test.




 Note that when the right\-hand side of a LIKE or GLOB operator is
 a [parameter](lang_expr.html#varparam) and the statement is prepared using [sqlite3\_prepare\_v2()](c3ref/prepare.html)
 or [sqlite3\_prepare16\_v2()](c3ref/prepare.html) then the statement is automatically reparsed
 and recompiled on the first [sqlite3\_step()](c3ref/step.html) call of each run if the binding
 to the right\-hand side parameter has changed since the previous run.
 This reparse and recompile is essentially the same action that occurs
 following a schema change. The recompile is necessary so that the query
 planner can examine the new value bound to the right\-hand side of the
 LIKE or GLOB operator and determine whether or not to employ the
 optimization described above.




# 6\. The Skip\-Scan Optimization



 The general rule is that indexes are only useful if there are 
 WHERE\-clause constraints on the left\-most columns of the index.
 However, in some cases,
 SQLite is able to use an index even if the first few columns of
 the index are omitted from the WHERE clause but later columns 
 are included.





 Consider a table such as the following:




```
CREATE TABLE people(
  name TEXT PRIMARY KEY,
  role TEXT NOT NULL,
  height INT NOT NULL, -- in cm
  CHECK( role IN ('student','teacher') )
);
CREATE INDEX people_idx1 ON people(role, height);

```


 The people table has one entry for each person in a large
 organization. Each person is either a "student" or a "teacher",
 as determined by the "role" field. The table also records the height in
 centimeters of each person. The role and height are indexed.
 Notice that the left\-most column of the index is not very
 selective \- it only contains two possible values.





 Now consider a query to find the names of everyone in the
 organization that is 180cm tall or taller:





```
SELECT name FROM people WHERE height>=180;

```


 Because the left\-most column of the index does not appear in the
 WHERE clause of the query, one is tempted to conclude that the
 index is not usable here. However, SQLite is able to use the index.
 Conceptually, SQLite uses the index as if the query were more
 like the following:





```
SELECT name FROM people
 WHERE role IN (SELECT DISTINCT role FROM people)
   AND height>=180;

```


 Or this:




```
SELECT name FROM people WHERE role='teacher' AND height>=180
UNION ALL
SELECT name FROM people WHERE role='student' AND height>=180;

```


 The alternative query formulations shown above are conceptual only.
 SQLite does not really transform the query. 
 The actual query plan is like this:
 SQLite locates the first possible value for "role", which it
 can do by rewinding the "people\_idx1" index to the beginning and reading
 the first record. SQLite stores this first "role" value in an
 internal variable that we will here call "$role". Then SQLite
 runs a query like: "SELECT name FROM people WHERE role\=$role AND height\>\=180".
 This query has an equality constraint on the left\-most column of the
 index and so the index can be used to resolve that query. Once
 that query is finished, SQLite then uses the "people\_idx1" index to
 locate the next value of the "role" column, using code that is logically
 similar to "SELECT role FROM people WHERE role\>$role LIMIT 1".
 This new "role" value overwrites the $role variable, and the process
 repeats until all possible values for "role" have been examined.




 We call this kind of index usage a "skip\-scan" because the database
 engine is basically doing a full scan of the index but it optimizes the
 scan (making it less than "full") by occasionally skipping ahead to the
 next candidate value.




 SQLite might use a skip\-scan on an index if it knows that the first
 one or more columns contain many duplication values.
 If there are too few duplicates
 in the left\-most columns of the index, then it would
 be faster to simply step ahead to the next value, and thus do
 a full table scan, than to do a binary search on an index to locate
 the next left\-column value.




 The only way that SQLite can know that there are many duplicates
 in the left\-most columns of an index
 is if the [ANALYZE](lang_analyze.html) command has been run
 on the database.
 Without the results of ANALYZE, SQLite has to guess at the "shape" of
 the data in the table, and the default guess is that there are an average
 of 10 duplicates for every value in the left\-most column of the index.
 Skip\-scan only becomes profitable (it only gets to be faster than
 a full table scan) when the number of duplicates is about 18 or more.
 Hence, a skip\-scan is never used on a database that has not been analyzed.




# 7\. Joins



 SQLite implements joins as nested loops.
 The default order of the nested loops in a join is for the left\-most
 table in the FROM clause to form the outer loop and the right\-most
 table to form the inner loop.
 However, SQLite will nest the loops in a different order if doing so
 will help it to select better indexes.




 Inner joins can be freely reordered. However outer joins are
 neither commutative nor associative and hence will not be reordered.
 Inner joins to the left and right of an outer join might be reordered
 if the optimizer thinks that is advantageous but outer joins are
 always evaluated in the order in which they occur.




 SQLite [treats the CROSS JOIN operator specially](lang_select.html#crossjoin).
 The CROSS JOIN operator is commutative, in theory. However, SQLite chooses to
 never reorder tables in a CROSS JOIN. This provides a mechanism
 by which the programmer can force SQLite to choose a particular loop nesting
 order. 




 When selecting the order of tables in a join, SQLite uses an efficient
 polynomial\-time algorithm graph algorithm described in
 the [Next Generation Query Planner](queryplanner-ng.html) document. Because of this,
 SQLite is able to plan queries with 50\- or 60\-way joins in a matter of
 microseconds




 Join reordering is automatic and usually works well enough that
 programmers do not have to think about it, especially if [ANALYZE](lang_analyze.html)
 has been used to gather statistics about the available indexes,
 though occasionally some hints from the programmer are needed.
 Consider, for example, the following schema:




```
CREATE TABLE node(
   id INTEGER PRIMARY KEY,
   name TEXT
);
CREATE INDEX node_idx ON node(name);
CREATE TABLE edge(
   orig INTEGER REFERENCES node,
   dest INTEGER REFERENCES node,
   PRIMARY KEY(orig, dest)
);
CREATE INDEX edge_idx ON edge(dest,orig);

```


 The schema above defines a directed graph with the ability to store a
 name at each node. Now consider a query against this schema:




```
SELECT *
  FROM edge AS e,
       node AS n1,
       node AS n2
 WHERE n1.name = 'alice'
   AND n2.name = 'bob'
   AND e.orig = n1.id
   AND e.dest = n2.id;

```


 This query asks for is all information about edges that go from
 nodes labeled "alice" to nodes labeled "bob".
 The query optimizer in SQLite has basically two choices on how to
 implement this query. (There are actually six different choices, but
 we will only consider two of them here.)
 Pseudocode below demonstrating these two choices.




Option 1:



```
foreach n1 where n1.name='alice' do:
  foreach n2 where n2.name='bob' do:
    foreach e where e.orig=n1.id and e.dest=n2.id
      return n1.*, n2.*, e.*
    end
  end
end

```


Option 2:



```
foreach n1 where n1.name='alice' do:
  foreach e where e.orig=n1.id do:
    foreach n2 where n2.id=e.dest and n2.name='bob' do:
      return n1.*, n2.*, e.*
    end
  end
end

```


 The same indexes are used to speed up every loop in both implementation
 options.
 The only difference in these two query plans is the order in which
 the loops are nested.




 So which query plan is better? It turns out that the answer depends on
 what kind of data is found in the node and edge tables.




 Let the number of alice nodes be M and the number of bob nodes be N.
 Consider two scenarios. In the first scenario, M and N are both 2 but
 there are thousands of edges on each node. In this case, option 1 is
 preferred. With option 1, the inner loop checks for the existence of
 an edge between a pair of nodes and outputs the result if found. 
 Because there are only 2 alice and bob nodes each, the inner loop
 only has to run four times and the query is very quick. Option 2 would
 take much longer here. The outer loop of option 2 only executes twice,
 but because there are a large number of edges leaving each alice node,
 the middle loop has to iterate many thousands of times. It will be
 much slower. So in the first scenario, we prefer to use option 1\.




 Now consider the case where M and N are both 3500\. Alice nodes are
 abundant. This time suppose each of these nodes is connected by only one
 or two edges. Now option 2 is preferred. With option 2,
 the outer loop still has to run 3500 times, but the middle loop only
 runs once or twice for each outer loop and the inner loop will only
 run once for each middle loop, if at all. So the total number of
 iterations of the inner loop is around 7000\. Option 1, on the other
 hand, has to run both its outer loop and its middle loop 3500 times
 each, resulting in 12 million iterations of the middle loop.
 Thus in the second scenario, option 2 is nearly 2000 times faster
 than option 1\.




 So you can see that depending on how the data is structured in the table,
 either query plan 1 or query plan 2 might be better. Which plan does
 SQLite choose by default? As of version 3\.6\.18, without running [ANALYZE](lang_analyze.html),
 SQLite will choose option 2\.
 If the [ANALYZE](lang_analyze.html) command is run in order to gather statistics,
 a different choice might be made if the statistics indicate that the
 alternative is likely to run faster.



## 7\.1\. Manual Control Of Join Order



 SQLite almost always picks the best join order automatically. It is
 very rare that a developer needs to intervene to give the query planner
 hints about the best join order. The best policy is to make use
 of [PRAGMA optimize](pragma.html#pragma_optimize) to ensure that the query planner has access to
 up\-to\-date statistics on the shape of the data in the database.




 This section describes techniques by which developers can control the
 join order in SQLite, to work around any performance problems that may
 arise. However, the use of these techniques is not recommended, except
 as a last resort.




 If you do encounter a situation where SQLite is picking a suboptimal
 join order even after running [PRAGMA optimize](pragma.html#pragma_optimize), please report your
 situation on the [SQLite Community Forum](https://sqlite.org/forum) so
 that the SQLite maintainers can make new refinements to the query planner
 such that manual intervention is not required.




### 7\.1\.1\. Manual Control Of Query Plans Using SQLITE\_STAT Tables



 SQLite provides the ability for advanced programmers to exercise control
 over the query plan chosen by the optimizer. One method for doing this
 is to fudge the [ANALYZE](lang_analyze.html) results in the [sqlite\_stat1](fileformat2.html#stat1tab) table.




### 7\.1\.2\. Manual Control of Query Plans using CROSS JOIN



 Programmers can force SQLite to use a particular loop nesting order
 for a join by using the CROSS JOIN operator instead of just JOIN, 
 INNER JOIN, NATURAL JOIN, or a "," join. Though CROSS JOINs are
 commutative in theory, SQLite chooses to never reorder the tables in
 a CROSS JOIN. Hence, the left table of a CROSS JOIN will always be
 in an outer loop relative to the right table.




 In the following query, the optimizer is free to reorder the 
 tables of FROM clause any way it sees fit:




```
SELECT *
  FROM node AS n1,
       edge AS e,
       node AS n2
 WHERE n1.name = 'alice'
   AND n2.name = 'bob'
   AND e.orig = n1.id
   AND e.dest = n2.id;

```


 In the following logically equivalent formulation of the same query,
 the substitution of "CROSS JOIN" for the "," means that the order
 of tables must be N1, E, N2\.




```
SELECT *
  FROM node AS n1 CROSS JOIN
       edge AS e CROSS JOIN
       node AS n2
 WHERE n1.name = 'alice'
   AND n2.name = 'bob'
   AND e.orig = n1.id
   AND e.dest = n2.id;

```


 In the latter query, the query plan must be 
 [option 2](#option2). Note that
 you must use the keyword "CROSS" in order to disable the table reordering
 optimization; INNER JOIN, NATURAL JOIN, JOIN, and other similar
 combinations work just like a comma join in that the optimizer is
 free to reorder tables as it sees fit. (Table reordering is also
 disabled on an outer join, but that is because outer joins are not
 associative or commutative. Reordering tables in OUTER JOIN changes
 the result.)




 See "[The Fossil NGQP Upgrade Case Study](queryplanner-ng.html#fossilcasestudy)" for another real\-world example
 of using CROSS JOIN to manually control the nesting order of a join.
 The [query planner checklist](queryplanner-ng.html#howtofix) found later in the same document provides
 further guidance on manual control of the query planner.




# 8\. Choosing Between Multiple Indexes



 Each table in the FROM clause of a query can use at most one index
 (except when the [OR\-clause optimization](#or_opt) comes into
 play)
 and SQLite strives to use at least one index on each table. Sometimes,
 two or more indexes might be candidates for use on a single table.
 For example:




```
CREATE TABLE ex2(x,y,z);
CREATE INDEX ex2i1 ON ex2(x);
CREATE INDEX ex2i2 ON ex2(y);
SELECT z FROM ex2 WHERE x=5 AND y=6;

```


 For the SELECT statement above, the optimizer can use the ex2i1 index
 to lookup rows of ex2 that contain x\=5 and then test each row against
 the y\=6 term. Or it can use the ex2i2 index to lookup rows
 of ex2 that contain y\=6 then test each of those rows against the
 x\=5 term.




 When faced with a choice of two or more indexes, SQLite tries to estimate
 the total amount of work needed to perform the query using each option.
 It then selects the option that gives the least estimated work.




 To help the optimizer get a more accurate estimate of the work involved
 in using various indexes, the user may optionally run the [ANALYZE](lang_analyze.html) command.
 The [ANALYZE](lang_analyze.html) command scans all indexes of database where there might
 be a choice between two or more indexes and gathers statistics on the
 selectiveness of those indexes. The statistics gathered by
 this scan are stored in special database tables names shows names all
 begin with "**sqlite\_stat**".
 The content of these tables is not updated as the database
 changes so after making significant changes it might be prudent to
 rerun [ANALYZE](lang_analyze.html).
 The results of an ANALYZE command are only available to database connections
 that are opened after the ANALYZE command completes.




 The various **sqlite\_stat***N* tables contain information on how
 selective the various indexes are. For example, the [sqlite\_stat1](fileformat2.html#stat1tab)
 table might indicate that an equality constraint on column x reduces the
 search space to 10 rows on average, whereas an equality constraint on
 column y reduces the search space to 3 rows on average. In that case,
 SQLite would prefer to use index ex2i2 since that index is more selective.




## 8\.1\. Disqualifying WHERE Clause Terms using Unary\-"\+"



*Note: Disqualifying WHERE clause terms this way is not recommended.
 This is a work\-around.
 Only do this as a last resort to get the performance you need. If you
 find a situation where this work\-around is necessary, please report the
 situation on the [SQLite Community Forum](https://sqlite.org/forum) so
 that the SQLite maintainers can try to improve the query planner such
 that the work\-around is no longer required for your situation.*



 Terms of the WHERE clause can be manually disqualified for use with
 indexes by prepending a unary **\+** operator to the column name. The
 unary **\+** is a no\-op and will not generate any byte code in the prepared
 statement.
 However, the unary **\+** operator will prevent the term from
 constraining an index.
 So, in the example above, if the query were rewritten as:




```
SELECT z FROM ex2 WHERE +x=5 AND y=6;

```


 The **\+** operator on the **x** column will prevent that term from 
 constraining an index. This would force the use of the ex2i2 index.




 Note that the unary **\+** operator also removes 
 [type affinity](datatype3.html#affinity) from
 an expression, and in some cases this can cause subtle changes in
 the meaning of an expression.
 In the example above,
 if column **x** has [TEXT affinity](datatype3.html#affinity)
 then the comparison "x\=5" will be done as text. The **\+** operator
 removes the affinity. So the comparison "**\+x\=5**" will compare the text
 in column **x** with the numeric value 5 and will always be false.




## 8\.2\. Range Queries



 Consider a slightly different scenario:




```
CREATE TABLE ex2(x,y,z);
CREATE INDEX ex2i1 ON ex2(x);
CREATE INDEX ex2i2 ON ex2(y);
SELECT z FROM ex2 WHERE x BETWEEN 1 AND 100 AND y BETWEEN 1 AND 100;

```


 Further suppose that column x contains values spread out
 between 0 and 1,000,000 and column y contains values
 that span between 0 and 1,000\. In that scenario,
 the range constraint on column x should reduce the search space by
 a factor of 10,000 whereas the range constraint on column y should
 reduce the search space by a factor of only 10\. So the ex2i1 index
 should be preferred.




 SQLite will make this determination, but only if it has been compiled
 with [SQLITE\_ENABLE\_STAT3](compile.html#enable_stat3) or [SQLITE\_ENABLE\_STAT4](compile.html#enable_stat4).
 The [SQLITE\_ENABLE\_STAT3](compile.html#enable_stat3) and [SQLITE\_ENABLE\_STAT4](compile.html#enable_stat4) options causes
 the [ANALYZE](lang_analyze.html) command to collect a histogram of column content in the
 [sqlite\_stat3](fileformat2.html#stat3tab) or [sqlite\_stat4](fileformat2.html#stat4tab) tables and to use this histogram to 
 make a better guess at the best query to use for range constraints
 such as the above. The main difference between STAT3 and STAT4 is
 that STAT3 records histogram data for only the left\-most column of
 an index whereas STAT4 records histogram data for all columns of an
 index. For single\-column indexes, STAT3 and STAT4 work the same.




 The histogram data is only useful if the right\-hand side of the constraint
 is a simple compile\-time constant or [parameter](lang_expr.html#varparam) and not an expression.




 Another limitation of the histogram data is that it only applies to the
 left\-most column on an index. Consider this scenario:




```
CREATE TABLE ex3(w,x,y,z);
CREATE INDEX ex3i1 ON ex2(w, x);
CREATE INDEX ex3i2 ON ex2(w, y);
SELECT z FROM ex3 WHERE w=5 AND x BETWEEN 1 AND 100 AND y BETWEEN 1 AND 100;

```


 Here the inequalities are on columns x and y which are not the
 left\-most index columns. Hence, the histogram data which is collected no
 left\-most column of indexes is useless in helping to choose between the
 range constraints on columns x and y.




# 9\. Covering Indexes



 When doing an indexed lookup of a row, the usual procedure is to
 do a binary search on the index to find the index entry, then extract
 the [rowid](lang_createtable.html#rowid) from the index and use that [rowid](lang_createtable.html#rowid) to do a binary search on
 the original table. Thus a typical indexed lookup involves two
 binary searches.
 If, however, all columns that were to be fetched from the table are
 already available in the index itself, SQLite will use the values
 contained in the index and will never look up the original table
 row. This saves one binary search for each row and can make many
 queries run twice as fast.




 When an index contains all of the data needed for a query and when the
 original table never needs to be consulted, we call that index a
 "covering index".




# 10\. ORDER BY Optimizations



 SQLite attempts to use an index to satisfy the ORDER BY clause of a
 query when possible.
 When faced with the choice of using an index to satisfy WHERE clause
 constraints or satisfying an ORDER BY clause, SQLite does the same
 cost analysis described above
 and chooses the index that it believes will result in the fastest answer.




 SQLite will also attempt to use indexes to help satisfy GROUP BY clauses
 and the DISTINCT keyword. If the nested loops of the join can be arranged
 such that rows that are equivalent for the GROUP BY or for the DISTINCT are
 consecutive, then the GROUP BY or DISTINCT logic can determine if the 
 current row is part of the same group or if the current row is distinct
 simply by comparing the current row to the previous row.
 This can be much faster than the alternative of comparing each row to
 all prior rows.




## 10\.1\. Partial ORDER BY via Index



 If a query contains an ORDER BY clause with multiple terms, it might
 be that SQLite can use indexes to cause rows to come out in the order
 of some prefix of the terms in the ORDER BY but that later terms in
 the ORDER BY are not satisfied. In that case, SQLite does block sorting.
 Suppose the ORDER BY clause has four terms and the natural order of the
 query results in rows appearing in order of the first two terms. As
 each row is output by the query engine and enters the sorter, the 
 outputs in the current row corresponding to the first two terms of 
 the ORDER BY are compared against the previous row. If they have
 changed, the current sort is finished and output and a new sort is
 started. This results in a slightly faster sort. Even bigger
 advantages are that many fewer rows need to be held in memory,
 reducing memory requirements, and outputs can begin to appear before
 the core query has run to completion.




# 11\. Subquery Flattening



 When a subquery occurs in the FROM clause of a SELECT, the simplest
 behavior is to evaluate the subquery into a transient table, then run
 the outer SELECT against the transient table. Such a plan
 can be suboptimal since the transient table will not have any indexes
 and the outer query (which is likely a join) will be forced to either
 do full table scan on the transient table or else construct a
 [query\-time index](optoverview.html#autoindex) on the transient table, neither or which is likely
 to be particularly fast.




 To overcome this problem, SQLite attempts to flatten subqueries in
 the FROM clause of a SELECT.
 This involves inserting the FROM clause of the subquery into the
 FROM clause of the outer query and rewriting expressions in
 the outer query that refer to the result set of the subquery.
 For example:




```
SELECT t1.a, t2.b FROM t2, (SELECT x+y AS a FROM t1 WHERE z<100) WHERE a>5

```


 Would be rewritten using query flattening as:




```
SELECT t1.x+t1.y AS a, t2.b FROM t2, t1 WHERE z<100 AND a>5

```


 There is a long list of conditions that must all be met in order for
 query flattening to occur. Some of the constraints are marked as 
 obsolete by italic text. These extra constraints are retained in the
 documentation to preserve the numbering of the other constraints.




 Casual readers are not expected to understand all of these rules.
 The point here is that flattening rules are subtle and complex.
 There have been multiple bugs over the years caused by
 over\-aggressive query flattening. On the other hand, performance
 of complex queries and/or queries involving views tends to suffer
 if query flattening is more conservative.






1. *(Obsolete)*
2. *(Obsolete)*
3. If the subquery is the right operand of a LEFT JOIN then
	1. the subquery may not be a join, and
	2. the FROM clause of the subquery may
	 not contain a virtual table, and
	3. the outer query may not be DISTINCT.
4. The subquery is not DISTINCT.
5. *(Obsolete \- subsumed into constraint 4\)*
6. *(Obsolete)*
7. The subquery has a FROM clause.
8. The subquery does not use LIMIT or the outer query is
 not a join.
9. The subquery does not use LIMIT or the outer query
 does not use aggregates.
10. *(Obsolete)*
11. The subquery and the outer query do not both have ORDER BY clauses.
12. *(Obsolete \- subsumed into constraint 3\)*
13. The subquery and outer query do not both use LIMIT.
14. The subquery does not use OFFSET.
15. If the outer query is part of a compound select, then the
 subquery may not have a LIMIT clause.
16. If the outer query is an aggregate, then the subquery may
 not contain ORDER BY.
17. If the sub\-query is a compound SELECT, then
	1. all compound operators must be UNION ALL, and
	2. no terms with the subquery compound may be aggregate
	 or DISTINCT, and
	3. every term within the subquery must have a FROM clause, and
	4. the outer query may not be an aggregateor DISTINCT query.
	5. the subquery may not contain window functions.
	6. the subquery must not be the right\-hand side of a LEFT JOIN.
	7. either the subquery is the first element of the outer query
	 or there are not RIGHT or FULL JOINs in any arm of the subquery.
	8. the corresponding result set expressions in all arms of the
	 compound subquery must have the same [affinity](datatype3.html#affinity).

 The parent and sub\-query may contain WHERE clauses. Subject to
 rules (11\), (12\) and (13\), they may also contain ORDER BY,
 LIMIT and OFFSET clauses.
18. If the sub\-query is a compound select, then all terms of the
 ORDER by clause of the parent must be simple references to 
 columns of the sub\-query.
19. If the subquery uses LIMIT then the outer query may not
 have a WHERE clause.
20. If the sub\-query is a compound select, then it must not use
 an ORDER BY clause.
21. If the subquery uses LIMIT, then the outer query may not be
 DISTINCT.
22. The subquery may not be a recursive CTE.
23. If the outer query is a recursive CTE, then the sub\-query
 may not be a compound query.
24. *(Obsolete)*
25. Neither the subquery nor the outer query may contain
 a [window function](windowfunctions.html) in the result set nor the ORDER BY clause.
26. The subquery may not be the right operand of a RIGHT
 or FULL OUTER JOIN.
27. The subquery may not contain a FULL or RIGHT JOIN unless it
 is the first element of the parent query. Two subcases:
	1. the subquery is not a compound query.
	2. the subquery is a compound query and the RIGHT JOIN occurs
	 in any arm of the compound query. (See also (17g)).
28. The subquery is not a MATERIALIZED CTE.



 Query flattening is an important optimization when views are used as
 each use of a view is translated into a subquery.




# 12\. Subquery Co\-routines



 SQLite implements FROM\-clause subqueries in one of three ways:
 

1. [Flatten](optoverview.html#flattening) the subquery into its outer query
2. Evaluate the subquery into a transient table that exists for
 the duration of the one SQL statement that is being evaluated,
 then run the outer query against that transient table.
3. Evaluate the subquery in a co\-routine that runs in parallel with
 the outer query, providing rows to the outer query as needed.



 This section describes the third technique: implementing the subquery
 as a co\-routine.




 A co\-routine is like a subroutine in that it runs in the same thread
 as the caller and eventually returns control back to the caller. The
 difference is that a co\-routine also has the ability to return
 before it has finished, and then resume where it left off the next
 time it is called.




 When a subquery is implemented as a co\-routine, byte\-code is generated
 to implement the subquery as if it were a standalone query, except
 instead of returning rows of results back to the application, the
 co\-routine yields control back to the caller after each row is computed.
 The caller can then use that one computed row as part of its computation,
 then invoke the co\-routine again when it is ready for the next row.




 Co\-routines are better than storing the complete result set of the subquery
 in a transient table because co\-routines use less memory. With a co\-routine,
 only a single row of the result needs to be remembered, whereas all rows of
 the result must be stored for a transient table. Also, because the
 co\-routine does not need to run to completion before the outer query
 begins its work, the first rows of output can appear much sooner, and if
 the overall query is abandoned before it has finished, less work is done
 overall.




 On the other hand, if the result of the subquery must be scanned multiple
 times (because, for example, it is just one table in a join) then it
 is better to use a transient table to remember the entire result of the
 subquery, in order to avoid computing the subquery more than once.




## 12\.1\. Using Co\-routines to Defer Work until after the Sorting



 As of SQLite version 3\.21\.0 (2017\-10\-24\), the query planner will
 always prefer to use a co\-routine to implement FROM\-clause subqueries 
 that contains an ORDER BY clause and that are not part of a join when
 the result set of the outer query is "complex". This feature allows
 applications to shift expensive computations from before the
 sorter until after the sorter, which can result in faster operation.
 For example, consider this query:




```
SELECT expensive_function(a) FROM tab ORDER BY date DESC LIMIT 5;

```


 The goal of this query is to compute some value for the five most
 recent entries in the table. In the query above, the
 "expensive\_function()" is invoked prior to the sort and thus is
 invoked on every row of the table, even
 rows that are ultimately omitted due to the LIMIT clause.
 A co\-routine can be used to work around this:




```
SELECT expensive_function(a) FROM (
  SELECT a FROM tab ORDER BY date DESC LIMIT 5
);

```


 In the revised query, the subquery implemented by a co\-routine computes
 the five most recent values for "a". Those five values are passed from the
 co\-routine up into the outer query where the "expensive\_function()" is
 invoked on only the specific rows that the application cares about.




 The query planner in future versions of SQLite might grow smart enough
 to make transformations such as the above automatically, in both directions.
 That is to say, future versions of SQLite might transform queries of the
 first form into the second, or queries written the second way into the
 first. As of SQLite version 3\.22\.0 (2018\-01\-22\), the query planner
 will flatten the subquery if the outer query does not make use of any
 user\-defined functions or subqueries in its result set. For the examples
 shown above, however, SQLite implements each of the queries as
 written.




# 13\. The MIN/MAX Optimization



 Queries that contain a single MIN() or MAX() aggregate function whose
 argument is the left\-most column of an index might be satisfied
 by doing a single index lookup rather than by scanning the entire table.
 Examples:




```
SELECT MIN(x) FROM table;
SELECT MAX(x)+1 FROM table;

```


# 14\. Automatic Query\-Time Indexes



 When no indexes are available to aid the evaluation of a query, SQLite
 might create an automatic index that lasts only for the duration
 of a single SQL statement.
 Automatic indexes are also sometimes called "Query\-time indexes".
 Since the cost of constructing the automatic or query\-time index is
 O(NlogN) (where N is the number of entries in the table) and the cost of
 doing a full table scan is only O(N), an automatic index will
 only be created if SQLite expects that the lookup will be run more than
 logN times during the course of the SQL statement. Consider an example:




```
CREATE TABLE t1(a,b);
CREATE TABLE t2(c,d);
-- Insert many rows into both t1 and t2
SELECT * FROM t1, t2 WHERE a=c;

```


 In the query above, if both t1 and t2 have approximately N rows, then
 without any indexes the query will require O(N\*N) time. On the other
 hand, creating an index on table t2 requires O(NlogN) time and using
 that index to evaluate the query requires an additional O(NlogN) time.
 In the absence of [ANALYZE](lang_analyze.html) information, SQLite guesses that N is one
 million and hence it believes that constructing the automatic index will
 be the cheaper approach.




 An automatic query\-time index might also be used for a subquery:




```
CREATE TABLE t1(a,b);
CREATE TABLE t2(c,d);
-- Insert many rows into both t1 and t2
SELECT a, (SELECT d FROM t2 WHERE c=b) FROM t1;

```


 In this example, the t2 table is used in a subquery to translate values
 of the t1\.b column. If each table contains N rows, SQLite expects that
 the subquery will run N times, and hence it will believe it is faster
 to construct an automatic, transient index on t2 first and then use
 that index to satisfy the N instances of the subquery.




 The automatic indexing capability can be disabled at run\-time using
 the [automatic\_index pragma](pragma.html#pragma_automatic_index). Automatic indexing is turned on by
 default, but this can be changed so that automatic indexing is off
 by default using the [SQLITE\_DEFAULT\_AUTOMATIC\_INDEX](compile.html#default_automatic_index) compile\-time option.
 The ability to create automatic indexes can be completely disabled by
 compiling with the [SQLITE\_OMIT\_AUTOMATIC\_INDEX](compile.html#omit_automatic_index) compile\-time option.




 In SQLite [version 3\.8\.0](releaselog/3_8_0.html) (2013\-08\-26\) and later, 
 an [SQLITE\_WARNING\_AUTOINDEX](rescode.html#warning_autoindex) message is sent
 to the [error log](errlog.html) every time a statement is prepared that uses an
 automatic index. Application developers can and should use these warnings
 to identify the need for new persistent indexes in the schema.




 Do not confuse automatic indexes with the [internal indexes](fileformat2.html#intschema) (having names
 like "sqlite\_autoindex\_*table*\_*N*") that are sometimes
 created to implement a [PRIMARY KEY constraint](lang_createtable.html#primkeyconst) or [UNIQUE constraint](lang_createtable.html#uniqueconst).
 The automatic indexes described here exist only for the duration of a
 single query, are never persisted to disk, and are only visible to a
 single database connection. Internal indexes are part of the implementation
 of PRIMARY KEY and UNIQUE constraints, are long\-lasting and persisted
 to disk, and are visible to all database connections. The term "autoindex"
 appears in the names of [internal indexes](fileformat2.html#intschema) for legacy reasons and does
 not indicate that internal indexes and automatic indexes are related.




## 14\.1\. Hash Joins



 An automatic index is almost the same thing as a
 [hash join](https://en.wikipedia.org/wiki/Hash_join). The only difference
 is that a B\-Tree is used instead of a hash table. If you are willing to
 say that the transient B\-Tree constructed for an automatic index is
 really just a fancy hash table, then a query that uses an automatic
 index is just a hash join.




 SQLite constructs a transient index instead of a hash table in this
 instance because it already has a robust and high performance B\-Tree
 implementation at hand, whereas a hash\-table would need to be added.
 Adding a separate hash table implementation to handle this one case
 would increase the size of the library (which is designed for use on
 low\-memory embedded devices) for minimal performance gain. SQLite might
 be enhanced with a hash\-table implementation someday, but for now it seems
 better to continue using automatic indexes in cases where client/server
 database engines might use a hash join.




# 15\. The WHERE\-Clause Push\-Down Optimization



 If a subquery cannot be [flattened](optoverview.html#flattening) into the outer query, it might
 still be possible to enhance performance by "pushing down" WHERE clause
 terms from the outer query into the subquery. Consider an example:




```
CREATE TABLE t1(a INT, b INT);
CREATE TABLE t2(x INT, y INT);
CREATE VIEW v1(a,b) AS SELECT DISTINCT a, b FROM t1;

SELECT x, y, b
  FROM t2 JOIN v1 ON (x=a)
 WHERE b BETWEEN 10 AND 20;

```


 The view v1 cannot be [flattened](optoverview.html#flattening) because it is DISTINCT. It must
 instead be run as a subquery with the results being stored in a
 transient table, then the join is performed between t2 and the
 transient table. The push\-down optimization pushes down the
 "b BETWEEN 10 AND 20" term into the view. This makes the transient
 table smaller, and helps the subquery to run faster if there
 is an index on t1\.b. The resulting evaluation is like this:




```
SELECT x, y, b
  FROM t2
  JOIN (SELECT DISTINCT a, b FROM t1 WHERE b BETWEEN 10 AND 20)
 WHERE b BETWEEN 10 AND 20;

```


 The WHERE\-clause push\-down optimization cannot always be used. For example,
 if the subquery contains a LIMIT, then pushing down any part of
 the WHERE clause from the outer query could change the result of
 the inner query. There are other restrictions, explained in a
 comment in the source code on the pushDownWhereTerms() routine
 that implements this optimization.




 Do not confuse this optimization with the optimization by a similar name
 in MySQL. The MySQL push\-down optimization changes the order of evaluation
 of WHERE\-clause constraints such that those that can be evaluated using
 only the index and without having to find the corresponding table row are
 evaluated first, thus avoiding an unnecessary table row lookup if the
 constraint fails. For disambiguation, SQLite calls this the
 "MySQL push\-down optimization". SQLite does do the MySQL push\-down
 optimization too, in addition to the WHERE\-clause push\-down optimization.
 But the focus of this section is the WHERE\-clause push\-down optimization.




# 16\. The OUTER JOIN Strength Reduction Optimization



 An OUTER JOIN (either a LEFT JOIN, a RIGHT JOIN, or a FULL JOIN)
 can sometimes be simplified. A LEFT or RIGHT JOIN can be converted
 into an ordinary (INNER) JOIN, or a FULL JOIN might be converted into
 either a LEFT or a RIGHT JOIN. This can happen if there are terms
 in the WHERE clause that guarantee the same result after simplification.
 For example, if any
 column in the right\-hand table of the LEFT JOIN must be non\-NULL
 in order for the WHERE clause to be true, then the LEFT JOIN is
 demoted to an ordinary JOIN.




 The theorem prover that determines whether a join can be simplified is
 imperfect. It sometimes returns a false negative. In other words,
 it sometimes fails to prove that reducing the strength of an OUTER JOIN
 is safe when in fact it is safe.
 For example, the prover does not know
 the [datetime() SQL function](lang_datefunc.html#dttm) will always return NULL if its first
 argument is NULL, and so it will not recognize that the LEFT JOIN
 in the following query could be strength\-reduced:




```
SELECT urls.url
  FROM urls
  LEFT JOIN
    (SELECT *
      FROM (SELECT url_id AS uid, max(retrieval_time) AS rtime
              FROM lookups GROUP BY 1 ORDER BY 1)
      WHERE uid IN (358341,358341,358341)
    ) recent
    ON u.source_seed_id = recent.xyz OR u.url_id = recent.xyz
 WHERE
     DATETIME(recent.rtime) > DATETIME('now', '-5 days');

```


 It is possible that future enhancements to the prover might enable it
 to recognize that NULL inputs to certain built\-in functions
 always result in a NULL answer. However, not all built\-in
 functions have that property (for example [coalesce()](lang_corefunc.html#coalesce)) and, of
 course, the prover will never be able to reason about
 [application\-defined SQL functions](appfunc.html).




# 17\. The Omit OUTER JOIN Optimization



 Sometimes a LEFT or RIGHT JOIN can be completely omitted from a query without
 changing the result. This can happen if all of the following are
 true:






1. The query is not an aggregate
2. Either the query is DISTINCT or else the ON or USING clause
 on the OUTER JOIN constrains the join such that it matches
 only a single row
3. The right\-hand table of the LEFT JOIN or the left\-hand table of
 a RIGHT JOIN is not be used anywhere
 in the query outside of its own USING or ON clause.



 OUTER JOIN elimination often comes up when OUTER JOINs are used
 inside of views, and then the view is used in such as way that
 none of the columns on the right\-hand table of the LEFT JOIN or
 on the left\-hand table of a RIGHT JOIN are referenced.




 Here is a simple example of omitting a LEFT JOIN:




```
CREATE TABLE t1(ipk INTEGER PRIMARY KEY, v1);
CREATE TABLE t2(ipk INTEGER PRIMARY KEY, v2);
CREATE TABLE t3(ipk INTEGER PRIMARY KEY, v3);

SELECT v1, v3 FROM t1 
  LEFT JOIN t2 ON (t1.ipk=t2.ipk)
  LEFT JOIN t3 ON (t1.ipk=t3.ipk)

```


 The t2 table is completely unused in the query above, and so the
 query planner is able to implement the query as if it were written:




```
SELECT v1, v3 FROM t1 
  LEFT JOIN t3 ON (t1.ipk=t3.ipk)

```


 As of this writing, only LEFT JOINs are eliminated. This optimize
 has not yet been generalized to work with RIGHT JOINs as RIGHT JOIN
 is a relatively new addition to SQLite. That asymmetry will probably
 be corrected in a future release.





# 18\. The Constant Propagation Optimization



 When a WHERE clause contains two or more equality constraints connected
 by the AND operator such that all of the [affinities](datatype3.html#affinity) of the various
 constraints are the same, then SQLite might use the transitive property
 of equality to construct new "virtual" constraints that can be used to
 simplify expressions and/or improve performance. This is called the
 "constant\-propagation optimization".




 For example, consider the following schema and query:




```
CREATE TABLE t1(a INTEGER PRIMARY KEY, b INT, c INT);
SELECT * FROM t1 WHERE a=b AND b=5;

```


 SQLite looks at the "a\=b" and "b\=5" constraints and deduces that
 if those two constraints are true, then it must also be the case
 that "a\=5" is true. This means that the desired row can be looked up
 quickly using a value of 5 for the INTEGER PRIMARY KEY.


*This page last modified on [2024\-05\-10 14:25:41](https://sqlite.org/docsrc/honeypot) UTC* 


