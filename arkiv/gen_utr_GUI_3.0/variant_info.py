class VariantInfo:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_variant_details(self, variant_code):
        acmg_info = self.data_manager.translate_acmg(variant_code.get('acmg', 'Unknown'))
        inheritance_info = self.data_manager.translate_inheritance(variant_code.get('inheritance', 'Unknown'))
        zygosity_info = self.data_manager.translate_zygosity(variant_code.get('zygosity', 'Unknown'))

        return {
            'acmg': acmg_info,
            'inheritance': inheritance_info,
            'zygosity': zygosity_info
        }
