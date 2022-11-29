import math

import Metashape
import pymap3d as pm

def get_chunk_center(chunk):
    center = Metashape.Vector((0,0,0))
    return chunk.crs.project(chunk.transform.matrix.mulp(center))

def calculate_mean(vectors):
    sum = Metashape.Vector((0,0,0))
    for vector in vectors:
        sum += vector
    return sum / len(vectors)

def get_cartesian_crs(crs):
    ecef_crs = crs.geoccs
    if ecef_crs is None:
        ecef_crs = Metashape.CoordinateSystem('LOCAL')
    return ecef_crs

def calculate_rotation_dx(alpha):
    sina = math.sin(alpha)
    cosa = math.cos(alpha)
    mat = Metashape.Matrix([[0, 0, 0], [0, -sina, -cosa], [0, cosa, -sina]])
    return mat

def calculate_rotation_dy(alpha):
    sina = math.sin(alpha)
    cosa = math.cos(alpha)
    mat = Metashape.Matrix([[-sina, 0, cosa], [0, 0, 0], [-cosa, 0, -sina]])
    return mat

def calculate_rotation_dz(alpha):
    sina = math.sin(alpha)
    cosa = math.cos(alpha)
    mat = Metashape.Matrix([[-sina, -cosa, 0], [cosa, -sina, 0], [0, 0, 0]])
    return mat

def get_antenna_transform(sensor):
    location = sensor.antenna.location
    if location is None:
        location = sensor.antenna.location_ref
    if location is None:
        location = Metashape.Vector([0.0, 0.0, 0.0])
    rotation = sensor.antenna.rotation
    if rotation is None:
        rotation = sensor.antenna.rotation_ref
    if rotation is None:
        rotation = Metashape.Vector([0.0, 0.0, 0.0])
    mat = Metashape.Matrix.Diag((1, -1, -1, 1)) \
        * Metashape.Matrix.Translation(location) \
        * Metashape.Matrix.Rotation(Metashape.Utils.ypr2mat(rotation))
    return mat

def get_euler_angles_name(euler_angles):
    if euler_angles == Metashape.EulerAnglesOPK:
        return "OPK"
    if euler_angles == Metashape.EulerAnglesPOK:
        return "POK"
    if euler_angles == Metashape.EulerAnglesYPR:
        return "YPR"
    if euler_angles == Metashape.EulerAnglesANK:
        return "ANK"

def calculate_estimated_pose(camera):
    """
    camera: Metashape.Camera
    """
    chunk = camera.chunk
    camera = camera

    # NOTE: Some important properties for future reference
    # chunk.region.center
    # chunk.transform
    # camera_transform

    # If the camera is not align, return
    if not camera.transform:
        return

    transform = chunk.transform.matrix
    crs = chunk.crs

    # If the cameras are defined in a datum other than the chunk
    if chunk.camera_crs:
        transform = Metashape.CoordinateSystem.datumTransform(crs, 
            chunk.camera_crs) * transform
        crs = chunk.camera_crs

    # Get ECEF
    ecef_crs = get_cartesian_crs(crs)

    # Transformation from camera to ECEF (but without proper rotation)
    camera_transform = transform * camera.transform
    
    # Compensate for lever arm / misalignment
    antenna_transform = get_antenna_transform(camera.sensor)
    location_ecef = camera_transform.translation() \
        + camera_transform.rotation() * antenna_transform.translation()
    rotation_ecef = camera_transform.rotation() \
        * antenna_transform.rotation()
    
    # Transform estimated location to world coordinate system
    estimated_location = \
        Metashape.CoordinateSystem.transform(location_ecef, ecef_crs, crs)

    # Get orientation relative to local frame
    if chunk.euler_angles == Metashape.EulerAnglesOPK \
        or chunk.euler_angles == Metashape.EulerAnglesPOK:
        localframe = crs.localframe(location_ecef)
    else:
        localframe = ecef_crs.localframe(location_ecef)

    estimated_rotation = Metashape.utils.mat2euler(
        localframe.rotation() * rotation_ecef, chunk.euler_angles)
    
    return estimated_location, estimated_rotation
