import json

def load_gene_data():
    json_path = r"H:\pythonmall\gen_utr_GUI_2.0\all_genes_data.json"
    
    with open(json_path, mode='r', encoding='utf-8') as file:
        genes_data = json.load(file)
    
    gene_transcripts = {gene: data['transcript'] for gene, data in genes_data.items() if 'f' in gene}  # För koagulation
    gene_diseases = {gene: data['genetic_disease_models'] for gene, data in genes_data.items() if 'f' in gene}  # För koagulation

    new_genes = {gene: data['transcript'] for gene, data in genes_data.items() if 'f' not in gene}  # För medfödd anemi
    new_gene_diseases = {gene: data['genetic_disease_models'] for gene, data in genes_data.items() if 'f' not in gene}  # För medfödd anemi

    return gene_transcripts, gene_diseases, new_genes, new_gene_diseases

def load_translation_data():
    acmg_translation = {
        '1': 'Benign',
        '2': 'Troligen benign',
        '3': 'Osäker signifikans',
        '4': 'Troligen patogen',
        '5': 'Patogen'
    }

    zygosity_translation = {
        '1': 'Hemizygot',
        '2': 'Heterozygot',
        '3': 'Homozygot'
    }

    inheritance_translation = {
        '1': 'Autosomalt dominant',
        '2': 'Autosomalt recessiv',
        '3': 'Recessiv, X-bunden'
    }

    return acmg_translation, zygosity_translation, inheritance_translation
