import ifcopenshell

def extract_material_information(ifc_product):
    # Liste für Materialinformationen
    material_list = []

    # Überprüfe, ob das IFC-Produkt vorhanden ist
    if ifc_product:
        # Extrahiere das Material des IFC-Produkts
        ifc_material = ifcopenshell.util.element.get_material(ifc_product)
        # Überprüfe, ob das Material vorhanden ist
        if ifc_material:
            # Bestimme den Materialtyp und rufe die entsprechende Funktion auf
            material_type = determine_material_type(ifc_material)
            material_list = extract_material_info_by_type(ifc_material, material_type)

    return material_list

def determine_material_type(ifc_material):
    # Bestimme den Typ des IFC-Materials
    if ifc_material.is_a('IfcMaterial'):
        return 'simple'
    elif ifc_material.is_a('IfcMaterialList'):
        return 'list'
    elif ifc_material.is_a('IfcMaterialConstituentSet'):
        return 'constituent_set'
    elif ifc_material.is_a('IfcMaterialLayerSetUsage'):
        return 'layer_set_usage'
    elif ifc_material.is_a('IfcMaterialProfileSetUsage'):
        return 'profile_set_usage'
    else:
        return None

def extract_material_info_by_type(ifc_material, material_type):
    # Extrahiere Materialinformationen basierend auf dem Materialtyp
    material_list = []

    if material_type == 'simple':
        mat_dict = {}
        mat_dict["Material"] = ifc_material.Name
        mat_dict["LayerThickness"] = ""  # Platz für zusätzliche Informationen, hier leer gelassen
        material_list.append(mat_dict)

    elif material_type == 'list':
        for materials in ifc_material.Materials:
            mat_dict = {}
            mat_dict["Material"] = materials.Name
            mat_dict["LayerThickness"] = ""  # Platz für zusätzliche Informationen, hier leer gelassen
            material_list.append(mat_dict)

    elif material_type == 'constituent_set':
        for material_constituents in ifc_material.MaterialConstituents:
            mat_dict = {}
            mat_dict["Material"] = material_constituents.Material.Name
            mat_dict["LayerThickness"] = ""  # Platz für zusätzliche Informationen, hier leer gelassen
            material_list.append(mat_dict)

    elif material_type == 'layer_set_usage':
        for material_layer in ifc_material.ForLayerSet.MaterialLayers:
            mat_dict = {}
            mat_dict["Material"] = material_layer.Material.Name
            mat_dict["LayerThickness"] = material_layer.LayerThickness
            material_list.append(mat_dict)

    elif material_type == 'profile_set_usage':
        for material_profile in ifc_material.ForProfileSet.MaterialProfiles:
            mat_dict = {}
            mat_dict["Material"] = material_profile.Material.Name
            mat_dict["LayerThickness"] = ""  # Platz für zusätzliche Informationen, hier leer gelassen
            material_list.append(mat_dict)

    return material_list
