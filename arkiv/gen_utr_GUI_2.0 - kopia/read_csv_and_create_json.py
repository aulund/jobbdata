import csv
import json

def read_csv_and_create_json(csv_file, json_file):
    try:
        data = []
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

        with open(json_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)
        print(f"CSV data successfully converted to JSON: {json_file}")
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except IOError:
        print(f"Error: Unable to read the file {csv_file} or write to {json_file}.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
# read_csv_and_create_json('input.csv', 'output.json')
