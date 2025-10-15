# collect_variant_data.py

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

def collect_variant_data():
    """Collects data for a single genetic variant."""
    variant = {}
    variant['Gene'] = input("Vilken gen gäller analysen? (t.ex. f8, vwf, serpinc1, fgg, fga, fgb, f9, f13, f11, f7, f10): ").lower()
    
    if variant['Gene'] not in gene_transcripts:
        print("Okänd gen. Kontrollera genens kortnamn och försök igen.")
        return collect_variant_data()
    
    variant['Transcript'] = gene_transcripts[variant['Gene']]
    variant['Disease'] = gene_diseases[variant['Gene']]
    variant['Nucleotide change'] = input("Vad är den specifika nukleotidförändringen? (t.ex. c.6371A>G): ")
    variant['Protein change'] = input("Vad är den specifika proteinkodande förändringen? (t.ex. p.Tyr2124Cys): ")
    zygosity_code = input("Vad är zygositeten för varianten? (1: Hemizygot, 2: Heterozygot, 3: Homozygot): ")
    variant['Zygosity'] = zygosity_translation.get(zygosity_code, 'Osäker zygositet')
    inheritance_code = input("Hur är varianten nedärvd? (1: Autosomalt dominant, 2: Autosomalt recessiv, 3: Recessiv, X-bunden): ")
    variant['Inheritance'] = inheritance_translation.get(inheritance_code, 'Osäker nedärvning')
    acmg_code = input("Hur bedöms varianten enligt ACMG-kriterierna? (ange siffra 1-5): ")
    variant['ACMG criteria assessment'] = acmg_translation.get(acmg_code, 'Osäker signifikans')
    variant['ClinVar and hemophilia database reports'] = input("Finns det några tidigare rapporter i ClinVar- och hemofilidatabaserna? Beskriv kortfattat: ")
    variant['Further studies'] = input("Är varianten intressant för vidare studier? (ja/nej): ").lower()
    
    if variant['Gene'] == 'f8':
        variant['Inversions'] = input("Har inversionerna i intron 1 och 22 gjorts? (ja/nej): ").lower()
        if variant['Inversions'] == 'ja':
            variant['Inversion result'] = input("Vad var resultatet av inversionerna? ")
        elif variant['Inversions'] == 'nej':
            variant['Inversion reason'] = input("Varför gjordes inte inversionerna? ")
        else:
            variant['Inversions'] = None  # Säkerställ att det alltid finns ett värde för inversioner.
    
    return variant
