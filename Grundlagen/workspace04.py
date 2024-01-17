import ifcopenshell 
from ifcopenshell.api import run
import uuid
import ifcopenshell.template
import ifcopenshell.geom as geom

# Erstellung von IFC-Vorlagen
ifcfile = ifcopenshell.template.create(
    filename="Test_IFC_temp",
    creator="Jonas Urwyler",
    organization="Schubiger AG",
    schema_identifier="IFC2x3",
    project_name="Test Zone Creation"
)

# Erhalten Sie Referenzen zu Instanzen, die in der Vorlage definiert sind
owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
project = ifcfile.by_type("IfcProject")[0]
context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]

# Erhalten Sie Referenzen zu Instanzen, die in der Vorlage definiert sind
site = run("root.create_entity", ifcfile, ifc_class="IfcSite", name="My Site")
building = run("root.create_entity", ifcfile, ifc_class="IfcBuilding", name="Building A")
storey = run("root.create_entity", ifcfile, ifc_class="IfcBuildingStorey", name="Ground Floor")

# Da der Standort unsere oberste Ebene ist, weisen Sie ihn dem Projekt zu.
# Platzieren Sie dann unser Gebäude auf dem Grundstück und unser Stockwerk in dem Gebäude.
run("aggregate.assign_object", ifcfile, relating_object=project, product=site)
run("aggregate.assign_object", ifcfile, relating_object=site, product=building)
run("aggregate.assign_object", ifcfile, relating_object=building, product=storey)

settings = geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

ifcfile.createIfcRelContainedInSpatialStructure(
    create_guid(),
    owner_history,
    "Building Storey Container",
    None,
    wall_list,
    storey)

# Schreiben des Inhalts der IFC  Datei auf die Festplatte
ifcfile.write(r"C:\Users\MichalRontsinsky\Downloads\Temp\Sperrzonen_CAS.ifc")


""" 
import ifcopenshell

def get_location(ifc_file):
    # Öffnen Sie die IFC-Datei
    ifc_file = ifcopenshell.open(ifc_file)

    # Holen Sie sich das Projekt-Objekt (IfcProject)
    project = ifc_file.by_type('IfcProject')[0]

    # Holen Sie sich die geografischen Positionsinformationen
    if 'IfcSite' in project.IsDecomposedBy[0].RelatedObjects[0].is_a():
        site = project.IsDecomposedBy[0].RelatedObjects[0]
        latitude = site.RefLatitude
        longitude = site.RefLongitude
        elevation = site.RefElevation
        return latitude, longitude, elevation
    else:
        return None

# Beispielaufruf
ifc_file_path = 'pfad_zur_ihre_erste_ifc_datei.ifc'
location = get_location(ifc_file_path)

if location:
    print(f"Geografische Position: Latitude {location[0]}, Longitude {location[1]}, Elevation {location[2]}")
else:
    print("Keine geografischen Positionsinformationen gefunden.") """
