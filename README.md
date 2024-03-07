# Accessible route planning

This repository contains a pipeline for **accessible route planning**. More specifically, it contains code to generate a accessible network and code to subsequently plan routes on this network given a set of user preferences. The following preferences that can be set by a user are included:
* **Minimum sidewalk width**
* **Maximum curb height**
* **Preference for walking or cycling**

Demonstration data has been included to run the pipeline. 


The methods can serve as inspiration, or can be applied as-is under some specific assumptions:
1. Usage in The Netherlands;
2. Point clouds in LAS format and tiled following [specific rules](datasets); and
3. Corresponding AHN data.

## Goal
This repository is designed to address the challenges faced by less mobile individuals, particularly wheelchair users, in urban environments. The primary objective of this project is to enable citizens with reduced mobility to participate independently and equitably in city life. 
The result is a personalized route planner, contributing to enhanced accessibility for less mobile individuals as they navigate urban spaces. The repository provides a factual and technical resource for developers and contributors interested in advancing the accessibility of urban environments for diverse user needs.

## Folder Structure

 * [`data`](./data) _Demo dataset to get started_
   * [`input`](./data/input) _input to get started_
     * [`ahn`](./datasets/input/ahn) _AHN data_
     * [`bgt`](./datasets/input/bgt) _BGT data_
     * [`pointcloud`](./datasets/input/pointcloud) _Example unlabelled urban point clouds_
   * [`output`](./data/output) _output to get started_
     * [`pointcloud`](./datasets/output/pointcloud) _Example labelled urban point clouds_
 * [`notebooks`](./notebooks) _Jupyter notebooks tutorials_
 * [`src`](./src/upcp) _Python source code_

---

## Installation 

This code has been tested with `Python == 3.8` on `Linux` and `MacOS`. 

**IMPORTANT** It is required to build two seperate environments. The first environment (steps 2a to 2c) is used to generate the network and the second environment (step 3) is used to plan routes on the network.

1) Clone this repository:

```bash
git clone https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning.git
```

2a) Create network generation environment and install dependencies:
    
```bash
pip install -r requirements_network_generation.txt
```

2b) Install the [Urban Point Cloud Processing](https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Processing) package from source:
    
```bash
python -m pip install git+https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Processing.git#egg=upcp
```

2c) **(Optional for demonstration purposes)**  install `cccorelib` and `pycc` from the [CloudCompare-PythonPlugin](https://github.com/tmontaigu/CloudCompare-PythonPlugin) project by following the summary instructions below; for more details and Windows instructions see [their GitHub page](https://github.com/tmontaigu/CloudCompare-PythonPlugin/blob/master/docs/building.rst#building-as-independent-wheels). Please note, these two packages are not available on the Python Package Index (PyPi).

Building these packages requires Qt.

```bash
git checkout https://github.com/tmontaigu/CloudCompare-PythonPlugin.git
cd CloudCompare-PythonPlugin
pip install --upgrade pip  # Requires version >= 21.1
```
```bash
# For Mac OS
export CMAKE_PREFIX_PATH=/usr/local/opt/qt@5
```
```bash
pip install wrapper/cccorelib
pip install wrapper/pycc
```

3) Create route planning environment and install dependencies:
    
```bash
pip install -r requirements_route_planning.txt
```


## Usage

We provide [notebooks](notebooks) that altogether make up the pipeline to generate the accessible network and plan routes. The notebooks should be run in a specific order, which can be found in the [notebooks README](./notebooks/README.md).   

## Contributing

Feel free to help out! [Open an issue](https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning/issues), submit a [PR](https://github.com/Amsterdam-AI-Team/Accessible_Route_Planning/pulls) or [contact us](https://amsterdamintelligence.com/contact/).




## Acknowledgements

This repository was created by [Amsterdam Intelligence](https://amsterdamintelligence.com/) for the City of Amsterdam.

## License 

This project is licensed under the terms of the European Union Public License 1.2 (EUPL-1.2).
