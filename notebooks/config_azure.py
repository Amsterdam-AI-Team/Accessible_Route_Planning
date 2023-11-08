"""Paths when running on Azure (AML)"""

# Main output folder
out_folder = "/home/azureuser/cloudfiles/code/blobfuse/sidewalk/processed_data/"

# Output path for storing polygon(s) for the pilot area
output_pilot_area = f'{out_folder}route_planning/pilot_area.geojson'

# BGT path
bgt_road_file = f'{out_folder}bgt/bgt_voetpad.csv'

# Basic pedestrian network
output_basic_network = f'{out_folder}route_planning/basic_pedestrian_network.gpkg'