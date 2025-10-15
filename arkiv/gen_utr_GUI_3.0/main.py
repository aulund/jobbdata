from generate_document import DocumentGenerator
from gui_manager import GUIManager
from data_manager import DataManager

def main():
    data_manager = DataManager()

    document_generator = DocumentGenerator(data_manager)
    gui_manager = GUIManager(document_generator)
    gui_manager.run()

if __name__ == "__main__":
    main()
