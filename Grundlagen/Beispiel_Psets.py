import ifcopenshell
import ifcopenshell.util.element

def getStorey(ele):
    lev_Obj = None

    if ele.is_a('IfcSpatialStructureElement') and ele.is_a('IfcSpace'):
        lev_Obj = ele.Decomposes[0][4]
    else:
        lev_Obj = ifcopenshell.util.element.get_container(ele)
        

    return lev_Obj

def get_psets(obj):

    ##TO-DO Geschoss für die Z-Höhe einbauen



    all_psets = ifcopenshell.util.element.get_psets(obj, psets_only=False)
    pset = all_psets.get('Pset_WallCommon')
    prop = pset.get('IsExternal')
    print(prop)

    

model_url = r"C:\Users\MichalRontsinsky\OneDrive - beyondBIM\Dokumente\VS_Projects\LakeHub\ARC_Modell_NEST_230328.ifc"

ifc = ifcopenshell.open(model_url)
all_objects = ifc.by_type("IfcWallStandardCase")

for w in all_objects:
    get_psets(w)



