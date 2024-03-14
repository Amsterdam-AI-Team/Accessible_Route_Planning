import sys
sys.path.append('../notebooks')

import shapely.geometry as sg
import shapely.ops as so
from centerline.geometry import Centerline
import numpy as np
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Polygon
from scipy.spatial import cKDTree
import settings as st

import settings as st


def fix_invalid(poly):
    """
    Fix invalid polygons by buffering and converting to MultiPolygon if needed.

    Parameters:
    - poly (shapely.geometry.Polygon or shapely.geometry.MultiPolygon): Input polygon.

    Returns:
    shapely.geometry.Polygon or shapely.geometry.MultiPolygon: Fixed polygon.
    """
    orig_multi = type(poly) == sg.MultiPolygon
    if ~poly.is_valid:
        poly = poly.buffer(0)
        if type(poly) == sg.Polygon and orig_multi:
            poly = sg.MultiPolygon([poly])
    return poly


def extract_interior(poly):
    """
    Extract interior polygons from a polygon.

    Parameters:
    - poly (shapely.geometry.Polygon): Input polygon.

    Returns:
    Tuple (shapely.geometry.Polygon, shapely.geometry.MultiPolygon): Tuple containing
    the exterior polygon and interior polygons.
    """
    if poly.interiors:
        int_polys = sg.MultiPolygon([sg.Polygon(list(lr.coords)) for lr in poly.interiors])
        return sg.Polygon(list(poly.exterior.coords)), int_polys
    else:
        return poly, sg.MultiPolygon()


def get_centerlines(polygon, interpolation_distance=0.5):
    """
    Get centerlines from a polygon.

    Parameters:
    - polygon (shapely.geometry.Polygon): Input polygon.
    - interpolation_distance (float): Interpolation distance for centerline calculation.

    Returns:
    centerline.geometry.Centerline or np.nan: Centerline object or np.nan if calculation fails.
    """
    try:
        x = Centerline(polygon, interpolation_distance=interpolation_distance)
    except Exception as e:
        print(e)
        x = np.nan
    return x


def remove_short_lines(line, min_se_length=5):
    """
    Remove short lines from a MultiLineString.

    Parameters:
    - line (shapely.geometry.MultiLineString): Input MultiLineString.
    - min_se_length (float): Minimum length for a line to be retained.

    Returns:
    shapely.geometry.MultiLineString: MultiLineString with short lines removed.
    """
    if line.type == 'MultiLineString':
        passing_lines = []
        for i, linestring in enumerate(line.geoms):
            other_lines = sg.MultiLineString([x for j, x in enumerate(line.geoms) if j != i])
            p0 = sg.Point(linestring.coords[0])
            p1 = sg.Point(linestring.coords[-1])
            is_deadend = False
            if p0.disjoint(other_lines):
                is_deadend = True
            if p1.disjoint(other_lines):
                is_deadend = True
            if not is_deadend or linestring.length > min_se_length:
                passing_lines.append(linestring)
        return sg.MultiLineString(passing_lines)
    if line.type == 'LineString':
        return line


def linestring_to_segments(linestring):
    """
    Convert a LineString to a list of LineString segments.

    Parameters:
    - linestring (shapely.geometry.LineString): Input LineString.

    Returns:
    list of shapely.geometry.LineString: List of LineString segments.
    """
    linestrings = []
    for i in range(len(linestring.coords) - 1):
        linestrings.append(sg.LineString([linestring.coords[i], linestring.coords[i+1]]))
    return linestrings


def get_segments(line):
    """
    Get segments from a MultiLineString or LineString.

    Parameters:
    - line (shapely.geometry.MultiLineString or shapely.geometry.LineString): Input geometry.

    Returns:
    list of shapely.geometry.LineString: List of LineString segments.
    """
    line_segments = []
    if line.type == 'MultiLineString':
        for linestring in line.geoms:
            line_segments.extend(linestring_to_segments(linestring))
    if line.type == 'LineString':
        line_segments.extend(linestring_to_segments(line))
    return line_segments


def interpolate_by_distance(linestring, resolution=1):
    """
    Interpolate points along a LineString with a specified resolution.

    Parameters:
    - linestring (shapely.geometry.LineString): Input LineString.
    - resolution (float): Interpolation resolution.

    Returns:
    list of shapely.geometry.Point: Interpolated points.
    """
    all_points = []
    count = round(linestring.length / resolution) + 1
    if count == 1:
        all_points.append(linestring.interpolate(linestring.length / 2))
    else:
        for i in range(count):
            all_points.append(linestring.interpolate(resolution * i))
    return all_points


def interpolate(line, resolution=1):
    """
    Interpolate points along a MultiLineString or LineString with a specified resolution.

    Parameters:
    - line (shapely.geometry.MultiLineString or shapely.geometry.LineString): Input geometry.
    - resolution (float): Interpolation resolution.

    Returns:
    shapely.geometry.MultiPoint: Interpolated points.
    """
    if line.type == 'MultiLineString':
        all_points = []
        for linestring in line:
            all_points.extend(interpolate_by_distance(linestring, resolution))
        return sg.MultiPoint(all_points)
    if line.type == 'LineString':
        return sg.MultiPoint(interpolate_by_distance(line, resolution))


def polygon_to_multilinestring(polygon):
    """
    Convert a polygon to a MultiLineString.

    Parameters:
    - polygon (shapely.geometry.Polygon): Input polygon.

    Returns:
    shapely.geometry.MultiLineString: MultiLineString representation of the polygon.
    """
    return sg.MultiLineString([polygon.exterior] + [line for line in polygon.interiors])


def get_avg_width(poly, segments, resolution=1, precision=2):
    """
    Calculate average and minimum widths for line segments within a polygon.

    Parameters:
    - poly (shapely.geometry.Polygon): Input polygon.
    - segments (shapely.geometry.MultiLineString): MultiLineString of line segments.
    - resolution (float): Interpolation resolution.
    - precision (int): Number of decimal places for the result.

    Returns:
    Tuple (numpy.ndarray, numpy.ndarray): Arrays of average and minimum widths.
    """
    avg_width = []
    min_width = []
    sidewalk_lines = polygon_to_multilinestring(poly)
    for segment in segments:
        points = interpolate(segment, resolution)
        distances = []
        for point in points.geoms:
            p1, p2 = so.nearest_points(sidewalk_lines, point)
            distances.append(p1.distance(p2))
        avg_width.append(sum(distances) / len(distances) * 2)
        min_width.append(min(distances) * 2)
    return np.round(avg_width, precision), np.round(min_width, precision)


def get_avg_width_cl(poly, segments, resolution=1, precision=2):
    """
    Calculate average and minimum widths for line segments within a polygon using centerlines.

    Parameters:
    - poly (shapely.geometry.Polygon): Input polygon.
    - segments (shapely.geometry.MultiLineString or shapely.geometry.LineString): MultiLineString
      or LineString of line segments.
    - resolution (float): Interpolation resolution.
    - precision (int): Number of decimal places for the result.

    Returns:
    pandas.Series: Series with 'avg_width' and 'min_width' values.
    """
    sidewalk_lines = polygon_to_multilinestring(poly)
    points = interpolate(segments, resolution)
    distances = []
    for point in points.geoms:
        p1, p2 = so.nearest_points(sidewalk_lines, point)
        distances.append(p1.distance(p2))
    avg_width = sum(distances) / len(distances) * 2
    min_width = min(distances) * 2
    return pd.Series([np.round(avg_width, precision), np.round(min_width, precision)])


def get_route_width(route_weight):
    """
    Map route weight to corresponding route width.

    Parameters:
    - route_weight (float): Route weight value.

    Returns:
    float: Mapped route width.
    """
    if route_weight == 0:
        route_width = np.nan
    elif (route_weight > 0) & (route_weight < 100):
        route_width = st.width_6
    elif (route_weight >= 100) & (route_weight < 10000):
        route_width = st.width_5
    elif (route_weight >= 10000) & (route_weight < 1000000):
        route_width = st.width_4
    elif (route_weight >= 1000000) & (route_weight < 100000000):
        route_width = st.width_3
    elif (route_weight >= 100000000) & (route_weight < 10000000000):
        route_width = st.width_2
    elif (route_weight >= 10000000000) & (route_weight < 1000000000000):
        route_width = st.width_1
    elif (route_weight >= 1000000000000) & (route_weight < 100000000000000):
        route_width = st.min_path_width
    elif route_weight == 100000000000000:
        route_width = 0
    elif route_weight > 100000000000000:
        route_width = np.nan
    else:
        route_width = np.nan
    return route_width


def create_df_centerlines(centerline):
    """
    Create a GeoDataFrame from centerline geometry.

    Parameters:
    - centerline (centerline.geometry.Centerline or shapely.geometry.MultiLineString
      or shapely.geometry.LineString): Centerline geometry.

    Returns:
    geopandas.GeoDataFrame: GeoDataFrame with 'geometry', 'length', and 'route_weight' columns.
    """
    centerline_list = []
    if centerline.type == 'LineString':
        centerline_list.append(centerline)
    if centerline.type == 'MultiLineString':
        for line in centerline:
            centerline_list.append(line)
    centerline_df = gpd.GeoDataFrame(centerline_list, columns=['geometry'])
    centerline_df['length'] = centerline_df['geometry'].length
    centerline_df['route_weight'] = np.nan
    return centerline_df


def cut(line, distance):
    """
    Cut a LineString in two at a specified distance from its starting point.

    Parameters:
    - line (shapely.geometry.LineString): Input LineString.
    - distance (float): Distance from the starting point to cut the line.

    Returns:
    list of shapely.geometry.LineString: List of cut LineStrings.
    """
    if distance <= 0.0 or distance >= line.length:
        return [sg.LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(sg.Point(p))
        if pd == distance:
            return [sg.LineString(coords[:i+1]), sg.LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            line_1 = sg.LineString(coords[:i] + [(cp.x, cp.y)])
            line_2 = sg.LineString([(cp.x, cp.y)] + coords[i:])
            return [line_1, line_2]


def shorten_linestrings(centerline_df, max_ls_length):
    """
    Shorten LineStrings in a GeoDataFrame to a specified maximum length.

    Parameters:
    - centerline_df (geopandas.GeoDataFrame): GeoDataFrame with 'geometry',
      'length', and 'route_weight' columns.
    - max_ls_length (float): Maximum length for LineStrings.

    Returns:
    geopandas.GeoDataFrame: GeoDataFrame with shortened LineStrings.
    """
    while centerline_df['length'].max() > max_ls_length:
        id_longest_ls = centerline_df['length'].idxmax()
        longest_ls = centerline_df.iloc[[id_longest_ls]]['centerlines'].values[0]
        cut_ls = cut(longest_ls, max_ls_length-0.01)
        cut_ls_df = gpd.GeoDataFrame(cut_ls, columns=['centerlines']).set_geometry('centerlines')
        cut_ls_df['length'] = cut_ls_df['centerlines'].length
        cut_ls_df['cl_id'] = centerline_df['cl_id'][id_longest_ls]
        centerline_df = centerline_df.drop(index=id_longest_ls)
        centerline_df = pd.concat([centerline_df, cut_ls_df]).reset_index(drop=True)
    return centerline_df


def remove_interiors(polygon, eps):
    """
    Remove interiors from a polygon based on area threshold.

    Parameters:
    - polygon (shapely.geometry.Polygon): Input polygon.
    - eps (float): Area threshold for interiors.

    Returns:
    shapely.geometry.Polygon: Polygon with interiors removed.
    """
    list_interiors = []
    for interior in polygon.interiors:
        p = sg.Polygon(interior)
        if p.area > eps:
            list_interiors.append(interior)
    return sg.Polygon(polygon.exterior.coords, holes=list_interiors)


def create_mls_per_sidewalk(df, crs):
    """
    Create a MultiLineString GeoDataFrame from segments based on sidewalk_id.

    Parameters:
    - df (pandas.DataFrame): DataFrame with 'sidewalk_id' and 'geometry' columns.
    - crs (int or str): Coordinate Reference System.

    Returns:
    geopandas.GeoDataFrame: MultiLineString GeoDataFrame with 'geometry' column.
    """
    mls_list = []
    for sidewalk_id in df['sidewalk_id'].unique():
        df_segments_id = df[df['sidewalk_id'] == sidewalk_id]
        mls_id = sg.MultiLineString(list(df_segments_id['geometry']))
        mls_list.append(mls_id)
    return GeoDataFrame(geometry=mls_list, crs=crs)


def bbox_to_polygon(bbox):
    """
    Convert a bounding box to a Polygon.

    Parameters:
    - bbox (tuple): Bounding box coordinates (xmin, ymin, xmax, ymax).

    Returns:
    shapely.geometry.Polygon: Polygon representation of the bounding box.
    """
    return Polygon([bbox[0], (bbox[0][0], bbox[1][1]), bbox[1], (bbox[1][0], bbox[0][1])])


def infer_column_by_distance(gdf1, gdf2, column_name):
    """
    Replace column values in gdf1 with values from gdf2 for the closest rows across gdf1 and gdf2.

    Parameters:
    - gdf1 (geopandas.GeoDataFrame): GeoDataFrame to be updated.
    - gdf2 (geopandas.GeoDataFrame): GeoDataFrame with reference values.
    - column_name (str): Column name to be updated.

    Returns:
    geopandas.GeoDataFrame: Updated GeoDataFrame.
    """
    spatial_index_gdf2 = cKDTree(gdf2.geometry.apply(lambda geom: (geom.x, geom.y)).tolist())
    _, indices_gdf2 = spatial_index_gdf2.query(gdf1.geometry.apply(
        lambda geom: (geom.x, geom.y)).tolist())
    closest_rows_gdf2 = gdf2.iloc[indices_gdf2].reset_index(drop=True)
    gdf1[column_name] = closest_rows_gdf2[column_name].to_list()
    return gdf1


def dist(a, b):
    """
    Calculate Euclidean distance between two points.

    Parameters:
    - a (tuple): Coordinates of point A.
    - b (tuple): Coordinates of point B.

    Returns:
    float: Euclidean distance between points A and B.
    """
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def reverse_line(line):
    """
    Reverse the coordinates of a LineString.

    Parameters:
    - line (shapely.geometry.LineString): Input LineString.

    Returns:
    shapely.geometry.LineString: Reversed LineString.
    """
    return sg.LineString(line.coords[::-1])
