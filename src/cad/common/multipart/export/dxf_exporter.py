from __future__ import annotations

import ezdxf
from shapely.geometry import MultiPolygon, Polygon

from ..assembly import Assembly, PartInstance


class DXFExporter:
    def __init__(self, units="MM"):
        self.units = units

    def emit(self, assembly: Assembly, selection: list[PartInstance], **opts):
        doc = ezdxf.new("R2018")
        if self.units == "MM":
            doc.units = ezdxf.units.MM
        msp = doc.modelspace()

        for inst, profile in assembly.iter_sheet_profiles():
            if inst not in selection:
                continue
            geom = profile.geometry
            self._write_polygon(msp, geom)

        return doc  # caller can saveas

    def _write_polygon(self, msp, geom):
        if isinstance(geom, Polygon):
            self._write_single_polygon(msp, geom)
        elif isinstance(geom, MultiPolygon):
            for g in geom.geoms:
                self._write_single_polygon(msp, g)

    def _write_single_polygon(self, msp, poly: Polygon):
        msp.add_lwpolyline(list(poly.exterior.coords))
        for interior in poly.interiors:
            msp.add_lwpolyline(list(interior.coords))
