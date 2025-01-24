import json
import os

def combine_json_files(folder_path):
  train_data = []
  dev_data = []
  for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
      file_path = os.path.join(folder_path, filename)
      with open(file_path, 'r') as f:
        try:
          data = json.load(f)
          # Assuming each file contains a list of JSON objects
          if '_test' in file_path:
            dev_data.extend(data)
          else:
            train_data.extend(data)
        except json.JSONDecodeError as e:
          print(f"Error decoding JSON in file {filename}: {e}")
      
  return train_data, dev_data

train_data, dev_data = combine_json_files('examples')
print(f'Numb train examples: {len(train_data)}, Numb dev examples: {len(dev_data)}')

gold_sql = []
for idx, item in enumerate(dev_data):
    item['question_id'] = idx
    gold_sql.append((item['query'], item['db_id']))
with open("train.json", "w") as outfile:
  json.dump(train_data, outfile, indent=4)
with open("dev.json", "w") as outfile:
  json.dump(dev_data, outfile, indent=4)
with open("dev_gold.sql", "w") as outfile:
  for sql, db_id in gold_sql:
      outfile.write(sql + "\t" + db_id + "\n")
