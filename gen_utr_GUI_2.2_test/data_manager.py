import json
import logging
import os

logger = logging.getLogger(__name__)


def load_gene_data():
    """
    Loads gene data and translation files needed for the application.
    
    Returns:
        tuple: (gene_data, acmg_translation, zygosity_translation, inheritance_translation)
        
    Raises:
        FileNotFoundError: If any required JSON file is missing
        json.JSONDecodeError: If any JSON file is malformed
    """
    try:
        with open('combined_gene_data.json', 'r', encoding='utf-8') as f:
            gene_data = json.load(f)
        
        with open('acmg_translation.json', 'r', encoding='utf-8') as f:
            acmg_translation = json.load(f)

        with open('zygosity_translation.json', 'r', encoding='utf-8') as f:
            zygosity_translation = json.load(f)

        with open('inheritance_translation.json', 'r', encoding='utf-8') as f:
            inheritance_translation = json.load(f)

        logger.info("Successfully loaded all data files")
        return gene_data, acmg_translation, zygosity_translation, inheritance_translation
        
    except FileNotFoundError as e:
        logger.error(f"Required data file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in data file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading data files: {e}")
        raise
