




SQLite Syntax: select\-stmt




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







# select\-stmt









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



















  


Used by:   [common\-table\-expression](./common-table-expression.html)   [create\-table\-stmt](./create-table-stmt.html)   [create\-trigger\-stmt](./create-trigger-stmt.html)   [create\-view\-stmt](./create-view-stmt.html)   [expr](./expr.html)   [insert\-stmt](./insert-stmt.html)   [sql\-stmt](./sql-stmt.html)   [table\-or\-subquery](./table-or-subquery.html)   [with\-clause](./with-clause.html)  

References:   [common\-table\-expression](./common-table-expression.html)   [compound\-operator](./compound-operator.html)   [expr](./expr.html)   [join\-clause](./join-clause.html)   [ordering\-term](./ordering-term.html)   [result\-column](./result-column.html)   [table\-or\-subquery](./table-or-subquery.html)   [window\-defn](./window-defn.html)  

See also:   [changes.html](../changes.html)   [lang\_aggfunc.html](../lang_aggfunc.html)   [lang\_altertable.html](../lang_altertable.html)   [lang\_attach.html](../lang_attach.html)   [lang\_createindex.html](../lang_createindex.html)   [lang\_createtable.html](../lang_createtable.html)   [lang\_createtrigger.html](../lang_createtrigger.html)   [lang\_createview.html](../lang_createview.html)   [lang\_delete.html](../lang_delete.html)   [lang\_expr.html](../lang_expr.html)   [lang\_insert.html](../lang_insert.html)   [lang\_returning.html](../lang_returning.html)   [lang\_select.html](../lang_select.html)   [lang\_update.html](../lang_update.html)   [lang\_upsert.html](../lang_upsert.html)   [lang\_with.html](../lang_with.html)   [partialindex.html](../partialindex.html)   [releaselog/3\_35\_3\.html](../releaselog/3_35_3.html)   [releaselog/3\_35\_4\.html](../releaselog/3_35_4.html)   [releaselog/3\_35\_5\.html](../releaselog/3_35_5.html)

