# Word Document Template Instructions

## Creating a Custom Template

To use a custom Word document template for variant reports:

1. Create a Word document named `variant_report_template.docx`
2. Place it in the same directory as the Python files
3. Add your desired formatting, headers, logos, and standard text
4. The application will use this template and append the variant data

## Template Content Suggestions

Your template can include:
- **Company/Lab logo** in the header
- **Standard header text** (lab name, contact info)
- **Formatting styles** for headings and paragraphs
- **Footer** with page numbers, disclaimers, etc.
- **Standard introduction text**

## How It Works

- If `variant_report_template.docx` exists, the app loads it
- If the template is not found, the app creates a blank document
- Variant data is appended after any template content

## Example Python Code to Create a Basic Template

```python
from docx import Document

# Create template
doc = Document()

# Add your header
doc.add_heading('Genetisk Analys Laboratorium', level=1)
doc.add_paragraph('Kontakt: info@lab.se | Tel: 123-456')
doc.add_paragraph()
doc.add_paragraph('─' * 60)
doc.add_paragraph()

# Save template
doc.save('variant_report_template.docx')
```

## Testing

After creating your template:
1. Run the application
2. Generate a test report
3. Verify the template formatting appears correctly
4. Adjust template as needed

## Notes

- Template is optional - app works without it
- Same template used for variants and normal findings
- Template affects all generated reports
- Update template anytime by replacing the file
