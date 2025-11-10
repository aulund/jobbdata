import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging
from generate_document import generate_document
import config

logger = logging.getLogger(__name__)

# Import export and database modules
try:
    from export import export_to_excel, export_to_pdf, is_excel_available, is_pdf_available
    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False
    logger.warning("Export module not available")

try:
    from database import VariantDatabase
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logger.warning("Database module not available")


class VariantInfoCollector:
    def __init__(self, root, general_info, gene_data, acmg_translation, zygosity_translation, inheritance_translation, submit_data, show_general_info_step):
        self.root = root
        self.general_info = general_info
        self.gene_data = gene_data
        self.acmg_translation = acmg_translation
        self.zygosity_translation = zygosity_translation
        self.inheritance_translation = inheritance_translation
        self.submit_data = submit_data
        self.show_general_info_step = show_general_info_step
        self.data = {"variants": []}

        # Initialize transcript and disease variables
        self.transcript_var = tk.StringVar()
        self.disease_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        variant_frame = ttk.LabelFrame(self.frame, text="Variantinformation")
        variant_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

        self.label_gene_category = ttk.Label(variant_frame, text="Välj genkategori:")
        self.label_gene_category.grid(column=0, row=0, padx=10, pady=5)
        self.combo_gene_category = ttk.Combobox(variant_frame, values=list(self.gene_data.keys()), state="readonly")
        self.combo_gene_category.grid(column=1, row=0, padx=10, pady=5)
        self.combo_gene_category.bind("<<ComboboxSelected>>", self.update_genes)

        self.label_gene = ttk.Label(variant_frame, text="Vilken gen gäller analysen?")
        self.label_gene.grid(column=0, row=1, padx=10, pady=5)
        self.combo_gene = ttk.Combobox(variant_frame, state="readonly")
        self.combo_gene.grid(column=1, row=1, padx=10, pady=5)
        self.combo_gene.bind("<<ComboboxSelected>>", self.autofill_gene_data)

        self.label_nucleotide_change = ttk.Label(variant_frame, text="Specifik nukleotidförändring:")
        self.label_nucleotide_change.grid(column=0, row=2, padx=10, pady=5)
        self.entry_nucleotide_change = ttk.Entry(variant_frame, width=30)
        self.entry_nucleotide_change.grid(column=1, row=2, padx=10, pady=5)
        # HGVS hint label
        self.label_nucleotide_hint = ttk.Label(variant_frame, text="(Format: 123A>G eller 456del)", font=("Arial", 8), foreground="gray")
        self.label_nucleotide_hint.grid(column=1, row=2, padx=10, pady=5, sticky="e")

        self.label_protein_change = ttk.Label(variant_frame, text="Specifik proteinkodande förändring:")
        self.label_protein_change.grid(column=0, row=3, padx=10, pady=5)
        self.entry_protein_change = ttk.Entry(variant_frame, width=30)
        self.entry_protein_change.grid(column=1, row=3, padx=10, pady=5)
        # HGVS hint label
        self.label_protein_hint = ttk.Label(variant_frame, text="(Format: Arg123Cys eller Leu456del)", font=("Arial", 8), foreground="gray")
        self.label_protein_hint.grid(column=1, row=3, padx=10, pady=5, sticky="e")

        self.label_zygosity = ttk.Label(variant_frame, text="Vad är zygositeten för varianten?")
        self.label_zygosity.grid(column=0, row=4, padx=10, pady=5)
        self.combo_zygosity = ttk.Combobox(variant_frame, values=list(self.zygosity_translation.values()), state="readonly")
        self.combo_zygosity.grid(column=1, row=4, padx=10, pady=5)

        self.label_inheritance = ttk.Label(variant_frame, text="Hur är varianten nedärvd?")
        self.label_inheritance.grid(column=0, row=5, padx=10, pady=5)
        self.combo_inheritance = ttk.Combobox(variant_frame, values=list(self.inheritance_translation.values()), state="readonly")
        self.combo_inheritance.grid(column=1, row=5, padx=10, pady=5)

        self.label_acmg = ttk.Label(variant_frame, text="Hur bedöms varianten enligt ACMG-kriterierna?")
        self.label_acmg.grid(column=0, row=6, padx=10, pady=5)
        self.combo_acmg = ttk.Combobox(variant_frame, values=list(self.acmg_translation.values()), state="readonly")
        self.combo_acmg.grid(column=1, row=6, padx=10, pady=5)

        self.label_clinvar = ttk.Label(variant_frame, text="Variantinformation och tidigare rapporterade fynd:")
        self.label_clinvar.grid(column=0, row=7, padx=10, pady=5)
        self.text_clinvar = tk.Text(variant_frame, height=5, width=40)
        self.text_clinvar.grid(column=1, row=7, padx=10, pady=5)

        self.label_further_studies = ttk.Label(variant_frame, text="Är varianten intressant för vidare studier?")
        self.label_further_studies.grid(column=0, row=8, padx=10, pady=5)
        self.combo_further_studies = ttk.Combobox(variant_frame, values=config.YES_NO_OPTIONS, state="readonly")
        self.combo_further_studies.grid(column=1, row=8, padx=10, pady=5)

        # Labels to display the autofilled transcript and disease
        self.label_transcript = ttk.Label(variant_frame, text="Transkript:")
        self.label_transcript.grid(column=0, row=9, padx=10, pady=5)
        self.transcript_display = ttk.Label(variant_frame, textvariable=self.transcript_var)
        self.transcript_display.grid(column=1, row=9, padx=10, pady=5)

        self.label_disease = ttk.Label(variant_frame, text="Sjukdom:")
        self.label_disease.grid(column=0, row=10, padx=10, pady=5)
        self.disease_display = ttk.Label(variant_frame, textvariable=self.disease_var)
        self.disease_display.grid(column=1, row=10, padx=10, pady=5)

        # Variant-knappar
        self.button_add_variant = ttk.Button(self.frame, text="Lägg till variant", command=self.add_variant)
        self.button_add_variant.grid(column=0, row=11, padx=10, pady=5)

        # Variant list management
        list_frame = ttk.LabelFrame(self.frame, text="Tillagda varianter")
        list_frame.grid(column=0, row=12, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        self.variant_listbox = tk.Listbox(list_frame, height=5, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.variant_listbox.yview)
        
        self.variant_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Remove variant button
        self.button_remove_variant = ttk.Button(self.frame, text="Ta bort vald variant", command=self.remove_variant)
        self.button_remove_variant.grid(column=0, row=13, padx=10, pady=5)

        self.button_submit = ttk.Button(self.frame, text="Avsluta och generera rapport", command=self.submit_all)
        self.button_submit.grid(column=1, row=13, padx=10, pady=5)
        
        # Export options
        export_frame = ttk.LabelFrame(self.frame, text="Export alternativ")
        export_frame.grid(column=0, row=14, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.export_excel_var = tk.BooleanVar(value=False)
        self.export_pdf_var = tk.BooleanVar(value=False)
        self.save_to_db_var = tk.BooleanVar(value=True)
        
        excel_available = EXPORT_AVAILABLE and is_excel_available()
        pdf_available = EXPORT_AVAILABLE and is_pdf_available()
        
        self.check_excel = ttk.Checkbutton(
            export_frame, 
            text="Exportera till Excel", 
            variable=self.export_excel_var,
            state="normal" if excel_available else "disabled"
        )
        self.check_excel.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        
        self.check_pdf = ttk.Checkbutton(
            export_frame, 
            text="Konvertera till PDF", 
            variable=self.export_pdf_var,
            state="normal" if pdf_available else "disabled"
        )
        self.check_pdf.grid(column=0, row=1, padx=10, pady=5, sticky="w")
        
        self.check_db = ttk.Checkbutton(
            export_frame, 
            text="Spara i databas", 
            variable=self.save_to_db_var,
            state="normal" if DATABASE_AVAILABLE else "disabled"
        )
        self.check_db.grid(column=0, row=2, padx=10, pady=5, sticky="w")

        # Ny knapp: normalfynd
        self.button_normal = ttk.Button(self.frame, text="Generera normalfynd", command=self.generate_normal_finding)
        self.button_normal.grid(column=0, row=15, columnspan=2, padx=10, pady=5)

        # Tillbaka-knapp
        self.button_back = ttk.Button(self.frame, text="Tillbaka", command=self.show_previous_step)
        self.button_back.grid(column=0, row=16, columnspan=2, padx=10, pady=5)


    def update_genes(self, event):
        category = self.combo_gene_category.get()
        genes = list(self.gene_data[category].keys())  # Get the genes for the selected category
        self.combo_gene['values'] = genes

    def autofill_gene_data(self, event):
        """Autofill transcript and disease information when a gene is selected."""
        gene = self.combo_gene.get()
        gene_info = self.gene_data[self.combo_gene_category.get()].get(gene, {})

        transcript = gene_info.get('Transcript', config.DEFAULT_UNKNOWN_VALUE)
        disease = gene_info.get('Disease', config.DEFAULT_UNKNOWN_VALUE)
        kategori = gene_info.get('Category', 'Övrigt')

        self.transcript_var.set(transcript)
        self.disease_var.set(disease)

        self.data['Transcript'] = transcript
        self.data['Disease'] = disease
        self.data['Category'] = kategori
        
        logger.info(f"Autofilled data for gene {gene}: {transcript}, {disease}")


    def add_variant(self):
        """Add a variant to the list after validation."""
        # Validate required fields
        if not self.combo_gene.get():
            messagebox.showerror("Fel", "Välj en gen")
            return
            
        gene = self.combo_gene.get()
        if gene not in self.gene_data[self.combo_gene_category.get()]:
            messagebox.showerror("Fel", "Okänd gen. Kontrollera genens kortnamn och försök igen.")
            return
        
        if not self.entry_nucleotide_change.get().strip():
            messagebox.showerror("Fel", "Ange nukleotidförändring")
            return
            
        if not self.entry_protein_change.get().strip():
            messagebox.showerror("Fel", "Ange proteinförändring")
            return
            
        if not self.combo_zygosity.get():
            messagebox.showerror("Fel", "Välj zygositet")
            return
            
        if not self.combo_acmg.get():
            messagebox.showerror("Fel", "Välj ACMG-bedömning")
            return

        variant = {
            "Gene": gene,
            "Nucleotide change": self.entry_nucleotide_change.get().strip(),
            "Protein change": self.entry_protein_change.get().strip(),
            "Zygosity": self.combo_zygosity.get(),
            "Inheritance": self.combo_inheritance.get(),
            "ACMG criteria assessment": self.combo_acmg.get(),
            "ClinVar and hemophilia database reports": self.text_clinvar.get("1.0", tk.END).strip(),
            "Further studies": self.combo_further_studies.get()
        }
        self.data["variants"].append(variant)
        
        # Update the listbox with the new variant
        self._update_variant_listbox()
        
        # Clear the input fields for the next variant
        self._clear_variant_fields()
        
        logger.info(f"Added variant for gene {gene}")
        messagebox.showinfo("Info", f"Varianten har lagts till. Totalt {len(self.data['variants'])} variant(er).")

    def _update_variant_listbox(self):
        """Update the listbox to show all added variants."""
        self.variant_listbox.delete(0, tk.END)
        for i, variant in enumerate(self.data["variants"], 1):
            display_text = f"{i}. {variant['Gene']} - c.{variant['Nucleotide change']} p.{variant['Protein change']}"
            self.variant_listbox.insert(tk.END, display_text)
    
    def _clear_variant_fields(self):
        """Clear all variant input fields after adding a variant."""
        self.entry_nucleotide_change.delete(0, tk.END)
        self.entry_protein_change.delete(0, tk.END)
        self.combo_zygosity.set('')
        self.combo_inheritance.set('')
        self.combo_acmg.set('')
        self.text_clinvar.delete("1.0", tk.END)
        self.combo_further_studies.set('')
    
    def remove_variant(self):
        """Remove the selected variant from the list."""
        selection = self.variant_listbox.curselection()
        if not selection:
            messagebox.showwarning("Varning", "Välj en variant att ta bort från listan")
            return
        
        index = selection[0]
        removed_variant = self.data["variants"][index]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Bekräfta borttagning",
            f"Vill du ta bort varianten för {removed_variant['Gene']}?"
        )
        
        if confirm:
            self.data["variants"].pop(index)
            self._update_variant_listbox()
            logger.info(f"Removed variant for gene {removed_variant['Gene']}")
            messagebox.showinfo("Info", f"Varianten har tagits bort. Totalt {len(self.data['variants'])} variant(er) kvar.")

    def submit_all(self):
        """Submit all collected data and generate the document."""
        if not self.data["variants"]:
            messagebox.showerror("Fel", "Du måste lägga till minst en variant innan du skickar in.")
            return

        # Merge general info with variant data
        self.data["LID-NR"] = self.general_info.get("LID-NR", config.DEFAULT_UNKNOWN_VALUE)
        self.data["Proband"] = self.general_info.get("Proband", config.DEFAULT_UNKNOWN_VALUE)
        self.data["Genotype"] = self.general_info.get("Genotype", config.DEFAULT_UNKNOWN_VALUE)
        self.data["Phenotype"] = self.general_info.get("Phenotype", config.DEFAULT_UNKNOWN_VALUE)
        self.data["Sequencing method"] = self.general_info.get("Sequencing method", config.DEFAULT_UNKNOWN_VALUE)
        self.data["Exon"] = self.general_info.get("Exon", "")

        # Determine output directory based on category
        kategori = self.data.get("Category", "Övrigt")
        output_directory = config.OUTPUT_PATHS.get(kategori, config.OUTPUT_PATHS["Övrigt"])

        logger.info(f"Generating document for category: {kategori}")
        
        # Generate document
        output_file = generate_document(self.data, output_directory)
        
        if output_file:
            success_msg = f"Rapporten har genererats:\n{output_file}"
            
            # Handle Excel export
            if self.export_excel_var.get() and EXPORT_AVAILABLE:
                excel_file = export_to_excel(self.data, output_directory)
                if excel_file:
                    success_msg += f"\n\nExcel: {excel_file}"
                    logger.info(f"Excel export successful: {excel_file}")
                else:
                    logger.warning("Excel export failed")
            
            # Handle PDF export
            if self.export_pdf_var.get() and EXPORT_AVAILABLE:
                pdf_file = export_to_pdf(output_file)
                if pdf_file:
                    success_msg += f"\n\nPDF: {pdf_file}"
                    logger.info(f"PDF export successful: {pdf_file}")
                else:
                    logger.warning("PDF export failed")
            
            # Handle database save
            if self.save_to_db_var.get() and DATABASE_AVAILABLE:
                try:
                    db = VariantDatabase()
                    saved_ids = db.save_variant_data(self.data)
                    if saved_ids:
                        success_msg += f"\n\nSparat i databas (IDs: {', '.join(map(str, saved_ids))})"
                        logger.info(f"Saved to database with IDs: {saved_ids}")
                    db.close()
                except Exception as e:
                    logger.error(f"Database save failed: {e}")
            
            messagebox.showinfo("Success", success_msg)
            self.submit_data(self.data)
        else:
            messagebox.showerror("Fel", "Ett fel uppstod vid generering av rapporten. Se loggen för detaljer.")




    def show_previous_step(self):
        self.frame.grid_forget()
        self.show_general_info_step()

    def generate_normal_finding(self):
        """Generate a document for normal finding (no variants detected)."""
        gene = self.combo_gene.get()
        if not gene:
            messagebox.showerror("Fel", "Välj en gen först.")
            return

        gene_info = self.gene_data[self.combo_gene_category.get()].get(gene, {})
        transcript = gene_info.get('Transcript', config.DEFAULT_UNKNOWN_VALUE)
        disease = gene_info.get('Disease', config.DEFAULT_UNKNOWN_VALUE)
        category = gene_info.get('Category', 'Övrigt')

        self.data = {
            "variants": [],
            "Transcript": transcript,
            "Disease": disease,
            "Category": category,
            "Gene": gene,
            "Normalfynd": True,
            "LID-NR": self.general_info.get("LID-NR", config.DEFAULT_UNKNOWN_VALUE),
            "Proband": self.general_info.get("Proband", config.DEFAULT_UNKNOWN_VALUE),
            "Genotype": self.general_info.get("Genotype", config.DEFAULT_UNKNOWN_VALUE),
            "Phenotype": self.general_info.get("Phenotype", config.DEFAULT_UNKNOWN_VALUE),
            "Sequencing method": self.general_info.get("Sequencing method", config.DEFAULT_UNKNOWN_VALUE),
            "Exon": self.general_info.get("Exon", "")
        }

        # Map category to output directory
        mapped_category = config.CATEGORY_MAPPING.get(category, "Övrigt")
        output_directory = config.NORMAL_FINDING_PATHS.get(mapped_category, config.NORMAL_FINDING_PATHS["Övrigt"])

        logger.info(f"Generating normal finding for {gene} in category {mapped_category}")
        
        output_file = generate_document(self.data, output_directory)
        
        if output_file:
            success_msg = f"Normalfynd har genererats:\n{output_file}"
            
            # Handle Excel export
            if self.export_excel_var.get() and EXPORT_AVAILABLE:
                excel_file = export_to_excel(self.data, output_directory)
                if excel_file:
                    success_msg += f"\n\nExcel: {excel_file}"
                    logger.info(f"Excel export successful: {excel_file}")
            
            # Handle PDF export
            if self.export_pdf_var.get() and EXPORT_AVAILABLE:
                pdf_file = export_to_pdf(output_file)
                if pdf_file:
                    success_msg += f"\n\nPDF: {pdf_file}"
                    logger.info(f"PDF export successful: {pdf_file}")
            
            # Handle database save
            if self.save_to_db_var.get() and DATABASE_AVAILABLE:
                try:
                    db = VariantDatabase()
                    saved_ids = db.save_variant_data(self.data)
                    if saved_ids:
                        success_msg += f"\n\nSparat i databas (IDs: {', '.join(map(str, saved_ids))})"
                        logger.info(f"Saved to database with IDs: {saved_ids}")
                    db.close()
                except Exception as e:
                    logger.error(f"Database save failed: {e}")
            
            messagebox.showinfo("Success", success_msg)
            self.submit_data(self.data)
        else:
            messagebox.showerror("Fel", "Ett fel uppstod vid generering av normalfynd. Se loggen för detaljer.")
