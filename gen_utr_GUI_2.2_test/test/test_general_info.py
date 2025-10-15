import unittest
import tkinter as tk
from general_info import GeneralInfoCollector

class TestGeneralInfoCollector(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.general_info_collector = GeneralInfoCollector(self.root, lambda x: x)
    
    def tearDown(self):
        self.root.destroy()

    def test_toggle_proband_fields(self):
        self.general_info_collector.combo_proband_known.set("ja")
        self.general_info_collector.toggle_proband_fields(None)
        self.assertEqual(str(self.general_info_collector.entry_proband["state"]), "normal")
        
        self.general_info_collector.combo_proband_known.set("nej")
        self.general_info_collector.toggle_proband_fields(None)
        self.assertEqual(str(self.general_info_collector.entry_proband["state"]), "disabled")
    
    def test_update_exon_entry(self):
        self.general_info_collector.combo_seq_method.set("Sanger")
        self.general_info_collector.update_exon_entry(None)
        self.assertEqual(str(self.general_info_collector.entry_exon["state"]), "normal")
        
        self.general_info_collector.combo_seq_method.set("MPS")
        self.general_info_collector.update_exon_entry(None)
        self.assertEqual(str(self.general_info_collector.entry_exon["state"]), "disabled")
    
    def test_collect_data(self):
        self.general_info_collector.entry_lidnr.insert(0, "12345")
        self.general_info_collector.combo_proband_known.set("ja")
        self.general_info_collector.entry_proband.insert(0, "test_proband")
        self.general_info_collector.entry_genotype.insert(0, "test_genotype")
        self.general_info_collector.entry_phenotype.insert(0, "test_phenotype")
        self.general_info_collector.combo_seq_method.set("Sanger")
        self.general_info_collector.entry_exon.insert(0, "test_exon")
        
        self.general_info_collector.collect_data()
        
        self.assertEqual(self.general_info_collector.data["LID-NR"], "12345")
        self.assertEqual(self.general_info_collector.data["Proband"], "test_proband")
        self.assertEqual(self.general_info_collector.data["Genotype"], "test_genotype")
        self.assertEqual(self.general_info_collector.data["Phenotype"], "test_phenotype")
        self.assertEqual(self.general_info_collector.data["Sequencing method"], "Sanger")
        self.assertEqual(self.general_info_collector.data["Exon"], "test_exon")

if __name__ == '__main__':
    unittest.main()
