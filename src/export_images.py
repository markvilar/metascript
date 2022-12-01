import os

from pathlib import Path

import Metashape


def export_images(root: Path, chunk):
    directory = root / chunk.label
    if not os.path.exists(directory): os.mkdir(directory)

    directory = directory / "images"
    if not os.path.exists(directory): os.mkdir(directory)
    
    print("Exporting images to: {0}".format(directory))

    for camera in chunk.cameras:
        if not camera.transform:
            continue

        filepath = directory / (camera.label + ".jpeg")        
        if os.path.exists(filepath):
            continue

        image = camera.image()
        
        image.save(str(filepath))


def on_execute():
    app = Metashape.app
    document = app.document
    console = app.console_pane

    directory = Path(app.getExistingDirectory())

    chunk = document.chunk

    for chunk in document.chunks:
        if not chunk.enabled:
            continue
    
        export_images(directory, chunk)


def main():
    label = "Scripts/Export images"
    Metashape.app.removeMenuItem(label)
    Metashape.app.addMenuItem(label, on_execute)
    print("To execute this script press {0}".format(label))

if __name__ == "__main__":
    main()
