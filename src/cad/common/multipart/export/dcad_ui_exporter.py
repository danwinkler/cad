from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

from ..assembly import Assembly, PartInstance


@dataclass
class DCADUIExporter:
    """Exporter that pushes an assembly to a running dcad_ui Electron app.

    Usage:
        asm.export(DCADUIExporter())

    Parameters
    ----------
    url: str
        Endpoint for the dcad_ui update route.
    include_geometry: bool
        Whether to embed geometry (polygons) in the payload. If False, only metadata & joints.
    timeout: float
        Timeout (seconds) for the HTTP POST.
    quiet: bool
        If True, suppress network errors (fails silently with a return value of False).
    print_success: bool
        If True and push succeeds, prints a confirmation message.
    """

    url: str = "http://localhost:5123/update"
    include_geometry: bool = True
    timeout: float = 0.5
    quiet: bool = True
    print_success: bool = True

    def emit(
        self, assembly: Assembly, selection: list[PartInstance], **opts
    ):  # noqa: D401
        # selection currently ignored; dcad_ui expects whole assembly
        # Avoid importing serialize_assembly from package root to prevent circular import.
        data = assembly.to_dict(include_geometry=self.include_geometry)
        payload = json.dumps(data).encode()
        req = urllib.request.Request(url=self.url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp.read()
            if self.print_success:
                print("Pushed assembly to dcad_ui.")
            return True
        except urllib.error.URLError as e:
            if not self.quiet:
                print(f"dcad_ui push failed: {e}")
            return False
