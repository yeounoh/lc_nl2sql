import json
import os

def combine_json_files(folder_path):
  combined_data = []
  for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
      file_path = os.path.join(folder_path, filename)
      with open(file_path, 'r') as f:
        try:
          data = json.load(f)
          # Assuming each file contains a list of JSON objects
          combined_data.extend(data)
        except json.JSONDecodeError as e:
          print(f"Error decoding JSON in file {filename}: {e}")
  return combined_data

combined_data = combine_json_files('examples')
for idx, item in enumerate(combined_data):
    item['question_id'] = idx
with open("dev.json", "w") as outfile:
  json.dump(combined_data, outfile, indent=4)
