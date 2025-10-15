import csv
import json

def read_csv_and_create_json(csv_path, json_path):
    genes_data = {}

    with open(csv_path, mode='r', encoding='latin1') as file:  # Ändra kodning till latin1
        csv_reader = csv.DictReader(file, delimiter=';')  # Ange att delimiter är semikolon
        print(f"Column names: {csv_reader.fieldnames}")  # Lägg till denna rad för att skriva ut kolumnnamnen
        for row in csv_reader:
            gene_symbol = row['hgnc_symbol']
            genes_data[gene_symbol] = {
                'hgnc_id': row['hgnc_id'],
                'transcript': row['disease_associated_transcripts'],
                'genetic_disease_models': row['genetic_disease_models']
            }

    with open(json_path, mode='w', encoding='utf-8') as file:
        json.dump(genes_data, file, ensure_ascii=False, indent=4)

    print(f"JSON file created at {json_path}")

if __name__ == "__main__":
    csv_path = r"G:\Kul\Kemi_DNA\DNA-lab, Kemi9Fem Huddinge\Medfödd anemi\genpanel_hemolys.csv"
    json_path = r"H:\pythonmall\gen_utr_GUI_2.0\genes_data.json"

    read_csv_and_create_json(csv_path, json_path)
