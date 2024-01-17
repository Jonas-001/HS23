import Processors.config_processor as conf_pro
import Processors.ifc_processor as ifc_p
import Processors.export_processor as exp_p
import ifcopenshell
import os
from Helpers.Data_Helpers import Data_Holder, filterConfig

# Globale Variablen - Listen
glb_conf_lst = []
glb_conf_folder = ""
glb_export_lst = []

def create_new_ifc_file(template_ifc_path, config_list, new_ifc_path):
    template_ifc_file = ifcopenshell.open(template_ifc_path)
    
    for data_holder in config_list:
        entity_name = data_holder.category  # Die Entity-Namen sind bereits "IfcClass"
        new_element = template_ifc_file.create_entity(entity_name)
        new_element.Name = data_holder.category
        # Hier können Sie weitere Eigenschaften entsprechend Ihren Anforderungen setzen
        template_ifc_file.by_type(entity_name).append(new_element)
    
    template_ifc_file.write(new_ifc_path)
    template_ifc_file.close()
    
def start_func():
    # Hauptfunktion zum Ausführen

    print("Hauptprogramm gestartet")

    # Schritt 1 > Einlesen der Konfiguration
    glb_conf_set = conf_pro.read_source_data()
    glb_conf_lst = glb_conf_set[0]
    glb_conf_folder = glb_conf_set[1]

    # Schritt 2 > Auswerten der IFC-Datei
    glb_export_lst = ifc_p.process_ifc_data(glb_conf_lst)

    # Schritt 3 > Export der Ergebnisse als Excel
    exp_p.export_data(glb_export_lst, glb_conf_lst, glb_conf_folder)
    
    # Schritt 4 > Erstellen der neuen IFC-Datei
    template_ifc_path = r"C:\Users\joni_\Documents\Studium HSLU\VS_Projects\IFC-Editor\ARC_Modell_NEST_230328.ifc" 
    new_ifc_path = r"C:\Users\joni_\Documents\Studium HSLU\VS_Projects\IFC-Editor\neue_ifc_datei.ifc" 
    create_new_ifc_file(template_ifc_path, glb_conf_lst, new_ifc_path)
    print(f"Die neue IFC-Datei wurde erstellt: {new_ifc_path}")

# Als Hauptprogramm ausführen
if __name__ == '__main__':
    start_func()

