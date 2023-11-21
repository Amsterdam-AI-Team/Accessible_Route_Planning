"""Paths when running on Azure (AML)"""

# Main output folder
out_folder = "/home/azureuser/cloudfiles/code/blobfuse/sidewalk/processed_data/route_planning/"

# Output path for storing polygon(s) for the pilot area
output_pilot_area = f'{out_folder}pilot_area.geojson'

# Basic pedestrian network
output_basic_network = f'{out_folder}basic_pedestrian_network.gpkg'

# Output path for a map of the basic network
basic_network_map = f'{out_folder}basic_pedestrian_network_map.html'