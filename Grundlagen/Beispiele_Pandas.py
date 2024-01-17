import pandas as pd

base_file_path_1 = r"C:\Users\MichalRontsinsky\OneDrive - beyondBIM\PERSONAL\PROJEKTE\HSLU\Digital Twin Design and Engineering\Raumliste_Demo.xlsx"
base_file_path_2 = r"C:\Users\MichalRontsinsky\OneDrive - beyondBIM\PERSONAL\PROJEKTE\HSLU\Digital Twin Design and Engineering\Raumliste_Demo.xlsx"
base_file_path_3 = r"C:\Users\MichalRontsinsky\OneDrive - beyondBIM\PERSONAL\PROJEKTE\HSLU\Digital Twin Design and Engineering\Raumliste_Demo.xlsx"

base_df_1 = pd.read_excel(base_file_path_1, sheet_name="Sheet1")
base_df_2 = pd.read_excel(base_file_path_2, sheet_name="Sheet1")
base_df_3 = pd.read_excel(base_file_path_3, sheet_name="Sheet1")

#BEISPIEL > Einlesen CSV
#base_df = pd.read_csv(base_file_path)

#HNF Filtern > Beispiel DataFrame filtern durch Abgleich Spalte und Wert

hnf_df = -[base_df_1["SIA416"] == "HNF"]

#Beispiel Filtern der Liste mit Objekten
#wand_df = base_df[base_df["Objekt"] == "Wand"]

print(hnf_df)

#Summe aus den gefilterten Daten

print(hnf_df["Raumflaeche [m²]"].sum())

wand_flaeche = hnf_df["Raumflaeche [m²]"].sum()


#Flächen berechnen
#df.columns.get_loc('B')
#Raumflaeche [m²]

#Loc nur Spalte SIA416

filt_df = base_df_1.loc[ : ,"SIA416"]
print(filt_df)

#iLoc mit index, z.B. erst 10 Zeilen von SIA416 Spalte

filt_df_iloc = base_df_1.iloc[0:10, base_df_1.columns.get_loc('SIA416')]
print(filt_df_iloc)



