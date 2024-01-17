from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["ifcopenshell", "openpyxl"],
    "include_files": [],  # Füge hier zusätzliche Dateien hinzu, wenn erforderlich
}

executables = [
    Executable(
        "ifc_extractor.py",
        base="Win32GUI",  # Dies deaktiviert die Konsole
        target_name="ifc_extractor.exe",  # Korrekte Schreibweise für den Zielpfad der ausführbaren Datei
        icon=r"C:\Users\joni_\Documents\Studium HSLU\VS_Projects\IFC-Editor\Grundlagen/Icon_Extractor.ico",  # Passe dies an den Pfad zu deinem Icon an
    )
]

setup(
    name="IFC_Extractor",
    version="1.0",
    description="Es ermöglicht die einzelnen IFC-Elemente in eine Exceldatei auszulesen",
    options={"build_exe": build_exe_options},
    executables=executables,
    install_requires=[
        "ifcopenshell==0.6.0",
        "openpyxl==3.0.14",
    ],
)
