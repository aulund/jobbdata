import unittest
import tkinter as tk
from variant_info import VariantInfoCollector

class TestVariantInfoCollector(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.general_info = {
            "LID-NR": "12345",
            "Proband": "test_proband",
            "Genotype": "test_genotype",
            "Phenotype": "test_phenotype",
            "Sequencing method": "Sanger",
            "Exon": "test_exon"
        }
        self.gene_transcripts = {"f8": "NM_000132"}
        self.gene_diseases = {"f8": "Hemofili A"}
        self.new_genes = {"ANK1": {"Transcript": "NM_001142446.1", "Disease": "AD"}}
        self.new_gene_diseases = {"ANK1": "AD"}
        self.acmg_translation = {"1": "Benign"}
        self.zygosity_translation = {"1": "Hemizygot"}
        self.inheritance_translation = {"1": "Autosomalt dominant"}
        self.variant_info_collector = VariantInfoCollector(
            self.root, self.general_info, self.gene_transcripts, self.gene_diseases, self.new_genes, self.new_gene_diseases,
            self.acmg_translation, self.zygosity_translation, self.inheritance_translation, lambda x: x, lambda x: x
        )
    
    def tearDown(self):
        self.root.destroy()

    def test_update_genes(self):
        self.variant_info_collector.combo_gene_category.set("Medfödd anemi")
        self.variant_info_collector.update_genes(None)
        self.assertIn("ANK1", self.variant_info_collector.combo_gene["values"])
        
        self.variant_info_collector.combo_gene_category.set("Koagulation")
        self.variant_info_collector.update_genes(None)
        self.assertIn("f8", self.variant_info_collector.combo_gene["values"])
    
    def test_autofill_gene_data(self):
        self.variant_info_collector.combo_gene.set("ANK1")
        self.variant_info_collector.autofill_gene_data(None)
        self.assertEqual(self.variant_info_collector.data["Transcript"], "NM_001142446.1")
        self.assertEqual(self.variant_info_collector.data["Disease"], "AD")

        self.variant_info_collector.combo_gene.set("f8")
        self.variant_info_collector.autofill_gene_data(None)
        self.assertEqual(self.variant_info_collector.data["Transcript"], "NM_000132")
        self.assertEqual(self.variant_info_collector.data["Disease"], "Hemofili A")

    def test_add_variant(self):
        self.variant_info_collector.combo_gene.set("f8")
        self.variant_info_collector.entry_nucleotide_change.insert(0, "c.1234A>G")
        self.variant_info_collector.entry_protein_change.insert(0, "p.Tyr412Cys")
        self.variant_info_collector.combo_zygosity.set("1")
        self.variant_info_collector.combo_inheritance.set("1")
        self.variant_info_collector.combo_acmg.set("1")
        self.variant_info_collector.text_clinvar.insert("1.0", "ClinVar data")
        self.variant_info_collector.combo_further_studies.set("ja")
        
        self.variant_info_collector.add_variant()
        
        variant = self.variant_info_collector.data["variants"][0]
        self.assertEqual(variant["Gene"], "f8")
        self.assertEqual(variant["Nucleotide change"], "c.1234A>G")
        self.assertEqual(variant["Protein change"], "p.Tyr412Cys")
        self.assertEqual(variant["Zygosity"], "Hemizygot")
        self.assertEqual(variant["Inheritance"], "Autosomalt dominant")
        self.assertEqual(variant["ACMG criteria assessment"], "Benign")
        self.assertEqual(variant["ClinVar and hemophilia database reports"], "ClinVar data")
        self.assertEqual(variant["Further studies"], "ja")

    def test_submit_all(self):
        self.variant_info_collector.combo_gene.set("f8")
        self.variant_info_collector.entry_nucleotide_change.insert(0, "c.1234A>G")
        self.variant_info_collector.entry_protein_change.insert(0, "p.Tyr412Cys")
        self.variant_info_collector.combo_zygosity.set("1")
        self.variant_info_collector.combo_inheritance.set("1")
        self.variant_info_collector.combo_acmg.set("1")
        self.variant_info_collector.text_clinvar.insert("1.0", "ClinVar data")
        self.variant_info_collector.combo_further_studies.set("ja")
        
        self.variant_info_collector.add_variant()
        self.variant_info_collector.submit_all()

        self.assertTrue(len(self.variant_info_collector.data["variants"]) > 0)

if __name__ == '__main__':
    unittest.main()
