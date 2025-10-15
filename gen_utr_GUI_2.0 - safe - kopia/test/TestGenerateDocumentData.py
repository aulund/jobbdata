import unittest
from unittest.mock import patch
import tkinter as tk
from gui_manager import MainGUI, VariantInfoCollector

class TestGenerateDocumentData(unittest.TestCase):
    @patch('generate_document.generate_document')
    def test_data_passed_to_generate_document(self, mock_generate_document):
        # Mock data setup
        mock_gene_data = {
            'Category1': {
                'SPTA1': {
                    'Transcript': 'NM_003126',
                    'Disease': 'Hereditary elliptocytosis'
                }
            }
        }
        mock_acmg_translation = {"Benign": "Benign"}
        mock_zygosity_translation = {"Hemizygot": "Hemizygot"}
        mock_inheritance_translation = {"Autosomalt dominant": "Autosomalt dominant"}

        root = tk.Tk()
        app = MainGUI(root, mock_gene_data, mock_acmg_translation, mock_zygosity_translation, mock_inheritance_translation)

        # Simulating the steps
        app.general_info_collector.data = {
            'LID-NR': '9999',
            'Proband': 'Proband inte känt',
            'Genotype': '',
            'Phenotype': '',
            'Sequencing method': 'MPS',
            'Exon': ''
        }

        # Directly call show_variant_info_step to bypass UI interaction
        app.show_variant_info_step(app.general_info_collector.data)
        app.variant_info_collector.combo_gene_category.set('Category1')
        app.variant_info_collector.combo_gene.set('SPTA1')
        app.variant_info_collector.entry_nucleotide_change.insert(0, '1234')
        app.variant_info_collector.entry_protein_change.insert(0, '5678')
        app.variant_info_collector.combo_zygosity.set('Hemizygot')
        app.variant_info_collector.combo_inheritance.set('Autosomalt dominant')
        app.variant_info_collector.combo_acmg.set('Benign')
        app.variant_info_collector.text_clinvar.insert("1.0", "ClinVar report")
        app.variant_info_collector.combo_further_studies.set('nej')
        app.variant_info_collector.add_variant()

        # Directly trigger the method that should call generate_document
        app.variant_info_collector.submit_all()

        # Assert that generate_document was called
        mock_generate_document.assert_called_once()

        # Check what was passed to generate_document
        passed_data = mock_generate_document.call_args[0][0]
        print(f"Data passed to generate_document: {passed_data}")

        # Validate the expected data structure
        self.assertEqual(passed_data['LID-NR'], '9999')
        self.assertEqual(passed_data['Transcript'], 'NM_003126')
        self.assertEqual(passed_data['Disease'], 'Hereditary elliptocytosis')

if __name__ == '__main__':
    unittest.main()
