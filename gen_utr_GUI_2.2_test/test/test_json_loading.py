import unittest
import json

class TestGeneDataLoading(unittest.TestCase):
    
    def setUp(self):
        # This method will run before each test.
        with open('combined_gene_data.json', 'r', encoding='utf-8') as f:
            self.gene_data = json.load(f)
    
    def test_json_structure(self):
        """Test that the JSON structure contains expected categories and genes."""
        
        # Ensure top-level categories exist
        self.assertIn("Koagulation", self.gene_data, "Category 'Koagulation' is missing in JSON data")
        self.assertIn("Medfödd anemi", self.gene_data, "Category 'Medfödd anemi' is missing in JSON data")
        
        # Ensure each category contains expected gene keys and subkeys
        koagulation_genes = self.gene_data["Koagulation"]
        medfodd_anemi_genes = self.gene_data["Medfödd anemi"]
        
        # Example genes to check for in each category
        expected_koagulation_genes = ["F2", "F5", "F8"]
        expected_medfodd_anemi_genes = ["ANK1", "SPTB", "HBB"]
        
        for gene in expected_koagulation_genes:
            self.assertIn(gene, koagulation_genes, f"Gene '{gene}' is missing in 'Koagulation' category")
            self.assertIn("Transcript", koagulation_genes[gene], f"Transcript missing for gene '{gene}'")
            self.assertIn("Disease", koagulation_genes[gene], f"Disease missing for gene '{gene}'")
            self.assertIn("Category", koagulation_genes[gene], f"Category missing for gene '{gene}'")
        
        for gene in expected_medfodd_anemi_genes:
            self.assertIn(gene, medfodd_anemi_genes, f"Gene '{gene}' is missing in 'Medfödd anemi' category")
            self.assertIn("Transcript", medfodd_anemi_genes[gene], f"Transcript missing for gene '{gene}'")
            self.assertIn("Disease", medfodd_anemi_genes[gene], f"Disease missing for gene '{gene}'")
            self.assertIn("Category", medfodd_anemi_genes[gene], f"Category missing for gene '{gene}'")

    def test_category_encoding(self):
        """Test that the category names are correctly encoded and accessible."""
        # Test that categories are correctly encoded
        self.assertIn("Medfödd anemi", self.gene_data, "Category 'Medfödd anemi' has incorrect encoding")
        self.assertIn("Koagulation", self.gene_data, "Category 'Koagulation' has incorrect encoding")
        
        # Ensure accessing works without errors
        medfodd_anemi_genes = self.gene_data["Medfödd anemi"]
        koagulation_genes = self.gene_data["Koagulation"]
        
        self.assertIsInstance(medfodd_anemi_genes, dict, "'Medfödd anemi' genes data should be a dictionary")
        self.assertIsInstance(koagulation_genes, dict, "'Koagulation' genes data should be a dictionary")


if __name__ == '__main__':
    unittest.main()
