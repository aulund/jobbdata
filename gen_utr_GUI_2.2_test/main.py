from gui_manager import run_gui
from data_manager import load_gene_data

def main():
    gene_data, acmg_translation, zygosity_translation, inheritance_translation = load_gene_data()

    run_gui(
        gene_data=gene_data,
        acmg_translation=acmg_translation,
        zygosity_translation=zygosity_translation,
        inheritance_translation=inheritance_translation
    )

if __name__ == "__main__":
    main()
