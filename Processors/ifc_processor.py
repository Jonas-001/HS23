import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
import pandas as pd
import os
import Helpers.Data_Helpers as hlp

# Importieren Sie die Hilfsfunktionen für Storey-Extraktion
from Helpers.Storey_Helpers import getStorey, getBuilding
# Importieren Sie die neue Helper-Funktion
from Helpers.Material_Helpers import extract_material_information


#Globale Variablen - Listen

export_lst = []


def process_ifc_data(conf_lst, ifc_path):
    global export_lst  # Nutze die globalen Variablen des Moduls

    #IFC Datein Auswerten und Daten strukturiert speichern

    for _c in conf_lst:
        
    
        _source_file = os.path.basename(ifc_path)  # Extrahiere den Dateinamen aus dem IFC-Pfad
        _source_folder = os.path.dirname(ifc_path)  # Extrahiere den Ordner aus dem IFC-Pfad

        _source_path = os.path.join(_source_folder, _source_file)
        check_file = os.path.isfile(_source_path)

        if(check_file):

            ifc_file = ifcopenshell.open(_source_path)
            # Extrahiere Elemente vom angegebenen IFC-Typ
            elements = ifc_file.by_type(_c.category)
            
            # Liste zur temporären Speicherung der exportierten Daten für die aktuelle Konfiguration
            tmp_exp_data_from_current_config = []

            # Iteriere durch jedes IFC-Element des angegebenen Typs
            for _e in elements:
                #print(_e.Name)                
                tmp_exp_data = []              
                
                # Extrahiere die Pset-Eigenschaften des IFC-Elements
                act_prop = ifcopenshell.util.element.get_psets(_e, psets_only=False)
                # Extrahiere allgemeine Informationen über das IFC-Element
                act_info = _e.get_info()
                
                try:
                    tmp_exp_data.append(act_info.get("GlobalId"))
                    tmp_exp_data.append(act_info.get("type"))

    
                except:
                    continue       
                
                # Iteriere durch jede konfigurierte Eigenschaft
                for _p in _c.prop_list:
                    #print(str(_p.pset) != "nan")
                    
                    try:
                        if(str(_p.pset) != "nan"):
                            act_val = act_prop.get(_p.pset).get(_p.prop)
                        else:                     
                            act_val = act_info.get(_p.prop)
                            
                        #print(act_val)

                        tmp_exp_data.append(act_val)

                    except:
                        act_val = "" 
                        tmp_exp_data.append(act_val)
 
                 # Extrahiere Materialinformationen
                materials_info = get_ifc_materials(_e)

                # Füge Materialinformationen zur temporären Exportdatenliste hinzu (als dritte Spalte)
                tmp_exp_data.insert(2, materials_info)

                # Extrahiere Storey- und Gebäudeinformationen
                storey_info = getStorey(_e)
                building_info = getBuilding(_e)

                tmp_exp_data.insert(3, storey_info)
                tmp_exp_data.insert(4, building_info)

                tmp_exp_data_from_current_config.append(tmp_exp_data)

            exp_holder = hlp.Exp_Holder(_c.branch, tmp_exp_data_from_current_config)
            export_lst.append(exp_holder)

    return export_lst

# Funktion zur Extraktion von IFC-Materialinformationen
def get_ifc_materials(ifc_product):
    return extract_material_information(ifc_product)