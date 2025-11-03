# Genetisk Variant Datainsamling - Version 2.2

Detta är en GUI-applikation för insamling av genetisk variantdata och generering av rapporter.

## Funktioner

- Insamling av allmän patientinformation (LID-NR, proband, sekvenseringsmetod)
- Registrering av variantinformation (gen, nukleotid-/proteinförändringar, zygositet, ACMG-klassificering)
- Automatisk generering av Word-dokument med rapporter
- Stöd för normalfynd (inga varianter påvisade)

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
- Möjlighet att redigera/ta bort varianter efter tillägg
- Förhandsgranskning av rapport innan generering
- Export till andra format (PDF, Excel)
- Databaslagring av varianter
- Enhetstester
