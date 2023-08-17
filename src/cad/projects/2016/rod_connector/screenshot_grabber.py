import math
import os
import platform
import subprocess

system = platform.system()
if system == "Windows":
    pgm = "C:\Program Files\OpenSCAD\openscad.exe"
else:
    pgm = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"


def get_structure_images():
    for i in range(1, 8):
        subprocess.call(
            [
                pgm,
                "-o",
                "images/image" + str(i) + ".png",
                "structure" + str(i) + ".py.scad",
            ]
        )


def get_connector_images():
    for i in range(60):
        print(i)
        subprocess.call(
            [
                pgm,
                "-o",
                "images/varE/" + str(i) + ".png",
                "designs/varE/" + str(i) + ".scad",
            ]
        )


def rotate_scad_file():
    for i in range(4):
        subprocess.call(
            [
                pgm,
                "-D",
                "angle=" + str(i * 90),
                "-o",
                "images/rot/" + str(i) + ".png",
                "connector.py.scad",
            ]
        )


def output_stls():
    for i in range(60):
        print(i)
        subprocess.call(
            [
                pgm,
                "-o",
                "stls/varE/" + str(i) + ".stl",
                "designs/varE/" + str(i) + ".scad",
            ]
        )


def build_vases():
    files = os.listdir("vase/")
    files = [f for f in files if f[-5:] == ".scad"]
    for f in files:
        print(f)
        subprocess.call([pgm, "-o", "vase/" + f.split(".")[0] + ".stl", "vase/" + f])


get_connector_images()
# get_structure_images()
# rotate_scad_file()
# output_stls()
# build_vases()
