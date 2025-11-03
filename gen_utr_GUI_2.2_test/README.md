# Genetisk Variant Datainsamling - Version 2.3

Detta är en GUI-applikation för insamling av genetisk variantdata och generering av rapporter.

## Funktioner

- Insamling av allmän patientinformation (LID-NR, proband, sekvenseringsmetod)
- Registrering av variantinformation (gen, nukleotid-/proteinförändringar, zygositet, ACMG-klassificering)
- **Varianthantering**: Visa, ta bort och hantera tillagda varianter innan generering
- **HGVS-formathjälp**: Inbyggda formatanvisningar för nukleotid- och proteinförändringar
- Automatisk generering av Word-dokument med rapporter
- Stöd för normalfynd (inga varianter påvisade)

## Förbättringar i version 2.3

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
- **Generera rapport**: När alla varianter är tillagda, klicka "Avsluta och generera rapport"

### Normalfynd

För prover utan patogena varianter:
1. Välj gen
2. Klicka "Generera normalfynd"

## Installation

### Beroenden

```bash
pip install python-docx pillow
```

### Körning

```bash
python main.py
```

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
