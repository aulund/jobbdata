import json

def create_json_files():
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

    new_genes = {
        'ANK1': 'NM_001142446.1',
        'SPTB': 'NM_001024858.2',
        'SPTA1': 'NM_003126.2',
        # Add more genes as needed...
    }

    new_gene_diseases = {
        'ANK1': 'AD',
        'SPTB': 'AD',
        'SPTA1': 'AR, AD',
        # Add more gene diseases as needed...
    }

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

    with open('gene_transcripts.json', 'w') as f:
        json.dump(gene_transcripts, f)
    
    with open('gene_diseases.json', 'w') as f:
        json.dump(gene_diseases, f)

    with open('new_genes.json', 'w') as f:
        json.dump(new_genes, f)
    
    with open('new_gene_diseases.json', 'w') as f:
        json.dump(new_gene_diseases, f)
    
    with open('acmg_translation.json', 'w') as f:
        json.dump(acmg_translation, f)
    
    with open('zygosity_translation.json', 'w') as f:
        json.dump(zygosity_translation, f)
    
    with open('inheritance_translation.json', 'w') as f:
        json.dump(inheritance_translation, f)

if __name__ == "__main__":
    create_json_files()
