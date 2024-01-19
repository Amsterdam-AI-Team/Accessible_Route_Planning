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

# Basic pedestrian network with widths and crossings
output_file_crossings = f'{out_folder}basic_pedestrian_network_widths_including_crossings.gpkg'

# Output path for a map of the basic network with widths
network_map_widths = f'{out_folder}basic_pedestrian_network_map_widths.html'

# Output path for final network
network_map_final = f'{out_folder}network_map_final.html'