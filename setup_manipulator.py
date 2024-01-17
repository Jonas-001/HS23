from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["ifcopenshell", "openpyxl"],
    "include_files": [],  # Füge hier zusätzliche Dateien hinzu, wenn erforderlich
}

executables = [
    Executable(
        "ifc_excel_manipulator.py",
        base="Win32GUI",  # Dies deaktiviert die Konsole
        target_name="ifc_excel_manipulator.exe",  # Korrekte Schreibweise für den Zielpfad der ausführbaren Datei
        icon=r"C:\Users\joni_\Documents\Studium HSLU\VS_Projects\IFC-Editor\Grundlagen/Icon_Manipulator.ico",  # Passe dies an den Pfad zu deinem Icon an
    )
]

setup(
    name="IFC_Excel_Manipulator",
    version="1.0",
    description="Es ermöglicht die IFC-Datei anhand einer Excel-Liste zu manipulieren. Es ermöglicht die Zuweisung von neuen Pset und kann ebenfalls den Export einzelner Elemente definieren.",
    options={"build_exe": build_exe_options},
    executables=executables,
    install_requires=[
        "ifcopenshell==0.6.0",
        "openpyxl==3.0.14",
    ],
)
