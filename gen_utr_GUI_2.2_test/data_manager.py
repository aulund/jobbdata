import json

def load_gene_data():
    with open('combined_gene_data.json', 'r') as f:
        gene_data = json.load(f)
    
    with open('acmg_translation.json', 'r') as f:
        acmg_translation = json.load(f)

    with open('zygosity_translation.json', 'r') as f:
        zygosity_translation = json.load(f)

    with open('inheritance_translation.json', 'r') as f:
        inheritance_translation = json.load(f)

    return gene_data, acmg_translation, zygosity_translation, inheritance_translation



def load_translation_data():
    """
    Loads translation data for zygosity, ACMG criteria, and inheritance.

    Returns:
        dict: A dictionary containing all translation data needed for the application.
    """
    with open('zygosity_translation.json', 'r') as f:
        zygosity_translation = json.load(f)
    
    with open('acmg_translation.json', 'r') as f:
        acmg_translation = json.load(f)
    
    with open('inheritance_translation.json', 'r') as f:
        inheritance_translation = json.load(f)
    
    return {
        'zygosity': zygosity_translation,
        'acmg': acmg_translation,
        'inheritance': inheritance_translation
    }

def load_all_data():
    with open('combined_gene_data.json', 'r') as f:
        gene_data = json.load(f)
    
    with open('acmg_translation.json', 'r') as f:
        acmg_translation = json.load(f)

    with open('zygosity_translation.json', 'r') as f:
        zygosity_translation = json.load(f)

    with open('inheritance_translation.json', 'r') as f:
        inheritance_translation = json.load(f)

    return gene_data, acmg_translation, zygosity_translation, inheritance_translation


# Example usage:
if __name__ == "__main__":
    data = load_all_data()
    print("Gene data loaded:", data['genes'].keys())
    print("Translation data loaded:", data['translations'].keys())
