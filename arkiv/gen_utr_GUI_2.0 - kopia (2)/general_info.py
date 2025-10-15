import tkinter as tk
from tkinter import ttk, messagebox

class GeneralInfo:
    def __init__(self, master):
        self.master = master
        self.data = {}
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.master)
        self.frame.grid(column=0, row=0, padx=10, pady=10)

        self.label_lid = ttk.Label(self.frame, text="LID-NR")
        self.label_lid.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.entry_lid = ttk.Entry(self.frame)
        self.entry_lid.grid(column=1, row=0, padx=10, pady=5, sticky="ew")

        self.label_proband_known = ttk.Label(self.frame, text="Känner du till probandet?")
        self.label_proband_known.grid(column=0, row=1, padx=10, pady=5, sticky="w")
        self.combo_proband_known = ttk.Combobox(self.frame, values=["Ja", "Nej"])
        self.combo_proband_known.grid(column=1, row=1, padx=10, pady=5, sticky="ew")

        self.label_proband = ttk.Label(self.frame, text="Vad är probandets namn?")
        self.label_proband.grid(column=0, row=2, padx=10, pady=5, sticky="w")
        self.entry_proband = ttk.Entry(self.frame)
        self.entry_proband.grid(column=1, row=2, padx=10, pady=5, sticky="ew")

        self.label_genotype = ttk.Label(self.frame, text="Vad är probandets genotyp?")
        self.label_genotype.grid(column=0, row=3, padx=10, pady=5, sticky="w")
        self.entry_genotype = ttk.Entry(self.frame)
        self.entry_genotype.grid(column=1, row=3, padx=10, pady=5, sticky="ew")

        self.label_phenotype = ttk.Label(self.frame, text="Vad är probandets fenotyp?")
        self.label_phenotype.grid(column=0, row=4, padx=10, pady=5, sticky="w")
        self.entry_phenotype = ttk.Entry(self.frame)
        self.entry_phenotype.grid(column=1, row=4, padx=10, pady=5, sticky="ew")

        self.label_sequencing_method = ttk.Label(self.frame, text="Vilken sekvenseringsmetod användes? (MPS eller Sanger):")
        self.label_sequencing_method.grid(column=0, row=5, padx=10, pady=5, sticky="w")
        self.combo_sequencing_method = ttk.Combobox(self.frame, values=["MPS", "Sanger"])
        self.combo_sequencing_method.grid(column=1, row=5, padx=10, pady=5, sticky="ew")

        self.label_exon = ttk.Label(self.frame, text="Vilket exon analyserades?")
        self.label_exon.grid(column=0, row=6, padx=10, pady=5, sticky="w")
        self.entry_exon = ttk.Entry(self.frame)
        self.entry_exon.grid(column=1, row=6, padx=10, pady=5, sticky="ew")

        self.button_next = ttk.Button(self.frame, text="Nästa", command=self.collect_data)
        self.button_next.grid(column=0, row=7, columnspan=2, pady=10)

    def collect_data(self):
        try:
            self.data = {
                'LID-NR': self.entry_lid.get(),
                'Proband': "Proband inte känt" if self.combo_proband_known.get().lower() == "nej" else self.entry_proband.get(),
                'Genotype': "" if self.combo_proband_known.get().lower() == "nej" else self.entry_genotype.get(),
                'Phenotype': "" if self.combo_proband_known.get().lower() == "nej" else self.entry_phenotype.get(),
                'Sequencing Method': self.combo_sequencing_method.get(),
                'Exon': self.entry_exon.get()
            }
            print(self.data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to collect data: {e}")

    def get_data(self):
        return self.data
