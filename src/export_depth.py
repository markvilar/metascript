import os

from pathlib import Path

import Metashape


def export_depth(root: Path, chunk):
    directory = root / chunk.label
    if not os.path.exists(directory): os.mkdir(directory)

    directory = directory / "depth"
    if not os.path.exists(directory): os.mkdir(directory)
    
    print("Exporting depth maps to: {0}".format(directory))

    for camera in chunk.cameras:
        if not camera.transform:
            continue

        if not camera.enabled:
            continue

        filepath = str(directory / (camera.label + ".tif"))
        if os.path.exists(filepath):
            continue

        depth = chunk.depth_maps[camera].image()
        depth = depth.convert(" ","F16")
        compr = Metashape.ImageCompression()
        compr.tiff_compression = \
            Metashape.ImageCompression().TiffCompressionDeflate
        depth.save(str(directory / (camera.label + ".tif")), compression=compr)


def on_execute():
    app = Metashape.app
    document = app.document
    console = app.console_pane

    directory = Path(app.getExistingDirectory())

    chunk = document.chunk

    print(chunk.label)
    for chunk in document.chunks:
        if not chunk.enabled:
            continue
    
        export_depth(directory, chunk)


def main():
    label = "Scripts/Export depth"
    Metashape.app.removeMenuItem(label)
    Metashape.app.addMenuItem(label, on_execute)
    print("To execute this script press {0}".format(label))

if __name__ == "__main__":
    main()
