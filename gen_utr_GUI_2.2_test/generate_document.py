import os
from docx import Document

def generate_document(data, output_path):
    try:
        print("Starting report generation...")

        if not data:
            print("Ingen data att generera dokument från.")
            return

        print("Data received:", data)

        # Normalfynd?
        if data.get("Normalfynd", False):
            generate_normalfinding_document(data, output_path)
            return

        # Fortsätt med variantfynd
        doc = Document()
        main_heading = f"{data['LID-NR']} -- {data['variants'][0]['Gene'].upper()}"
        doc.add_heading(main_heading, level=1)

        doc.add_paragraph("------------------------------")
        for i, variant in enumerate(data['variants'], 1):
            variant['Transcript'] = variant.get('Transcript', data.get('Transcript', 'N/A'))
            variant['Disease'] = variant.get('Disease', data.get('Disease', 'N/A'))
            
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

        filename = f"{data['LID-NR']}_{data['variants'][0]['Gene'].upper()}.docx"
        output_file = os.path.join(output_path, filename)
        doc.save(output_file)
        print(f"Dokumentet har skapats och sparats som '{output_file}'")

    except Exception as e:
        print(f"An error occurred during report generation: {e}")

def generate_normalfinding_document(data, output_path):
    doc = Document()

    gene = data.get("Gene", "okänd gen")
    lid_nr = data.get("LID-NR", "okänt ID")
    transcript = data.get("Transcript", "")
    sequencing_method = data.get("Sequencing method", "okänd metod")
    category = data.get("Category", "okänd kategori")

    main_heading = f"{lid_nr} -- {gene.upper()}"
    doc.add_heading(main_heading, level=1)

    doc.add_paragraph("------------------------------")
    doc.add_paragraph("Normalt Fynd:")
    doc.add_paragraph(
        f"Vid genetisk analys av genen {gene} ({transcript}) med metoden {sequencing_method} "
        f"påvisades inga avvikelser av möjlig klinisk betydelse."
    )
    doc.add_paragraph("------------------------------")

    genomic_info = process_genomic_analysis_info(data)
    doc.add_paragraph("Genomisk Analys:")
    doc.add_paragraph(genomic_info)
    doc.add_paragraph("------------------------------")

    sender_info = get_sender_info()
    doc.add_paragraph("Avsändare:")
    doc.add_paragraph(sender_info)
    doc.add_paragraph("------------------------------")

    filename = f"{lid_nr}_{gene.upper()}_normalfynd.docx"
    output_file = os.path.join(output_path, filename)
    doc.save(output_file)
    print(f"Normalfyndsdokument har skapats och sparats som '{output_file}'")

def process_variant_info(variant):
    gene = variant.get('Gene', 'N/A')
    transcript = variant.get('Transcript', 'N/A')
    nucleotide_change = variant.get('Nucleotide change', 'N/A').strip()
    protein_change = variant.get('Protein change', 'N/A').strip()
    zygosity = variant.get('Zygosity', 'N/A')
    inheritance = variant.get('Inheritance', 'N/A')
    disease = variant.get('Disease', 'N/A')
    
    info = (f"{gene} ({transcript}): c.{nucleotide_change} p.{protein_change} {zygosity}.\n"
            f"Det är troligt att varianten orsakar {disease}.\n"
            f"Nedärvning: {inheritance}.")
    return info

def process_assessment_info(variant):
    acmg = variant.get('ACMG criteria assessment', 'N/A')
    clinvar = variant.get('ClinVar and hemophilia database reports', 'N/A')
    
    info = (f"Bedömning enligt ACMG-kriterierna: {acmg}.\n"
            f"Sammanfattning och utlåtande: {clinvar}.")
    return info

def process_proband_info(data):
    proband = data.get('Proband', 'N/A')
    genotype = data.get('Genotype', 'N/A')
    phenotype = data.get('Phenotype', 'N/A')

    info = f"{proband}\n"
    if proband != 'N/A':
        info += (f"Genotyp: {genotype}\n"
                 f"Fenotyp: {phenotype}")
    return info

def process_genomic_analysis_info(data):
    sequencing_method = data.get('Sequencing method', 'N/A').strip().lower()
    exon = data.get('Exon', 'N/A')

    if sequencing_method == 'sanger':
        return f"Exon {exon} av {data.get('Gene', 'genen')} har analyserats med Sangersekvensering."
    else:
        return (
            "Alla kodande regioner med flankerande icke-kodande sekvenser har analyserats med MPS. "
            "Sekvensdata har mappats mot referenssekvens (GRCh37/hg19). "
            "Analysen innefattar endast exon och exon-intron-gränser och därför ingår inte "
            "promotor-, intron- och icke-kodande-regioner i analysen."
        )

def get_sender_info():
    return "MVH August Lundholm, Molekylärbiolog"
