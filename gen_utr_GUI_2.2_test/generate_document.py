import os
import logging
from docx import Document
import config

logger = logging.getLogger(__name__)

# Template file name (can be customized)
TEMPLATE_FILE = "variant_report_template.docx"


def generate_document(data, output_path):
    """
    Generate a Word document with genetic variant information using a template if available.
    
    Args:
        data: Dictionary containing all collected variant and patient information
        output_path: Directory path where the document should be saved
        
    Returns:
        str: Path to the generated document, or None if generation failed
    """
    try:
        logger.info("Starting report generation...")

        if not data:
            logger.error("No data provided for document generation")
            return None
        
        # Validate output path
        if not output_path or '..' in output_path:
            logger.error(f"Invalid output path: {output_path}")
            return None

        # Check if this is a normal finding
        if data.get("Normalfynd", False):
            return generate_normalfinding_document(data, output_path)

        # Validate required data
        if not data.get("variants"):
            logger.error("No variants provided in data")
            return None
            
        if not data.get("LID-NR"):
            logger.error("No LID-NR provided in data")
            return None

        # Try to load template, otherwise create blank document
        template_path = os.path.join(os.path.dirname(__file__), TEMPLATE_FILE)
        if os.path.exists(template_path):
            doc = Document(template_path)
            logger.info(f"Using template: {template_path}")
        else:
            doc = Document()
            logger.info("No template found, creating blank document")
        
        # Generate variant finding document
        main_heading = f"{data['LID-NR']} -- {data['variants'][0]['Gene'].upper()}"
        doc.add_heading(main_heading, level=1)

        doc.add_paragraph("------------------------------")
        for i, variant in enumerate(data['variants'], 1):
            variant['Transcript'] = variant.get('Transcript', data.get('Transcript', config.DEFAULT_UNKNOWN_VALUE))
            variant['Disease'] = variant.get('Disease', data.get('Disease', config.DEFAULT_UNKNOWN_VALUE))
            
            variant_info = process_variant_info(variant)
            doc.add_paragraph(f"Genetisk Variant {i}:")
            doc.add_paragraph(variant_info)

            assessment_info = process_assessment_info(variant)
            doc.add_paragraph(assessment_info)
            doc.add_paragraph("------------------------------")

        proband_info = process_proband_info(data)
        doc.add_paragraph("Proband:")
        doc.add_paragraph(proband_info)
        doc.add_paragraph("------------------------------")

        genomic_analysis_info = process_genomic_analysis_info(data)
        doc.add_paragraph("Genomisk Analys:")
        doc.add_paragraph(genomic_analysis_info)
        doc.add_paragraph("------------------------------")

        sender_info = get_sender_info()
        doc.add_paragraph("Avsändare:")
        doc.add_paragraph(sender_info)
        doc.add_paragraph("------------------------------")

        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)

        filename = f"{data['LID-NR']}_{data['variants'][0]['Gene'].upper()}.docx"
        output_file = os.path.join(output_path, filename)
        doc.save(output_file)
        logger.info(f"Document successfully created: {output_file}")
        return output_file

    except Exception as e:
        logger.error(f"Error during report generation: {e}", exc_info=True)
        return None

def generate_normalfinding_document(data, output_path):
    """
    Generate a Word document for normal finding (no variants detected) using a template if available.
    
    Args:
        data: Dictionary containing gene and patient information
        output_path: Directory path where the document should be saved
        
    Returns:
        str: Path to the generated document, or None if generation failed
    """
    try:
        # Validate output path
        if not output_path or '..' in output_path:
            logger.error(f"Invalid output path: {output_path}")
            return None
        
        # Try to load template, otherwise create blank document
        template_path = os.path.join(os.path.dirname(__file__), TEMPLATE_FILE)
        if os.path.exists(template_path):
            doc = Document(template_path)
            logger.info(f"Using template for normal finding: {template_path}")
        else:
            doc = Document()
            logger.info("No template found for normal finding, creating blank document")

        gene = data.get("Gene", "okänd gen")
        lid_nr = data.get("LID-NR", "okänt ID")
        transcript = data.get("Transcript", "")
        sequencing_method = data.get("Sequencing method", "okänd metod")

        main_heading = f"{lid_nr} -- {gene.upper()}"
        doc.add_heading(main_heading, level=1)

        doc.add_paragraph("------------------------------")
        doc.add_paragraph("Normalt Fynd:")
        
        normal_text = config.NORMAL_FINDING_TEXT.format(
            gene=gene,
            transcript=transcript,
            method=sequencing_method
        )
        doc.add_paragraph(normal_text)
        doc.add_paragraph("------------------------------")

        genomic_info = process_genomic_analysis_info(data)
        doc.add_paragraph("Genomisk Analys:")
        doc.add_paragraph(genomic_info)
        doc.add_paragraph("------------------------------")

        sender_info = get_sender_info()
        doc.add_paragraph("Avsändare:")
        doc.add_paragraph(sender_info)
        doc.add_paragraph("------------------------------")

        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)

        filename = f"{lid_nr}_{gene.upper()}_normalfynd.docx"
        output_file = os.path.join(output_path, filename)
        doc.save(output_file)
        logger.info(f"Normal finding document created: {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"Error generating normal finding document: {e}", exc_info=True)
        return None

def process_variant_info(variant):
    """
    Process variant information into formatted text.
    
    Args:
        variant: Dictionary containing variant details
        
    Returns:
        str: Formatted variant information
    """
    gene = variant.get('Gene', config.DEFAULT_UNKNOWN_VALUE)
    transcript = variant.get('Transcript', config.DEFAULT_UNKNOWN_VALUE)
    nucleotide_change = variant.get('Nucleotide change', config.DEFAULT_UNKNOWN_VALUE).strip()
    protein_change = variant.get('Protein change', config.DEFAULT_UNKNOWN_VALUE).strip()
    zygosity = variant.get('Zygosity', config.DEFAULT_UNKNOWN_VALUE)
    inheritance = variant.get('Inheritance', config.DEFAULT_UNKNOWN_VALUE)
    disease = variant.get('Disease', config.DEFAULT_UNKNOWN_VALUE)
    
    info = (f"{gene} ({transcript}): c.{nucleotide_change} p.{protein_change} {zygosity}.\n"
            f"Det är troligt att varianten orsakar {disease}.\n"
            f"Nedärvning: {inheritance}.")
    return info


def process_assessment_info(variant):
    """
    Process ACMG assessment and ClinVar information.
    
    Args:
        variant: Dictionary containing assessment details
        
    Returns:
        str: Formatted assessment information
    """
    acmg = variant.get('ACMG criteria assessment', config.DEFAULT_UNKNOWN_VALUE)
    clinvar = variant.get('ClinVar and hemophilia database reports', config.DEFAULT_UNKNOWN_VALUE)
    
    info = (f"Bedömning enligt ACMG-kriterierna: {acmg}.\n"
            f"Sammanfattning och utlåtande: {clinvar}.")
    return info


def process_proband_info(data):
    """
    Process proband information.
    
    Args:
        data: Dictionary containing proband details
        
    Returns:
        str: Formatted proband information
    """
    proband = data.get('Proband', config.DEFAULT_UNKNOWN_VALUE)
    genotype = data.get('Genotype', config.DEFAULT_UNKNOWN_VALUE)
    phenotype = data.get('Phenotype', config.DEFAULT_UNKNOWN_VALUE)

    info = f"{proband}\n"
    if proband != config.DEFAULT_UNKNOWN_VALUE and proband != config.DEFAULT_UNKNOWN_PROBAND:
        info += (f"Genotyp: {genotype}\n"
                 f"Fenotyp: {phenotype}")
    return info


def process_genomic_analysis_info(data):
    """
    Process genomic analysis information based on sequencing method.
    
    Args:
        data: Dictionary containing sequencing method and other details
        
    Returns:
        str: Formatted genomic analysis information
    """
    sequencing_method = data.get('Sequencing method', config.DEFAULT_UNKNOWN_VALUE).strip().lower()
    exon = data.get('Exon', '')
    gene = data.get('Gene', 'genen')

    if sequencing_method == 'sanger':
        return config.GENOMIC_ANALYSIS_SANGER.format(exon=exon, gene=gene)
    else:
        return config.GENOMIC_ANALYSIS_MPS


def get_sender_info():
    """
    Get sender information for the document.
    
    Returns:
        str: Sender information
    """
    return config.SENDER_INFO
