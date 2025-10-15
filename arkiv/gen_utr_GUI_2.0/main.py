import os
from gui_manager import run_gui
from generate_document import generate_document
from data_manager import load_gene_data

def main():
    gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation = load_gene_data()
    data = run_gui(gene_transcripts, gene_diseases, new_genes, new_gene_diseases, acmg_translation, zygosity_translation, inheritance_translation)
    output_path = 'H:\\pythonmall\\gen_utr_GUI_2.0\\output'  # Ange önskad sökväg här
    print(f"Genererar dokument med följande data:\n{data}")
    generate_document(data, output_path)

if __name__ == "__main__":
    main()
