# main.py
from collect_variant_data import main as collect_variant_data
from generate_document import generate_document

def main():
    data = collect_variant_data()
    generate_document(data)

if __name__ == "__main__":
    main()
