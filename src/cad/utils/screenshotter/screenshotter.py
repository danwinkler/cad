import platform
import subprocess
from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_projects():
    projects = []
    for year in (BASE_DIR / "projects").iterdir():
        if year.is_dir():
            for project in year.iterdir():
                if project.is_dir() and project.name != "__pycache__":
                    projects.append(project)
    return projects


def get_scad_files(path):
    return list(path.rglob("*.scad"))


def capture_screenshot(scad_file, image_path):
    if platform.system() == "Windows":
        pgm = "C:\Program Files\OpenSCAD\openscad.exe"
    elif platform.system() == "Darwin":
        pgm = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
    subprocess.call([pgm, "-o", image_path, scad_file])


def main():
    # Generate screenshots for all projects
    projects = get_projects()
    for project in projects:
        scad_files = get_scad_files(project)
        if scad_files:
            year = project.parent.name
            project_name = project.name

            image_path = (
                BASE_DIR
                / "utils"
                / "screenshotter"
                / "images"
                / f"{year}_{project_name}.png"
            )

            if not image_path.exists():
                print(f"Capturing screenshot for {project_name}")
                capture_screenshot(
                    scad_files[0],
                    image_path,
                )

    # Generate grid of screenshots
    images = list((BASE_DIR / "utils" / "screenshotter" / "images").rglob("*.png"))

    # Sort images by reverse year
    # Images start with either "YYYY" or "yYYYY" (literally the letter y)
    def get_year_from_filename(image_filename):
        if image_filename[0] == "y":
            return int(image_filename[1:5])
        return int(image_filename[:4])

    images.sort(key=lambda x: get_year_from_filename(x.name), reverse=True)

    image_size = 150
    grid_width = 5
    grid_height = len(images) // grid_width

    grid = Image.new(
        "RGB",
        (grid_width * image_size, grid_height * image_size),
        color=(255, 255, 255),
    )

    for i, image in enumerate(images):
        x = (i % grid_width) * image_size
        y = (i // grid_width) * image_size
        to_paste = Image.open(image)
        to_paste.thumbnail((image_size, image_size))
        grid.paste(to_paste, (x, y))

    grid.save(BASE_DIR / "utils" / "screenshotter" / "grid.png")


if __name__ == "__main__":
    main()
