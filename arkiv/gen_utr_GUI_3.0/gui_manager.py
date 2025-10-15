import tkinter as tk
from tkinter import scrolledtext

class GUIManager:
    def __init__(self, document_generator):
        self.document_generator = document_generator
        self.root = tk.Tk()
        self.root.title("Gene Report Generator")

        self.label = tk.Label(self.root, text="Enter gene names (comma-separated):")
        self.label.pack()

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack()

        self.generate_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.generate_button.pack()

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack()

    def generate_report(self):
        gene_names = self.entry.get().split(',')
        report = self.document_generator.generate_full_report([gene.strip() for gene in gene_names])
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, report)

    def run(self):
        self.root.mainloop()
