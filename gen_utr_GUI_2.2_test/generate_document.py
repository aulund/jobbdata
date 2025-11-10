import os
import logging
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import config

logger = logging.getLogger(__name__)

# Template file name (can be customized)
TEMPLATE_FILE = "variant_report_template.docx"


def add_horizontal_line(paragraph):
    """
    Add a horizontal line (border) to a paragraph.
    
    Args:
        paragraph: The paragraph to add the border to
    """
    p = paragraph._element
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')  # Border size
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '4472C4')  # Professional blue color
    pBdr.append(bottom)
    pPr.append(pBdr)


def style_heading(paragraph, text, level=1, color=None):
    """
    Apply professional styling to a heading.
    
    Args:
        paragraph: The paragraph to style
        text: The text content
        level: Heading level (1-3)
        color: Optional RGB color tuple (r, g, b)
    """
    run = paragraph.add_run(text)
    
    if level == 1:
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = RGBColor(68, 114, 196) if not color else RGBColor(*color)  # Professional blue
    elif level == 2:
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(68, 114, 196) if not color else RGBColor(*color)
    else:
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(89, 89, 89) if not color else RGBColor(*color)  # Dark gray
    
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT


def add_section_heading(doc, text, level=2):
    """
    Add a professional section heading with styling.
    
    Args:
        doc: Document object
        text: Heading text
        level: Heading level
        
    Returns:
        The created paragraph
    """
    paragraph = doc.add_paragraph()
    style_heading(paragraph, text, level)
    return paragraph


def add_styled_paragraph(doc, text, bold=False, indent=False):
    """
    Add a styled paragraph with consistent formatting.
    
    Args:
        doc: Document object
        text: Paragraph text
        bold: Whether to make text bold
        indent: Whether to indent the paragraph
        
    Returns:
        The created paragraph
    """
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    
    if bold:
        run.font.bold = True
    
    if indent:
        paragraph.paragraph_format.left_indent = Inches(0.25)
    
    paragraph.paragraph_format.space_after = Pt(6)
    return paragraph


def add_spacer(doc, size=12):
    """
    Add vertical spacing between sections.
    
    Args:
        doc: Document object
        size: Space size in points
    """
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(size)


def add_variant_table(doc, variant, variant_number):
    """
    Add a professionally formatted table for variant information.
    
    Args:
        doc: Document object
        variant: Dictionary containing variant details
        variant_number: The number/index of this variant
    """
    # Add variant heading
    add_section_heading(doc, f"Genetisk Variant {variant_number}", level=2)
    add_spacer(doc, 6)
    
    # Create table with 2 columns
    table = doc.add_table(rows=0, cols=2)
    table.style = 'Light Grid Accent 1'
    
    # Helper function to add a row
    def add_row(label, value):
        row = table.add_row()
        label_cell = row.cells[0]
        value_cell = row.cells[1]
        
        # Style label cell
        label_para = label_cell.paragraphs[0]
        label_run = label_para.add_run(label)
        label_run.font.bold = True
        label_run.font.size = Pt(10)
        label_run.font.color.rgb = RGBColor(68, 114, 196)
        
        # Style value cell
        value_para = value_cell.paragraphs[0]
        value_run = value_para.add_run(str(value))
        value_run.font.size = Pt(10)
    
    # Add variant details
    gene = variant.get('Gene', config.DEFAULT_UNKNOWN_VALUE)
    transcript = variant.get('Transcript', config.DEFAULT_UNKNOWN_VALUE)
    nucleotide_change = variant.get('Nucleotide change', config.DEFAULT_UNKNOWN_VALUE).strip()
    protein_change = variant.get('Protein change', config.DEFAULT_UNKNOWN_VALUE).strip()
    zygosity = variant.get('Zygosity', config.DEFAULT_UNKNOWN_VALUE)
    inheritance = variant.get('Inheritance', config.DEFAULT_UNKNOWN_VALUE)
    disease = variant.get('Disease', config.DEFAULT_UNKNOWN_VALUE)
    acmg = variant.get('ACMG criteria assessment', config.DEFAULT_UNKNOWN_VALUE)
    clinvar = variant.get('ClinVar and hemophilia database reports', config.DEFAULT_UNKNOWN_VALUE)
    
    add_row("Gen", f"{gene}")
    add_row("Transkript", f"{transcript}")
    add_row("Nukleotidförändring", f"c.{nucleotide_change}")
    add_row("Proteinförändring", f"p.{protein_change}")
    add_row("Zygositet", f"{zygosity}")
    add_row("Nedärvning", f"{inheritance}")
    add_row("Sjukdom", f"{disease}")
    add_row("ACMG-bedömning", f"{acmg}")
    
    # Set column widths
    table.columns[0].width = Inches(2.0)
    table.columns[1].width = Inches(4.5)
    
    add_spacer(doc, 6)
    
    # Add clinical significance paragraph
    if clinvar != config.DEFAULT_UNKNOWN_VALUE and clinvar.strip():
        add_styled_paragraph(doc, "Sammanfattning och utlåtande:", bold=True)
        add_styled_paragraph(doc, clinvar, indent=True)
    
    add_spacer(doc, 12)


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
        
        # Generate variant finding document with professional styling
        main_heading = f"Genetisk Rapport: {data['LID-NR']} - {data['variants'][0]['Gene'].upper()}"
        heading_para = doc.add_paragraph()
        style_heading(heading_para, main_heading, level=1)
        
        # Add decorative line
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 12)
        
        # Add each variant with professional table format
        for i, variant in enumerate(data['variants'], 1):
            variant['Transcript'] = variant.get('Transcript', data.get('Transcript', config.DEFAULT_UNKNOWN_VALUE))
            variant['Disease'] = variant.get('Disease', data.get('Disease', config.DEFAULT_UNKNOWN_VALUE))
            
            add_variant_table(doc, variant, i)

        # Proband information section
        add_section_heading(doc, "Proband Information", level=2)
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 6)
        
        proband_info = process_proband_info(data)
        add_styled_paragraph(doc, proband_info)
        add_spacer(doc, 12)

        # Genomic analysis section
        add_section_heading(doc, "Genomisk Analys", level=2)
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 6)
        
        genomic_analysis_info = process_genomic_analysis_info(data)
        add_styled_paragraph(doc, genomic_analysis_info)
        add_spacer(doc, 12)

        # Add references section
        add_references_section(doc)
        add_spacer(doc, 12)

        # Sender information section
        add_section_heading(doc, "Avsändare", level=2)
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 6)
        
        sender_info = get_sender_info()
        add_styled_paragraph(doc, sender_info)

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

        # Main heading with professional styling
        main_heading = f"Genetisk Rapport: {lid_nr} - {gene.upper()}"
        heading_para = doc.add_paragraph()
        style_heading(heading_para, main_heading, level=1)
        
        # Add decorative line
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 12)

        # Normal finding section
        add_section_heading(doc, "Normalt Fynd", level=2)
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 6)
        
        normal_text = config.NORMAL_FINDING_TEXT.format(
            gene=gene,
            transcript=transcript,
            method=sequencing_method
        )
        add_styled_paragraph(doc, normal_text)
        add_spacer(doc, 12)

        # Genomic analysis section
        add_section_heading(doc, "Genomisk Analys", level=2)
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 6)
        
        genomic_info = process_genomic_analysis_info(data)
        add_styled_paragraph(doc, genomic_info)
        add_spacer(doc, 12)

        # Add references section
        add_references_section(doc)
        add_spacer(doc, 12)

        # Sender information section
        add_section_heading(doc, "Avsändare", level=2)
        line_para = doc.add_paragraph()
        add_horizontal_line(line_para)
        add_spacer(doc, 6)
        
        sender_info = get_sender_info()
        add_styled_paragraph(doc, sender_info)

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


def add_references_section(doc):
    """
    Add a professional references section to the document.
    
    Args:
        doc: Document object
    """
    add_section_heading(doc, "Referenser", level=2)
    line_para = doc.add_paragraph()
    add_horizontal_line(line_para)
    add_spacer(doc, 6)
    
    references = [
        "Genome Reference Consortium Human Build (2022), Vol. 37.",
        "Clinical genomics (2022), Stockholm, Sverige. Tillgängligt vid: https://www.scilifelab.se/facilities/clinical-genomics-stockholm/",
        "Scout (2022), Tillgängligt vid: https://github.com/Clinical-Genomics/scout",
        "Landrum MJ, Lee JM, Benson M, Brown GR, Chao C, Chitipiralla S, Gu B, Hart J, Hoffman D, Jang W, Karapetyan K, Katz K, Liu C, Maddipatla Z, Malheiro A, McDaniel K, Ovetsky M, Riley G, Zhou G, Holmes JB, Kattman BL, Maglott DR. ClinVar: improving access to variant interpretations and supporting evidence. Nucleic Acids Res, 2018 Jan 4. PubMed PMID: 29165669",
        "EAHAD Coagulation Factor Variant Databases (2022): https://dbs.eahad.org",
        "Richards, Sue et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Genetics in medicine: official journal of the American College of Medical Genetics vol. 17,5 (2015): 405-24. doi:10.1038/gim.2015.30"
    ]
    
    for i, ref in enumerate(references, 1):
        para = doc.add_paragraph()
        run = para.add_run(f"{i}. {ref}")
        run.font.size = Pt(9)
        run.font.name = 'Calibri'
        para.paragraph_format.left_indent = Inches(0.25)
        para.paragraph_format.space_after = Pt(3)
