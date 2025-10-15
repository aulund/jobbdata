# main.py
from collect_variant_data import collect_variant_data
from generate_document import generate_document

def main():
    data = {}
    data['LID-NR'] = input("Ange LID-NR på remissen: ")
    proband_known = input("Finns det ett känt proband? (ja/nej): ").lower()
    if proband_known == 'ja':
        data['Proband'] = input("Vem är proband? (t.ex. patientens namn eller initialer): ")
        data['Genotype'] = input("Vad är probandets genotyp? ")
        data['Phenotype'] = input("Vad är probandets fenotyp? ")
    else:
        data['Proband'] = "Proband inte känt"
        data['Genotype'] = ""
        data['Phenotype'] = ""
    data['Sequencing method'] = input("Vilken sekvenseringsmetod användes? (MPS eller Sanger): ").lower()
    if data['Sequencing method'] == 'sanger':
        data['Exon'] = input("Vilket exon analyserades? ")
    data['variants'] = []  # Initialisera listan här

    inversion_asked = False

    collecting = True
    while collecting:
        variant = collect_variant_data()
        if variant['Gene'] == 'f8' and not inversion_asked:
            variant['Inversions'] = input("Har inversionerna i intron 1 och 22 gjorts? (ja/nej): ").lower()
            if variant['Inversions'] == 'ja':
                variant['Inversion result'] = input("Vad var resultatet av inversionerna? ")
            elif variant['Inversions'] == 'nej':
                variant['Inversion reason'] = input("Varför gjordes inte inversionerna? ")
            inversion_asked = True
        else:
            variant['Inversions'] = None
        data['variants'].append(variant)
        if input("Vill du lägga till en annan variant? (ja/nej): ").lower() != 'ja':
            collecting = False

    generate_document(data)

if __name__ == "__main__":
    main()
