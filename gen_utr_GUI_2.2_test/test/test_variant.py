import unittest
import tkinter as tk
from unittest.mock import MagicMock
from variant_info import VariantInfoCollector

class TestVariantInfoCollector(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        general_info = {}
        gene_transcripts = {"ANK1": {"Transcript": "NM_001142446.1"}, "SPTB": {"Transcript": "NM_001024858.2"}}
        gene_diseases = {"ANK1": "Disease1", "SPTB": "Disease2"}
        new_genes = {"GENE3": {"Transcript": "NM_003"}, "GENE4": {"Transcript": "NM_004"}}
        new_gene_diseases = {}
        acmg_translation = {"1": "Pathogenic", "2": "Likely Pathogenic"}
        zygosity_translation = {"1": "Homozygous", "2": "Heterozygous"}
        inheritance_translation = {"1": "Autosomal Dominant", "2": "Autosomal Recessive"}
        submit_data = lambda x: None
        show_general_info_step = lambda: None

        self.collector = VariantInfoCollector(
            root=self.root,
            general_info=general_info,
            gene_transcripts=gene_transcripts,
            gene_diseases=gene_diseases,
            new_genes=new_genes,
            new_gene_diseases=new_gene_diseases,
            acmg_translation=acmg_translation,
            zygosity_translation=zygosity_translation,
            inheritance_translation=inheritance_translation,
            submit_data=submit_data,
            show_general_info_step=show_general_info_step
        )

    def tearDown(self):
        self.root.destroy()

    def test_update_genes(self):
        # Test updating genes with "Medfödd anemi" category
        self.collector.combo_gene_category.set("Medfödd anemi")
        self.collector.update_genes(None)
        expected_genes_anemi = ["ANK1", "SPTB"]
        self.assertEqual(list(self.collector.combo_gene['values']), expected_genes_anemi)

        # Test updating genes with "Koagulation" category
        self.collector.combo_gene_category.set("Koagulation")
        self.collector.update_genes(None)
        expected_genes_koagulation = ["F8", "F9"]
        self.assertEqual(list(self.collector.combo_gene['values']), expected_genes_koagulation)

    def test_autofill_gene_data(self):
        # Simulate selecting a gene and autofill data
        self.collector.combo_gene_category.set("Medfödd anemi")
        self.collector.update_genes(None)
        self.collector.combo_gene.set("ANK1")
        self.collector.autofill_gene_data(None)

        # Check if transcript and disease fields are correctly populated
        self.assertEqual(self.collector.transcript_var.get(), "NM_001142446.1")
        self.assertEqual(self.collector.disease_var.get(), "Hereditary spherocytosis")

if __name__ == '__main__':
    unittest.main()
