import laspy
import numpy as np


def read_las(las_path):
    """
    Read LAS file and extract point coordinates and labels.

    Parameters:
    - las_path (str): Path to the LAS file.

    Returns:
    Tuple of NumPy arrays (points, labels).
    """
    pointcloud = laspy.read(las_path)

    if 'label' not in pointcloud.point_format.extra_dimension_names:
        labels = np.zeros((len(pointcloud.x),), dtype='uint16')
    else:
        labels = pointcloud.label
    
    x = (np.array(pointcloud.x))
    y = (np.array(pointcloud.y))
    z = (np.array(pointcloud.z))
    points = np.vstack((x, y, z)).T

    return points, labels
