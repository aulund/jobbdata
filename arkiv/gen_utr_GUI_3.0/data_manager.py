import json
import os

class JSONHandler:
    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def write_json(data, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

class DataManager:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        self.gene_data = JSONHandler.read_json(os.path.join(base_path, 'genes_data.json'))
        self.disease_data = JSONHandler.read_json(os.path.join(base_path, 'gene_diseases.json'))
        self.transcript_data = JSONHandler.read_json(os.path.join(base_path, 'gene_transcripts.json'))
        self.acmg_translation = JSONHandler.read_json(os.path.join(base_path, 'acmg_translation.json'))
        self.inheritance_translation = JSONHandler.read_json(os.path.join(base_path, 'inheritance_translation.json'))
        self.zygosity_translation = JSONHandler.read_json(os.path.join(base_path, 'zygosity_translation.json'))

    def get_gene_info(self, gene_name):
        return self.gene_data.get(gene_name, {})

    def get_disease_info(self, gene_name):
        return self.disease_data.get(gene_name, "Unknown")

    def get_transcript_info(self, gene_name):
        return self.transcript_data.get(gene_name, "Unknown")

    def translate_acmg(self, acmg_code):
        return self.acmg_translation.get(acmg_code, "Unknown")

    def translate_inheritance(self, inheritance_code):
        return self.inheritance_translation.get(inheritance_code, "Unknown")

    def translate_zygosity(self, zygosity_code):
        return self.zygosity_translation.get(zygosity_code, "Unknown")
