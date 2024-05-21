import requests
import sys
sys.path.append('../notebooks')

import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

import settings as st

# Base URL for the Web Feature Service
WFS_URL = 'https://api.data.amsterdam.nl/v1/wfs/bgt/?'

def scrape_amsterdam_bgt(bbox=None):
    """
    Scrape BGT layer information from the Amsterdam WFS.
    Parameters:
    - bbox (tuple): Optional bounding box ((minx, miny), (maxx, maxy)).
    Returns:
    JSON response or None if the request fails.
    """
    # Build the request parameters
    params = {
        'SERVICE': 'WFS',
        'VERSION': '2.0.0',
        'REQUEST': 'GetFeature',
        'TYPENAMES': 'wegdelen-geometrie',
        'OUTPUTFORMAT': 'geojson'
    }
    
    if bbox:
        bbox_string = ','.join(map(str, [bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]]))
        params['BBOX'] = bbox_string
    
    # Send the GET request
    response = requests.get(WFS_URL, params=params)
    try:
        return response.json()
    except ValueError:
        return None

def get_bgt_data_for_bbox(bbox, layers):
    """
    Scrape BGT data within a specified bounding box for given layers.
    Parameters:
    - bbox (tuple): Bounding box coordinates ((minx, miny), (maxx, maxy)).
    - layers (list): List of BGT layers to scrape.
    Returns:
    GeoDataFrame with the BGT data for the specified layers.
    """
    # Retrieve data from WFS
    json_content = scrape_amsterdam_bgt(bbox=bbox)

    # Filter items and extract required data
    features = [
        (item['properties']['bgt_functie'], Polygon(item['geometry']['coordinates'][0]))
        for item in json_content.get('features', [])
        if item['properties']['bgt_functie'] in layers
    ]

    # Unpack features if non-empty
    if features:
        bgt_functies, geometries = zip(*features)
    else:
        bgt_functies, geometries = [], []

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame({
        'naam': bgt_functies,
        'geometry': geometries
    }, geometry='geometry', crs=st.CRS)

    return gdf