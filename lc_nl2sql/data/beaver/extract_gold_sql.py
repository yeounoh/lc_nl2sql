import os
import sys
import json
ROOT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(ROOT_PATH)

from lc_nl2sql.llm_base.api_model import GeminiModel

gold_sqls = []
with open('queries.json', 'r') as file:
    data = json.load(file)
    for item in data:
        if 'sql' in item:
            gold_sqls.append((item['sql'], 'dw'))

model = GeminiModel("400355794761")
with open("dev_gold.sql", "w") as outfile:
  for sql, db_id in gold_sqls:
      sql = model._generate_sql(f"You are sqlite expert.\n"
                          "Rewrite the below SQL query according to the following rules:\n"
                          "- all table aliases are properly defined using a keyword `AS`.\n"
                          "- do not use window function (partition over) so it's compatible with older sqlite version.\n"
                          "- remove lower(), as it is case insensitive.\n\n"
                          "-------------------------------------------------------\n"
                          f"{sql}\n"
                          "-------------------------------------------------------\n"
                          "Only return the modified SQL query string so it can be executed verbatim.\n"
                          "If nothing to fix, just return the query as-is.")
      outfile.write(sql + "\t" + db_id + "\n")