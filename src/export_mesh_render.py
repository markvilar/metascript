import os

from pathlib import Path

import Metashape

def export_depth(chunk, directory: Path):
    if not os.path.exists(directory): os.mkdir(directory)
    
    print("Exporting depth to: {0}".format(directory))

    # Get mesh
    mesh = chunk.model

    # Loop over cameras and render normal map
    for camera in chunk.cameras:
        if not camera.transform:
            continue

        if not camera.enabled:
            continue

        filepath = str(directory / (camera.label + ".tiff"))
        if os.path.exists(filepath):
            continue

        # Create depth image and convert to real values
        depth_image = mesh.renderDepth(camera.transform,
            camera.calibration, add_alpha=False)
        depth_image = depth_image * chunk.transform.scale

        # Set up compression
        compr = Metashape.ImageCompression()
        compr.tiff_compression = \
            Metashape.ImageCompression().TiffCompressionDeflate

        # Save image
        depth_image.save(filepath, compression=compr)


def export_normal(chunk, directory: Path):
    if not os.path.exists(directory): os.mkdir(directory)

    print("Exporting normals to: {0}".format(directory))

    # Get mesh
    mesh = chunk.model

    # Loop over cameras and render normal map
    for camera in chunk.cameras:
        if not camera.transform:
            continue

        if not camera.enabled:
            continue

        filepath = str(directory / (camera.label + ".tif"))
        if os.path.exists(filepath):
            continue

        # Create normal image
        normal_image = mesh.renderNormalMap(camera.transform,
            camera.calibration, add_alpha=False)
        normal_image = normal_image.convert("RGB", "F32")

        # TODO: Transform to axis aligned coordinates
        rotation = camera.transform.rotation()

        print(rotation)
       
        # Set up compression
        compr = Metashape.ImageCompression()
        compr.tiff_compression = \
            Metashape.ImageCompression().TiffCompressionDeflate

        # Save image
        normal_image.save(filepath, compression=compr)
        return

def on_render_depth():
    app = Metashape.app
    document = app.document

    directory = Path(app.getExistingDirectory())
    export_depth(document.chunk, directory)

def on_render_normal():
    app = Metashape.app
    document = app.document

    directory = Path(app.getExistingDirectory())
    export_normal(document.chunk, directory)

def main():
    depth_label = "Scripts/Render depth images (mesh)"
    Metashape.app.removeMenuItem(depth_label)
    Metashape.app.addMenuItem(depth_label, on_render_depth)

    normal_label = "Scripts/Render normal images (mesh)"
    Metashape.app.removeMenuItem(normal_label)
    Metashape.app.addMenuItem(normal_label, on_render_normal)

    print("To execute this script press {0}".format(depth_label))
    print("To execute this script press {0}".format(normal_label))

if __name__ == "__main__":
    main()
