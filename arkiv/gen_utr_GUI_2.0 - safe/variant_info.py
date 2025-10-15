import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class VariantInfoCollector:
    def __init__(self, root, general_info, gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation, submit_data, show_general_info_step):
        self.root = root
        self.general_info = general_info
        self.gene_transcripts = gene_transcripts
        self.gene_diseases = gene_diseases
        self.new_genes = new_genes
        self.new_gene_diseases = new_gene_diseases
        self.acmg_translation = acmg_translation
        self.zygosity_translation = zygosity_translation
        self.inheritance_translation = inheritance_translation
        self.submit_data = submit_data
        self.show_general_info_step = show_general_info_step
        self.data = {"variants": []}

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        variant_frame = ttk.LabelFrame(self.frame, text="Variantinformation")
        variant_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        self.label_gene_category = ttk.Label(variant_frame, text="Välj genkategori:")
        self.label_gene_category.grid(column=0, row=0, padx=10, pady=5)
        self.combo_gene_category = ttk.Combobox(variant_frame, values=["Koagulation", "Medfödd anemi"], state="readonly")
        self.combo_gene_category.grid(column=1, row=0, padx=10, pady=5)
        self.combo_gene_category.bind("<<ComboboxSelected>>", self.update_genes)

        self.label_gene = ttk.Label(variant_frame, text="Vilken gen gäller analysen?")
        self.label_gene.grid(column=0, row=1, padx=10, pady=5)
        self.combo_gene = ttk.Combobox(variant_frame, state="readonly")
        self.combo_gene.grid(column=1, row=1, padx=10, pady=5)
        self.combo_gene.bind("<<ComboboxSelected>>", self.autofill_gene_data)

        self.label_nucleotide_change = ttk.Label(variant_frame, text="Specifik nukleotidförändring:")
        self.label_nucleotide_change.grid(column=0, row=2, padx=10, pady=5)
        self.entry_nucleotide_change = ttk.Entry(variant_frame)
        self.entry_nucleotide_change.grid(column=1, row=2, padx=10, pady=5)

        self.label_protein_change = ttk.Label(variant_frame, text="Specifik proteinkodande förändring:")
        self.label_protein_change.grid(column=0, row=3, padx=10, pady=5)
        self.entry_protein_change = ttk.Entry(variant_frame)
        self.entry_protein_change.grid(column=1, row=3, padx=10, pady=5)

        self.label_zygosity = ttk.Label(variant_frame, text="Vad är zygositeten för varianten?")
        self.label_zygosity.grid(column=0, row=4, padx=10, pady=5)
        self.combo_zygosity = ttk.Combobox(variant_frame, values=list(self.zygosity_translation.keys()), state="readonly")
        self.combo_zygosity.grid(column=1, row=4, padx=10, pady=5)

        self.label_inheritance = ttk.Label(variant_frame, text="Hur är varianten nedärvd?")
        self.label_inheritance.grid(column=0, row=5, padx=10, pady=5)
        self.combo_inheritance = ttk.Combobox(variant_frame, values=list(self.inheritance_translation.keys()), state="readonly")
        self.combo_inheritance.grid(column=1, row=5, padx=10, pady=5)

        self.label_acmg = ttk.Label(variant_frame, text="Hur bedöms varianten enligt ACMG-kriterierna?")
        self.label_acmg.grid(column=0, row=6, padx=10, pady=5)
        self.combo_acmg = ttk.Combobox(variant_frame, values=list(self.acmg_translation.keys()), state="readonly")
        self.combo_acmg.grid(column=1, row=6, padx=10, pady=5)

        self.label_clinvar = ttk.Label(variant_frame, text="Variantinformation och tidigare rapporterade fynd:")
        self.label_clinvar.grid(column=0, row=7, padx=10, pady=5)
        self.text_clinvar = tk.Text(variant_frame, height=5, width=40)
        self.text_clinvar.grid(column=1, row=7, padx=10, pady=5)

        self.label_further_studies = ttk.Label(variant_frame, text="Är varianten intressant för vidare studier?")
        self.label_further_studies.grid(column=0, row=8, padx=10, pady=5)
        self.combo_further_studies = ttk.Combobox(variant_frame, values=["ja", "nej"], state="readonly")
        self.combo_further_studies.grid(column=1, row=8, padx=10, pady=5)

        self.button_add_variant = ttk.Button(self.frame, text="Lägg till variant", command=self.add_variant)
        self.button_add_variant.grid(column=0, row=9, padx=10, pady=5)

        self.button_submit = ttk.Button(self.frame, text="Avsluta och generera rapport", command=self.submit_all)
        self.button_submit.grid(column=1, row=9, padx=10, pady=5)

        self.button_back = ttk.Button(self.frame, text="Tillbaka", command=self.show_previous_step)
        self.button_back.grid(column=0, row=10, columnspan=2, padx=10, pady=5)

    def update_genes(self, event):
        category = self.combo_gene_category.get()
        if category == "Medfödd anemi":
            genes = list(self.new_genes.keys())
        else:
            genes = list(self.gene_transcripts.keys())
        self.combo_gene['values'] = genes

    def autofill_gene_data(self, event):
        gene = self.combo_gene.get()
        if gene in self.new_genes:
            gene_info = self.new_genes[gene]
            self.data['Transcript'] = gene_info['Transcript']
            self.data['Disease'] = gene_info['Disease']
        elif gene in self.gene_transcripts:
            gene_info = self.gene_transcripts[gene]
            self.data['Transcript'] = gene_info
            self.data['Disease'] = self.gene_diseases.get(gene, '')

    def add_variant(self):
        gene = self.combo_gene.get()
        if gene not in self.new_genes and gene not in self.gene_transcripts:
            messagebox.showerror("Fel", "Okänd gen. Kontrollera genens kortnamn och försök igen.")
            return

        variant = {
            "Gene": gene,
            "Transcript": self.data.get('Transcript', ''),
            "Disease": self.data.get('Disease', ''),
            "Nucleotide change": self.entry_nucleotide_change.get(),
            "Protein change": self.entry_protein_change.get(),
            "Zygosity": self.translate_data(self.combo_zygosity.get(), self.zygosity_translation),
            "Inheritance": self.translate_data(self.combo_inheritance.get(), self.inheritance_translation),
            "ACMG criteria assessment": self.translate_data(self.combo_acmg.get(), self.acmg_translation),
            "ClinVar and hemophilia database reports": self.text_clinvar.get("1.0", tk.END).strip(),
            "Further studies": self.combo_further_studies.get()
        }
        self.data["variants"].append(variant)
        messagebox.showinfo("Info", "Varianten har lagts till.")
        print(self.data)  # Kontrollera att varianten lagts till korrekt

    def submit_all(self):
        if not self.data["variants"]:
            messagebox.showerror("Fel", "Du måste lägga till minst en variant innan du skickar in.")
            return
        self.submit_data(self.data)

    def show_previous_step(self):
        self.frame.grid_forget()
        self.show_general_info_step()

    @staticmethod
    def translate_data(value, translation_dict):
        return translation_dict.get(value, value)
