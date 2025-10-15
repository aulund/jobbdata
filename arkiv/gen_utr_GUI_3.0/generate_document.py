class DocumentGenerator:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def generate_gene_report(self, gene_name):
        gene_info = self.data_manager.get_gene_info(gene_name)
        disease_info = self.data_manager.get_disease_info(gene_name)
        transcript_info = self.data_manager.get_transcript_info(gene_name)

        report = (
            f"Gene: {gene_name}\n"
            f"HGNC ID: {gene_info.get('hgnc_id', 'Unknown')}\n"
            f"Transcript: {transcript_info}\n"
            f"Genetic Disease Models: {gene_info.get('genetic_disease_models', 'Unknown')}\n"
            f"Disease: {disease_info}\n"
        )
        return report

    def generate_full_report(self, gene_list):
        report = ""
        for gene_name in gene_list:
            report += self.generate_gene_report(gene_name)
            report += "\n" + "-"*40 + "\n"
        return report
