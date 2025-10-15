import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class GeneralInfoCollector:
    def __init__(self, root, show_variant_info_step):
        self.root = root
        self.show_variant_info_step = show_variant_info_step
        self.data = {}
        
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        self.label_title = ttk.Label(self.frame, text="Genetisk Variant Datainsamling", font=("Helvetica", 16))
        self.label_title.grid(column=0, row=0, columnspan=2, pady=10)

        # Adding DNA helix image
        self.dna_image = Image.open("dna_helix.png")
        self.dna_image = self.dna_image.resize((100, 100), Image.LANCZOS)
        self.dna_photo = ImageTk.PhotoImage(self.dna_image)
        self.label_dna_image = ttk.Label(self.frame, image=self.dna_photo)
        self.label_dna_image.grid(column=0, row=1, columnspan=2, pady=10)

        self.label_lidnr = ttk.Label(self.frame, text="Ange LID-NR på remissen:")
        self.label_lidnr.grid(column=0, row=2, padx=10, pady=5, sticky="e")
        self.entry_lidnr = ttk.Entry(self.frame)
        self.entry_lidnr.grid(column=1, row=2, padx=10, pady=5)

        self.label_proband_known = ttk.Label(self.frame, text="Finns det ett känt proband? (ja/nej):")
        self.label_proband_known.grid(column=0, row=3, padx=10, pady=5, sticky="e")
        self.combo_proband_known = ttk.Combobox(self.frame, values=["ja", "nej"], state="readonly")
        self.combo_proband_known.grid(column=1, row=3, padx=10, pady=5)
        self.combo_proband_known.bind("<<ComboboxSelected>>", self.toggle_proband_fields)

        self.label_proband = ttk.Label(self.frame, text="Vem är proband? (t.ex. patientens namn eller initialer):")
        self.label_proband.grid(column=0, row=4, padx=10, pady=5, sticky="e")
        self.entry_proband = ttk.Entry(self.frame)
        self.entry_proband.grid(column=1, row=4, padx=10, pady=5)

        self.label_genotype = ttk.Label(self.frame, text="Vad är probandets genotyp?")
        self.label_genotype.grid(column=0, row=5, padx=10, pady=5, sticky="e")
        self.entry_genotype = ttk.Entry(self.frame)
        self.entry_genotype.grid(column=1, row=5, padx=10, pady=5)

        self.label_phenotype = ttk.Label(self.frame, text="Vad är probandets fenotyp?")
        self.label_phenotype.grid(column=0, row=6, padx=10, pady=5, sticky="e")
        self.entry_phenotype = ttk.Entry(self.frame)
        self.entry_phenotype.grid(column=1, row=6, padx=10, pady=5)

        self.label_seq_method = ttk.Label(self.frame, text="Vilken sekvenseringsmetod användes? (MPS eller Sanger):")
        self.label_seq_method.grid(column=0, row=7, padx=10, pady=5, sticky="e")
        self.combo_seq_method = ttk.Combobox(self.frame, values=["MPS", "Sanger"], state="readonly")
        self.combo_seq_method.grid(column=1, row=7, padx=10, pady=5)
        self.combo_seq_method.bind("<<ComboboxSelected>>", self.update_exon_entry)

        self.label_exon = ttk.Label(self.frame, text="Vilket exon analyserades?")
        self.label_exon.grid(column=0, row=8, padx=10, pady=5, sticky="e")
        self.entry_exon = ttk.Entry(self.frame)
        self.entry_exon.grid(column=1, row=8, padx=10, pady=5)
        self.entry_exon.config(state="normal")

        self.button_next = ttk.Button(self.frame, text="Nästa", command=self.collect_data)
        self.button_next.grid(column=0, row=9, columnspan=2, pady=10)

    def toggle_proband_fields(self, event):
        if self.combo_proband_known.get() == "ja":
            self.entry_proband.config(state="normal")
            self.entry_genotype.config(state="normal")
            self.entry_phenotype.config(state="normal")
        else:
            self.entry_proband.config(state="disabled")
            self.entry_genotype.config(state="disabled")
            self.entry_phenotype.config(state="disabled")

    def update_exon_entry(self, event):
        if self.combo_seq_method.get() == "Sanger":
            self.entry_exon.config(state="normal")
        else:
            self.entry_exon.config(state="disabled")

    def collect_data(self):
        self.data["LID-NR"] = self.entry_lidnr.get()
        self.data["Proband"] = self.entry_proband.get() if self.combo_proband_known.get() == "ja" else "Proband inte känt"
        self.data["Genotype"] = self.entry_genotype.get() if self.combo_proband_known.get() == "ja" else ""
        self.data["Phenotype"] = self.entry_phenotype.get() if self.combo_proband_known.get() == "ja" else ""
        self.data["Sequencing method"] = self.combo_seq_method.get()
        self.data["Exon"] = self.entry_exon.get() if self.combo_seq_method.get() == "Sanger" else ""

        self.show_next_step(self.data)

    def show_next_step(self, data):
        self.frame.grid_forget()
        self.show_variant_info_step(data)
