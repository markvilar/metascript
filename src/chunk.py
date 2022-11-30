import os

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import open3d
import pandas as pd

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
