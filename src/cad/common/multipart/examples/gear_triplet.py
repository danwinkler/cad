import pathlib

from cad.common.multipart import (
    Assembly,
    DCADUIExporter,
    DXFExporter,
    GearJoint,
    GearPartDefinition,
    Transform,
)

current_dir = pathlib.Path(__file__).parent


def build_example():
    asm = Assembly(name="gear_triplet")
    # Teeth counts
    gear_a = GearPartDefinition(teeth=24, tooth_width=1.0, thickness=3)
    gear_b = GearPartDefinition(teeth=16, tooth_width=1.0, thickness=3)
    gear_c = GearPartDefinition(teeth=12, tooth_width=1.0, thickness=3)

    # Profiles to get pitch radii
    prof_a = gear_a.get_profile_2d(None)
    prof_b = gear_b.get_profile_2d(None)
    prof_c = gear_c.get_profile_2d(None)
    r_a = prof_a.metadata["pitch_radius"]
    r_b = prof_b.metadata["pitch_radius"]
    r_c = prof_c.metadata["pitch_radius"]

    # Placement along +X chain
    x_a = 0.0
    x_b = r_a + r_b
    x_c = x_b + r_b + r_c

    # Half tooth offsets for mesh visuals
    half_b = 0.5 * (360.0 / gear_b.teeth)
    half_c = 0.5 * (360.0 / gear_c.teeth)

    a_inst = asm.add_part(
        gear_a, transform=Transform.at(x=x_a, y=0, z=0), material={"color": "#1976d2"}
    )
    b_inst = asm.add_part(
        gear_b,
        transform=Transform.at(x=x_b, y=0, z=0, rz=half_b),
        material={"color": "#ff9800"},
    )
    c_inst = asm.add_part(
        gear_c, transform=Transform.at(x=x_c, y=0, z=0), material={"color": "#4caf50"}
    )

    # Joints: A drives B, B drives C
    asm.add_joint(GearJoint(id="j1", driver=a_inst, driven=b_inst, ratio=r_a / r_b))
    asm.add_joint(GearJoint(id="j2", driver=b_inst, driven=c_inst, ratio=r_b / r_c))

    return asm


if __name__ == "__main__" or __name__ == "main__":
    asm = build_example()
    asm.export(DCADUIExporter())
    print("Gear triplet example built & push attempted.")
