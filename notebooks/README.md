# Notebooks

These jupyter notebooks make up the pipeline to create an accessible network and plan routes on that network given a set of user preferences. The notebooks should be run in the order than is listed below.

**IMPORTANT** 
- **It is not neccessary to run notebook 5 for demonstration purposes. Labelled point clouds have been provided in the output folder.** 
- **Notebooks 1 untill 9 should be run using the network generation environment (steps 2a untill 2c in the installation process).** 
- **Notebook 10 should be run using the route planning environment (step 3 in the installation process).**

---

[1. Pilot area extraction](1.%20Get%20pilot%20area.ipynb) -- obtain geojson of area for accessible network.

[2. Create basic networks]()
* [2a. Create basic walking network](2a.%20Create%20basic%20network.ipynb) -- create a basic walking network to navigate on.
* [2b. Create bike network](2b.%20Create%20bike%20network.ipynb) -- create the bike network to navigate on.
* [2c. Create road network](2c.%20Create%20road%20network.ipynb) -- create road network (car and bicycle roads) which is used to determine if generated crossings are valid

[3. Project sidewalk widths onto network](3.%20Get%20sidewalk%20widths%20on%20network.ipynb) -- project and add sidewalk widths to the walking network generated in step 2a.

[4. Generate crossings from OpenStreetMap, Project Sidewalk and traffic sign features]()
* [4a. Get OpenStreetMap crossing features](4a.%20Get%20osm%20crossing%20features.ipynb) -- obtain crossing features from OSM which are used to generate crossings.
* [4b. Get Project Sidewalk crossing features](4b.%20Get%20project%20sidewalk%20crossing%20features.ipynb) -- obtain crossing features from Project Sidewalk which are used to generate crossings.
* [4c. Get traffic sign features](4c.%20Get%20traffic%20sign%20features.ipynb) -- obtain crossing features from traffic signs which are used to generate crossings.
* [4d. Generate crossings from OSM, Project Sidewalk and traffic sign features](4d.%20Generate%20crossings%20from%20osm,%20ps%20and%20ts%20features.ipynb) -- generate crossings from features retrieved in steps 4a, 4b and 4c.

[5. Ground and road fusion](5.%20Ground%20and%20road_fusion.ipynb) -- obtain point clouds which have a labelled ground and road which are used to calculate curb height.

[6. Generate crossings from curb height information]()
* [6a. Get curb heights](6a.%20Get%20curb%20heights.ipynb) -- obtain curb heights from point clouds to generate crossings.
* [6a. Generate crossings from curb height information](6b.%20Generate%20crossings%20from%20curb%20height%20information.ipynb) -- generate crossings from curb height information.

[]()

[7. Add public transport stops to the network]()
* [7a. Get public transport stop features](7a.%20Get%20public%20transport%20stop%20features.ipynb) -- obtain public transport stop features.
* [7b. Generate public transport stop connections](7b.%20Generate%20public%20transport%20stop%20connections.ipynb) -- obtain edges that connect the walking network and public transport stops.

[8. Generate walking and bike connections](8.%20Generate%20walk%20and%20bike%20network%20connections.ipynb) -- obtain edges that connect the walking and bike network.

[9. Merge networks and crossings](9.%20Merge%20networks%20and%20crossings.ipynb) -- merge the walking network, bike network, crossings and public transport stops.

[10. Plan routes](10.%20Plan%20routes.ipynb) -- plan routes on the accessible network given a set of user preferences.
