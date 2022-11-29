from functools import partial
from pathlib import Path

import tqdm

import Metashape


def export_sensors(chunk, output: Path):
    if not chunk.enabled:
        print("Chunk {0} is not enabled.".format(chunk.label))
        return

    label = chunk.label

    for sensor in chunk.sensors:
        index = chunk.sensors.index(sensor)
        if sensor.calibration:
            file = "{0}_sensor_{1:02d}.xml".format(label, index)
            path = output / file
            sensor.calibration.save(
                    str(path), 
                    format=Metashape.CalibrationFormatOpenCV
                )


def on_execute():
    print("\nExporting models")
    app = Metashape.app

    document = app.document
    console = app.console_pane
    console.clear()

    directory = Path(Metashape.app.getExistingDirectory())

    for chunk in document.chunks:
        if not chunk.enabled:
            continue

        index = document.chunks.index(chunk)

        # Save sensor calibration files
        export_sensors(chunk, directory)

    
def main():
    label = "Scripts/Export sensors"
    Metashape.app.removeMenuItem(label)
    Metashape.app.addMenuItem(label, on_execute)
    print("To execute this script press: {0}".format(label))


if __name__ == "__main__":
    main()
