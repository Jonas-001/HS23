import ifcopenshell 
from ifcopenshell.api import run
import uuid
import ifcopenshell.template
import ifcopenshell.geom as geom


O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

# Erzeugt ein IfcAxis2Placement3D aus Location, Axis und RefDirection, die als Python-Tupel angegeben sind
def create_ifcaxis2placement(ifcfile, point=O, dir1=Z, dir2=X):
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement

# Erzeugt ein IfcLocalPlacement aus Location, Axis und RefDirection, angegeben als Python-Tupel, und relativer Platzierung
def create_ifclocalplacement(ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
    axis2placement = create_ifcaxis2placement(ifcfile,point,dir1,dir2)
    ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
    return ifclocalplacement2

# Erzeugt eine IfcPolyLine aus einer Liste von Punkten, die als Python-Tupel angegeben sind
def create_ifcpolyline(ifcfile, point_list):
    ifcpts = []
    for point in point_list:
        point = ifcfile.createIfcCartesianPoint(point)
        ifcpts.append(point)
    polyline = ifcfile.createIfcPolyLine(ifcpts)
    return polyline

# Erzeugt einen IfcExtrudedAreaSolid aus einer Liste von Punkten, die als Python-Tupel angegeben sind
def create_ifcextrudedareasolid(ifcfile, point_list, ifcaxis2placement, extrude_dir, extrusion):
    polyline = create_ifcpolyline(ifcfile, point_list)
    ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    ifcdir = ifcfile.createIfcDirection(extrude_dir)
    ifcextrudedareasolid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
    return ifcextrudedareasolid

def zone(p):
    list_w = []
    for index, item in enumerate(p):
        w = ifcfile.createIfcBuildingElementProxy(
            create_guid(),
            owner_history,
            "SPZ_"+str(index+1),
            "Beschreibung der SPZ",
            None,
            create_ifclocalplacement(ifcfile, point=item),
            product_shape,
            None
        )
        list_w.append(w)
    return list_w

create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)



## START HAUPT SCRIPT HIER

# Erstellung von IFC-Vorlagen
ifcfile = ifcopenshell.template.create(
    filename="Test_IFC_temp",
    creator="Michal Rontsinsky",
    organization="HSLU",
    schema_identifier="IFC2x3",
    project_name="Test Zone Creation"
)



# Erhalten Sie Referenzen zu Instanzen, die in der Vorlage definiert sind
owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
project = ifcfile.by_type("IfcProject")[0]
context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]

# Erstellen Sie einen Standort, ein Gebäude und ein Stockwerk. Viele Hierarchien sind möglich.
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



#Solid und Shape für Sperrzone erstellen
##Sperrzone Parameter

sp_radius = 0.5
sp_height = 1.0

##Sperrzone Parameter

polyline = create_ifcpolyline(ifcfile, [(0.0, 0.0, 0.0), (0.0, 0.0, sp_height)])

solid = ifcfile.createIfcSweptDiskSolid()

solid.Directrix = polyline

solid.Radius = sp_radius
solid.InnerRadius=None
solid.StartParam = 0.0
solid.EndParam = 1.0

body_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "AdvancedSweptSolid", [solid])

product_shape = ifcfile.createIfcProductDefinitionShape(None, None, [body_representation])

point_list = [
    (0., 0., 0.),
    (-5., 0., 0.),
    (0., 5., 0.),
    (10., 10., 2.),
    (-10., -10., 5.),
    (20., 20., 5.),
    (30., -10., -25.)
]

wall_list = zone(point_list)

# Beziehen Sie das Fenster und die Wand auf das Stockwerk des Gebäudes
ifcfile.createIfcRelContainedInSpatialStructure(
    create_guid(),
    owner_history,
    "Building Storey Container",
    None,
    wall_list,
    storey)

# Schreiben des Inhalts der IFC  Datei auf die Festplatte
ifcfile.write(r"C:\Users\MichalRontsinsky\Downloads\Temp\Sperrzonen_CAS.ifc")
