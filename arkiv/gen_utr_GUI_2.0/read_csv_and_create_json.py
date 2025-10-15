import csv
import json

def read_csv_and_create_json(csv_path, json_path):
    data = {}
    with open(csv_path, 'r', encoding='ISO-8859-1') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')
        for row in csv_reader:
            gene_symbol = row['hgnc_symbol']
            data[gene_symbol] = {
                "Transcript": row['disease_associated_transcripts'],
                "Disease": row['genetic_disease_models']
            }
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

csv_path = 'G:\\Kul\\Kemi_DNA\\DNA-lab, Kemi9Fem Huddinge\\Medfödd anemi\\genpanel_hemolys.csv'
json_path = 'H:\\pythonmall\\gen_utr_GUI_2.0\\new_genes.json'
read_csv_and_create_json(csv_path, json_path)
