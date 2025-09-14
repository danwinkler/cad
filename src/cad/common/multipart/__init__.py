from .assembly import Assembly, PartInstance
from .definitions import (
    BuildContext,
    GearPartDefinition,
    PartDefinition,
    SheetPartDefinition,
)
from .export import DCADUIExporter, DXFExporter
from .geometry import Profile2D, Transform
from .joints import GearJoint


def serialize_assembly(assembly: Assembly, include_geometry: bool = True):
    return assembly.to_dict(include_geometry=include_geometry)


__all__ = [
    "Assembly",
    "PartInstance",
    "Transform",
    "Profile2D",
    "SheetPartDefinition",
    "GearPartDefinition",
    "PartDefinition",
    "BuildContext",
    "GearJoint",
    "DXFExporter",
    "DCADUIExporter",
    "serialize_assembly",
]
