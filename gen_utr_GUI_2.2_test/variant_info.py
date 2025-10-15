import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from generate_document import generate_document

class VariantInfoCollector:
    def __init__(self, root, general_info, gene_data, acmg_translation, zygosity_translation, inheritance_translation, submit_data, show_general_info_step):
        self.root = root
        self.general_info = general_info
        self.gene_data = gene_data
        self.acmg_translation = acmg_translation
        self.zygosity_translation = zygosity_translation
        self.inheritance_translation = inheritance_translation
        self.submit_data = submit_data
        self.show_general_info_step = show_general_info_step
        self.data = {"variants": []}

        # Initialize transcript and disease variables
        self.transcript_var = tk.StringVar()
        self.disease_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        variant_frame = ttk.LabelFrame(self.frame, text="Variantinformation")
        variant_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        self.label_gene_category = ttk.Label(variant_frame, text="Välj genkategori:")
        self.label_gene_category.grid(column=0, row=0, padx=10, pady=5)
        self.combo_gene_category = ttk.Combobox(variant_frame, values=list(self.gene_data.keys()), state="readonly")
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
        self.combo_zygosity = ttk.Combobox(variant_frame, values=list(self.zygosity_translation.values()), state="readonly")
        self.combo_zygosity.grid(column=1, row=4, padx=10, pady=5)

        self.label_inheritance = ttk.Label(variant_frame, text="Hur är varianten nedärvd?")
        self.label_inheritance.grid(column=0, row=5, padx=10, pady=5)
        self.combo_inheritance = ttk.Combobox(variant_frame, values=list(self.inheritance_translation.values()), state="readonly")
        self.combo_inheritance.grid(column=1, row=5, padx=10, pady=5)

        self.label_acmg = ttk.Label(variant_frame, text="Hur bedöms varianten enligt ACMG-kriterierna?")
        self.label_acmg.grid(column=0, row=6, padx=10, pady=5)
        self.combo_acmg = ttk.Combobox(variant_frame, values=list(self.acmg_translation.values()), state="readonly")
        self.combo_acmg.grid(column=1, row=6, padx=10, pady=5)

        self.label_clinvar = ttk.Label(variant_frame, text="Variantinformation och tidigare rapporterade fynd:")
        self.label_clinvar.grid(column=0, row=7, padx=10, pady=5)
        self.text_clinvar = tk.Text(variant_frame, height=5, width=40)
        self.text_clinvar.grid(column=1, row=7, padx=10, pady=5)

        self.label_further_studies = ttk.Label(variant_frame, text="Är varianten intressant för vidare studier?")
        self.label_further_studies.grid(column=0, row=8, padx=10, pady=5)
        self.combo_further_studies = ttk.Combobox(variant_frame, values=["ja", "nej"], state="readonly")
        self.combo_further_studies.grid(column=1, row=8, padx=10, pady=5)

        # Labels to display the autofilled transcript and disease
        self.label_transcript = ttk.Label(variant_frame, text="Transkript:")
        self.label_transcript.grid(column=0, row=9, padx=10, pady=5)
        self.transcript_display = ttk.Label(variant_frame, textvariable=self.transcript_var)
        self.transcript_display.grid(column=1, row=9, padx=10, pady=5)

        self.label_disease = ttk.Label(variant_frame, text="Sjukdom:")
        self.label_disease.grid(column=0, row=10, padx=10, pady=5)
        self.disease_display = ttk.Label(variant_frame, textvariable=self.disease_var)
        self.disease_display.grid(column=1, row=10, padx=10, pady=5)

        # Variant-knappar
        self.button_add_variant = ttk.Button(self.frame, text="Lägg till variant", command=self.add_variant)
        self.button_add_variant.grid(column=0, row=11, padx=10, pady=5)

        self.button_submit = ttk.Button(self.frame, text="Avsluta och generera rapport", command=self.submit_all)
        self.button_submit.grid(column=1, row=11, padx=10, pady=5)

        # Ny knapp: normalfynd
        self.button_normal = ttk.Button(self.frame, text="Generera normalfynd", command=self.generate_normal_finding)
        self.button_normal.grid(column=0, row=12, columnspan=2, padx=10, pady=5)

        # Tillbaka-knapp
        self.button_back = ttk.Button(self.frame, text="Tillbaka", command=self.show_previous_step)
        self.button_back.grid(column=0, row=13, columnspan=2, padx=10, pady=5)


    def update_genes(self, event):
        category = self.combo_gene_category.get()
        genes = list(self.gene_data[category].keys())  # Get the genes for the selected category
        self.combo_gene['values'] = genes

    def autofill_gene_data(self, event):
        gene = self.combo_gene.get()
        gene_info = self.gene_data[self.combo_gene_category.get()].get(gene, {})

        transcript = gene_info.get('Transcript', 'N/A')
        disease = gene_info.get('Disease', 'N/A')
        kategori = gene_info.get('Category', 'Övrigt')

        self.transcript_var.set(transcript)
        self.disease_var.set(disease)

        self.data['Transcript'] = transcript
        self.data['Disease'] = disease
        self.data['Category'] = kategori  # ← Lägg till kategorin här


    def add_variant(self):
        gene = self.combo_gene.get()
        if gene not in self.gene_data[self.combo_gene_category.get()]:
            messagebox.showerror("Fel", "Okänd gen. Kontrollera genens kortnamn och försök igen.")
            return

        variant = {
            "Gene": gene,
            "Nucleotide change": self.entry_nucleotide_change.get(),
            "Protein change": self.entry_protein_change.get(),
            "Zygosity": self.combo_zygosity.get(),
            "Inheritance": self.combo_inheritance.get(),
            "ACMG criteria assessment": self.combo_acmg.get(),
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

        self.data["LID-NR"] = self.general_info.get("LID-NR", "N/A")
        self.data["Proband"] = self.general_info.get("Proband", "N/A")
        self.data["Genotype"] = self.general_info.get("Genotype", "N/A")
        self.data["Phenotype"] = self.general_info.get("Phenotype", "N/A")
        self.data["Sequencing method"] = self.general_info.get("Sequencing method", "N/A")
        self.data["Exon"] = self.general_info.get("Exon", "N/A")

        # Bestäm output-directory beroende på kategori
        kategori = self.data.get("Category", "Övrigt")

        output_paths = {
            "Medfodd anemi": r"U:\DNA_Sekvenseringsresultat\Remissvar Medfödd anemi\väntande på att svaras ut",
            "Koagulation": r"U:\DNA_Sekvenseringsresultat\Remissvar Koagulation\väntande på att svaras ut",
            "Övrigt": r"U:\DNA_Sekvenseringsresultat\Remissvar Övrigt\väntande på att svaras ut"
            }

        output_directory = output_paths.get(kategori, output_paths["Övrigt"])

        # Skapa katalog om den inte finns
        import os
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        generate_document(self.data, output_directory)
        self.submit_data(self.data)




    def show_previous_step(self):
        self.frame.grid_forget()
        self.show_general_info_step()

    def generate_normal_finding(self):
        gene = self.combo_gene.get()
        if not gene:
            messagebox.showerror("Fel", "Välj en gen först.")
            return

        gene_info = self.gene_data[self.combo_gene_category.get()].get(gene, {})
        transcript = gene_info.get('Transcript', 'N/A')
        disease = gene_info.get('Disease', 'N/A')
        category = gene_info.get('Category', 'Övrigt')

        self.data = {
            "variants": [],
            "Transcript": transcript,
            "Disease": disease,
            "Category": category,
            "Gene": gene,
            "Normalfynd": True,
            "LID-NR": self.general_info.get("LID-NR", "N/A"),
            "Proband": self.general_info.get("Proband", "N/A"),
            "Genotype": self.general_info.get("Genotype", "N/A"),
            "Phenotype": self.general_info.get("Phenotype", "N/A"),
            "Sequencing method": self.general_info.get("Sequencing method", "N/A"),
            "Exon": self.general_info.get("Exon", "N/A")
        }

        # Kategori → mapp
        category_map = {
            "Medfodd anemi": "Hemolys",
            "Koagulation": "Koagulation"
        }
        mapped_category = category_map.get(category, "Övrigt")

        output_paths = {
            "Hemolys": r"U:\DNA_Sekvenseringsresultat\Remissvar Hemolys",
            "Koagulation": r"U:\DNA_Sekvenseringsresultat\Remissvar Koagulation",
            "Övrigt": r"U:\DNA_Sekvenseringsresultat\Remissvar Övrigt"
        }

        output_directory = output_paths[mapped_category]

        import os
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        print(f"Genererar normalfynd för {gene} → {output_directory}")
        generate_document(self.data, output_directory)

        self.submit_data(self.data)
