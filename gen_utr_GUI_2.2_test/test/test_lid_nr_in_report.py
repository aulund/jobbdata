import unittest
import tkinter as tk
from unittest.mock import patch
from gui_manager import MainGUI
from data_manager import load_all_data
import generate_document  # Import the module where generate_document is defined
import os

class TestLIDNRInReport(unittest.TestCase):
    def setUp(self):
        self.gene_data, self.acmg_translation, self.zygosity_translation, self.inheritance_translation = load_all_data()
        self.root = tk.Tk()
        self.app = MainGUI(
            self.root,
            gene_data=self.gene_data,
            acmg_translation=self.acmg_translation,
            zygosity_translation=self.zygosity_translation,
            inheritance_translation=self.inheritance_translation
        )
        # Simulate transitioning to the variant info step
        self.app.show_variant_info_step(self.app.data)

    @patch('generate_document.generate_document')  # Use the full path to the function
    def test_lid_nr_in_report(self, mock_generate_document):
        # Set up test data in GeneralInfoCollector
        self.app.general_info_collector.data = {
            'LID-NR': '12345',
            'Proband': 'Test Proband',
            'Genotype': 'AA',
            'Phenotype': 'Normal',
            'Sequencing method': 'MPS',
            'Exon': ''
        }
        
        # Simulate the user input for the variant information
        self.app.variant_info_collector.data = {
            'variants': [{
                'Gene': 'F2',
                'Nucleotide change': 'c.1234G>A',
                'Protein change': 'p.Val412Met',
                'Zygosity': 'Heterozygot',
                'Inheritance': 'Autosomalt recessiv',
                'ACMG criteria assessment': 'Benign',
                'ClinVar and hemophilia database reports': 'No significant findings',
                'Further studies': 'No'
            }],
            'Transcript': 'NM_000506',
            'Disease': 'Prothrombin deficiency or thrombophilia'
        }

        # Call the submit method to trigger report generation
        self.app.variant_info_collector.submit_all()

        # Check that the generate_document was called with the correct data
        mock_generate_document.assert_called_once()
        args, kwargs = mock_generate_document.call_args
        data_passed = args[0]  # The first argument is the data passed to generate_document

        # Check that LID-NR is correctly passed in data
        self.assertIn('LID-NR', data_passed)
        self.assertEqual(data_passed['LID-NR'], '12345')

        # Check that the filename is generated correctly
        output_path = args[1]
        expected_filename = os.path.join('H:\\pythonmall\\gen_utr_GUI_2.0 - safe - kopia\\output', '12345_F2.docx')
        self.assertTrue(output_path.endswith(expected_filename))

if __name__ == '__main__':
    unittest.main()
