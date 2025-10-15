import tkinter as tk
from tkinter import ttk
from general_info import GeneralInfoCollector
from variant_info import VariantInfoCollector

class MainGUI:
    def __init__(self, root, gene_data, acmg_translation, zygosity_translation, inheritance_translation):
        self.root = root
        self.root.title("Genetisk Variant Datainsamling")
        
        self.gene_data = gene_data
        self.acmg_translation = acmg_translation
        self.zygosity_translation = zygosity_translation
        self.inheritance_translation = inheritance_translation
        
        self.general_info_collector = GeneralInfoCollector(self.root, self.show_variant_info_step)
        self.variant_info_collector = None
        
        self.data = {}

    def show_variant_info_step(self, data):
        self.data = data
        if self.general_info_collector:
            self.general_info_collector.frame.grid_forget()
        self.variant_info_collector = VariantInfoCollector(
            root=self.root,
            general_info=self.data,  # Pass the general info data
            gene_data=self.gene_data,  # This should include both transcripts and diseases
            acmg_translation=self.acmg_translation,
            zygosity_translation=self.zygosity_translation,
            inheritance_translation=self.inheritance_translation,
            submit_data=self.submit_data,
            show_general_info_step=self.show_general_info_step
        )
        print("Data passed to variant step:", self.data)
        self.variant_info_collector.frame.grid()

    def show_general_info_step(self):
        if self.variant_info_collector:
            self.variant_info_collector.frame.grid_forget()
        self.general_info_collector.frame.grid()

    def submit_data(self, data):
        self.data.update(data)
        self.root.quit()

def run_gui(gene_data, acmg_translation, zygosity_translation, inheritance_translation):
    root = tk.Tk()
    app = MainGUI(
        root,
        gene_data=gene_data,
        acmg_translation=acmg_translation,
        zygosity_translation=zygosity_translation,
        inheritance_translation=inheritance_translation
    )
    root.mainloop()

    return app.data
