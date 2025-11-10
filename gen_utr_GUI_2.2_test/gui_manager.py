import tkinter as tk
from tkinter import ttk
import logging
from general_info import GeneralInfoCollector
from variant_info import VariantInfoCollector
import config

logger = logging.getLogger(__name__)


class MainGUI:
    """Main GUI controller for the genetic variant data collection application."""
    
    def __init__(self, root, gene_data, acmg_translation, zygosity_translation, inheritance_translation):
        self.root = root
        self.root.title(f"{config.APP_TITLE} v{config.APP_VERSION}")
        
        self.gene_data = gene_data
        self.acmg_translation = acmg_translation
        self.zygosity_translation = zygosity_translation
        self.inheritance_translation = inheritance_translation
        
        self.general_info_collector = GeneralInfoCollector(self.root, self.show_variant_info_step)
        self.variant_info_collector = None
        
        self.data = {}
        logger.info("MainGUI initialized")

    def show_variant_info_step(self, data):
        """Display the variant information collection step."""
        self.data = data
        if self.general_info_collector:
            self.general_info_collector.frame.grid_forget()
            
        self.variant_info_collector = VariantInfoCollector(
            root=self.root,
            general_info=self.data,
            gene_data=self.gene_data,
            acmg_translation=self.acmg_translation,
            zygosity_translation=self.zygosity_translation,
            inheritance_translation=self.inheritance_translation,
            submit_data=self.submit_data,
            show_general_info_step=self.show_general_info_step
        )
        logger.info("Showing variant info step")
        self.variant_info_collector.frame.grid()

    def show_general_info_step(self):
        """Display the general information collection step."""
        if self.variant_info_collector:
            self.variant_info_collector.frame.grid_forget()
        logger.info("Showing general info step")
        self.general_info_collector.frame.grid()

    def submit_data(self, data):
        """Submit collected data and close the application."""
        self.data.update(data)
        logger.info("Data submitted, closing application")
        self.root.quit()


def run_gui(gene_data, acmg_translation, zygosity_translation, inheritance_translation):
    """
    Run the GUI application.
    
    Args:
        gene_data: Dictionary containing gene information
        acmg_translation: Dictionary for ACMG criteria translation
        zygosity_translation: Dictionary for zygosity translation
        inheritance_translation: Dictionary for inheritance translation
        
    Returns:
        dict: Collected data from the application
    """
    root = tk.Tk()
    app = MainGUI(
        root,
        gene_data=gene_data,
        acmg_translation=acmg_translation,
        zygosity_translation=zygosity_translation,
        inheritance_translation=inheritance_translation
    )
    root.mainloop()

    return app.data
