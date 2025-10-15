import csv
import json

class CSVtoJSONConverter:
    def __init__(self, csv_file, json_file):
        self.csv_file = csv_file
        self.json_file = json_file

    def convert(self):
        data = {}
        with open(self.csv_file, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                gene = row['gene']
                data[gene] = row

        with open(self.json_file, mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
