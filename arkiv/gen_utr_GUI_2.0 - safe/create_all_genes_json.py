import csv
import json

def read_csv_and_create_json(csv_path, json_path):
    genes_data = {}

    # Lägg till koagulationsgenerna
    gene_transcripts = {
        'f8': 'NM_000132',
        'vwf': 'NM_000552',
        'serpinc1': 'NM_000488',
        'fgg': 'NM_000509',
        'fga': 'NM_000508',
        'fgb': 'NM_005141',
        'f9': 'NM_000133',
        'f13': 'NM_001993',
        'f11': 'NM_000128',
        'f7': 'NM_000131',
        'f10': 'NM_000504'
    }

    gene_diseases = {
        'f8': 'Hemofili A',
        'vwf': 'von Willebrands sjukdom',
        'serpinc1': 'Antitrombinbrist',
        'fgg': 'Afibrinogenemi eller Dysfibrinogenemi',
        'fga': 'Afibrinogenemi eller Dysfibrinogenemi',
        'fgb': 'Afibrinogenemi eller Dysfibrinogenemi',
        'f9': 'Hemofili B',
        'f13': 'Faktor XIII-brist',
        'f11': 'Faktor XI-brist (Hemofili C)',
        'f7': 'Faktor VII-brist',
        'f10': 'Faktor X-brist'
    }

    for gene, transcript in gene_transcripts.items():
        genes_data[gene] = {
            'hgnc_id': '',
            'transcript': transcript,
            'genetic_disease_models': gene_diseases[gene]
        }

    # Lägg till gener från CSV-filen
    with open(csv_path, mode='r', encoding='latin1') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        print(f"Column names: {csv_reader.fieldnames}")
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
    json_path = r"H:\pythonmall\gen_utr_GUI_2.0\all_genes_data.json"

    read_csv_and_create_json(csv_path, json_path)
