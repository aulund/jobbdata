# collect_variant_data.py

import json

with open('gene_transcripts.json', 'r') as file:
    gene_transcripts = json.load(file)

with open('gene_diseases.json', 'r') as file:
    gene_diseases = json.load(file)

with open('acmg_translation.json', 'r') as file:
    acmg_translation = json.load(file)

with open('zygosity_translation.json', 'r') as file:
    zygosity_translation = json.load(file)

with open('inheritance_translation.json', 'r') as file:
    inheritance_translation = json.load(file)

def get_input_with_validation(prompt, valid_options=None, default=None):
    while True:
        response = input(f"{prompt} {'Exempel: ' + default if default else ''}").lower()
        if response == '' and default is not None:
            return default
        if not valid_options or response in valid_options:
            return response
        else:
            print(f"Ogiltigt val. Välj ett av följande alternativ: {', '.join(valid_options)}")

def collect_f8_variant_info(variant):
    variant['Inversions'] = get_input_with_validation("Har inversionerna i intron 1 och 22 gjorts? (ja/nej): ", ["ja", "nej"])
    if variant['Inversions'] == 'ja':
        variant['Inversion result'] = input("Vad var resultatet av inversionerna? ")
    elif variant['Inversions'] == 'nej':
        variant['Inversion reason'] = input("Varför gjordes inte inversionerna? ")
    else:
        variant['Inversions'] = None
    return variant

def collect_variant_data():
    """Collects data for a single genetic variant."""
    variant = {}
    variant['Gene'] = get_input_with_validation("Vilken gen gäller analysen? (t.ex. f8, vwf, serpinc1, fgg, fga, fgb, f9, f13, f11, f7, f10): ", gene_transcripts.keys())

    variant['Transcript'] = gene_transcripts[variant['Gene']]
    variant['Disease'] = gene_diseases[variant['Gene']]
    variant['Nucleotide change'] = input("Vad är den specifika nukleotidförändringen? (t.ex. c.6371A>G): ")
    variant['Protein change'] = input("Vad är den specifika proteinkodande förändringen? (t.ex. p.Tyr2124Cys): ")
    zygosity_code = get_input_with_validation("Vad är zygositeten för varianten? (1: Hemizygot, 2: Heterozygot, 3: Homozygot): ", zygosity_translation.keys())
    variant['Zygosity'] = zygosity_translation.get(zygosity_code, 'Osäker zygositet')
    inheritance_code = get_input_with_validation("Hur är varianten nedärvd? (1: Autosomalt dominant, 2: Autosomalt recessiv, 3: Recessiv, X-bunden): ", inheritance_translation.keys())
    variant['Inheritance'] = inheritance_translation.get(inheritance_code, 'Osäker nedärvning')
    acmg_code = get_input_with_validation("Hur bedöms varianten enligt ACMG-kriterierna? (ange siffra 1-5): ", acmg_translation.keys())
    variant['ACMG criteria assessment'] = acmg_translation.get(acmg_code, 'Osäker signifikans')
    variant['ClinVar and hemophilia database reports'] = input("Finns det några tidigare rapporter i ClinVar- och hemofilidatabaserna? Beskriv kortfattat: ")
    variant['Further studies'] = get_input_with_validation("Är varianten intressant för vidare studier? (ja/nej): ", ["ja", "nej"])

    if variant['Gene'] == 'f8':
        variant = collect_f8_variant_info(variant)
    
    print("\nSammanfattning av inmatade data:")
    for key, value in variant.items():
        print(f"{key}: {value}")
    
    confirm = get_input_with_validation("Är dessa uppgifter korrekta? (ja/nej): ", ["ja", "nej"])
    if confirm == "nej":
        variant = edit_variant_data(variant)
    
    return variant

def edit_variant_data(variant):
    """Allows user to edit the collected data for a genetic variant."""
    print("\nRedigera uppgifterna. Lämna fältet tomt för att behålla det befintliga värdet.")
    
    new_gene = get_input_with_validation("Vilken gen gäller analysen? (t.ex. f8, vwf, serpinc1, fgg, fga, fgb, f9, f13, f11, f7, f10): ", gene_transcripts.keys(), variant['Gene'])
    if new_gene != variant['Gene']:
        variant['Gene'] = new_gene
        variant['Transcript'] = gene_transcripts[variant['Gene']]
        variant['Disease'] = gene_diseases[variant['Gene']]
    
    new_value = input(f"Vad är den specifika nukleotidförändringen? (t.ex. c.6371A>G) [{variant['Nucleotide change']}]: ")
    if new_value:
        variant['Nucleotide change'] = new_value

    new_value = input(f"Vad är den specifika proteinkodande förändringen? (t.ex. p.Tyr2124Cys) [{variant['Protein change']}]: ")
    if new_value:
        variant['Protein change'] = new_value

    zygosity_code = get_input_with_validation("Vad är zygositeten för varianten? (1: Hemizygot, 2: Heterozygot, 3: Homozygot): ", zygosity_translation.keys(), variant['Zygosity'])
    if zygosity_code != variant['Zygosity']:
        variant['Zygosity'] = zygosity_translation.get(zygosity_code, 'Osäker zygositet')

    inheritance_code = get_input_with_validation("Hur är varianten nedärvd? (1: Autosomalt dominant, 2: Autosomalt recessiv, 3: Recessiv, X-bunden): ", inheritance_translation.keys(), variant['Inheritance'])
    if inheritance_code != variant['Inheritance']:
        variant['Inheritance'] = inheritance_translation.get(inheritance_code, 'Osäker nedärvning')

    acmg_code = get_input_with_validation("Hur bedöms varianten enligt ACMG-kriterierna? (ange siffra 1-5): ", acmg_translation.keys(), variant['ACMG criteria assessment'])
    if acmg_code != variant['ACMG criteria assessment']:
        variant['ACMG criteria assessment'] = acmg_translation.get(acmg_code, 'Osäker signifikans')

    new_value = input(f"Finns det några tidigare rapporter i ClinVar- och hemofilidatabaserna? Beskriv kortfattat [{variant['ClinVar and hemophilia database reports']}]: ")
    if new_value:
        variant['ClinVar and hemophilia database reports'] = new_value

    further_studies = get_input_with_validation("Är varianten intressant för vidare studier? (ja/nej): ", ["ja", "nej"], variant['Further studies'])
    if further_studies != variant['Further studies']:
        variant['Further studies'] = further_studies

    if variant['Gene'] == 'f8':
        variant = collect_f8_variant_info(variant)

    return variant
