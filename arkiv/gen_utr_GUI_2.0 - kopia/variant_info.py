import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class VariantInfo:
    def __init__(self, master, gene_transcripts, gene_diseases, new_genes, new_gene_diseases):
        self.master = master
        self.gene_transcripts = gene_transcripts
        self.gene_diseases = gene_diseases
        self.new_genes = new_genes
        self.new_gene_diseases = new_gene_diseases
        self.data = {}
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.master)
        self.frame.grid(column=0, row=0, padx=10, pady=10)

        self.label_gene = ttk.Label(self.frame, text="Gene:")
        self.label_gene.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.combo_gene = ttk.Combobox(self.frame)
        self.combo_gene.grid(column=1, row=0, padx=10, pady=5, sticky="ew")
        self.combo_gene['values'] = list(self.new_genes.keys())

        self.label_nucleotide = ttk.Label(self.frame, text="Nucleotide change:")
        self.label_nucleotide.grid(column=0, row=1, padx=10, pady=5, sticky="w")
        self.entry_nucleotide = ttk.Entry(self.frame)
        self.entry_nucleotide.grid(column=1, row=1, padx=10, pady=5, sticky="ew")

        self.label_protein = ttk.Label(self.frame, text="Protein change:")
        self.label_protein.grid(column=0, row=2, padx=10, pady=5, sticky="w")
        self.entry_protein = ttk.Entry(self.frame)
        self.entry_protein.grid(column=1, row=2, padx=10, pady=5, sticky="ew")

        self.label_zygosity = ttk.Label(self.frame, text="Zygosity:")
        self.label_zygosity.grid(column=0, row=3, padx=10, pady=5, sticky="w")
        self.combo_zygosity = ttk.Combobox(self.frame, values=["Homozygous", "Heterozygous"])
        self.combo_zygosity.grid(column=1, row=3, padx=10, pady=5, sticky="ew")

        self.label_inheritance = ttk.Label(self.frame, text="Inheritance:")
        self.label_inheritance.grid(column=0, row=4, padx=10, pady=5, sticky="w")
        self.combo_inheritance = ttk.Combobox(self.frame, values=["Autosomal Dominant", "Autosomal Recessive", "X-Linked"])
        self.combo_inheritance.grid(column=1, row=4, padx=10, pady=5, sticky="ew")

        self.label_acmg = ttk.Label(self.frame, text="ACMG criteria assessment:")
        self.label_acmg.grid(column=0, row=5, padx=10, pady=5, sticky="w")
        self.combo_acmg = ttk.Combobox(self.frame, values=["Pathogenic", "Likely Pathogenic", "Uncertain Significance", "Likely Benign", "Benign"])
        self.combo_acmg.grid(column=1, row=5, padx=10, pady=5, sticky="ew")

        self.label_clinvar = ttk.Label(self.frame, text="ClinVar and hemophilia database reports:")
        self.label_clinvar.grid(column=0, row=6, padx=10, pady=5, sticky="w")
        self.text_clinvar = tk.Text(self.frame, height=4)
        self.text_clinvar.grid(column=1, row=6, padx=10, pady=5, sticky="ew")

        self.label_studies = ttk.Label(self.frame, text="Further studies:")
        self.label_studies.grid(column=0, row=7, padx=10, pady=5, sticky="w")
        self.combo_studies = ttk.Combobox(self.frame, values=["Yes", "No"])
        self.combo_studies.grid(column=1, row=7, padx=10, pady=5, sticky="ew")

        self.button_submit = ttk.Button(self.frame, text="Submit", command=self.collect_data)
        self.button_submit.grid(column=0, row=8, columnspan=2, pady=10)

    def collect_data(self):
        try:
            gene = self.combo_gene.get().upper()
            if gene in self.gene_transcripts:
                self.data['Gene'] = gene
                self.data['Transcript'] = self.gene_transcripts[gene]
                self.data['Disease'] = self.gene_diseases[gene]
            elif gene in self.new_genes:
                self.data['Gene'] = gene
                self.data['Transcript'] = self.new_genes[gene]
                self.data['Disease'] = self.new_gene_diseases[gene]
            else:
                messagebox.showerror("Error", "Unknown gene. Please check the gene symbol and try again.")
                return

            self.data['Nucleotide change'] = self.entry_nucleotide.get()
            self.data['Protein change'] = self.entry_protein.get()
            self.data['Zygosity'] = self.combo_zygosity.get()
            self.data['Inheritance'] = self.combo_inheritance.get()
            self.data['ACMG criteria assessment'] = self.combo_acmg.get()
            self.data['ClinVar and hemophilia database reports'] = self.text_clinvar.get("1.0", tk.END).strip()
            self.data['Further studies'] = self.combo_studies.get()

            if self.data['Gene'] == 'F8':
                inversion_result = simpledialog.askstring("Inversion Result", "Were the inversions in intron 1 and 22 done? (yes/no)")
                if inversion_result.lower() == 'yes':
                    self.data['Inversions'] = 'yes'
                    self.data['Inversion result'] = simpledialog.askstring("Inversion Result", "What was the result of the inversions?")
                elif inversion_result.lower() == 'no':
                    self.data['Inversions'] = 'no'
                    self.data['Inversion reason'] = simpledialog.askstring("Inversion Result", "Why were the inversions not done?")
                else:
                    self.data['Inversions'] = None

            print(self.data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to collect data: {e}")

    def get_data(self):
        return self.data
