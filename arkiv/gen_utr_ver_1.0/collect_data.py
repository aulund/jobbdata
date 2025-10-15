# collect_data.py
from collect_variant_data import collect_variant_data

def collect_data():
    """Collects overall data for the genetic report."""
    data = {}
    data['LID-NR'] = input("Vad är LID-NR på remissen? ")
    data['Proband identification'] = input("Vem är proband? (t.ex. patientens namn eller initialer): ")
    data['Sequencing method'] = input("Vilken sekvenseringsmetod användes? (MPS eller Sanger): ").lower()
    
    if data['Sequencing method'] == 'sanger':
        data['Exon'] = input("Vilket exon sekvenserades? (t.ex. 14): ")

    data['variants'] = []
    while True:
        variant = collect_variant_data()
        data['variants'].append(variant)
        more_variants = input("Vill du lägga till en annan variant? (ja/nej): ").lower()
        if more_variants != 'ja':
            break

    return data
