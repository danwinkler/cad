import pathlib

from cad.common.multipart import (
    Assembly,
    DCADUIExporter,
    DXFExporter,
    GearJoint,
    GearPartDefinition,
    Transform,
    serialize_assembly,
)

current_dir = pathlib.Path(__file__).parent


def build_example():
    asm = Assembly(name="gear_pair")
    gear_a = GearPartDefinition(teeth=24, tooth_width=1.0, thickness=3)
    gear_b = GearPartDefinition(teeth=12, tooth_width=1.0, thickness=3)
    # Build profiles to access pitch radii for explicit placement
    prof_a = gear_a.get_profile_2d(None)
    prof_b = gear_b.get_profile_2d(None)
    r_a = prof_a.metadata["pitch_radius"]
    r_b = prof_b.metadata["pitch_radius"]
    center_dist = r_a + r_b

    # Place driver at origin, driven at +X so teeth mesh (approx pitch circle contact)
    a_inst = asm.add_part(
        gear_a,
        transform=Transform.at(x=0, y=0, z=0),
        material={"color": "#1976d2"},  # blue-ish driver
    )
    # Compute half-tooth angular pitch for driven gear to visually align teeth valleys/peaks.
    # Angular pitch (degrees) = 360 / teeth. Using half places tooth edge into mating gap.
    half_tooth_deg = 0.5 * (360.0 / gear_b.teeth)
    b_inst = asm.add_part(
        gear_b,
        transform=Transform.at(x=center_dist, y=0, z=0, rz=half_tooth_deg),
        material={"color": "#ff9800"},  # orange driven
    )

    asm.add_joint(GearJoint(id="g1", driver=a_inst, driven=b_inst, ratio=r_a / r_b))

    return asm


if __name__ == "main__" or __name__ == "__main__":
    asm = build_example()
    asm.export(DCADUIExporter())
