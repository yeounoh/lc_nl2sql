




SQLite Syntax: expr




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







# expr








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






  


Used by:   [aggregate\-function\-invocation](./aggregate-function-invocation.html)   [attach\-stmt](./attach-stmt.html)   [column\-constraint](./column-constraint.html)   [compound\-select\-stmt](./compound-select-stmt.html)   [create\-index\-stmt](./create-index-stmt.html)   [create\-trigger\-stmt](./create-trigger-stmt.html)   [delete\-stmt](./delete-stmt.html)   [delete\-stmt\-limited](./delete-stmt-limited.html)   [factored\-select\-stmt](./factored-select-stmt.html)   [filter\-clause](./filter-clause.html)   [frame\-spec](./frame-spec.html)   [function\-arguments](./function-arguments.html)   [indexed\-column](./indexed-column.html)   [insert\-stmt](./insert-stmt.html)   [join\-constraint](./join-constraint.html)   [ordering\-term](./ordering-term.html)   [over\-clause](./over-clause.html)   [result\-column](./result-column.html)   [returning\-clause](./returning-clause.html)   [select\-core](./select-core.html)   [select\-stmt](./select-stmt.html)   [simple\-function\-invocation](./simple-function-invocation.html)   [simple\-select\-stmt](./simple-select-stmt.html)   [table\-constraint](./table-constraint.html)   [table\-or\-subquery](./table-or-subquery.html)   [update\-stmt](./update-stmt.html)   [update\-stmt\-limited](./update-stmt-limited.html)   [upsert\-clause](./upsert-clause.html)   [window\-defn](./window-defn.html)   [window\-function\-invocation](./window-function-invocation.html)  

References:   [filter\-clause](./filter-clause.html)   [function\-arguments](./function-arguments.html)   [literal\-value](./literal-value.html)   [over\-clause](./over-clause.html)   [raise\-function](./raise-function.html)   [select\-stmt](./select-stmt.html)   [type\-name](./type-name.html)  

See also:   [lang\_aggfunc.html](../lang_aggfunc.html)   [lang\_altertable.html](../lang_altertable.html)   [lang\_attach.html](../lang_attach.html)   [lang\_createindex.html](../lang_createindex.html)   [lang\_createtable.html](../lang_createtable.html)   [lang\_createtrigger.html](../lang_createtrigger.html)   [lang\_createview.html](../lang_createview.html)   [lang\_delete.html](../lang_delete.html)   [lang\_expr.html](../lang_expr.html)   [lang\_insert.html](../lang_insert.html)   [lang\_returning.html](../lang_returning.html)   [lang\_select.html](../lang_select.html)   [lang\_update.html](../lang_update.html)   [lang\_upsert.html](../lang_upsert.html)   [lang\_with.html](../lang_with.html)   [partialindex.html](../partialindex.html)

