from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from ..geometry import Profile2D


@dataclass
class BuildContext:
    cache: dict | None = None


class PartDefinition(Protocol):
    id: str

    def kind(self) -> str: ...  # 'sheet' | 'solid' | 'hybrid'

    def parameters(self) -> dict: ...

    def get_profile_2d(self, ctx: BuildContext) -> Optional[Profile2D]: ...

    # Future: get_solid_3d
