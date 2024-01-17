import statistics
import numpy as np
from shapely.geometry import MultiPoint
from shapely.ops import split, snap

from upcp.labels import Labels
from upcp.utils import clip_utils

import curb_utils


def create_mask(points, labels, polygons):
    label_mask = np.zeros(len(points), dtype=bool)

    # Already labelled ground points can be labelled as road.
    mask = (labels == Labels.GROUND) | (labels == Labels.ROAD)
    mask_ids = np.where(mask)[0]

    road_mask = np.zeros((len(mask_ids),), dtype=bool)
    for polygon in polygons:
        clip_mask = clip_utils.poly_clip(points[mask, :], polygon)
        road_mask = road_mask | clip_mask

    label_mask[mask_ids[road_mask]] = True

    return label_mask


def calculate_curb_height(points, labels, segment_polygon, min_nr_points): # calculate median over all points
    curb_height = np.nan
    available_points = True

    label_mask = curb_utils.create_mask(points, labels, [segment_polygon,]) # TODO
    points_in_segment = points[label_mask]
    labels_in_segment = labels[label_mask]
    
    z_values_road = points_in_segment[labels_in_segment == Labels.ROAD][:, -1]

    if len(z_values_road) > min_nr_points:
        z_values_road.sort()
        road_height = statistics.median(z_values_road)
    else:
        available_points = False

    z_values_sidewalk = points_in_segment[labels_in_segment == Labels.GROUND][:, -1]
    if len(z_values_sidewalk) > min_nr_points:
        z_values_sidewalk.sort()
        sidewalk_height = statistics.median(z_values_sidewalk)
    else:
        available_points = False

    if available_points:
        curb_height = sidewalk_height - road_height
    
    return curb_height, available_points

def get_height_color(curb_height, available_points, min_h):
    if not available_points:
        color = 'black'
        return color
    
    if curb_height < min_h:
        color = 'green'
    else:
        color = 'orange'
    return color

def get_points_on_line(line, distance_delta):
    # generate the equidistant points
    distances = np.arange(0, line.length, distance_delta)
    points = MultiPoint([line.interpolate(distance) for distance in distances] + [(line.coords[0], line.coords[-2])]) # line.boundary[1]
    return points[:-1] # Exclude last (duplicate) point

def split_line_by_point(line, point, tolerance: float=1): # TO DO Tolerence is belangrijk, misschien hier nog mee tweaken
    return split(snap(line, point, tolerance), point)