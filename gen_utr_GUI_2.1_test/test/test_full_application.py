import unittest
import tkinter as tk
from gui_manager import run_gui
from generate_document import generate_document

class TestFullApplication(unittest.TestCase):
    def setUp(self):
        # Set up the initial data needed for the application
        self.gene_data = {
            "Koagulation": {
                "F8": {
                    "Transcript": "NM_000132",
                    "Disease": "Hemophilia A",
                    "Category": "Koagulation"
                }
            },
            "Medfodd anemi": {
                "ANK1": {
                    "Transcript": "NM_001142446",
                    "Disease": "Hereditary spherocytosis",
                    "Category": "Medfodd anemi"
                }
            }
        }
        self.acmg_translation = {
            "PVS1": "Pathogenic Very Strong",
            "PS1": "Pathogenic Strong"
        }
        self.zygosity_translation = {
            "Het": "Heterozygous",
            "Hom": "Homozygous"
        }
        self.inheritance_translation = {
            "AD": "Autosomal Dominant",
            "AR": "Autosomal Recessive"
        }

    def test_full_application(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window during testing

        # Run the GUI with predefined data
        collected_data = run_gui(
            self.gene_data,
            self.acmg_translation,
            self.zygosity_translation,
            self.inheritance_translation
        )

        # Simulate the data input process
        patient_data = {
            "Patient ID": "12345",
            "Patient Name": "John Doe"
        }
        variants = [
            {
                "Gene": "F8",
                "Category": "Koagulation",
                "Transcript": "NM_000132",
                "Nucleotide Change": "c.1234A>T",
                "Protein Change": "p.Lys123*",
                "Zygosity": "Heterozygous",
                "Inheritance": "Autosomal Dominant",
                "ACMG Criteria": "PVS1",
                "ClinVar Reports": "None",
                "Further Studies": "Yes"
            }
        ]

        # Merge the patient data and variants into the collected data
        collected_data.update(patient_data)
        collected_data["variants"] = variants

        # Generate the document based on the collected data
        document_generated = generate_document(collected_data)

        # Verify the document was generated successfully
        self.assertTrue(document_generated, "Document generation failed")

        root.destroy()  # Clean up the GUI resources

if __name__ == "__main__":
    unittest.main()
