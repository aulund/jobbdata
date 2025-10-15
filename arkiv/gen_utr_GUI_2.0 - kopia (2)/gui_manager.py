import tkinter as tk
from general_info import GeneralInfoCollector
from variant_info import VariantInfoCollector

class MainGUI:
    def __init__(self, root, gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation):
        self.root = root
        self.gene_transcripts = gene_transcripts
        self.gene_diseases = gene_diseases
        self.new_genes = new_genes
        self.new_gene_diseases = new_gene_diseases
        self.acmg_translation = acmg_translation
        self.zygosity_translation = zygosity_translation
        self.inheritance_translation = inheritance_translation
        
        self.general_info_collector = GeneralInfoCollector(self.root, self.show_variant_info_step)
        self.general_info_collector.frame.grid(column=0, row=0, padx=10, pady=5)

    def show_variant_info_step(self, general_info):
        self.general_info_collector.frame.grid_remove()
        self.variant_info_collector = VariantInfoCollector(
            self.root, self.gene_transcripts, self.gene_diseases, self.new_genes, self.new_gene_diseases,
            self.acmg_translation, self.zygosity_translation, self.inheritance_translation, self.show_general_info_step
        )
        self.variant_info_collector.frame.grid(column=0, row=0, padx=10, pady=5)

    def show_general_info_step(self):
        self.variant_info_collector.frame.grid_remove()
        self.general_info_collector.frame.grid(column=0, row=0, padx=10, pady=5)

def run_gui(gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation):
    root = tk.Tk()
    root.title("Genetisk Variant Datainsamling")
    main_gui = MainGUI(root, gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation)
    root.mainloop()
    return main_gui.general_info_collector.get_data()
