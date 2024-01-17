import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Processors import copy_processor as copy_p
from Processors import transformation_processor as trans_p

class IfcExcelManipulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("IFC Excel Manipulator")
        self.master.configure(bg="#DCE6F1")

        self.default_font = ('Calibri', 12)
        self.master.option_add('*Font', self.default_font)

        # Create a custom style for buttons
        self.master.style = ttk.Style()
        self.master.style.configure('TButton', font=self.default_font)

        self.create_widgets()

    def create_widgets(self):
        ifc_frame = ttk.Frame(self.master, padding="10", style="TFrame")
        ifc_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        xls_frame = ttk.Frame(self.master, padding="10", style="TFrame")
        xls_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        export_frame = ttk.Frame(self.master, padding="10", style="TFrame")
        export_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        filename_frame = ttk.Frame(self.master, padding="10", style="TFrame")
        filename_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        ifc_label = ttk.Label(ifc_frame, text="Wähle IFC-Datei:", style="TLabel")
        ifc_label.grid(row=0, column=0, sticky="w")

        ifc_entry = ttk.Entry(ifc_frame, font=self.default_font)
        ifc_entry.grid(row=0, column=1, sticky="ew")

        ifc_browse_button = ttk.Button(ifc_frame, text="Durchsuchen", command=lambda: self.browse_button(ifc_entry), style="TButton")
        ifc_browse_button.grid(row=0, column=2, sticky="ew")

        xls_label = ttk.Label(xls_frame, text="Wähle Excel-Datei:", style="TLabel")
        xls_label.grid(row=0, column=0, sticky="w")

        xls_entry = ttk.Entry(xls_frame, font=self.default_font)
        xls_entry.grid(row=0, column=1, sticky="ew")

        xls_browse_button = ttk.Button(xls_frame, text="Durchsuchen", command=lambda: self.browse_button(xls_entry), style="TButton")
        xls_browse_button.grid(row=0, column=2, sticky="ew")

        export_label = ttk.Label(export_frame, text="Wähle Zielordner:", style="TLabel")
        export_label.grid(row=0, column=0, sticky="w")

        export_entry = ttk.Entry(export_frame, font=self.default_font)
        export_entry.grid(row=0, column=1, sticky="ew")

        export_browse_button = ttk.Button(export_frame, text="Durchsuchen", command=lambda: self.select_folder(export_entry), style="TButton")
        export_browse_button.grid(row=0, column=2, sticky="ew")

        filename_label = ttk.Label(filename_frame, text="Dateiname:", style="TLabel")
        filename_label.grid(row=0, column=0, sticky="w")

        filename_entry = ttk.Entry(filename_frame, font=self.default_font)
        filename_entry.grid(row=0, column=1, sticky="ew")

        start_button = ttk.Button(self.master, text="Start", command=lambda: self.process_data(ifc_entry.get(), xls_entry.get(), export_entry.get(), filename_entry.get()), style="TButton")
        start_button.grid(row=4, column=0, pady=10)

    def browse_button(self, entry):
        filename = filedialog.askopenfilename(title="Datei auswählen")
        entry.delete(0, tk.END)
        entry.insert(0, filename)

    def select_folder(self, entry):
        foldername = filedialog.askdirectory(title="Ordner auswählen")
        entry.delete(0, tk.END)
        entry.insert(0, foldername)

    def process_data(self, ifc_path, xls_path, export_path, filename):
        if ifc_path and xls_path and export_path:
            # Update the call to the transform_elements function to use the full file path
            transformed_ifc_path = copy_p.keep_elements_from_excel(ifc_path, xls_path, export_path, filename)
            trans_p.transform_elements(export_path, xls_path, filename)
            print("Verarbeitung abgeschlossen.")

            # Close the Tkinter window
            self.master.destroy()
        else:
            print("Bitte wählen Sie IFC-Datei, Excel-Datei und Zielordner aus.")

if __name__ == "__main__":
    root = tk.Tk()
    app = IfcExcelManipulatorGUI(root)
    root.mainloop()

