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



0. Run get_pilot_area.ipynb to the polygon(s) of the area(s) to work with
1. Run create_basic_network.ipynb to create the basic pedestrian network
2. Run get_sidewalk_widths_on_network.ipynb to add obstacle-free widths to the basic network
   
optional for now:
3a. Run xxxxx to get curb heights, curb ramps, crossings and crosswalks from OSM, Project Sidewalk, point clouds and traffic signs
3b. Run xxxxx to add all crossings to network

4. Run create_baseline_model.ipynb to get a bench mark for accessible route planning on your network
   

## Contributing

Feel free to help out! [Open an issue](https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning/issues), submit a [PR](https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning/pulls) or [contact us](https://amsterdamintelligence.com/contact/).




## Acknowledgements

This repository was created by [Amsterdam Intelligence](https://amsterdamintelligence.com/) for the City of Amsterdam.



Optional: add citation or references here.


## License 

This project is licensed under the terms of the European Union Public License 1.2 (EUPL-1.2).
