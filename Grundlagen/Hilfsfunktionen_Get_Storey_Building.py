#Hilffunktion zum Auslesen der IFC-Struktur

def getStorey(ele):
    lev_name = ""

    if ele.is_a('IfcSpatialStructureElement') and ele.is_a('IfcSpace'):
        lev_name = ele.Decomposes[0][4].Name
    else:
        lev_obj = ifcopenshell.util.element.get_container(ele)
        lev_name = lev_obj.Name

    return lev_name

def getBuilding(ele):

    building_name = ""

    if ele.is_a('IfcSpatialStructureElement') and ele.is_a('IfcSpace'):
        lev_obj = ele.Decomposes[0][4]
        building_obj = lev_obj.Decomposes[0][4]
        #print(ele.Decomposes[0])
    elif ele.is_a('IfcSpatialStructureElement') and ele.is_a('IfcBuildingStorey'):
        building_obj = ele.Decomposes[0][4]
    else:
        lev_obj = ifcopenshell.util.element.get_container(ele)
        building_obj = lev_obj.Decomposes[0][4]

    
    building_name = building_obj.Name

    return building_name