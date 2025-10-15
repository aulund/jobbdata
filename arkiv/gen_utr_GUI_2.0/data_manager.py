import json

def load_gene_data():
    with open('gene_transcripts.json', 'r') as f:
        gene_transcripts = json.load(f)
    with open('gene_diseases.json', 'r') as f:
        gene_diseases = json.load(f)
    with open('new_genes.json', 'r') as f:
        new_genes = json.load(f)
    with open('new_gene_diseases.json', 'r') as f:
        new_gene_diseases = json.load(f)
    with open('acmg_translation.json', 'r') as f:
        acmg_translation = json.load(f)
    with open('zygosity_translation.json', 'r') as f:
        zygosity_translation = json.load(f)
    with open('inheritance_translation.json', 'r') as f:
        inheritance_translation = json.load(f)
    return gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation


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
