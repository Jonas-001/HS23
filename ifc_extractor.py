import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Processors import config_processor as conf_pro
from Processors import ifc_processor as ifc_p
from Processors import export_processor as exp_p

class IfcDataExtractorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("IFC Datenextraktor")
        self.master.configure(bg="#DCE6F1")

        self.default_font = ('Calibri', 12)
        self.master.option_add('*Font', self.default_font)

        # Erstellen Sie einen benutzerdefinierten Stil für Buttons
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

        ifc_label = ttk.Label(ifc_frame, text="Wähle die IFC-Datei aus:", style="TLabel")
        ifc_label.grid(row=0, column=0, sticky="w")

        ifc_entry = ttk.Entry(ifc_frame, font=self.default_font)
        ifc_entry.grid(row=0, column=1, sticky="ew")

        ifc_browse_button = ttk.Button(ifc_frame, text="Durchsuchen", command=lambda: self.browse_button(ifc_entry), style="TButton")
        ifc_browse_button.grid(row=0, column=2, sticky="ew")

        xls_label = ttk.Label(xls_frame, text="Wähle den Elementplan.xlsx aus:", style="TLabel")
        xls_label.grid(row=0, column=0, sticky="w")

        xls_entry = ttk.Entry(xls_frame, font=self.default_font)
        xls_entry.grid(row=0, column=1, sticky="ew")

        xls_browse_button = ttk.Button(xls_frame, text="Durchsuchen", command=lambda: self.browse_button(xls_entry), style="TButton")
        xls_browse_button.grid(row=0, column=2, sticky="ew")

        export_label = ttk.Label(export_frame, text="Wähle den Zielordner für den Export:", style="TLabel")
        export_label.grid(row=0, column=0, sticky="w")

        export_entry = ttk.Entry(export_frame, font=self.default_font)
        export_entry.grid(row=0, column=1, sticky="ew")

        export_browse_button = ttk.Button(export_frame, text="Durchsuchen", command=lambda: self.select_folder(export_entry), style="TButton")
        export_browse_button.grid(row=0, column=2, sticky="ew")

        start_button = ttk.Button(self.master, text="Start", command=lambda: self.start_func(ifc_entry.get(), xls_entry.get(), export_entry.get()), style="TButton")
        start_button.grid(row=3, column=0, pady=10)

    def browse_button(self, entry):
        filename = filedialog.askopenfilename()
        entry.delete(0, tk.END)
        entry.insert(0, filename)

    def select_folder(self, entry):
        foldername = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, foldername)

    def start_func(self, ifc_path_entry, xls_path_entry, export_path_entry):
        # Hauptfunktion zum Ausführen
        global glb_conf_lst, glb_conf_folder, glb_export_lst

        print("Hauptprogramm gestartet")

        # Schritt 1 > Einlesen der Konfiguration
        glb_conf_set = conf_pro.read_source_data(ifc_path_entry, xls_path_entry)
        glb_conf_lst = glb_conf_set[0]
        glb_conf_folder = glb_conf_set[1]

        # Schritt 2 > Auswerten der IFC Datei
        glb_export_lst = ifc_p.process_ifc_data(glb_conf_lst, ifc_path_entry)

        # Schritt 3 > Export der Ergebnisse als Excel
        exp_p.export_data(glb_export_lst, glb_conf_lst, export_path_entry)

        # Schließe das Tkinter-Fenster
        self.master.destroy()

def main():
    root = tk.Tk()
    app = IfcDataExtractorGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
