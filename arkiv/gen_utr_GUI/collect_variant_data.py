import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd

# Läs in gener från JSON-filer
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

# Läs in nya gener från CSV
file_path = 'G:\Kul\Kemi_DNA\DNA-lab, Kemi9Fem Huddinge\Medfödd anemi\genpanel_hemolys.csv'
gene_data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

new_genes = dict(zip(gene_data['hgnc_symbol'], gene_data['disease_associated_transcripts']))
new_gene_diseases = dict(zip(gene_data['hgnc_symbol'], gene_data['genetic_disease_models']))

class VariantCollector:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetisk Variant Datainsamling")
        self.variant = {}
        self.data = {}

        self.create_widgets()

    def create_widgets(self):
        self.label_welcome = ttk.Label(self.root, text="Välkommen till genetisk variant datainsamling!")
        self.label_welcome.grid(column=0, row=0, columnspan=2, padx=10, pady=5)
        
        self.label_instructions = ttk.Label(self.root, text="Följ instruktionerna nedan för att ange information om den genetiska varianten.")
        self.label_instructions.grid(column=0, row=1, columnspan=2, padx=10, pady=5)
        
        self.label_lidnr = ttk.Label(self.root, text="Ange LID-NR på remissen:")
        self.label_lidnr.grid(column=0, row=2, padx=10, pady=5)
        self.entry_lidnr = ttk.Entry(self.root)
        self.entry_lidnr.grid(column=1, row=2, padx=10, pady=5)

        self.label_proband_known = ttk.Label(self.root, text="Finns det ett känt proband? (ja/nej):")
        self.label_proband_known.grid(column=0, row=3, padx=10, pady=5)
        self.combo_proband_known = ttk.Combobox(self.root, values=["ja", "nej"])
        self.combo_proband_known.grid(column=1, row=3, padx=10, pady=5)
        self.combo_proband_known.bind("<<ComboboxSelected>>", self.toggle_proband_fields)

        self.label_proband = ttk.Label(self.root, text="Vem är proband? (t.ex. patientens namn eller initialer):")
        self.label_proband.grid(column=0, row=4, padx=10, pady=5)
        self.entry_proband = ttk.Entry(self.root)
        self.entry_proband.grid(column=1, row=4, padx=10, pady=5)
        self.entry_proband.grid_remove()

        self.label_genotype = ttk.Label(self.root, text="Vad är probandets genotyp?")
        self.label_genotype.grid(column=0, row=5, padx=10, pady=5)
        self.entry_genotype = ttk.Entry(self.root)
        self.entry_genotype.grid(column=1, row=5, padx=10, pady=5)
        self.entry_genotype.grid_remove()

        self.label_phenotype = ttk.Label(self.root, text="Vad är probandets fenotyp?")
        self.label_phenotype.grid(column=0, row=6, padx=10, pady=5)
        self.entry_phenotype = ttk.Entry(self.root)
        self.entry_phenotype.grid(column=1, row=6, padx=10, pady=5)
        self.entry_phenotype.grid_remove()

        self.label_sequencing = ttk.Label(self.root, text="Vilken sekvenseringsmetod användes? (MPS eller Sanger):")
        self.label_sequencing.grid(column=0, row=7, padx=10, pady=5)
        self.combo_sequencing = ttk.Combobox(self.root, values=["mps", "sanger"])
        self.combo_sequencing.grid(column=1, row=7, padx=10, pady=5)
        self.combo_sequencing.bind("<<ComboboxSelected>>", self.toggle_exon_field)

        self.label_exon = ttk.Label(self.root, text="Vilket exon analyserades?")
        self.label_exon.grid(column=0, row=8, padx=10, pady=5)
        self.entry_exon = ttk.Entry(self.root)
        self.entry_exon.grid(column=1, row=8, padx=10, pady=5)
        self.entry_exon.grid_remove()

        self.label_gene_category = ttk.Label(self.root, text="Välj genkategori:")
        self.label_gene_category.grid(column=0, row=9, padx=10, pady=5)
        self.combo_gene_category = ttk.Combobox(self.root, values=["Koagulation", "Medfödd anemi"])
        self.combo_gene_category.grid(column=1, row=9, padx=10, pady=5)
        self.combo_gene_category.bind("<<ComboboxSelected>>", self.toggle_gene_list)

        self.label_gene = ttk.Label(self.root, text="Vilken gen gäller analysen?")
        self.label_gene.grid(column=0, row=10, padx=10, pady=5)
        self.combo_gene = ttk.Combobox(self.root)
        self.combo_gene.grid(column=1, row=10, padx=10, pady=5)

        self.button_next = ttk.Button(self.root, text="Nästa", command=self.collect_general_data)
        self.button_next.grid(column=0, row=11, columnspan=2, padx=10, pady=10)

    def toggle_proband_fields(self, event):
        if self.combo_proband_known.get() == "ja":
            self.entry_proband.grid()
            self.entry_genotype.grid()
            self.entry_phenotype.grid()
        else:
            self.entry_proband.grid_remove()
            self.entry_genotype.grid_remove()
            self.entry_phenotype.grid_remove()

    def toggle_exon_field(self, event):
        if self.combo_sequencing.get().lower() == "sanger":
            self.entry_exon.grid()
        else:
            self.entry_exon.grid_remove()

    def toggle_gene_list(self, event):
        if self.combo_gene_category.get() == "Koagulation":
            self.combo_gene['values'] = list(gene_transcripts.keys())
        elif self.combo_gene_category.get() == "Medfödd anemi":
            self.combo_gene['values'] = list(new_genes.keys())

    def collect_general_data(self):
        self.data['LID-NR'] = self.entry_lidnr.get()
        self.data['Proband'] = self.entry_proband.get() if self.combo_proband_known.get() == 'ja' else "Proband inte känt"
        self.data['Genotype'] = self.entry_genotype.get() if self.combo_proband_known.get() == 'ja' else ""
        self.data['Phenotype'] = self.entry_phenotype.get() if self.combo_proband_known.get() == 'ja' else ""
        self.data['Sequencing method'] = self.combo_sequencing.get().lower()
        self.data['Exon'] = self.entry_exon.get() if self.combo_sequencing.get().lower() == 'sanger' else ""

        self.collect_variant_data()

    def collect_variant_data(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.label_gene = ttk.Label(self.root, text="Vilken gen gäller analysen?")
        self.label_gene.grid(column=0, row=0, padx=10, pady=5)
        self.combo_gene = ttk.Combobox(self.root)
        self.combo_gene.grid(column=1, row=0, padx=10, pady=5)

        self.label_nucleotide = ttk.Label(self.root, text="Specifik nukleotidförändring:")
        self.label_nucleotide.grid(column=0, row=1, padx=10, pady=5)
        self.entry_nucleotide = ttk.Entry(self.root)
        self.entry_nucleotide.grid(column=1, row=1, padx=10, pady=5)

        self.label_protein = ttk.Label(self.root, text="Specifik proteinkodande förändring:")
        self.label_protein.grid(column=0, row=2, padx=10, pady=5)
        self.entry_protein = ttk.Entry(self.root)
        self.entry_protein.grid(column=1, row=2, padx=10, pady=5)

        self.label_zygosity = ttk.Label(self.root, text="Vad är zygositeten för varianten?")
        self.label_zygosity.grid(column=0, row=3, padx=10, pady=5)
        self.combo_zygosity = ttk.Combobox(self.root, values=list(zygosity_translation.values()))
        self.combo_zygosity.grid(column=1, row=3, padx=10, pady=5)

        self.label_inheritance = ttk.Label(self.root, text="Hur är varianten nedärvd?")
        self.label_inheritance.grid(column=0, row=4, padx=10, pady=5)
        self.combo_inheritance = ttk.Combobox(self.root, values=list(inheritance_translation.values()))
        self.combo_inheritance.grid(column=1, row=4, padx=10, pady=5)

        self.label_acmg = ttk.Label(self.root, text="Hur bedöms varianten enligt ACMG-kriterierna?")
        self.label_acmg.grid(column=0, row=5, padx=10, pady=5)
        self.combo_acmg = ttk.Combobox(self.root, values=list(acmg_translation.values()))
        self.combo_acmg.grid(column=1, row=5, padx=10, pady=5)

        self.label_clinvar = ttk.Label(self.root, text="Tidigare rapporter i ClinVar och hemofilidatabaserna:")
        self.label_clinvar.grid(column=0, row=6, padx=10, pady=5)
        self.text_clinvar = tk.Text(self.root, height=5, width=40)
        self.text_clinvar.grid(column=1, row=6, padx=10, pady=5)

        self.label_further = ttk.Label(self.root, text="Är varianten intressant för vidare studier?")
        self.label_further.grid(column=0, row=7, padx=10, pady=5)
        self.combo_further = ttk.Combobox(self.root, values=["ja", "nej"])
        self.combo_further.grid(column=1, row=7, padx=10, pady=5)

        self.button_submit = ttk.Button(self.root, text="Skicka", command=self.submit_data)
        self.button_submit.grid(column=0, row=8, columnspan=2, padx=10, pady=10)

    def submit_data(self):
        gene = self.combo_gene.get().upper()
        if gene not in gene_transcripts and gene not in new_genes:
            messagebox.showerror("Fel", "Okänd gen. Kontrollera genens kortnamn och försök igen.")
            return
        
        if gene in gene_transcripts:
            self.variant['Gene'] = gene
            self.variant['Transcript'] = gene_transcripts[gene]
            self.variant['Disease'] = gene_diseases[gene]
        else:
            self.variant['Gene'] = gene
            self.variant['Transcript'] = new_genes[gene]
            self.variant['Disease'] = new_gene_diseases[gene]

        self.variant['Nucleotide change'] = self.entry_nucleotide.get()
        self.variant['Protein change'] = self.entry_protein.get()
        self.variant['Zygosity'] = self.combo_zygosity.get()
        self.variant['Inheritance'] = self.combo_inheritance.get()
        self.variant['ACMG criteria assessment'] = self.combo_acmg.get()
        self.variant['ClinVar and hemophilia database reports'] = self.text_clinvar.get("1.0", tk.END).strip()
        self.variant['Further studies'] = self.combo_further.get()

        if gene == 'F8':
            self.collect_f8_variant_info()

        print(self.variant)
        self.data['variants'] = [self.variant]
        messagebox.showinfo("Framgång", "Datan har samlats in framgångsrikt!")
        self.root.quit()

    def collect_f8_variant_info(self):
        inversion_result = simpledialog.askstring("Inversionsresultat", "Har inversionerna i intron 1 och 22 gjorts? (ja/nej)")
        if inversion_result.lower() == 'ja':
            self.variant['Inversions'] = 'ja'
            self.variant['Inversion result'] = simpledialog.askstring("Inversionsresultat", "Vad var resultatet av inversionerna?")
        elif inversion_result.lower() == 'nej':
            self.variant['Inversions'] = 'nej'
            self.variant['Inversion reason'] = simpledialog.askstring("Inversionsresultat", "Varför gjordes inte inversionerna?")
        else:
            self.variant['Inversions'] = None

def main():
    root = tk.Tk()
    app = VariantCollector(root)
    root.mainloop()
    return app.data

if __name__ == "__main__":
    main()
