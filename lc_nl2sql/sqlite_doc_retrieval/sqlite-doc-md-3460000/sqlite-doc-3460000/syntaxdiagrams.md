




Syntax Diagrams For SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# Syntax Diagrams For SQLite


#### aggregate\-function\-invocation:







aggregate\-func



(





DISTINCT







expr



)



filter\-clause












,





\*











ORDER



BY



ordering\-term

,







  

References:   [expr](#expr)   [filter\-clause](#filter-clause)   [ordering\-term](#ordering-term)  

See also:   <lang_aggfunc.html>   [lang\_expr.html\#\*funcinexpr](lang_expr.html#*funcinexpr)

#### alter\-table\-stmt:








ALTER



TABLE





schema\-name



.



table\-name











RENAME



TO



new\-table\-name



RENAME





COLUMN



column\-name



TO



new\-column\-name














ADD





COLUMN



column\-def











DROP





COLUMN



column\-name









Used by:   [sql\-stmt](#sql-stmt)  

References:   [column\-def](#column-def)  

See also:   <lang_altertable.html>

#### analyze\-stmt:







ANALYZE





schema\-name



.



table\-or\-index\-name











schema\-name






index\-or\-table\-name






Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_analyze.html>

#### attach\-stmt:







ATTACH





DATABASE



expr



AS



schema\-name









Used by:   [sql\-stmt](#sql-stmt)  

References:   [expr](#expr)  

See also:   <lang_attach.html>

#### begin\-stmt:







BEGIN





EXCLUSIVE







TRANSACTION










DEFERRED






IMMEDIATE






Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_transaction.html>

#### column\-constraint:











CONSTRAINT



name






PRIMARY



KEY



DESC





conflict\-clause





AUTOINCREMENT














ASC






NOT



NULL



conflict\-clause






UNIQUE



conflict\-clause






CHECK



(



expr



)






DEFAULT





(



expr



)






literal\-value






signed\-number






COLLATE



collation\-name






foreign\-key\-clause






GENERATED



ALWAYS



AS



(



expr



)









VIRTUAL






STORED






Used by:   [column\-def](#column-def)  

References:   [conflict\-clause](#conflict-clause)   [expr](#expr)   [foreign\-key\-clause](#foreign-key-clause)   [literal\-value](#literal-value)   [signed\-number](#signed-number)  

See also:   <gencol.html>   <lang_altertable.html>   <lang_createtable.html>   [lang\_createtable.html\#tablecoldef](lang_createtable.html#tablecoldef)

#### column\-def:







column\-name





type\-name



column\-constraint















Used by:   [alter\-table\-stmt](#alter-table-stmt)   [create\-table\-stmt](#create-table-stmt)  

References:   [column\-constraint](#column-constraint)   [type\-name](#type-name)  

See also:   <lang_altertable.html>   [lang\_altertable.html\#altertabaddcol](lang_altertable.html#altertabaddcol)   <lang_createtable.html>   [lang\_createtable.html\#tablecoldef](lang_createtable.html#tablecoldef)

#### column\-name\-list:







(





column\-name



)




,







Used by:   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)   [upsert\-clause](#upsert-clause)  

See also:   <lang_createtrigger.html>   <lang_insert.html>   <lang_update.html>   <lang_upsert.html>

#### comment\-syntax:









\-\-



anything\-except\-newline









newline

end\-of\-input









/\*






anything\-except\-\*/

\*/










  

See also:   <lang_comment.html>

#### commit\-stmt:









COMMIT




TRANSACTION




END











Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_transaction.html>

#### common\-table\-expression:







table\-name





(





column\-name



)



AS

NOT

MATERIALIZED


(



select\-stmt



)




,






















Used by:   [compound\-select\-stmt](#compound-select-stmt)   [delete\-stmt](#delete-stmt)   [delete\-stmt\-limited](#delete-stmt-limited)   [factored\-select\-stmt](#factored-select-stmt)   [insert\-stmt](#insert-stmt)   [select\-stmt](#select-stmt)   [simple\-select\-stmt](#simple-select-stmt)   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)  

References:   [select\-stmt](#select-stmt)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### compound\-operator:









UNION

UNION

INTERSECT

EXCEPT



ALL





















Used by:   [factored\-select\-stmt](#factored-select-stmt)   [select\-stmt](#select-stmt)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### compound\-select\-stmt:









WITH

RECURSIVE





common\-table\-expression






,




select\-core

ORDER



BY

LIMIT



expr








UNION

UNION



ALL





select\-core

INTERSECT

EXCEPT























ordering\-term

,













OFFSET



expr



,



expr




















  

References:   [common\-table\-expression](#common-table-expression)   [expr](#expr)   [ordering\-term](#ordering-term)   [select\-core](#select-core)  

See also:   [lang\_select.html\#compound](lang_select.html#compound)

#### conflict\-clause:









ON



CONFLICT



ROLLBACK

ABORT

FAIL

IGNORE

REPLACE































Used by:   [column\-constraint](#column-constraint)   [table\-constraint](#table-constraint)  

See also:   <lang_altertable.html>   <lang_conflict.html>   <lang_createtable.html>   [lang\_createtable.html\#notnullconst](lang_createtable.html#notnullconst)

#### create\-index\-stmt:







CREATE

UNIQUE

INDEX










IF



NOT



EXISTS








schema\-name



.



index\-name



ON



table\-name



(



indexed\-column



)

,







WHERE



expr













Used by:   [sql\-stmt](#sql-stmt)  

References:   [expr](#expr)   [indexed\-column](#indexed-column)  

See also:   <lang_createindex.html>   <partialindex.html>

#### create\-table\-stmt:







CREATE

TEMP

TEMPORARY

TABLE













IF



NOT



EXISTS








schema\-name



.



table\-name








(



column\-def

table\-constraint



,

)



table\-options

,




















AS



select\-stmt






Used by:   [sql\-stmt](#sql-stmt)  

References:   [column\-def](#column-def)   [select\-stmt](#select-stmt)   [table\-constraint](#table-constraint)   [table\-options](#table-options)  

See also:   <lang_createtable.html>

#### create\-trigger\-stmt:







CREATE

TEMP

TEMPORARY

TRIGGER













IF



NOT



EXISTS








schema\-name



.



trigger\-name



BEFORE

AFTER

INSTEAD



OF





















DELETE

INSERT

UPDATE







OF



column\-name

,





ON



table\-name













FOR



EACH



ROW



WHEN



expr

BEGIN



update\-stmt



;



END




insert\-stmt

delete\-stmt

select\-stmt



































Used by:   [sql\-stmt](#sql-stmt)  

References:   [delete\-stmt](#delete-stmt)   [expr](#expr)   [insert\-stmt](#insert-stmt)   [select\-stmt](#select-stmt)   [update\-stmt](#update-stmt)  

See also:   <lang_createtrigger.html>

#### create\-view\-stmt:







CREATE

TEMP

TEMPORARY

VIEW













IF



NOT



EXISTS








schema\-name



.



view\-name



(



column\-name



)



AS



select\-stmt










,






Used by:   [sql\-stmt](#sql-stmt)  

References:   [select\-stmt](#select-stmt)  

See also:   <lang_createview.html>

#### create\-virtual\-table\-stmt:







CREATE



VIRTUAL



TABLE



IF



NOT



EXISTS

schema\-name



.



table\-name

USING



module\-name



(



module\-argument



)




,























Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_createvtab.html>

#### cte\-table\-name:







table\-name



(



column\-name



)




,









Used by:   [recursive\-cte](#recursive-cte)   [with\-clause](#with-clause)  

See also:   <lang_with.html>   [lang\_with.html\#recursivecte](lang_with.html#recursivecte)

#### delete\-stmt:









WITH

RECURSIVE





common\-table\-expression






,




DELETE



FROM



qualified\-table\-name



returning\-clause





expr



WHERE
















Used by:   [create\-trigger\-stmt](#create-trigger-stmt)   [sql\-stmt](#sql-stmt)  

References:   [common\-table\-expression](#common-table-expression)   [expr](#expr)   [qualified\-table\-name](#qualified-table-name)   [returning\-clause](#returning-clause)  

See also:   <lang_createtrigger.html>   <lang_delete.html>

#### delete\-stmt\-limited:







WITH

RECURSIVE





common\-table\-expression






,




DELETE



FROM



qualified\-table\-name






WHERE



expr

returning\-clause

ORDER



BY



ordering\-term

,

LIMIT



expr



OFFSET



expr

,



expr












































Used by:   [sql\-stmt](#sql-stmt)  

References:   [common\-table\-expression](#common-table-expression)   [expr](#expr)   [ordering\-term](#ordering-term)   [qualified\-table\-name](#qualified-table-name)   [returning\-clause](#returning-clause)  

See also:   <lang_delete.html>

#### detach\-stmt:







DETACH



DATABASE



schema\-name









Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_detach.html>

#### drop\-index\-stmt:







DROP



INDEX



IF



EXISTS



schema\-name



.



index\-name












Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_dropindex.html>

#### drop\-table\-stmt:







DROP



TABLE



IF



EXISTS



schema\-name



.



table\-name












Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_droptable.html>

#### drop\-trigger\-stmt:







DROP



TRIGGER



IF



EXISTS



schema\-name



.



trigger\-name












Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_droptrigger.html>

#### drop\-view\-stmt:







DROP



VIEW



IF



EXISTS



schema\-name



.



view\-name












Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_dropview.html>

#### expr:







literal\-value




bind\-parameter






schema\-name



.



table\-name



.



column\-name












unary\-operator



expr






expr



binary\-operator



expr






function\-name



(



function\-arguments



)



filter\-clause





over\-clause












(



expr



)






,




CAST



(



expr



AS



type\-name



)






expr



COLLATE



collation\-name






expr



NOT



LIKE

GLOB

REGEXP

MATCH

expr

expr



ESCAPE



expr

































expr



ISNULL






NOTNULL

NOT



NULL












expr



IS



NOT





DISTINCT



FROM



expr








expr



NOT



BETWEEN



expr



AND



expr







expr



NOT



IN



(



select\-stmt



)








expr




,




schema\-name



.



table\-function



(



expr



)




table\-name






,










NOT



EXISTS



(



select\-stmt



)










CASE



expr



WHEN



expr



THEN



expr



ELSE



expr



END











raise\-function








Used by:   [aggregate\-function\-invocation](#aggregate-function-invocation)   [attach\-stmt](#attach-stmt)   [column\-constraint](#column-constraint)   [compound\-select\-stmt](#compound-select-stmt)   [create\-index\-stmt](#create-index-stmt)   [create\-trigger\-stmt](#create-trigger-stmt)   [delete\-stmt](#delete-stmt)   [delete\-stmt\-limited](#delete-stmt-limited)   [factored\-select\-stmt](#factored-select-stmt)   [filter\-clause](#filter-clause)   [frame\-spec](#frame-spec)   [function\-arguments](#function-arguments)   [indexed\-column](#indexed-column)   [insert\-stmt](#insert-stmt)   [join\-constraint](#join-constraint)   [ordering\-term](#ordering-term)   [over\-clause](#over-clause)   [result\-column](#result-column)   [returning\-clause](#returning-clause)   [select\-core](#select-core)   [select\-stmt](#select-stmt)   [simple\-function\-invocation](#simple-function-invocation)   [simple\-select\-stmt](#simple-select-stmt)   [table\-constraint](#table-constraint)   [table\-or\-subquery](#table-or-subquery)   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)   [upsert\-clause](#upsert-clause)   [window\-defn](#window-defn)   [window\-function\-invocation](#window-function-invocation)  

References:   [filter\-clause](#filter-clause)   [function\-arguments](#function-arguments)   [literal\-value](#literal-value)   [over\-clause](#over-clause)   [raise\-function](#raise-function)   [select\-stmt](#select-stmt)   [type\-name](#type-name)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### factored\-select\-stmt:







WITH

RECURSIVE





common\-table\-expression






,




select\-core

ORDER



BY

LIMIT



expr






compound\-operator










ordering\-term

,













OFFSET



expr



,



expr




















  

References:   [common\-table\-expression](#common-table-expression)   [compound\-operator](#compound-operator)   [expr](#expr)   [ordering\-term](#ordering-term)   [select\-core](#select-core)  

See also:   <lang_select.html>

#### filter\-clause:







FILTER



(



WHERE



expr



)






Used by:   [aggregate\-function\-invocation](#aggregate-function-invocation)   [expr](#expr)   [window\-function\-invocation](#window-function-invocation)  

References:   [expr](#expr)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### foreign\-key\-clause:







REFERENCES



foreign\-table



(



column\-name



)

,




ON



DELETE



SET



NULL

UPDATE




SET



DEFAULT




CASCADE




RESTRICT




NO



ACTION




MATCH



name























NOT



DEFERRABLE



INITIALLY



DEFERRED

INITIALLY



IMMEDIATE




















Used by:   [column\-constraint](#column-constraint)   [table\-constraint](#table-constraint)  

See also:   <lang_altertable.html>   [lang\_altertable.html\#altertabaddcol](lang_altertable.html#altertabaddcol)   <lang_createtable.html>

#### frame\-spec:







GROUPS




BETWEEN



UNBOUNDED



PRECEDING



AND



UNBOUNDED



FOLLOWING




RANGE






ROWS






UNBOUNDED



PRECEDING




expr



PRECEDING






CURRENT



ROW






expr



PRECEDING






CURRENT



ROW






expr



FOLLOWING








expr



PRECEDING




CURRENT



ROW






expr



FOLLOWING






EXCLUDE



CURRENT



ROW




EXCLUDE



GROUP




EXCLUDE



TIES




EXCLUDE



NO



OTHERS





















Used by:   [over\-clause](#over-clause)   [window\-defn](#window-defn)  

References:   [expr](#expr)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### function\-arguments:









DISTINCT







expr








,





\*











ORDER



BY



ordering\-term

,








Used by:   [expr](#expr)  

References:   [expr](#expr)   [ordering\-term](#ordering-term)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### indexed\-column:







column\-name



COLLATE



collation\-name





DESC








expr









ASC








Used by:   [create\-index\-stmt](#create-index-stmt)   [table\-constraint](#table-constraint)   [upsert\-clause](#upsert-clause)  

References:   [expr](#expr)  

See also:   <lang_createindex.html>   <lang_createtable.html>   [lang\_createtable.html\#primkeyconst](lang_createtable.html#primkeyconst)   [lang\_createtable.html\#uniqueconst](lang_createtable.html#uniqueconst)   <lang_createtrigger.html>   <lang_insert.html>   <lang_upsert.html>   <partialindex.html>

#### insert\-stmt:







WITH

RECURSIVE





common\-table\-expression






,








REPLACE

INSERT



OR



ROLLBACK





INTO










ABORT






FAIL






IGNORE






REPLACE






schema\-name



.



table\-name



AS



alias










(



column\-name



)

,














VALUES



(



expr



)



,




,






upsert\-clause






select\-stmt






upsert\-clause






DEFAULT



VALUES





returning\-clause











Used by:   [create\-trigger\-stmt](#create-trigger-stmt)   [sql\-stmt](#sql-stmt)  

References:   [common\-table\-expression](#common-table-expression)   [expr](#expr)   [returning\-clause](#returning-clause)   [select\-stmt](#select-stmt)   [upsert\-clause](#upsert-clause)  

See also:   <lang_createtrigger.html>   <lang_insert.html>

#### join\-clause:







table\-or\-subquery



join\-operator



table\-or\-subquery



join\-constraint












Used by:   [select\-core](#select-core)   [select\-stmt](#select-stmt)   [table\-or\-subquery](#table-or-subquery)   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)  

References:   [join\-constraint](#join-constraint)   [join\-operator](#join-operator)   [table\-or\-subquery](#table-or-subquery)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### join\-constraint:







USING



(



column\-name



)






,






ON



expr









Used by:   [join\-clause](#join-clause)  

References:   [expr](#expr)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#fromclause](lang_select.html#fromclause)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### join\-operator:







NATURAL





LEFT



OUTER





JOIN




,












RIGHT





FULL




INNER






CROSS






Used by:   [join\-clause](#join-clause)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#fromclause](lang_select.html#fromclause)   [lang\_select.html\#nonstd](lang_select.html#nonstd)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### literal\-value:







CURRENT\_TIMESTAMP






numeric\-literal




string\-literal






blob\-literal






NULL






TRUE






FALSE






CURRENT\_TIME






CURRENT\_DATE








Used by:   [column\-constraint](#column-constraint)   [expr](#expr)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### numeric\-literal:







digit

\_










.









E





e


digit

\_













.



digit

\_













\-



digit

\_








\+

















0x





0X

hexdigit

\_
















  

See also:   [lang\_expr.html\#litvalue](lang_expr.html#litvalue)

#### ordering\-term:







expr



COLLATE



collation\-name








DESC



ASC









NULLS



FIRST



NULLS



LAST









Used by:   [aggregate\-function\-invocation](#aggregate-function-invocation)   [compound\-select\-stmt](#compound-select-stmt)   [delete\-stmt\-limited](#delete-stmt-limited)   [factored\-select\-stmt](#factored-select-stmt)   [function\-arguments](#function-arguments)   [over\-clause](#over-clause)   [select\-stmt](#select-stmt)   [simple\-select\-stmt](#simple-select-stmt)   [update\-stmt\-limited](#update-stmt-limited)   [window\-defn](#window-defn)  

References:   [expr](#expr)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### over\-clause:







OVER



window\-name



(



base\-window\-name

PARTITION



BY



expr

,













ORDER



BY



ordering\-term

,











frame\-spec



)




















Used by:   [expr](#expr)  

References:   [expr](#expr)   [frame\-spec](#frame-spec)   [ordering\-term](#ordering-term)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### pragma\-stmt:







PRAGMA



schema\-name



.



pragma\-name



(



pragma\-value



)






\=



pragma\-value












Used by:   [sql\-stmt](#sql-stmt)  

References:   [pragma\-value](#pragma-value)  

See also:   [pragma.html\#syntax](pragma.html#syntax)

#### pragma\-value:







signed\-number




name

signed\-literal













Used by:   [pragma\-stmt](#pragma-stmt)  

References:   [signed\-number](#signed-number)  

See also:   [pragma.html\#syntax](pragma.html#syntax)

#### qualified\-table\-name:







schema\-name



.



table\-name



AS



alias









INDEXED



BY



index\-name

NOT



INDEXED




















Used by:   [delete\-stmt](#delete-stmt)   [delete\-stmt\-limited](#delete-stmt-limited)   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)  

See also:   <lang_createtrigger.html>   <lang_delete.html>   <lang_indexedby.html>   <lang_update.html>

#### raise\-function:







RAISE



(



ROLLBACK



,



error\-message



)






IGNORE




ABORT




FAIL










Used by:   [expr](#expr)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   [lang\_createtrigger.html\#raise](lang_createtrigger.html#raise)   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### recursive\-cte:







cte\-table\-name



AS



(



initial\-select



UNION



ALL



recursive\-select



)






UNION



  

References:   [cte\-table\-name](#cte-table-name)  

See also:   [lang\_with.html\#recursivecte](lang_with.html#recursivecte)

#### reindex\-stmt:







REINDEX



schema\-name



.





index\-name








table\-name









collation\-name









Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_reindex.html>

#### release\-stmt:







RELEASE



SAVEPOINT



savepoint\-name









Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_savepoint.html>

#### result\-column:







expr



AS



column\-alias














\*






table\-name



.



\*






Used by:   [select\-core](#select-core)   [select\-stmt](#select-stmt)  

References:   [expr](#expr)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### returning\-clause:







RETURNING



expr



AS



column\-alias














\*






,







Used by:   [delete\-stmt](#delete-stmt)   [delete\-stmt\-limited](#delete-stmt-limited)   [insert\-stmt](#insert-stmt)   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)  

References:   [expr](#expr)  

See also:   <lang_createtrigger.html>   <lang_delete.html>   <lang_insert.html>   <lang_returning.html>   <lang_update.html>

#### rollback\-stmt:







ROLLBACK



TRANSACTION



TO



SAVEPOINT



savepoint\-name















Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_savepoint.html>   <lang_transaction.html>

#### savepoint\-stmt:







SAVEPOINT



savepoint\-name






Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_savepoint.html>

#### select\-core:







SELECT



DISTINCT



result\-column

,







ALL






FROM



table\-or\-subquery

join\-clause

,

















WHERE



expr










GROUP



BY



expr



HAVING



expr

,


















WINDOW



window\-name



AS



window\-defn

,




















VALUES



(



expr



)






,

,











Used by:   [compound\-select\-stmt](#compound-select-stmt)   [factored\-select\-stmt](#factored-select-stmt)   [simple\-select\-stmt](#simple-select-stmt)  

References:   [expr](#expr)   [join\-clause](#join-clause)   [result\-column](#result-column)   [table\-or\-subquery](#table-or-subquery)   [window\-defn](#window-defn)  

See also:   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)

#### select\-stmt:








WITH

RECURSIVE





common\-table\-expression






,













SELECT



DISTINCT



result\-column

,







ALL






FROM



table\-or\-subquery

join\-clause

,

















WHERE



expr










GROUP



BY



expr



HAVING



expr

,


















WINDOW



window\-name



AS



window\-defn

,



















VALUES



(



expr



)




,

,









compound\-operator





select\-core

ORDER



BY

LIMIT



expr



ordering\-term

,

















OFFSET



expr



,



expr





















Used by:   [common\-table\-expression](#common-table-expression)   [create\-table\-stmt](#create-table-stmt)   [create\-trigger\-stmt](#create-trigger-stmt)   [create\-view\-stmt](#create-view-stmt)   [expr](#expr)   [insert\-stmt](#insert-stmt)   [sql\-stmt](#sql-stmt)   [table\-or\-subquery](#table-or-subquery)   [with\-clause](#with-clause)  

References:   [common\-table\-expression](#common-table-expression)   [compound\-operator](#compound-operator)   [expr](#expr)   [join\-clause](#join-clause)   [ordering\-term](#ordering-term)   [result\-column](#result-column)   [table\-or\-subquery](#table-or-subquery)   [window\-defn](#window-defn)  

See also:   [changes.html\#version\_3\_35\_3](changes.html#version_3_35_3)   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   [lang\_with.html\#recursivecte](lang_with.html#recursivecte)   <partialindex.html>   [releaselog/3\_35\_3\.html](releaselog/3_35_3.html)   [releaselog/3\_35\_4\.html](releaselog/3_35_4.html)   [releaselog/3\_35\_5\.html](releaselog/3_35_5.html)

#### signed\-number:







\+



numeric\-literal






\-







Used by:   [column\-constraint](#column-constraint)   [pragma\-value](#pragma-value)   [type\-name](#type-name)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>   [pragma.html\#syntax](pragma.html#syntax)

#### simple\-function\-invocation:







simple\-func



(



expr



)




,







\*





  

References:   [expr](#expr)  

See also:   <lang_corefunc.html>   [lang\_expr.html\#\*funcinexpr](lang_expr.html#*funcinexpr)

#### simple\-select\-stmt:







WITH

RECURSIVE





common\-table\-expression






,




select\-core

ORDER



BY

LIMIT



expr








ordering\-term

,















OFFSET



expr



,



expr




















  

References:   [common\-table\-expression](#common-table-expression)   [expr](#expr)   [ordering\-term](#ordering-term)   [select\-core](#select-core)  

See also:   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)

#### sql\-stmt:







EXPLAIN



QUERY



PLAN









alter\-table\-stmt






analyze\-stmt






attach\-stmt






begin\-stmt






commit\-stmt






create\-index\-stmt






create\-table\-stmt






create\-trigger\-stmt






create\-view\-stmt






create\-virtual\-table\-stmt






delete\-stmt






delete\-stmt\-limited






detach\-stmt






drop\-index\-stmt






drop\-table\-stmt






drop\-trigger\-stmt






drop\-view\-stmt






insert\-stmt






pragma\-stmt






reindex\-stmt






release\-stmt






rollback\-stmt






savepoint\-stmt






select\-stmt






update\-stmt






update\-stmt\-limited






vacuum\-stmt








Used by:   [sql\-stmt\-list](#sql-stmt-list)  

References:   [alter\-table\-stmt](#alter-table-stmt)   [analyze\-stmt](#analyze-stmt)   [attach\-stmt](#attach-stmt)   [begin\-stmt](#begin-stmt)   [commit\-stmt](#commit-stmt)   [create\-index\-stmt](#create-index-stmt)   [create\-table\-stmt](#create-table-stmt)   [create\-trigger\-stmt](#create-trigger-stmt)   [create\-view\-stmt](#create-view-stmt)   [create\-virtual\-table\-stmt](#create-virtual-table-stmt)   [delete\-stmt](#delete-stmt)   [delete\-stmt\-limited](#delete-stmt-limited)   [detach\-stmt](#detach-stmt)   [drop\-index\-stmt](#drop-index-stmt)   [drop\-table\-stmt](#drop-table-stmt)   [drop\-trigger\-stmt](#drop-trigger-stmt)   [drop\-view\-stmt](#drop-view-stmt)   [insert\-stmt](#insert-stmt)   [pragma\-stmt](#pragma-stmt)   [reindex\-stmt](#reindex-stmt)   [release\-stmt](#release-stmt)   [rollback\-stmt](#rollback-stmt)   [savepoint\-stmt](#savepoint-stmt)   [select\-stmt](#select-stmt)   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)   [vacuum\-stmt](#vacuum-stmt)  

See also:   <lang.html>   <lang_explain.html>

#### sql\-stmt\-list:








sql\-stmt








;





  

References:   [sql\-stmt](#sql-stmt)  

See also:   <lang.html>

#### table\-constraint:







CONSTRAINT



name

PRIMARY



KEY



(



indexed\-column



)



conflict\-clause











,




UNIQUE




CHECK



(



expr



)






FOREIGN



KEY



(



column\-name



)



foreign\-key\-clause






,






Used by:   [create\-table\-stmt](#create-table-stmt)  

References:   [conflict\-clause](#conflict-clause)   [expr](#expr)   [foreign\-key\-clause](#foreign-key-clause)   [indexed\-column](#indexed-column)  

See also:   <lang_createtable.html>   [lang\_createtable.html\#primkeyconst](lang_createtable.html#primkeyconst)   [lang\_createtable.html\#tablecoldef](lang_createtable.html#tablecoldef)   [lang\_createtable.html\#uniqueconst](lang_createtable.html#uniqueconst)

#### table\-options:







WITHOUT



ROWID





STRICT





,






Used by:   [create\-table\-stmt](#create-table-stmt)  

See also:   <lang_createtable.html>

#### table\-or\-subquery:







schema\-name



.



table\-name



AS



table\-alias






INDEXED



BY



index\-name

NOT



INDEXED









table\-function\-name



(



expr



)



,












AS



table\-alias











(



select\-stmt



)









(



table\-or\-subquery



)






,






join\-clause




Used by:   [join\-clause](#join-clause)   [select\-core](#select-core)   [select\-stmt](#select-stmt)   [update\-stmt](#update-stmt)   [update\-stmt\-limited](#update-stmt-limited)  

References:   [expr](#expr)   [join\-clause](#join-clause)   [select\-stmt](#select-stmt)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### type\-name:







name



(



signed\-number



,



signed\-number



)






(



signed\-number



)












Used by:   [column\-def](#column-def)   [expr](#expr)  

References:   [signed\-number](#signed-number)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### update\-stmt:







WITH

RECURSIVE





common\-table\-expression






,








UPDATE






OR



ROLLBACK





qualified\-table\-name

OR



REPLACE






OR



IGNORE






OR



FAIL






OR



ABORT











SET



column\-name\-list



\=



expr



column\-name


,







FROM



table\-or\-subquery

,






join\-clause








WHERE



expr











returning\-clause





Used by:   [create\-trigger\-stmt](#create-trigger-stmt)   [sql\-stmt](#sql-stmt)  

References:   [column\-name\-list](#column-name-list)   [common\-table\-expression](#common-table-expression)   [expr](#expr)   [join\-clause](#join-clause)   [qualified\-table\-name](#qualified-table-name)   [returning\-clause](#returning-clause)   [table\-or\-subquery](#table-or-subquery)  

See also:   <lang_createtrigger.html>   <lang_update.html>

#### update\-stmt\-limited:







WITH

RECURSIVE





common\-table\-expression






,








UPDATE






OR



ROLLBACK





qualified\-table\-name

OR



REPLACE






OR



IGNORE






OR



FAIL






OR



ABORT











SET



column\-name\-list



\=



expr



column\-name


,







FROM



table\-or\-subquery

,






join\-clause








WHERE



expr






returning\-clause





ORDER



BY



ordering\-term

,

LIMIT



expr



OFFSET



expr

,



expr




























Used by:   [sql\-stmt](#sql-stmt)  

References:   [column\-name\-list](#column-name-list)   [common\-table\-expression](#common-table-expression)   [expr](#expr)   [join\-clause](#join-clause)   [ordering\-term](#ordering-term)   [qualified\-table\-name](#qualified-table-name)   [returning\-clause](#returning-clause)   [table\-or\-subquery](#table-or-subquery)  

See also:   [lang\_update.html\#upfrom](lang_update.html#upfrom)

#### upsert\-clause:








ON



CONFLICT



(



indexed\-column



)



WHERE



expr





DO





,



conflict target





UPDATE



SET



column\-name\-list



\=



expr



WHERE



expr




NOTHING






,








column\-name









Used by:   [insert\-stmt](#insert-stmt)  

References:   [column\-name\-list](#column-name-list)   [expr](#expr)   [indexed\-column](#indexed-column)  

See also:   <lang_createtrigger.html>   <lang_insert.html>   <lang_upsert.html>

#### vacuum\-stmt:







VACUUM



schema\-name





INTO



filename







Used by:   [sql\-stmt](#sql-stmt)  

See also:   <lang_vacuum.html>

#### window\-defn:







(



base\-window\-name

PARTITION



BY



expr

,













ORDER



BY



ordering\-term

,











frame\-spec



)

















Used by:   [select\-core](#select-core)   [select\-stmt](#select-stmt)   [window\-function\-invocation](#window-function-invocation)  

References:   [expr](#expr)   [frame\-spec](#frame-spec)   [ordering\-term](#ordering-term)  

See also:   <lang_aggfunc.html>   <lang_altertable.html>   <lang_attach.html>   <lang_createindex.html>   <lang_createtable.html>   <lang_createtrigger.html>   <lang_createview.html>   <lang_delete.html>   <lang_expr.html>   <lang_insert.html>   <lang_returning.html>   <lang_select.html>   [lang\_select.html\#compound](lang_select.html#compound)   [lang\_select.html\#simpleselect](lang_select.html#simpleselect)   <lang_update.html>   <lang_upsert.html>   <lang_with.html>   <partialindex.html>

#### window\-function\-invocation:







window\-func



(



expr



)



filter\-clause



OVER



window\-name







window\-defn


,







\*





  

References:   [expr](#expr)   [filter\-clause](#filter-clause)   [window\-defn](#window-defn)  

See also:   [lang\_expr.html\#\*funcinexpr](lang_expr.html#*funcinexpr)

#### with\-clause:







WITH



RECURSIVE




cte\-table\-name



AS



NOT



MATERIALIZED



(



select\-stmt



)






MATERIALIZED







,






  

References:   [cte\-table\-name](#cte-table-name)   [select\-stmt](#select-stmt)  

See also:   <lang_with.html>

*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


