import ifcopenshell
import ifcopenshell.util.element

def getStorey(ele):
    lev_Obj = None

    if ele.is_a('IfcSpatialStructureElement') and ele.is_a('IfcSpace'):
        lev_Obj = ele.Decomposes[0][4]
    else:
        lev_Obj = ifcopenshell.util.element.get_container(ele)
        

    return lev_Obj

def get_wall_axis(obj):

    ##TO-DO Geschoss für die Z-Höhe einbauen

    #(#6726=IfcShapeRepresentation(#87,'Axis','Curve2D',(#6725)), #6737=IfcShapeRepresentation(#88,'Body','SweptSolid',(#6731)))
    #print(obj.Representation.Representations[0].Items[0])

    #Schritt 1 Wandachse

    representation = obj.Representation.Representations[0].Items[0]
    s_p = representation.Points[0]
    e_p = representation.Points[1]

    #print(s_p.Coordinates)
    #print(e_p.Coordinates)

    #Schritt 2 Basispunkt des Objektes im Lokalen System

    relative_placement = obj.ObjectPlacement.RelativePlacement.Location.Coordinates

    #Schritt 3 Parzelle / Site Location
    site_location = ifc.by_type('IfcSite')[0].ObjectPlacement.RelativePlacement.Location.Coordinates

    #Schritt 4 Geschoss Höhe

    storey_obj = getStorey(obj)
    storey_elev = 0.0

    if(storey_obj):
    
        storey_elev = storey_obj.Elevation
        print("Storey Elev: {}".format(str(storey_elev)))


    combined_coordinates_Start_Point = (
        s_p.Coordinates[0] + relative_placement[0] + site_location[0],
        s_p.Coordinates[1] + relative_placement[1] + site_location[1],
        storey_elev + site_location[2]
    )

    combined_coordinates_End_Point = (
        e_p.Coordinates[0] + relative_placement[0] + site_location[0],
        e_p.Coordinates[1] + relative_placement[1] + site_location[1],
        storey_elev + site_location[2]
    )

    print(combined_coordinates_Start_Point)
    print(combined_coordinates_End_Point)

    

model_url = r"C:\Users\MichalRontsinsky\OneDrive - beyondBIM\Dokumente\VS_Projects\LakeHub\ARC_Modell_NEST_230328.ifc"

ifc = ifcopenshell.open(model_url)
all_objects = ifc.by_type("IfcWallStandardCase")

for w in all_objects:
    get_wall_axis(w)




