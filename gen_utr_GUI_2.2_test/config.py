"""
Configuration file for the genetic variant data collection application.
Contains all configurable settings including output paths and constants.
"""

import os

# Application settings
APP_TITLE = "Genetisk Variant Datainsamling"
APP_VERSION = "2.6"

# Output directory configuration
# These paths are configurable and can be overridden by environment variables
OUTPUT_PATHS = {
    "Medfodd anemi": os.environ.get(
        "OUTPUT_PATH_ANEMI",
        r"U:\DNA_Sekvenseringsresultat\Remissvar Medfödd anemi\väntande på att svaras ut"
    ),
    "Koagulation": os.environ.get(
        "OUTPUT_PATH_KOAGULATION", 
        r"U:\DNA_Sekvenseringsresultat\Remissvar Koagulation\väntande på att svaras ut"
    ),
    "Övrigt": os.environ.get(
        "OUTPUT_PATH_OVRIGT",
        r"U:\DNA_Sekvenseringsresultat\Remissvar Övrigt\väntande på att svaras ut"
    )
}

# Normal finding output paths
NORMAL_FINDING_PATHS = {
    "Hemolys": os.environ.get(
        "OUTPUT_PATH_HEMOLYS",
        r"U:\DNA_Sekvenseringsresultat\Remissvar Hemolys"
    ),
    "Koagulation": os.environ.get(
        "OUTPUT_PATH_KOAGULATION_NORMAL",
        r"U:\DNA_Sekvenseringsresultat\Remissvar Koagulation"
    ),
    "Övrigt": os.environ.get(
        "OUTPUT_PATH_OVRIGT_NORMAL",
        r"U:\DNA_Sekvenseringsresultat\Remissvar Övrigt"
    )
}

# Category mapping for normal findings
CATEGORY_MAPPING = {
    "Medfodd anemi": "Hemolys",
    "Koagulation": "Koagulation"
}

# Data file paths
GENE_DATA_FILE = "combined_gene_data.json"
ACMG_TRANSLATION_FILE = "acmg_translation.json"
ZYGOSITY_TRANSLATION_FILE = "zygosity_translation.json"
INHERITANCE_TRANSLATION_FILE = "inheritance_translation.json"

# UI settings
DNA_IMAGE_FILE = "dna_helix.png"
DNA_IMAGE_SIZE = (100, 100)

# Sender information
SENDER_INFO = """Professor, Överläkare: Jovan Antovic
Sjukhuskemist: August Lundholm
Biomedicinsk analytiker: Somia Echehli"""

# Sequencing methods
SEQUENCING_METHODS = ["MPS", "Sanger"]

# Yes/No options (Swedish)
YES_NO_OPTIONS = ["ja", "nej"]

# Default values
DEFAULT_UNKNOWN_VALUE = "N/A"
DEFAULT_UNKNOWN_PROBAND = "Probandets genetiska status är inte känd"
DEFAULT_UNKNOWN_STATUS = "Ej känd"

# Genomic analysis text templates
GENOMIC_ANALYSIS_MPS = (
    "Alla kodande regioner med flankerande icke-kodande sekvenser har analyserats med MPS. "
    "Sekvensdata har mappats mot referenssekvens (GRCh37/hg19). "
    "Analysen innefattar endast exon och exon-intron-gränser och därför ingår inte "
    "promotor-, intron- och icke-kodande-regioner i analysen."
)

GENOMIC_ANALYSIS_SANGER = "Exon {exon} av {gene} har analyserats med Sangersekvensering."

NORMAL_FINDING_TEXT = (
    "Vid genetisk analys av genen {gene} ({transcript}) med metoden {method} "
    "påvisades inga avvikelser av möjlig klinisk betydelse."
)
