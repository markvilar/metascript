import Metashape

def export_matches(chunk, directory):
    tie_points = chunk.point_cloud
    points = tie_points.points
    point_projections = tie_points.projections
    point_count = len(points)

    camera_matches = dict()

    print("Computing matches...")
    start = time.time()

    # Loop for cameras and find points which are projected into it
    for camera in chunk.cameras:
        if not camera.transform:
            continue

        matches = set()
        point_index = 0
        current_projection = point_projections[camera]

        # Go through all points that are projected by the camera
        for current_point in current_projection:
            track_id = current_point.track_id

            while point_index < point_count \
                and points[point_index].track_id < track_id:
                point_index += 1
            
            # If the point part of the tie points, and the track ID matches
            if point_index < point_count \
                and points[point_index].track_id == track_id:
                    
                if tie_points.points[point_index].valid:
                    matches.add(point_index)
                
        camera_matches[camera] = matches

    correspondences = []
    for index, target in enumerate(chunk.cameras[:-1]):
        if target not in camera_matches.keys():
            continue
            
        for source in chunk.cameras[index+1:]:
            if source not in camera_matches.keys():
                continue

            matches = camera_matches[target] & camera_matches[source]
            num_matches = len(matches)
    
            if num_matches > 3:
                correspondences.append( 
                    (target.label, source.label, num_matches) )
            else:
                continue

    header = ["target", "source", "valid_matches"]
    path = directory / (chunk.label + "_matches.csv")
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for correspondence in correspondences:
            writer.writerow(correspondence)

    end = time.time()
    print("Loop {0} cameras in {1} seconds.".format(len(chunk.cameras), 
        end - start))

def export():
    app = Metashape.app
    document = app.document

    console = app.console_pane
    console.clear()

    # Get output directory
    directory = Path(Metashape.app.getExistingDirectory())

    # Loop through chunks and get matches
    for chunk in document.chunks:
        if not chunk.enabled:
            continue
        export_matches(chunk, directory)


def main():
    label = "Scripts/Export camera matches"
    Metashape.app.removeMenuItem(label)
    Metashape.app.addMenuItem(label, export)
    print("To execute this script press: {0}".format(label))


if __name__ == "__main__":
    main()
