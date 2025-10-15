import unittest
from tkinter import Tk
from variant_info import VariantInfoCollector

class TestVariantInfoCollector(unittest.TestCase):

    def setUp(self):
        # Set up a Tkinter root instance
        self.root = Tk()

        # Sample data to mimic the JSON structure loaded into the program
        self.gene_data = {
            "Koagulation": {
                "F2": {"Transcript": "NM_000506", "Disease": "Prothrombin deficiency", "Category": "Koagulation"},
                "F5": {"Transcript": "NM_000130", "Disease": "Factor V Leiden", "Category": "Koagulation"},
            },
            "Medfödd anemi": {
                "ANK1": {"Transcript": "NM_001142446", "Disease": "Hereditary spherocytosis", "Category": "Medfödd anemi"},
                "SPTB": {"Transcript": "NM_001024858", "Disease": "Hereditary spherocytosis", "Category": "Medfödd anemi"},
            }
        }
        self.acmg_translation = {"PVS1": "Pathogenic", "BS1": "Benign"}
        self.zygosity_translation = {"Homozygous": "Homozygot", "Heterozygous": "Heterozygot"}
        self.inheritance_translation = {"AD": "Autosomal Dominant", "AR": "Autosomal Recessive"}

        # Mock functions for submit_data and show_general_info_step
        def mock_submit_data(data):
            pass
        
        def mock_show_general_info_step():
            pass

        # Create an instance of the VariantInfoCollector with the sample data
        self.collector = VariantInfoCollector(
            self.root,
            gene_data=self.gene_data,
            acmg_translation=self.acmg_translation,
            zygosity_translation=self.zygosity_translation,
            inheritance_translation=self.inheritance_translation,
            submit_data=mock_submit_data,
            show_general_info_step=mock_show_general_info_step,
        )

    def tearDown(self):
        # Destroy the Tkinter root instance
        self.root.destroy()

    def test_update_genes_koagulation(self):
        # Simulate selecting "Koagulation" category
        self.collector.combo_gene_category.set("Koagulation")
        self.collector.update_genes(None)

        # Check if the combo_gene 'values' were correctly updated with the koagulation genes
        expected_genes = ['F2', 'F5']
        actual_genes = list(self.collector.combo_gene['values'])
        self.assertEqual(actual_genes, expected_genes, "Koagulation genes were not correctly updated")

    def test_update_genes_anemi(self):
        # Simulate selecting "Medfödd anemi" category
        self.collector.combo_gene_category.set("Medfödd anemi")
        self.collector.update_genes(None)

        # Check if the combo_gene 'values' were correctly updated with the medfödd anemi genes
        expected_genes = ['ANK1', 'SPTB']
        actual_genes = list(self.collector.combo_gene['values'])
        self.assertEqual(actual_genes, expected_genes, "Medfödd anemi genes were not correctly updated")


if __name__ == "__main__":
    unittest.main()
