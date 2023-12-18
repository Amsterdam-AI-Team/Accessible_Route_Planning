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

# Crossings from project sidewalk
output_project_sidewalk_crossings = f'{out_folder}project_sidewalk_crossings.gpkg'

# Crossings from OSM
output_osm_crossings = f'{out_folder}osm_crossings.gpkg'

# Crossings from traffic signs
output_traffic_sign_crossings = f'{out_folder}traffic_sign_crossings.gpkg'

# Crossings from curb height
output_curb_crossings_base = f'{out_folder}curb_crossings'

# Road network
output_road_network = f'{out_folder}road_network.gpkg'
