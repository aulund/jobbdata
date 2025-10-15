# append_to_excel.py
import os
import pandas as pd

def append_to_excel(data):
    """Appends interesting variants to the Excel file."""
    excel_path = "U:\\DNA_Sekvenseringsresultat\\Remissvar Koagulation\\variant_studier.xlsx"  # Changed the file name here
    rows = []
    for variant in data['variants']:
        if variant['Further studies'] == 'ja':
            rows.append({
                'LID-NR': data['LID-NR'],
                'Gene': variant['Gene'].upper(),
                'Transcript': variant['Transcript'],
                'Nucleotide change': variant['Nucleotide change'],
                'Protein change': variant['Protein change'],
                'Zygosity': variant['Zygosity'],
                'Disease': variant['Disease'],
                'ACMG criteria assessment': variant['ACMG criteria assessment']
            })

    if rows:
        df = pd.DataFrame(rows)
        try:
            if os.path.exists(excel_path):
                with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a') as writer:
                    existing_df = pd.read_excel(excel_path)
                    combined_df = pd.concat([existing_df, df], ignore_index=True)
                    combined_df.to_excel(writer, index=False)
            else:
                df.to_excel(excel_path, index=False)
            print(f"Information om intressanta varianter har lagts till '{excel_path}'")
        except PermissionError:
            print(f"Kan inte skriva till '{excel_path}'. Kontrollera att filen inte är öppen i ett annat program och försök igen.")
        except Exception as e:
            print(f"Ett fel uppstod vid skrivning till '{excel_path}': {e}")
