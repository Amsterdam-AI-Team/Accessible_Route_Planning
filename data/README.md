# Data

We supply a couple of point clouds for demonstration purpose and their corresponding ahn and bgt information. The point clouds are used to determine curb heights. Because we only need ground and road points from our point clouds to do this, the other points have been filtered out.

* `input/`
  * `pointcloud/filtered_**_**.laz`  
  Unlabelled 50x50m point clouds consisting of ground and road points, courtesy of [CycloMedia](https://www.cyclomedia.com/). See notes below for details.
  * `ahn/ahn_**_**.laz`  
  The corresponding AHN point clouds, which can also be generated using the [preprocessing tools](../notebooks/1.%20AHN%20preprocessing.ipynb).
  * `bgt/**_**.csv`  
  BGT information regarding streets for the point clouds.
  * `sidewalk_segments.gpkg`  
  Information on widths of sidewalk_segments, which can also be generated using [this repository](https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Sidewalk_Width).
* `output/`
  * `pointcloud/**_**.csv`  
    Pre-labelled 50x50m point clouds consisting of ground and road points, courtesy of [CycloMedia](https://www.cyclomedia.com/). See notes below for details.
  * `pilot_area.geojson`
    Predefined pilot area for demonstration purposes 

These files are sufficient to run the [notebooks](../notebooks). Some additional required data files can be downloaded with provided scripts.


## Some notes on the Datasets

This repository was designed to be used with specific data sources:

* LAS point clouds of urban scenes supplied by [CycloMedia](https://www.cyclomedia.com/).
* AHN3 or AHN4 point clouds downloaded from [ArcGIS](https://www.arcgis.com/apps/Embed/index.html?appid=a3dfa5a818174aa787392e461c80f781) or [GeoTiles](https://geotiles.nl).
* BGT data down from [PDOK](https://www.pdok.nl/) or the [Amsterdam API](https://map.data.amsterdam.nl/maps/bgtobjecten?).
* BAG data down from [3D BAG](https://data.3dbag.nl/)

The latter three sources are specific to The Netherlands.

We follow the naming conventions used by CycloMedia, which are based on _tile codes_. Each tile covers an area of exactly 50x50m, and is marked by the coordinates of the lower left corner following the Dutch _Rijksdriehoeksstelsel + NAP (EPSG:7415)_.

The tile code is generated as follows:

`tilecode = [X-coordinaat/50]_[Y-coordinaat/50]`

For example, 2386_9702 would translate to (119300, 485100) meters in RD coordinates or roughly (52.35264, 4.86321) degrees.
