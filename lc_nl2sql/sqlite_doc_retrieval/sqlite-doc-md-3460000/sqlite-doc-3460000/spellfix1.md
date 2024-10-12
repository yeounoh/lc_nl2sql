




The Spellfix1 Virtual Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Spellfix1 Virtual Table


►
Table Of Contents
[1\. Overview](#overview)
[2\. Search Refinements](#search_refinements)
[3\. Virtual Table Details](#virtual_table_details)
[4\. Algorithm](#algorithm)
[5\. Configurable Edit Distance](#configurable_edit_distance)
[6\. Dealing With Unusual And Difficult Spellings](#dealing_with_unusual_and_difficult_spellings)
[7\. Auxiliary Functions](#auxiliary_functions)
[8\. The editdist3 function](#the_editdist3_function)
[9\. The editdist3 COST table](#the_editdist3_cost_table)
[10\. Experimenting with the editcost3() function](#experimenting_with_the_editcost3_function)




# 1\. Overview


This spellfix1 [virtual table](vtab.html) can be used to search
a large vocabulary for close matches. For example, spellfix1
can be used to suggest corrections to misspelled words. Or,
it could be used with [FTS4](fts3.html#fts4) to do full\-text search using potentially
misspelled words.



The implementation for the spellfix1 virtual table is held in the
SQLite source tree in the miscellaneous extensions folder and in
particular in the file 
[ext/misc/spellfix1\.c](https://www.sqlite.org/src/finfo?name=ext/misc/spellfix.c).
The spellfix1 virtual table is not included in the SQLite [amalgamation](amalgamation.html)
and is not a part of any standard SQLite build. It is a [loadable extension](loadext.html).



Once the spellfix1 extension is loaded, an instance of the spellfix1 
virtual table is created like this:




> ```
> 
> CREATE VIRTUAL TABLE demo USING spellfix1;
> 
> ```


The "spellfix1" term is the name of the spellfix module and must be 
entered as shown. The "demo" term is the
name of the virtual table you will be creating and can be altered
to suit the needs of your application. The virtual table is initially
empty. In order for the virtual table to be useful, you will need to
populate it with your vocabulary. Suppose you
have a list of words in a table named "big\_vocabulary". Then do this:




> ```
> 
> INSERT INTO demo(word) SELECT word FROM big_vocabulary;
> 
> ```


If you intend to use this virtual table in cooperation with an [FTS4](fts3.html#fts4)
table (for spelling correction of search terms) then you might extract
the vocabulary using an [fts4aux](fts3.html#fts4aux) table:




> ```
> 
> INSERT INTO demo(word) SELECT term FROM search_aux WHERE col='*';
> 
> ```


You can also provide the virtual table with a "rank" for each word.
The "rank" is an estimate of how common the word is. Larger numbers
mean the word is more common. If you omit the rank when populating
the table, then a rank of 1 is assumed. But if you have rank 
information, you can supply it and the virtual table will show a
slight preference for selecting more commonly used terms. To
populate the rank from an fts4aux table "search\_aux" do something
like this:




> ```
> 
> INSERT INTO demo(word,rank)
>    SELECT term, documents FROM search_aux WHERE col='*';
> 
> ```


To query the virtual table, include a MATCH operator in the WHERE
clause. For example:




> ```
> 
> SELECT word FROM demo WHERE word MATCH 'kennasaw';
> 
> ```


Using a dataset of American place names (derived from
<http://geonames.usgs.gov/domestic/download_data.htm>) the query above
returns 20 results beginning with:




> ```
> 
> kennesaw
> kenosha
> kenesaw
> kenaga
> keanak
> 
> ```


If you append the character '\*' to the end of the pattern, then
a prefix search is performed. For example:




> ```
> 
> SELECT word FROM demo WHERE word MATCH 'kennes*';
> 
> ```


Yields 20 results beginning with:




> ```
> 
> kennesaw
> kennestone
> kenneson
> kenneys
> keanes
> keenes
> 
> ```


# 2\. Search Refinements


By default, the spellfix1 table returns no more than 20 results.
(It might return less than 20 if there were fewer good matches.)
You can change the upper bound on the number of returned rows by
adding a "top\=N" term to the WHERE clause of your query, where N
is the new maximum. For example, to see the 5 best matches:




> ```
> 
> SELECT word FROM demo WHERE word MATCH 'kennes*' AND top=5;
> 
> ```


Each entry in the spellfix1 virtual table is associated with
a particular language, identified by the integer "langid" column.
The default langid is 0 and if no other actions are taken, the
entire vocabulary is a part of the 0 language. But if your application
needs to operate in multiple languages, then you can specify different
vocabulary items for each language by specifying the langid field
when populating the table. For example:




> ```
> 
> INSERT INTO demo(word,langid) SELECT word, 0 FROM en_vocabulary;
> INSERT INTO demo(word,langid) SELECT word, 1 FROM de_vocabulary;
> INSERT INTO demo(word,langid) SELECT word, 2 FROM fr_vocabulary;
> INSERT INTO demo(word,langid) SELECT word, 3 FROM ru_vocabulary;
> INSERT INTO demo(word,langid) SELECT word, 4 FROM cn_vocabulary;
> 
> ```


After the virtual table has been populated with items from multiple
languages, specify the language of interest using a "langid\=N" term
in the WHERE clause of the query:




> ```
> 
> SELECT word FROM demo WHERE word MATCH 'hildes*' AND langid=1;
> 
> ```


Note that if you do not include the "langid\=N" term in the WHERE clause,
the search will be against language 0 (English in the example above.)
All spellfix1 searches are against a single language id. There is no
way to search all languages at once.
 



# 3\. Virtual Table Details


Each row in the spellfix1 virtual table has a unique rowid 
with seven columns plus five extra hidden columns.
The columns are as follows:




**rowid**


A unique integer number associated with each
vocabulary item in the table. This can be used
as a foreign key on other tables in the database.

**word**


The text of the word that matches the pattern.
Both word and pattern can contain unicode characters
and can be mixed case.

**rank**


This is the rank of the word, as specified in the
original INSERT statement.


**distance**


This is an edit distance or Levenshtein distance going
from the pattern to the word.

**langid**


This is the language\-id of the word. All queries are
against a single language\-id, which defaults to 0\.
For any given query this value is the same on all rows.

**score**


The score is a combination of rank and distance. The
idea is that a lower score is better. The virtual table
attempts to find words with the lowest score and 
by default (unless overridden by ORDER BY) returns
results in order of increasing score.

**matchlen**


In a prefix search, the matchlen is the number of characters in
the string that match against the prefix. For a non\-prefix search,
this is the same as length(word).

**phonehash**


This column shows the phonetic hash prefix that was used to restrict
the search. For any given query, this column should be the same for
every row. This information is available for diagnostic purposes and
is not normally considered useful in real applications.

**top**


(HIDDEN) For any query, this value is the same on all
rows. It is an integer which is the maximum number of
rows that will be output. The actually number of rows
output might be less than this number, but it will never
be greater. The default value for top is 20, but that
can be changed for each query by including a term of
the form "top\=N" in the WHERE clause of the query.

**scope**


(HIDDEN) For any query, this value is the same on all
rows. The scope is a measure of how widely the virtual
table looks for matching words. Smaller values of
scope cause a broader search. The scope is normally
chosen automatically and is capped at 4\. Applications
can change the scope by including a term of the form
"scope\=N" in the WHERE clause of the query. Increasing
the scope will make the query run faster, but will reduce
the possible corrections.

**srchcnt**


(HIDDEN) For any query, this value is the same on all
rows. This value is an integer which is the number of
words examined using the edit\-distance algorithm to
find the top matches that are ultimately displayed. This
value is for diagnostic use only.

**soundslike**


(HIDDEN) When inserting vocabulary entries, this field
can be set to a spelling that matches what the word
sounds like. See the DEALING WITH UNUSUAL AND DIFFICULT
SPELLINGS section below for details.

**command**


(HIDDEN) The value of the "command" column is always NULL. However,
applications can insert special strings into the "command" column in order
to provoke certain behaviors in the spellfix1 virtual table.
For example, inserting the string 'reset' into the "command" column
will cause the virtual table to reread its edit distance weights
(if there are any).

# 4\. Algorithm


The spellfix1 virtual table creates a single
shadow table named "%\_vocab" (where the % is replaced by the name of
the virtual table; Ex: "demo\_vocab" for the "demo" virtual table). 
the shadow table contains the following columns:




**id**


The unique id (INTEGER PRIMARY KEY)

**rank**


The rank of word.

**langid**


The language id for this entry.

**word**


The original UTF8 text of the vocabulary word

**k1**


The word transliterated into lower\-case ASCII. 
There is a standard table of mappings from non\-ASCII
characters into ASCII. Examples: "æ" \-\> "ae",
"þ" \-\> "th", "ß" \-\> "ss", "á" \-\> "a", ... The
accessory function spellfix1\_translit(X) will do
the non\-ASCII to ASCII mapping. The built\-in lower(X)
function will convert to lower\-case. Thus:
k1 \= lower(spellfix1\_translit(word)).

If the word is already all lower\-case ASCII, then the k1 column
will contain a NULL. This reduces the storage requirements for
the %\_vocab table and helps spellfix to run a little faster.
Therefore, it is advantageous to populate as much of the spellfix
table as possible using lower\-case ASCII vocabulary.

**k2**


This field holds a phonetic code derived from coalesce(k1,word).
Letters that have similar sounds are mapped into the same symbol.
For example, all vowels and vowel clusters become the
single symbol "A". And the letters "p", "b", "f", and
"v" all become "B". All nasal sounds are represented
as "N". And so forth. The mapping is based on
ideas found in Soundex, Metaphone, and other
long\-standing phonetic matching systems. This key can
be generated by the function spellfix1\_phonehash(X). 
Hence: k2 \= spellfix1\_phonehash(coalesce(k1,word))

There is also a function for computing the Wagner edit distance or the
Levenshtein distance between a pattern and a word. This function
is exposed as spellfix1\_editdist(X,Y). The edit distance function
returns the "cost" of converting X into Y. Some transformations
cost more than others. Changing one vowel into a different vowel,
for example is relatively cheap, as is doubling a constant, or
omitting the second character of a double\-constant. Other transformations
or more expensive. The idea is that the edit distance function returns
a low cost for words that are similar and a higher cost for words
that are further apart. In this implementation, the maximum cost
of any single\-character edit (delete, insert, or substitute) is 100,
with lower costs for some edits (such as transforming vowels).



The "score" for a comparison is the edit distance between the pattern
and the word, adjusted down by the base\-2 logarithm of the word rank.
For example, a match with distance 100 but rank 1000 would have a
score of 122 (\= 100 \- log2(1000\) \+ 32\) whereas a match with distance
100 with a rank of 1 would have a score of 131 (100 \- log2(1\) \+ 32\).
(NB: The constant 32 is added to each score to keep it from going
negative in case the edit distance is zero.) In this way, frequently
used words get a slightly lower cost which tends to move them toward
the top of the list of alternative spellings.



A straightforward implementation of a spelling corrector would be
to compare the search term against every word in the vocabulary
and select the 20 with the lowest scores. However, there will 
typically be hundreds of thousands or millions of words in the
vocabulary, and so this approach is not fast enough.



Suppose the term that is being spell\-corrected is X. To limit
the search space, X is converted to a k2\-like key using the
equivalent of:




> ```
> 
>    key = spellfix1_phonehash(lower(spellfix1_translit(X)))
> 
> ```


This key is then limited to "scope" characters. The default scope
value is 4, but an alternative scope can be specified using the
"scope\=N" term in the WHERE clause. After the key has been truncated,
the edit distance is run against every term in the vocabulary that
has a k2 value that begins with the abbreviated key.



For example, suppose the input word is "Paskagula". The phonetic 
key is "BACACALA" which is then truncated to 4 characters "BACA".
The edit distance is then run on the 4980 entries (out of
272,597 entries total) of the vocabulary whose k2 values begin with
BACA, yielding "Pascagoula" as the best match.



Only terms of the vocabulary with a matching langid are searched.
Hence, the same table can contain entries from multiple languages
and only the requested language will be used. The default langid
is 0\.




# 5\. Configurable Edit Distance


The built\-in Wagner edit\-distance function with fixed weights can be
replaced by the [editdist3()](spellfix1.html#editdist3) edit\-distance function
with application\-defined weights and support for unicode, by specifying
the "edit\_cost\_table\=*TABLENAME*" parameter to the spellfix1 module
when the virtual table is created.
For example:




> ```
> 
> CREATE VIRTUAL TABLE demo2 USING spellfix1(edit_cost_table=APPCOST);
> 
> ```


The [editdist3()](spellfix1.html#editdist3) edit\-distance function can also be selected or 
deselected at run\-time by inserting an appropriate string into the
"command" column of the virtual table:



> ```
> 
> INSERT INTO demo2(command) VALUES('edit_cost_table=APPCOST');
> 
> ```


In the examples above, the APPCOST table would be interrogated to find
the edit distance coefficients. It is the presence of the "edit\_cost\_table\="
parameter to the spellfix1 module name that causes editdist3() to be used
in place of the built\-in edit distance function. If APPCOST is an empty
string, then the built\-in Wagner edit\-distance function is used.



The edit distance coefficients are normally read from the APPCOST table
once and there after stored in memory. Hence, run\-time changes to the
APPCOST table will not normally affect the edit distance results.
However, inserting the special string 'reset' into the "command" column of the
virtual table causes the edit distance coefficients to be reread the
APPCOST table. Hence, applications should run a SQL statement similar
to the following when changes to the APPCOST table occur:




> INSERT INTO demo2(command) VALUES("reset");


# 6\. Dealing With Unusual And Difficult Spellings


The algorithm above works quite well for most cases, but there are
exceptions. These exceptions can be dealt with by making additional
entries in the virtual table using the "soundslike" column.



For example, many words of Greek origin begin with letters "ps" where
the "p" is silent. Ex: psalm, pseudonym, psoriasis, psyche. In
another example, many Scottish surnames can be spelled with an
initial "Mac" or "Mc". Thus, "MacKay" and "McKay" are both pronounced
the same.



Accommodation can be made for words that are not spelled as they
sound by making additional entries into the virtual table for the
same word, but adding an alternative spelling in the "soundslike"
column. For example, the canonical entry for "psalm" would be this:




> ```
> 
>   INSERT INTO demo(word) VALUES('psalm');
> 
> ```


To enhance the ability to correct the spelling of "salm" into
"psalm", make an addition entry like this:




> ```
> 
>   INSERT INTO demo(word,soundslike) VALUES('psalm','salm');
> 
> ```


It is ok to make multiple entries for the same word as long as
each entry has a different soundslike value. Note that if no
soundslike value is specified, the soundslike defaults to the word
itself.



Listed below are some cases where it might make sense to add additional
soundslike entries. The specific entries will depend on the application
and the target language.



* Silent "p" in words beginning with "ps": psalm, psyche
* Silent "p" in words beginning with "pn": pneumonia, pneumatic
* Silent "p" in words beginning with "pt": pterodactyl, ptolemaic
* Silent "d" in words beginning with "dj": djinn, Djikarta
* Silent "k" in words beginning with "kn": knight, Knuthson
* Silent "g" in words beginning with "gn": gnarly, gnome, gnat
* "Mac" versus "Mc" beginning Scottish surnames
* "Tch" sounds in Slavic words: Tchaikovsky vs. Chaykovsky
* The letter "j" pronounced like "h" in Spanish: LaJolla
* Words beginning with "wr" versus "r": write vs. rite
* Miscellaneous problem words such as "debt", "tsetse",
 "Nguyen", "Van Nuyes".


# 7\. Auxiliary Functions


The source code module that implements the spellfix1 virtual table also
implements several SQL functions that might be useful to applications
that employ spellfix1 or for testing or diagnostic work while developing
applications that use spellfix1\. The following auxiliary functions are
available:




**editdist3(P,W)  
editdist3(P,W,L)  
editdist3(T)**


These routines provide direct access to the version of the Wagner
edit\-distance function that allows for application\-defined weights
on edit operations. The first two forms of this function compare
pattern P against word W and return the edit distance. In the first
function, the langid is assumed to be 0 and in the second, the
langid is given by the L parameter. The third form of this function
reloads edit distance coefficients from the table named by T.

**spellfix1\_editdist(P,W)**


This routine provides access to the built\-in Wagner edit\-distance
function that uses default, fixed costs. The value returned is
the edit distance needed to transform W into P.

**spellfix1\_phonehash(X)**


This routine constructs a phonetic hash of the pure ascii input word X
and returns that hash. This routine is used internally by spellfix1 in
order to transform the K1 column of the shadow table into the K2
column.

**spellfix1\_scriptcode(X)**


Given an input string X, this routine attempts to determine the dominant
script of that input and returns the ISO\-15924 numeric code for that
script. The current implementation understands the following scripts:
* 215 \- Latin
* 220 \- Cyrillic
* 200 \- Greek


Additional language codes might be added in future releases.

**spellfix1\_translit(X)**


This routine transliterates unicode text into pure ascii, returning
the pure ascii representation of the input text X. This is the function
that is used internally to transform vocabulary words into the K1
column of the shadow table.



# 8\. The editdist3 function


The editdist3 algorithm is a function that computes the minimum edit 
distance (a.k.a. the Levenshtein distance) between two input strings.
The editdist3 algorithm is a configurable alternative to the default
edit distance function of spellfix1\.
Features of editdist3 include:



* It works with unicode (UTF8\) text.
* A table of insertion, deletion, and substitution costs can be 
 provided by the application.
* Multi\-character insertions, deletions, and substitutions can be
 enumerated in the cost table.


# 9\. The editdist3 COST table


To program the costs of editdist3, create a table such as the following:




> ```
> 
> CREATE TABLE editcost(
>   iLang INT,   -- The language ID
>   cFrom TEXT,  -- Convert text from this
>   cTo   TEXT,  -- Convert text into this
>   iCost INT    -- The cost of doing the conversion
> );
> 
> ```


The cost table can be named anything you want \- it does not have to be
called "editcost". And the table can contain additional columns.
The only requirement is that the
table must contain the four columns show above, with exactly the names shown.



The iLang column is a non\-negative integer that identifies a set of costs
appropriate for a particular language. The editdist3 function will only use
a single iLang value for any given edit\-distance computation. The default
value is 0\. It is recommended that applications that only need to use a
single language always use iLang\=\=0 for all entries.



The iCost column is the numeric cost of transforming cFrom into cTo. This
value should be a non\-negative integer, and should probably be less than 100\.
The default single\-character insertion and deletion costs are 100 and the
default single\-character to single\-character substitution cost is 150\. A
cost of 10000 or more is considered "infinite" and causes the rule to be
ignored.



The cFrom and cTo columns show edit transformation strings. Either or both
columns may contain more than one character. Or either column (but not both)
may hold an empty string. When cFrom is empty, that is the cost of inserting
cTo. When cTo is empty, that is the cost of deleting cFrom.



In the spellfix1 algorithm, cFrom is the text as the user entered it and
cTo is the correctly spelled text as it exists in the database. The goal
of the editdist3 algorithm is to determine how close the user\-entered text is
to the dictionary text.



There are three special\-case entries in the cost table:





| cFrom | cTo | Meaning |
| --- | --- | --- |
| '' | '?' | The default insertion cost |
| '?' | '' | The default deletion cost |
| '?' | '?' | The default substitution cost |


If any of the special\-case entries shows above are omitted, then the
value of 100 is used for insertion and deletion and 150 is used for
substitution. To disable the default insertion, deletion, and/or substitution
set their respective cost to 10000 or more.



Other entries in the cost table specific transforms for particular 
characters.
The cost of specific transforms should be less than the default costs, or else
the default costs will take precedence and the specific transforms will never 
be used.



Some example, cost table entries:




> ```
> 
> INSERT INTO editcost(iLang, cFrom, cTo, iCost)
> VALUES(0, 'a', 'ä', 5);
> 
> ```


The rule above says that the letter "a" in user input can be matched against
the letter "ä" in the dictionary with a penalty of 5\.




> ```
> 
> INSERT INTO editcost(iLang, cFrom, cTo, iCost)
> VALUES(0, 'ss', 'ß', 8);
> 
> ```


The number of characters in cFrom and cTo do not need to be the same. The
rule above says that "ss" on user input will match "ß" with a penalty of 8\.



# 10\. Experimenting with the editcost3() function


The spellfix1 virtual table
uses editdist3 if the "edit\_cost\_table\=TABLE" option
is specified as an argument when the spellfix1 virtual table is created. 
But editdist3 can also be tested directly using the built\-in "editdist3()"
SQL function. The editdist3() SQL function has 3 forms:



1. editdist3('TABLENAME');
2. editdist3('string1', 'string2');
3. editdist3('string1', 'string2', langid);


The first form loads the edit distance coefficients from a table called
'TABLENAME'. Any prior coefficients are discarded. So when experimenting
with weights and the weight table changes, simply rerun the single\-argument
form of editdist3() to reload revised coefficients. Note that the 
edit distance
weights used by the editdist3() SQL function are independent from the
weights used by the spellfix1 virtual table.



The second and third forms return the computed edit distance between strings
'string1' and "string2'. In the second form, a language id of 0 is used.
The language id is specified in the third form.



