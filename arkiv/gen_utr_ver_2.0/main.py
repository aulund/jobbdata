# main.py
from collect_variant_data import collect_variant_data
from generate_document import generate_document
from collect_variant_data import get_input_with_validation

def main():
    print("Välkommen till genetisk variant datainsamling!")
    print("Följ instruktionerna nedan för att ange information om den genetiska varianten.")

    data = {}
    data['LID-NR'] = input("Ange LID-NR på remissen: ")
    proband_known = get_input_with_validation("Finns det ett känt proband? (ja/nej): ", ["ja", "nej"])
    if proband_known == 'ja':
        data['Proband'] = input("Vem är proband? (t.ex. patientens namn eller initialer): ")
        data['Genotype'] = input("Vad är probandets genotyp? ")
        data['Phenotype'] = input("Vad är probandets fenotyp? ")
    else:
        data['Proband'] = "Proband inte känt"
        data['Genotype'] = ""
        data['Phenotype'] = ""
    data['Sequencing method'] = get_input_with_validation("Vilken sekvenseringsmetod användes? (MPS eller Sanger): ", ["mps", "sanger"])
    if data['Sequencing method'] == 'sanger':
        data['Exon'] = input("Vilket exon analyserades? ")
    data['variants'] = []

    collecting = True
    while collecting:
        variant = collect_variant_data()
        data['variants'].append(variant)
        collecting = get_input_with_validation("Vill du lägga till en annan variant? (ja/nej): ", ["ja", "nej"]) == "ja"

    generate_document(data)

if __name__ == "__main__":
    main()
