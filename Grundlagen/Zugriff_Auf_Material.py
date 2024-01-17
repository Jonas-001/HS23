def get_ifc_materials(ifc_product):

    material_list = []

    #deprecated from IFC2x3
    #IfcMaterialList

    #IfcMaterialLayerSet
    #IfcMaterialLayerSetUsage

    #new entity from IFC4
    #IfcMaterialConstituentSet
    #IfcMaterialProfileSet

    if ifc_product:
        ifc_material = ifcopenshell.util.element.get_material(ifc_product)
        if ifc_material:    

            if ifc_material.is_a('IfcMaterial'):
                mat_dict = {}
                mat_dict["Material"] = ifc_material.Name
                mat_dict["LayerThickness"] = ""                    
                material_list.append(mat_dict)

            if ifc_material.is_a('IfcMaterialList'):
                for materials in ifc_material.Materials:
                    mat_dict = {}
                    mat_dict["Material"] = materials.Name
                    mat_dict["LayerThickness"] = ""       
                    material_list.append(mat_dict)

            if ifc_material.is_a('IfcMaterialConstituentSet'):
                for material_constituents in ifc_material.MaterialConstituents:
                    mat_dict = {}
                    mat_dict["Material"] = material_constituents.Material.Name
                    mat_dict["LayerThickness"] = ""  
                    material_list.append(mat_dict)

            if ifc_material.is_a('IfcMaterialLayerSetUsage'):
                for material_layer in ifc_material.ForLayerSet.MaterialLayers:
                    mat_dict = {}
                    mat_dict["Material"] = material_layer.Material.Name
                    mat_dict["LayerThickness"] = material_layer.LayerThickness 

                    material_list.append(mat_dict)

            if ifc_material.is_a('IfcMaterialProfileSetUsage'):
                for material_profile in (ifc_material.ForProfileSet.MaterialProfiles):
                    mat_dict = {}
                    mat_dict["Material"] = material_profile.Material.Name
                    mat_dict["LayerThickness"] = ""  
                    material_list.append(mat_dict)

    if not material_list:
        material_list.append(None)

    return material_list