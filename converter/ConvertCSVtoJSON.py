import json
import csv
import os

def load_csv(file_path):
    with open(file_path) as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def convert_csv_to_json(csv_path):
    json_path = csv_path.replace('.csv', '.json')
    
    data = load_csv(csv_path)
    new_json_data = {"cards": []}
    for i in range(0, len(data)):
        temp_card = {
            "ID": i+1,
            "Question": data[i][1],
            "Answer": data[i][0],
            "Records": []
        }
        new_json_data["cards"].append(temp_card)
        
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(new_json_data, f, ensure_ascii=False, indent=4)

convert_csv_to_json('ch12-1.csv')

