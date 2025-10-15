import unittest
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_manager = DataManager()

    def test_get_gene_info(self):
        gene_info = self.data_manager.get_gene_info('ANK1')
        self.assertIsNotNone(gene_info)
        self.assertEqual(gene_info['hgnc_id'], '492')

    def test_translate_acmg(self):
        acmg_translation = self.data_manager.translate_acmg("1")
        self.assertEqual(acmg_translation, "Benign")

if __name__ == '__main__':
    unittest.main()
