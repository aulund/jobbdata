import json

def create_all_genes_json(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            genes_data = json.load(infile)
        
        with open(output_file, 'w') as outfile:
            json.dump(genes_data, outfile, indent=4)
        print(f"Successfully created JSON file: {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file {input_file}.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
# create_all_genes_json('input.json', 'output.json')
