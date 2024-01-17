import tkinter as tk
from tkinter import ttk, filedialog
import ifcopenshell

def open_ifc_file():
    global open_ifc_file
    file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if file_path:
    ifc_file = ifcopenshell.open(file_path)
    list_elements_per_storey()

def list_elements_per_storey():
    if not ifc_file:
        return
    
    storeys = ifc_file.by_type("ifcBuildingStorey")
    text_output.delete(1.0, tk.END)

    for storey in storeys:
        related_elements = [rel.RelatedElements for rel in storey.ContainsElements]
        element_count = sum(len(elem) for elem in related_elements)
        text_output.insert(tk.END, f"Stockwerk: {storey.Name} - Elemente: {}")