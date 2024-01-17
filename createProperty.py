import ifcopenshell
import ifcopenshell.api
import ifcopenshell.util.element

#ifc = ifcopenshell.api.run("project.create_file")
#element = ifc.createIfcWall()

ifc_path = r"./ARC_Modell_NEST_230328.ifc"
ifc_file = ifcopenshell.open(ifc_path)
element = ifc_file.by_type("IfcWall")[0]

pset = ifcopenshell.api.run("pset.add_pset", ifc, product=element, name="Pset_HSLU")
ifcopenshell.api.run("pset.edit_pset", ifc, pset=pset, properties={"foo": "foobar", "foo2": "foobaz"})

psets = ifcopenshell.util.element.get_psets(element)
ifcopenshell.api.run("pset.edit_pset", ifc, pset=ifc.by_id(psets["Pset_HSLU"]["id"]), properties={"Material": "Beton"})
print(ifcopenshell.util.element.get_psets(element))


