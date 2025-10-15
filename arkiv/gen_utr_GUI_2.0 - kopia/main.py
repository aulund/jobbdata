import os
import json
from tkinter import Tk
from general_info import GeneralInfo
from variant_info import VariantInfo

def create_sample_genes_file(file_path):
    sample_data = {
        "transcripts": {
            "GENE1": "Transcript1",
            "GENE2": "Transcript2"
        },
        "diseases": {
            "GENE1": "Disease1",
            "GENE2": "Disease2"
        },
        "new_genes": {
            "GENE3": "Transcript3",
            "GENE4": "Transcript4"
        },
        "new_gene_diseases": {
            "GENE3": "Disease3",
            "GENE4": "Disease4"
        }
    }
    with open(file_path, 'w') as outfile:
        json.dump(sample_data, outfile, indent=4)
    print(f"Sample genes file created at {file_path}")

def load_genes_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON. Creating a sample file.")
        create_sample_genes_file(file_path)
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Creating a sample file.")
        create_sample_genes_file(file_path)
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

def main():
    # File path for the genes JSON file
    genes_file = 'new_genes.json'

    root = Tk()
    root.title("Genetic Data Collection")

    # Load data from new_genes.json
    genes_data = load_genes_data(genes_file)

    gene_transcripts = genes_data.get('transcripts', {})
    gene_diseases = genes_data.get('diseases', {})
    new_genes = genes_data.get('new_genes', {})
    new_gene_diseases = genes_data.get('new_gene_diseases', {})

    # Initialize the main application window
    general_info = GeneralInfo(master=root)
    variant_info = VariantInfo(
        master=root, 
        gene_transcripts=gene_transcripts, 
        gene_diseases=gene_diseases, 
        new_genes=new_genes, 
        new_gene_diseases=new_gene_diseases
    )

    root.mainloop()

if __name__ == "__main__":
    main()
