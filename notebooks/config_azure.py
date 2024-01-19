"""Paths when running on Azure (AML)"""

# Main folders
in_folder = "/home/azureuser/cloudfiles/code/blobfuse/sidewalk/processed_data/"
out_folder = "/home/azureuser/cloudfiles/code/blobfuse/sidewalk/processed_data/route_planning/"

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
segments_file = f'{in_folder}output/sidewalk_segments.gpkg'

# Basic pedestrian network with widths
output_file_widths = f'{out_folder}basic_pedestrian_network_widths.gpkg'

# Output path for a map of the basic network with widths
network_map_widths = f'{out_folder}basic_pedestrian_network_map_widths.html'

# Basic pedestrian network including crossings
output_basic_network_including_crossings = f'{out_folder}basic_pedestrian_network_widths_including_crossings.gpkg'

# Crossing features from project sidewalk
output_project_sidewalk_crossing_features = f'{out_folder}crossing_features/project_sidewalk/crossing_features_project_sidewalk.csv'

# Crossings from project sidewalk
output_project_sidewalk_crossings = f'{out_folder}project_sidewalk_crossings.gpkg'

# Crossing features from OSM
output_osm_crossing_features = f'{out_folder}crossing_features/OpenStreetMap/crossing_features_osm.csv'

# Crossings from OSM
output_osm_crossings = f'{out_folder}osm_crossings.gpkg'

# Crossing features from traffic signs
output_traffic_sign_crossing_features = f'{out_folder}crossing_features/traffic_sign/crossing_features_traffic_sign.csv'

# Crossings from traffic signs
output_traffic_sign_crossings = f'{out_folder}traffic_sign_crossings.gpkg'

# Curb heights 
output_curb_heigts = f'{out_folder}curb_heights/curbs_and_heights.csv'

# Crossings from curb height
output_curb_crossings_base = f'{out_folder}curb_crossings'

# Connections walking network and cycling network
output_walk_bike_connections_base = f'{out_folder}walk_bike_network_connections'

# Road network
output_road_network = f'{out_folder}road_network.gpkg'



# Folders in ovl container

# Main folder
base_folder_ovl = '/home/azureuser/cloudfiles/code/blobfuse/ovl/'

# Ahn folder
ahn_folder = f'{base_folder_ovl}ahn/Amsterdam/ahn4_npz/'

# BGT folder
bgt_folder = f'{base_folder_ovl}bgt/bgt_roads/'

# Folder with unlabeled input point clouds
in_folder_point_clouds = f'{base_folder_ovl}pointcloud/Unlabeled/Amsterdam/'

# Folder with ground and road labeled output point clouds
out_folder_point_clouds = f'{base_folder_ovl}pointcloud/Labeled/ground_and_road/'