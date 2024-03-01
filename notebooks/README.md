# Notebooks

These jupyter notebooks make up the pipeline to create an accessible network and plan routes on that network given a set of user preferences. The notebooks should be run in the order than is listed below.

**IMPORTANT** 
- **It is not neccessary to run notebook 5 for demonstration purposes. Labelled point clouds have been provided in the output folder.** 
- **Notebooks 1 untill 9 should be run using the network generation environment (steps 2a untill 2c in the installation process).** 
- **Notebook 10 should be run using the route planning environment (step 3 in the installation process).**

---

[1. Pilot area extraction](1.%20get_pilot_area.ipynb) -- obtain geojson of area for accessible network.
* [2a. Create basic walking network](2a.%20create_basic_network.ipynb) -- create a basic walking network to navigate on.
* [2b. Create bike network](2b.%20create_bike_network.ipynb) -- create the bike network to navigate on.
* [2c. Create road network](2c.%20create_road_network.ipynb) -- create road network (car and bicycle roads) which is used to determine if generated crossings are valid

[3. Project sidewalk widths onto network](3.%20get_sidewalk_widths_on_network.ipynb) -- project and add sidewalk widths to the walking network generated in step 2a.
* [4a. Get OpenStreetMap crossing features](4a.%20get_osm_crossing_features.ipynb) -- obtain crossing features from OSM which are used to generate crossings.
* [4b. Get Project Sidewalk crossing features](4b.%20get_project_sidewalk_crossing_features.ipynb) -- obtain crossing features from Project Sidewalk which are used to generate crossings.
* [4c. Get traffic sign features](4a.%20get_osm_crossing_features.ipynb) -- obtain crossing features from traffic signs which are used to generate crossings.
* [4d. Generate OSM, Project Sidewalk and traffic sign crossings](4d.%20generate_osm_ps_ts_crossings.ipynb) -- generate crossings from features retrieved in steps 4a, 4b and 4c.

[5. Ground and road fusion](5.%20ground_and_road_fusion.ipynb) -- obtain point clouds which have a labelled ground and road which are used to calculate curb height.

* [6a. Get curb heights](6a.%get_curb_heights.ipynb) -- obtain curb heights from point clouds to generate crossings.
* [6a. Generate curb ramp crossings](6b.%20generate_curb_ramp_crossings.ipynb) -- generate crossings from curb height information.

[]()

* [7a. Get public transport stop features](7a.%20get_public_transport_stop_features.ipynb) -- obtain public transport stop features.
* [7b. Generate public transport stop connections](7b.%20generate_public_transport_stop_connections.ipynb) -- obtain edges that connect the walking network and public transport stops.

[8. Generate walking and bike connections](8.%20generate_walking_and_bike_network_connections.ipynb) -- obtain edges that connect the walking and bike network.

[9. Merge networks and crossings](9.%20merge_networks_and_crossings.ipynb) -- merge the walking network, bike network, crossings and public transport stops.

[10. Plan routes](10.%plan_routes.ipynb) -- plan routes on the accessible network given a set of user preferences.
