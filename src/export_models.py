from pathlib import Path

import Metashape

def export_model(chunk, path, low: int, high: int):
    if chunk.dense_cloud:
        # Remove points below within confidence interval
        chunk.dense_cloud.setConfidenceFilter(low, high)
        chunk.dense_cloud.removePoints(list(range(128)))
        chunk.dense_cloud.resetFilters()
        
        # Export dense cloud
        chunk.exportPoints(
                path=str(path),
                source_data=Metashape.DenseCloudData,
                binary=False,
                format=Metashape.PointsFormatPLY,
                save_normals=True,
                save_colors=True,
                save_confidence=True,
                save_classes=False,
                crs=Metashape.CoordinateSystem("EPSG::4326"),
            )
    else:
        print("Chunk {0} does not have a dense cloud.".format(chunk.label))


def on_execute():
    print("\nExporting models")
    app = Metashape.app

    # Model confidence limits
    confidence_low = 0
    confidence_high = 1

    document = app.document
    console = app.console_pane
    console.clear()

    directory = Path(Metashape.app.getExistingDirectory())

    # Remove disabled chunks
    chunks = [chunk for chunk in document.chunks if chunk.enabled]

    for chunk in chunks:
        path = directory / (chunk.label + "_dense_global.ply")
        export_model(chunk, path, confidence_low, confidence_high)

def main():
    label = "Scripts/Export models"
    Metashape.app.removeMenuItem(label)
    Metashape.app.addMenuItem(label, on_execute)
    print("To execute this script press: {0}".format(label))


if __name__ == "__main__":
    main()
