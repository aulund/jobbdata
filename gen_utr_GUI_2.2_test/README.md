# Genetisk Variant Datainsamling - Version 2.6

Detta är en GUI-applikation för insamling av genetisk variantdata och generering av rapporter.

## Funktioner

- Insamling av allmän patientinformation (LID-NR, proband, sekvenseringsmetod)
- Registrering av variantinformation (gen, nukleotid-/proteinförändringar, zygositet, ACMG-klassificering)
- **Varianthantering**: Visa, ta bort och hantera tillagda varianter innan generering
- **HGVS-formathjälp**: Inbyggda formatanvisningar för nukleotid- och proteinförändringar
- **Excel-export till kollektiva filer**: Exportera och lägg till data till gemensamma Excel-filer uppdelade per genkategori
- **PDF-export**: Konvertera Word-dokument till PDF-format
- **Databaslagring**: Spara varianter i SQLite-databas för historik och analys
- **Dokumentmallar**: Använd anpassade Word-mallar för rapporter
- **Professionell dokumentformatering**: Automatisk generering av professionella Word-dokument med styling
- Automatisk generering av Word-dokument med rapporter
- Stöd för normalfynd (inga varianter påvisade)

## Förbättringar i version 2.6

### Professionell dokumentformatering
- **Professionell typografi**: Stiliserade rubriker med professionell blå färg (#4472C4)
  - Huvudrubrik: 20pt fetstil
  - Sektionsrubriker: 16pt fetstil
  - Brödtext: 11pt Calibri för bättre läsbarhet
  
- **Strukturerade datatabeller**: Variantinformation presenteras i professionella tabeller
  - Tvåkolumnslayout med etiketter och värden
  - Stiliserade headers i blått
  - Tydlig och lättläst formatering
  
- **Visuell hierarki**: Förbättrad dokumentstruktur
  - Professionella blå horisontella linjer mellan sektioner
  - Konsekvent avstånd mellan element
  - Tydliga sektionsgränser
  
- **Formell referenssektion**: Numrerad lista med vetenskapliga referenser
  - Genome Reference Consortium
  - Clinical Genomics Stockholm
  - ClinVar databas
  - ACMG-riktlinjer
  
- **Förbättrad avsändarinformation**: Komplett teamlista med roller

Se CHANGELOG_v2.6.md för fullständiga detaljer.

## Förbättringar i version 2.5

### Nya funktioner
- **Kollektiva Excel-filer**: Excel-export lägger nu till data till gemensamma filer
  - En fil per genkategori (Koagulation_collective.xlsx, Medfodd_anemi_collective.xlsx)
  - Data från alla körningar samlas i samma fil
  - Automatisk hantering av både nya och befintliga filer
  
- **Dokumentmallar**: Stöd för anpassade Word-mallar
  - Placera `variant_report_template.docx` i programmets mapp
  - Mallen används för både varianter och normalfynd
  - Fallback till blank dokument om mall saknas
  - Se TEMPLATE_INSTRUCTIONS.md för detaljer

## Förbättringar i version 2.5

### Nya funktioner
- **Excel-export**: Exportera alla variantdata till strukturerad Excel-fil med formatering
- **PDF-konvertering**: Automatisk konvertering av Word-dokument till PDF
- **Databas-integration**: 
  - SQLite-databas för persistent lagring
  - Automatisk databasskapa vid första körning
  - Lagrar all variantinformation med tidsstämpel
  - Möjlighet att söka historiska data per LID-NR eller gen
- **Export-alternativ**: Checkboxar i GUI för att välja exportformat
- **requirements.txt**: Specificerade beroenden för enkel installation

## Förbättringar i version 2.4

### Nya funktioner
- **Variantlista**: Visar alla tillagda varianter i en lista
- **Ta bort varianter**: Möjlighet att ta bort varianter innan rapportgenerering
- **Automatisk fältrensning**: Formuläret rensas efter att en variant läggs till
- **HGVS-formathjälp**: Visar formatexempel för nukleotid (123A>G) och protein (Arg123Cys) ändringar

## Förbättringar i version 2.2

### Kodkvalitet
- **Förbättrad felhantering**: Omfattande felhantering för alla filoperationer
- **Loggning**: Ersatt print-statements med professionell loggning
- **Kodstruktur**: Eliminerat duplicerad kod i `data_manager.py`
- **Validering**: Inmatningsvalidering för alla användarfält
- **Dokumentation**: Docstrings tillagda för alla funktioner och klasser

### Konfiguration
- **Konfigurationsfil** (`config.py`): Alla inställningar centraliserade
- **Miljövariabler**: Stöd för att överskriva output-paths via miljövariabler
- **Plattformsoberoende**: Förbättrat stöd för olika filsystem

### Användarvänlighet
- **Bättre feedback**: Mer informativa felmeddelanden och bekräftelser
- **Robusthet**: Applikationen hanterar saknade bilder och konfigurationer graciöst
- **Statusuppdateringar**: Tydligare information om antal tillagda varianter

## Användning

### Lägga till varianter

1. Välj genkategori och gen
2. Fyll i nukleotidförändring (format: 123A>G eller 456del)
3. Fyll i proteinförändring (format: Arg123Cys eller Leu456del)
4. Välj zygositet, nedärvning och ACMG-bedömning
5. Klicka "Lägg till variant"
6. Varianten visas i listan nedan

### Hantera varianter

- **Visa varianter**: Alla tillagda varianter visas i listan "Tillagda varianter"
- **Ta bort variant**: Välj en variant i listan och klicka "Ta bort vald variant"
- **Välj export-alternativ**: Kryssa i önskade exportformat (Excel, PDF, Databas)
- **Generera rapport**: När alla varianter är tillagda, klicka "Avsluta och generera rapport"

### Exportalternativ

- **Exportera till Excel**: Lägger till variantdata i kollektiva Excel-filer
  - Data läggs till i: `Koagulation_collective.xlsx` eller `Medfodd_anemi_collective.xlsx`
  - Automatisk uppdelning baserat på genkategori
  - Alla analyser samlas i samma fil för enkel överblick
  
- **Konvertera till PDF**: Konvertera Word-dokumentet automatiskt till PDF-format

- **Spara i databas**: Lagra variantdata i lokal SQLite-databas för framtida analys

### Word Dokumentmallar

För att använda anpassade mallar:
1. Skapa en Word-fil med namnet `variant_report_template.docx`
2. Placera den i samma mapp som programmet
3. Lägg till logotyp, rubrikstilar, och standardtext
4. Programmet använder mallen automatiskt

Se `TEMPLATE_INSTRUCTIONS.md` för detaljerad guide.

### Normalfynd

För prover utan patogena varianter:
1. Välj gen
2. Välj önskade export-alternativ
3. Klicka "Generera normalfynd"

## Installation

### Beroenden

**Grundläggande:**
```bash
pip install python-docx pillow
```

**Med alla export-funktioner (v2.4):**
```bash
pip install -r requirements.txt
```

Detta installerar:
- python-docx (Word-dokument)
- Pillow (bildhantering)
- openpyxl (Excel-export)
- docx2pdf (PDF-konvertering)
- sqlalchemy (databas)

**OBS:** PDF-export kräver Microsoft Word installerat på Windows. På andra plattformar kan alternativa lösningar användas.

### Körning

```bash
python main.py
```

## Databas

Applikationen skapar automatiskt en SQLite-databas (`variants.db`) vid första användningen om "Spara i databas" är aktiverat.

### Databasstruktur

- **Tabell**: `variants`
- **Lagrar**: LID-NR, gen, nukleotid/proteinförändringar, ACMG-bedömning, patientinformation, tidsstämpel
- **Användning**: Historisk data, statistik, sökningar

### Söka i databas

Databas-API:et tillhandahåller metoder för att:
- Hämta alla varianter för ett specifikt LID-NR
- Hämta alla varianter för en specifik gen
- Hämta de senaste N varianterna

## Konfiguration

Output-paths kan konfigureras via miljövariabler:

```bash
export OUTPUT_PATH_KOAGULATION="/path/to/koagulation"
export OUTPUT_PATH_ANEMI="/path/to/anemi"
export OUTPUT_PATH_OVRIGT="/path/to/ovrigt"
```

Eller genom att redigera `config.py` direkt.

## Loggning

Applikationen skapar en loggfil `app.log` som innehåller detaljerad information om:
- Applikationens start och avslut
- Dataladdning och validering
- Dokumentgenerering
- Fel och varningar

## Kodstruktur

- `main.py`: Huvudingång till applikationen
- `gui_manager.py`: GUI-koordinator
- `general_info.py`: Insamling av allmän patientinformation
- `variant_info.py`: Insamling av variantinformation
- `data_manager.py`: Hantering av JSON-datafiler
- `generate_document.py`: Dokumentgenerering
- `config.py`: Konfigurationsinställningar

## Nästa steg

Möjliga framtida förbättringar:
- Förhandsgranskning av rapport innan generering
- Export till andra format (PDF, Excel)
- Databaslagring av varianter
- Enhetstester
- Strikt HGVS-validering med reguljära uttryck
