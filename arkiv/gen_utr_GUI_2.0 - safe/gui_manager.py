from tkinter import Tk
from general_info import GeneralInfoCollector
from variant_info import VariantInfoCollector

class MainGUI:
    def __init__(self, root, gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation):
        self.root = root
        self.root.title("Genetisk Variant Datainsamling")
        
        self.general_info_collector = GeneralInfoCollector(self.root, self.show_variant_info_step)
        self.variant_info_collector = None
        
        self.gene_transcripts = gene_transcripts
        self.gene_diseases = gene_diseases
        self.new_genes = new_genes
        self.new_gene_diseases = new_gene_diseases
        self.acmg_translation = acmg_translation
        self.zygosity_translation = zygosity_translation
        self.inheritance_translation = inheritance_translation
        
        self.data = {}

    def show_variant_info_step(self, general_info):
        self.data.update(general_info)
        self.general_info_collector.frame.grid_forget()
        self.variant_info_collector = VariantInfoCollector(
            self.root,
            self.data,
            self.gene_transcripts,
            self.gene_diseases,
            self.new_genes,
            self.new_gene_diseases,
            self.acmg_translation,
            self.zygosity_translation,
            self.inheritance_translation,
            self.submit_data,
            self.show_general_info_step
        )

    def show_general_info_step(self):
        if self.variant_info_collector:
            self.variant_info_collector.frame.grid_forget()
        self.general_info_collector.frame.grid()

    def submit_data(self, data):
        self.data.update(data)
        self.root.quit()

def run_gui(gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation):
    root = Tk()
    app = MainGUI(root, gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation)
    root.mainloop()
    return app.data
