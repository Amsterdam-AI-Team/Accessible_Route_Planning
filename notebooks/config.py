"""Paths when running locally"""

# Main folders
in_folder = "../data/input/"
out_folder = "../data/output/"

# Output path for storing polygon(s) for the pilot area
output_pilot_area = f'{out_folder}pilot_area.geojson'

# Basic pedestrian network
output_basic_network = f'{out_folder}basic_pedestrian_network.gpkg'

# Sidewalk polygons related to basic pedestrian network
output_sidewalks_basic_network = f'{out_folder}sidewalks_basic_pedestrian_network.gpkg'

# Output path for a map of the basic network
basic_network_map = f'{out_folder}basic_pedestrian_network_map.html'

# Bike network
output_bike_network = f'{out_folder}bike_network.gpkg'

# Bike network cut up
output_bike_network_cut = f'{out_folder}bike_network_cut.gpkg'

# Path polygons related to bike network
output_bikepaths_bike_network = f'{out_folder}paths_bike_network.gpkg'

# Output path for a map of the basic network
bike_network_map = f'{out_folder}bike_network_map.html'

# Output paths notebook 5 (https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Sidewalk_Width)
segments_file = f'{in_folder}sidewalk_segments.gpkg'

# Basic pedestrian network with widths
output_file_widths = f'{out_folder}basic_pedestrian_network_widths.gpkg'

# Output path for a map of the basic network with widths
network_map_widths = f'{out_folder}basic_pedestrian_network_map_widths.html'

# Output path for final network
network_map_final = f'{out_folder}network_map_final.html'

# Basic pedestrian network including crossings
output_basic_network_including_crossings = f'{out_folder}basic_pedestrian_network_widths_including_crossings.gpkg'

# Crossing features from project sidewalk
output_project_sidewalk_crossing_features = f'{out_folder}crossing_features_project_sidewalk.gpkg'

# Crossings from project sidewalk
output_project_sidewalk_crossings = f'{out_folder}project_sidewalk_crossings.gpkg'

# Crossing features from OSM
output_osm_crossing_features = f'{out_folder}crossing_features_osm.gpkg'

# Crossings from OSM
output_osm_crossings = f'{out_folder}osm_crossings.gpkg'

# Crossing features from traffic signs
output_traffic_sign_crossing_features = f'{out_folder}crossing_features_traffic_sign.gpkg'

# Crossings from traffic signs
output_traffic_sign_crossings = f'{out_folder}traffic_sign_crossings.gpkg'

# Curb heights
output_curb_heigts = f'{out_folder}curbs_and_heights.gpkg'

# Crossings from curb height
output_curb_crossings_base = f'{out_folder}curb_crossings'

# Csv source file for traffic signs 
signs_file = f'{in_folder}2022juni_verkeersborden_obv_beeldherkenning.csv'

# XML source file for public transport (bus, tram and ferry) stops
ndov_public_transport_stops = f'{in_folder}ExportCHB20240314013152.xml'

# Features for public transport stops
output_public_transport_features = f'{out_folder}public_transport_features.gpkg'

# Connections walking network and public transport stops
output_walk_public_transport_stop_connections = f'{out_folder}walk_public_transport_stop_connections.gpkg'

# Connections walking network and cycling network
output_walk_bike_connections_base = f'{out_folder}walk_bike_network_connections'

# Road network
output_road_network = f'{out_folder}road_network.gpkg'

# Final network
output_final_network = f'{out_folder}final_network.gpkg'

# Ahn folder
ahn_folder = f'{in_folder}ahn/'

# BGT folder
bgt_folder = f'{in_folder}bgt/'

# Folder with unlabeled input point clouds
in_folder_point_clouds = f'{in_folder}pointcloud/'

# Folder with ground and road labeled output point clouds
out_folder_point_clouds = f'{out_folder}pointcloud/'
