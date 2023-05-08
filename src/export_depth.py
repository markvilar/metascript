import os

from pathlib import Path

import Metashape


def export_depth(directory: Path, chunk):
    assert directory.is_dir(), "{0} is not a directory".format(directory)
   
    print("Exporting depth maps to: {0}".format(directory))
    print(" - Number of cameras: {0}".format(len(chunk.cameras)))

    for camera in chunk.cameras:
        if not camera.transform:
            continue

        if not camera.enabled:
            print("Camera {0} disabled!".format(camera.label))
            continue

        filepath = str(directory / (camera.label + ".tif"))
        if os.path.exists(filepath):
            continue

        if camera in chunk.depth_maps:
            filepath = directory / (camera.label + ".tiff")
            if filepath.exists():
                continue
            depth = chunk.depth_maps[camera].image()
            compr = Metashape.ImageCompression()
            compr.tiff_compression = \
                Metashape.ImageCompression().TiffCompressionDeflate
            depth.save(str(filepath), compression=compr)
        else:
            print("Camera {0} does not have a depth map.".format(camera))


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
