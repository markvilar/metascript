import argparse
import os
import time
import xml.etree.ElementTree as ET

from xml.dom import minidom

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import open3d
import pandas as pd
import pymap3d as pmp
import tqdm

@dataclass
class TransformChunk():
    label: str=""
    cloud: open3d.geometry.PointCloud=None
    poses: pd.DataFrame=None

    def get_label(self):
        return self.label

    def get_poses(self):
        return self.poses

    def set_poses(self, poses):
        self.poses = poses

    def get_points(self):
        return np.asarray(self.cloud.points)

    def set_points(self, points: np.ndarray):
        self.cloud.points = open3d.utility.Vector3dVector(points)

    def get_normals(self):
        return np.asarray(self.cloud.normals)

    def set_normals(self, normals: np.ndarray):
        self.cloud.normals = open3d.utility.Vector3dVector(normals)

    def get_cloud(self):
        return self.cloud

    def get_centroid(self):
        points = self.get_points()
        min_values = np.amin(points, axis=0)
        max_values = np.amax(points, axis=0)
        return np.mean([min_values, max_values], axis=0)

    def load_cloud(self, path: Path):
        extension = os.path.splitext(path)[-1]
        assert extension == ".ply", "invalid model file format"

        # Extract dataset label from model file
        self.label = os.path.basename(path).split("_dense_global")[0]

        # Read cloud and transform from lonlat to latlon
        self.cloud = open3d.io.read_point_cloud(str(path))
        
        points = self.get_points()
        normals = self.get_normals()

        points[:, [0, 1]] = points[:, [1, 0]]
        normals[:, [0, 1]] = normals[:, [1, 0]]
        normals[:, 2] = -normals[:, 2]

        self.set_points(points)
        self.set_normals(normals)

    def load_poses(self, path: Path):
        extension = os.path.splitext(path)[-1]
        assert extension == ".csv", "invalid poses file format"
        self.poses = pd.read_csv(path)


def write_crs(origin: np.ndarray, local_frame: str, local_epsg: int,
    global_frame: str, global_epsg: int, path: Path):
    # Create document
    doc = minidom.Document()

    # Root
    root = doc.createElement("crs")
    doc.appendChild(root)

    # Local CRS
    local_crs = doc.createElement("local")
    local_crs.setAttribute("name", local_frame)
    local_crs.setAttribute("epsg", str(local_epsg))

    local_origin = doc.createElement("origin")
    local_origin.setAttribute("x", str(origin[0]))
    local_origin.setAttribute("y", str(origin[1]))
    local_origin.setAttribute("z", str(origin[2]))
    local_crs.appendChild(local_origin)

    root.appendChild(local_crs)

    # Global CRS
    global_crs = doc.createElement("global")
    global_crs.setAttribute("name", "wgs84")
    global_crs.setAttribute("epsg", str(global_epsg))
    root.appendChild(global_crs)

    with open(path, "w") as file:
        file.write(doc.toprettyxml(indent="  "))


def geodesic2ned(points: np.ndarray, origin: np.ndarray):
    vfunc = np.vectorize(pmp.geodetic2ned)
    transformed = np.zeros(shape=points.shape, dtype=np.float64)
    for i, point in enumerate(tqdm.tqdm(points, desc="Transforming...")):
        ned = vfunc(point[0], point[1], point[2], 
                origin[0], origin[1], origin[2])
        ned_vec = np.asarray(ned)
        transformed[i, :] = np.asarray(ned)

    return transformed


def transform_local(args):
    assert len(args.models) == len(args.poses), \
        "unequal number of models and camera files"
    for model in args.models:
        assert os.path.exists(model), "{0} does not exist".format(model)
    for poses in args.poses:
        assert os.path.exists(model), "{0} does not exist".format(poses)

    for model_path, poses_path in zip(args.models, args.poses):
        model_file = os.path.split(model_path)[-1]
        poses_file = os.path.split(poses_path)[-1]
        print("Loading:  {0},  {1}".format(model_file, poses_file))

    # Load data
    chunks = []
    for model_path, poses_path in zip(args.models, args.poses):
        chunk = TransformChunk()
        chunk.load_cloud(model_path)
        chunk.load_poses(poses_path)
        points = chunk.get_points()
        poses = chunk.get_poses()
        chunks.append(chunk)

    # Compute chunk centroid
    centroid = np.zeros(3)
    for chunk in chunks:
        centroid += chunk.get_centroid()
    centroid /= len(chunks)
    centroid[2] = 0

    origin = centroid
    
    print("Origin: {0}".format(origin))

    # TODO: Chunk label might not be exactly the same as cluster label
    label = chunks[0].get_label()
    write_crs(origin, 
        "ned", -1,
        "wgs84", 4326, 
        args.output / (label + "_crs.xml"))

    # Transform pose
    for chunk in chunks:
        poses = chunk.get_poses()
        
        # Transform poses
        positions = poses[["latitude", "longitude", "altitude"]]
        transformed_positions = geodesic2ned(positions.to_numpy(), origin)

        poses["north"] = transformed_positions[:, 0]
        poses["east"] = transformed_positions[:, 1]
        poses["down"] = transformed_positions[:, 2]

        transformed_poses = poses[["label", "north", "east", "down", "roll",
            "pitch", "yaw"]]

        label = chunk.get_label()
        transformed_poses.to_csv(args.output / (label + "_poses_local.csv"))
        chunk.set_poses(transformed_poses)

    for chunk in chunks:
        points = chunk.get_points()
        
        # TODO: Debug, remove print
        transformed_points = geodesic2ned(points, origin)
        chunk.set_points(transformed_points)
        cloud = chunk.get_cloud()

        plt.scatter(transformed_points[:, 1], transformed_points[:, 0])

        label = chunk.get_label()
        path = args.output / (label + "_dense_local.ply")
        open3d.io.write_point_cloud(str(path), cloud, write_ascii=True, 
            compressed=False)

    for chunk in chunks:
        fig = plt.figure()
        ax = fig.add_subplot()

        points = chunk.get_points()
        poses = chunk.get_poses()

        ax.scatter(points[:, 1], points[:, 0], s=1.0)
        ax.scatter(poses["east"], poses["north"], s=5.0)

        do_save = True
        if do_save:
            fig.savefig(args.output / "{0}.png".format(chunk.get_label()))

        
    
    do_plot = False
    if do_plot:
        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", 
            type=Path, 
            required=True,  
            nargs="+",
            help="point cloud files"
        )
    parser.add_argument("--poses", 
            type=Path, 
            required=True,  
            nargs="+",
            help="pose files"
        )
    parser.add_argument("--output",
            type=Path, 
            required=True,  
            help="output directory"
        )
    parser.add_argument("--export", 
            type=bool,
            action=argparse.BooleanOptionalAction,
            help="export transformed clouds"
        )
    
    transform_local(parser.parse_args())

if __name__ == "__main__":
    main()
