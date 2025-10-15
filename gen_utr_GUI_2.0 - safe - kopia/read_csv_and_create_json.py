import csv
import json

def read_csv_and_create_json(csv_file_path, json_file_path):
    data = {}

    # Open the CSV file with the correct delimiter
    with open(csv_file_path, mode='r', encoding='latin1') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')

        print("CSV Headers:", csv_reader.fieldnames)  # Debug: Check if headers are correct

        for row in csv_reader:
            gene_symbol = row.get('hgnc_symbol', '').strip()
            transcript_id = row.get('disease_associated_transcripts', '').strip()
            disease_name = row.get('genetic_disease_models', '').strip()

            if gene_symbol:
                data[gene_symbol] = {
                    'Transcript': transcript_id,
                    'Disease': disease_name
                }

    # Write the dictionary to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Example usage
    csv_file_path = r'G:\Kul\Kemi_DNA\DNA-lab, Kemi9Fem Huddinge\Medfödd anemi\genpanel_hemolys.csv'
    json_file_path = 'gene_transcripts.json'  # Set this to the appropriate JSON file path
    read_csv_and_create_json(csv_file_path, json_file_path)
