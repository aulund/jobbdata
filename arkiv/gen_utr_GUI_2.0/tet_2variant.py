import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self._handle_keyrelease)
        self['values'] = self._completion_list

    def _autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())
        _hits = []
        for item in self._completion_list:
            if item.lower().startswith(self.get().lower()):
                _hits.append(item)
        self._hits = _hits
        if _hits:
            self._hit_index = (self._hit_index + delta) % len(_hits)
            self.delete(0, tk.END)
            self.insert(0, _hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def _handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down'):
            if event.keysym == 'BackSpace':
                self.position = self.index(tk.END)
            if event.keysym == 'Left':
                if self.position < len(self.get()):
                    self.position -= 1
            if event.keysym == 'Right':
                if self.position < len(self.get()):
                    self.position += 1
        else:
            self.position = len(self.get())
        if event.keysym == 'Up':
            self._autocomplete(-1)
        elif event.keysym == 'Down':
            self._autocomplete(1)
        else:
            self._autocomplete()

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
        self.combo_gene = AutocompleteCombobox(variant_frame, state="normal")
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

        self.button_add_variant = ttk.Button(self.frame, text="Lägg till variant", command=self.add_variant)
        self.button_add_variant.grid(column=0, row=9, padx=10, pady=5)

        self.button_submit = ttk.Button(self.frame, text="Avsluta och generera rapport", command=self.submit_all)
        self.button_submit.grid(column=1, row=9, padx=10, pady=5)

        self.button_back = ttk.Button(self.frame, text="Tillbaka", command=self.show_previous_step)
        self.button_back.grid(column=0, row=10, columnspan=2, padx=10, pady=5)

    def update_genes(self, event):
        category = self.combo_gene_category.get()
        genes = self.new_genes if category == "Medfödd anemi" else list(self.gene_transcripts.keys())
        self.combo_gene.set_completion_list(genes)

    def autofill_gene_data(self, event):
        gene = self.combo_gene.get()
        if gene in self.new_gene_diseases:
            self.data['Disease'] = self.new_gene_diseases[gene]
        elif gene in self.gene_diseases:
            self.data['Disease'] = self.gene_diseases[gene]

    def add_variant(self):
        gene = self.combo_gene.get()
        if gene not in self.new_genes and gene not in self.gene_transcripts:
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
        self.submit_data(self.data)

    def show_previous_step(self):
        self.frame.grid_forget()
        self.show_general_info_step()

def translate_data(value, translation_dict):
    return translation_dict.get(value, value)

def autofill_gene_data(self, *args):
    gene = self.gene_var.get()
    if gene in self.new_genes:
        gene_info = self.new_genes[gene]
        self.transcript_var.set(gene_info['Transcript'])
        self.disease_var.set(gene_info['Disease'])
    else:
        messagebox.showerror("Fel", "Okänd gen. Kontrollera genens kortnamn och försök igen.")

self.data['Zygosity'] = translate_data(self.zygosity_var.get(), zygosity_translation)
self.data['Inheritance'] = translate_data(self.inheritance_var.get(), inheritance_translation)
self.data['ACMG'] = translate_data(self.acmg_var.get(), acmg_translation)
