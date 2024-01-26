# Accessible route planning

Create a pedestrian network and plan accessible routes on it.

## Background

## Folder Structure

* [`data`](./data): Sample data for demo purposes
* [`docs`](./docs): If main [README.md](./README.md) is not enough
* [`notebooks`](./notebooks): Jupyter notebooks / tutorials
* [`res`](./res): Relevant resources, e.g. [`images`](./res/images/) for the documentation
* [`scripts`](./scripts): Scripts for automating tasks
* [`src`](./src): All sourcecode files specific to this project
* [`tests`](./tests) Unit tests
* ...

## Installation 

1) Clone this repository:

```bash
git clone https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning.git
```




2) Install all dependencies:
    


```bash
pip install -r requirements.txt
```



The code has been tested with Python x.x on Linux/MacOS/Windows. 

## Usage

## How it works



1. Run get_pilot_area.ipynb to the polygon(s) of the area(s) to work with.
2. 
   1. Run create_basic_network.ipynb to create the basic pedestrian network.
   2. Run create_bike_network.ipynb to create a bike network based on BGT and OSM.
   3. Run create_road_network.ipynb to create road network which is used to obtain crossings.
3. Run get_sidewalk_widths_on_network.ipynb to add obstacle-free widths to the basic network.
4.
   1. Run get_osm_crossing_features.ipynb to obtain OpenStreetMap crossing features.
   2. Run get_project_sidewalk_crossing_features.ipynb to obtain Project Sidewalk crossing features.
   3. Run get_traffic_sign_features.ipynb to obtain zebra traffic sign crossing features.
   4. Run generate_osm_ps_ts_crossings.ipynb to generate crossings from features obtained is steps 3a, 3b and 3c.
5.
   1. Run ground_and_road_fusion.ipynb to obtain ground/road labeled point clouds.
   2. Run get_curb_heights.ipynb to obtain curb height features.
   3. Run generate_curb_ramp_crossings.ipynb to generate crossings from curb height features.
6. 
   1. Run get_public_transport_stop_features.ipynb to obtain public transport stop features.
   2. Run generate_public_transport_stop_connections.ipynb to obtain connections between walking network and stops.
7. Run generate_walking_and_bike_network_connections.ipynb to obtain connections between walking and bike network.
8. Run merge_network_and_crossings.ipynb to add generated crossings and public transport stops to walking and bike network network.

optional for now:

9. Run create_baseline_model.ipynb to get a benchmark for accessible route planning on your network.
   

## Contributing

Feel free to help out! [Open an issue](https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning/issues), submit a [PR](https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning/pulls) or [contact us](https://amsterdamintelligence.com/contact/).




## Acknowledgements

This repository was created by [Amsterdam Intelligence](https://amsterdamintelligence.com/) for the City of Amsterdam.



Optional: add citation or references here.


## License 

This project is licensed under the terms of the European Union Public License 1.2 (EUPL-1.2).
