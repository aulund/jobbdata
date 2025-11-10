import logging
from gui_manager import run_gui
from data_manager import load_gene_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the genetic variant data collection application."""
    try:
        logger.info("Starting application")
        gene_data, acmg_translation, zygosity_translation, inheritance_translation = load_gene_data()

        run_gui(
            gene_data=gene_data,
            acmg_translation=acmg_translation,
            zygosity_translation=zygosity_translation,
            inheritance_translation=inheritance_translation
        )
        logger.info("Application closed")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
