import os
import numpy as np 
import pandas as pd
import Helpers.Data_Helpers as hlp


def export_data(export_lst, conf_lst, export_folder):

    #Export der Daten als Excel
    #Export Extracted Data to Excel

    if len(export_lst) > 0:

        xls_file_name = "Export_Daten_IFC.xlsx"
        exp_path = os.path.join(export_folder, xls_file_name)

        check_file = os.path.isfile(exp_path)

        if(not(check_file)):
            pd.DataFrame([]).to_excel(exp_path)

        for exp_set in export_lst:
        
            col_lst = []
            col_lst.append("GUID")
            col_lst.append("Kategorie")
            
            _target_obj = hlp.filterConfig(exp_set.branch, conf_lst)
            print(_target_obj)
            
            if _target_obj != None:
                
                for _p_l in _target_obj.prop_list:
                    #print(_p_l)
                    _ps = _p_l.pset
                    _pr = _p_l.prop
                    
                    if(str(_ps) == "nan"):
                        _title = "{}".format(_pr)
                    else:
                        _title = "{}:{}".format(_ps, _pr)
                    
                    col_lst.append(_title)
                    print(_title)

                df = pd.DataFrame(exp_set.data, columns = col_lst)
                #print(exp_set.data)
                #df = pd.DataFrame(exp_set.data)
                       
                # Style-Definition
                def highlight_max(s):
                    # Überprüfe, ob die Serie numerische Werte enthält
                    if pd.api.types.is_numeric_dtype(s):
                        is_max = s == s.max()
                        return ['background-color: yellow' if v else '' for v in is_max]
                    else:
                        return ['' for _ in s]

                # Styling-Funktion für Zellenränder
                def border_style(val):
                    return 'border: 2px solid white'

                 # Styling-Funktion für abwechselnde Hintergrundfarben
                def background_color(val):
                    # Wenn die Zelle in der ersten Zeile ist, verwende den Header-Stil
                    if val == df.iloc[0, 0]:
                        return 'background-color: rgba(0, 128, 0, 0.6); font-weight: bold'
                    # Andernfalls, wechsle die Hintergrundfarbe basierend auf der Zeile
                    row_index = df.index.get_loc(val)
                    colors = ['rgba(0, 128, 0, 0.3)', 'rgba(0, 128, 0, 0.1)']
                    return f'background-color: {colors[row_index % len(colors)]}'

                # Styling-Funktion für die oberste Zeile
                def header_style(s):
                    return 'background-color: rgba(0, 128, 0, 0.6); font-weight: bold'

                # Styling-Funktion für Rahmen basierend auf den Werten in Spalte 2 und 15
                def random_color(val):
                    if val == df.iloc[0, 1]:  # Spalte 2
                        return f'border: 2px solid #{np.random.randint(0, 0xFFFFFF):06X}'
                    elif val == df.iloc[0, 14]:  # Spalte 15
                        return f'border: 2px solid #{np.random.randint(0, 0xFFFFFF):06X}'
                    else:
                        return ''

                # Erstelle eine Kopie des DataFrames und wende das Styling an
                styled_df = df.copy().style \
                    .applymap(border_style) \
                    .applymap(random_color) \
                    .applymap(background_color)

                # Excel-Datei schreiben
                with pd.ExcelWriter(exp_path, engine='openpyxl', if_sheet_exists='replace', mode='a') as writer:
                    # Schreibe den gestylten DataFrame in die Excel-Datei
                    styled_df.to_excel(writer, sheet_name=exp_set.branch, index=False)

        print("Final Step: Finished Export Excel...")
                
"""                 
                with pd.ExcelWriter(exp_path, engine='openpyxl', if_sheet_exists='replace', mode='a') as writer:  
                    df.to_excel(writer, sheet_name=exp_set.branch, index=False)
                                 

        print("Final Step: Finished Export Excel...")

                 # Style-Definition
                def highlight_max(s):
                    is_max = s == s.max()
                    return ['background-color: yellow' if v else '' for v in is_max]

                # Wende das Styling auf den gesamten DataFrame an
                df = df.style.apply(highlight_max, axis=0)
              """