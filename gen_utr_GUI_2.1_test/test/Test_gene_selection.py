import unittest
import tkinter as tk
from variant_info import VariantInfoCollector  # Ensure this is the correct module name

class TestGeneSelection(unittest.TestCase):
    def setUp(self):
        # Setup the test environment
        self.root = tk.Tk()
        self.gene_data = {
            'Koagulation': {
                'F2': {'Transcript': 'NM_000506', 'Disease': 'Prothrombin deficiency or thrombophilia'},
                'F5': {'Transcript': 'NM_000130', 'Disease': 'Factor V deficiency or thrombophilia'},
            },
            'Medfödd anemi': {
                'ANK1': {'Transcript': 'NM_001142446', 'Disease': 'Hereditary spherocytosis'},
                'SPTB': {'Transcript': 'NM_001024858', 'Disease': 'Hereditary spherocytosis'},
            }
        }
        self.acmg_translation = {"Benign": "Benign", "Likely benign": "Troligen benign"}
        self.zygosity_translation = {"Heterozygous": "Heterozygot", "Homozygous": "Homozygot"}
        self.inheritance_translation = {"Autosomal dominant": "Autosomalt dominant", "X-linked": "X-bunden"}

        # Create the VariantInfoCollector instance with the test data
        self.collector = VariantInfoCollector(
            root=self.root,
            general_info={},  # Use appropriate test data
            gene_data=self.gene_data,
            acmg_translation=self.acmg_translation,
            zygosity_translation=self.zygosity_translation,
            inheritance_translation=self.inheritance_translation,
            submit_data=lambda data: None,
            show_general_info_step=lambda: None
        )

    def tearDown(self):
        # Cleanup the Tkinter instance after each test
        self.root.destroy()

    def test_gene_selection_koagulation(self):
        # Select the Koagulation category and check if the correct genes are loaded
        self.collector.combo_gene_category.set('Koagulation')
        self.collector.update_genes(None)
        actual_genes = self.collector.combo_gene['values']
        expected_genes = ['F2', 'F5']
        self.assertEqual(list(actual_genes), expected_genes, "Koagulation genes were not correctly updated")

    def test_gene_selection_medfodd_anemi(self):
        # Select the Medfödd anemi category and check if the correct genes are loaded
        self.collector.combo_gene_category.set('Medfödd anemi')
        self.collector.update_genes(None)
        actual_genes = self.collector.combo_gene['values']
        expected_genes = ['ANK1', 'SPTB']
        self.assertEqual(list(actual_genes), expected_genes, "Medfödd anemi genes were not correctly updated")

if __name__ == "__main__":
    unittest.main()
