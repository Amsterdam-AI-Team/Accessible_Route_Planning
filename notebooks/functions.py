import sys
import os
import requests

import numpy as np
import pandas as pd

import geopandas as gpd
from geopandas import GeoDataFrame
import shapely.geometry as sg

data_crs = 'EPSG:28992'

## AREAS

def create_area_gdf(raw_data_area):
    """Create a clean GeoDataFrame from Amsterdam 'gebiedsindelingen' data"""
    # create dataframe
    raw_df_area = pd.DataFrame(raw_data_area)
    
    # create proper dataframe
    df_area = pd.DataFrame.from_records(raw_df_area.iloc[:, 0]) 
    df_area = df_area[['naam', 'code', 'geometrie']]
    
    # clean up geometry
    df_area = df_area.join(pd.DataFrame.from_records(df_area.iloc[:, 2]))
    df_area['geom'] = df_area['coordinates'].astype(str)
    df_area['geom'] = df_area['geom'].str.replace(r'[', '', regex = False)
    df_area['geom'] = df_area['geom'].str.replace(r']', '', regex = False)
    df_area['geom'] = df_area['geom'].str.replace(r' ', '', regex = False)
    
    # create proper polygon from coordinates
    df_area['geom'] = df_area['geom'].apply(lambda x: x.split(',')) 
    df_area['lon'] = df_area['geom'].apply(lambda x: np.array(x[0:][::2], dtype=np.float32))
    df_area['lat'] = df_area['geom'].apply(lambda x: np.array(x[1:][::2], dtype=np.float32))
    df_area['geometry'] = df_area.apply(lambda x: sg.Polygon(zip(x['lon'], x['lat'])), axis = 1)
    
    # create geodataframe
    gdf_area = GeoDataFrame(df_area, crs=data_crs)
    # gdf_area.to_crs('EPSG:4326', inplace=True)
    
    # remove redundant columns
    gdf_area = gdf_area.drop(['geometrie', 'type', 'coordinates', 'geom', 'lon', 'lat'], axis=1)
    
    return gdf_area


## BGT

BGT_use_columns = ['geometry', 'identificatie_lokaalid', 'naam']
BGT_namedict = {'BGT': 'bgt_functie', 'BGTPLUS': 'plus_type'}
WFS_URL = 'https://map.data.amsterdam.nl/maps/bgtobjecten?'

def get_bgt_data_for_bbox(bbox, layers):
    """Scrape BGT data in a given bounding box."""
    gdf = gpd.GeoDataFrame(columns=BGT_use_columns,
                           geometry='geometry', crs=data_crs)
    gdf.index.name = 'ogc_fid'

    content = []
    for layer in layers:
        # Scrape data from the Amsterdam WFS, this will return a json response.
        json_content = scrape_amsterdam_bgt(layer, bbox=bbox)
        layer_type = BGT_namedict[layer.split('_')[0]]

        # Parse the downloaded json response.
        if json_content is not None and len(json_content['features']) > 0:
            gdf = gpd.GeoDataFrame.from_features(
                                json_content, crs=data_crs).set_index('ogc_fid')
            gdf = gdf[gdf['bgt_status'] == 'bestaand']
            try:
                gdf['naam'] = gdf[layer_type]
            except:
                gdf['naam'] = layer
            content.append(gdf[BGT_use_columns])

    if len(content) > 0:
        gdf = pd.concat(content)
    return gdf


def scrape_amsterdam_bgt(layer_name, bbox=None):
    """
    Scrape BGT layer information from the WFS.
    Parameters
    ----------
    layer_name : str
        Information about the different layers can be found at:
        https://www.amsterdam.nl/stelselpedia/bgt-index/producten-bgt/prodspec-bgt-dgn-imgeo/
    Returns
    -------
    The WFS response in JSON format or a dict.
    """
    params = 'REQUEST=GetFeature&' \
             'SERVICE=wfs&' \
             'VERSION=2.0.0&' \
             'TYPENAME=' \
             + layer_name + '&'

    if bbox is not None:
        bbox_string = str(bbox[0][0]) + ',' + str(bbox[0][1]) + ',' \
                      + str(bbox[1][0]) + ',' + str(bbox[1][1])
        params = params + 'BBOX=' + bbox_string + '&'

    params = params + 'OUTPUTFORMAT=geojson'

    response = requests.get(WFS_URL + params)
    try:
        return response.json()
    except ValueError:
        return None

    