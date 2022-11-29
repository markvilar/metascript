import csv
import math

from pathlib import Path

import Metashape

from helpers import calculate_estimated_pose, get_chunk_center, calculate_mean


def save_estimated_reference():
    app = Metashape.app
    
    # Get directory
    directory = Path(Metashape.app.getExistingDirectory())

    document = app.document
    console = app.console_pane

    for chunk in chunks:
        if not chunk.enabled:
            continue
        
        path = directory / (chunk.label + "_cameras_global.csv")
        pose_header = ["label", "latitude", "longitude", "altitude", "roll", 
            "pitch", "yaw"]

        with open(path, 'w') as file:
            # Write header
            writer = csv.writer(file)
            writer.writerow(pose_header)
            for camera in chunk.cameras:
                if camera.type != Metashape.Camera.Type.Regular \
                    or not camera.transform:
                    continue

                label = camera.label

                # Get camera poses in ENU, YPR
                position, attitude = calculate_estimated_pose(camera)

                data = [label, position.y, position.x, position.z, 
                        attitude.z, attitude.y, attitude.x]
                
                writer.writerow(data)
            
def main():
    label = "Scripts/Export estimated cameras"
    Metashape.app.removeMenuItem(label)
    Metashape.app.addMenuItem(label, save_estimated_reference)
    print("To execute this script press {}".format(label))

if __name__ == "__main__":
    main()
