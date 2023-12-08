"""Settings that or not paths or secrets"""

# Select coordinate reference system
CRS = 'epsg:28992'

# Select area granularity (buurten/wijken/ggwgebieden/stadsdelen)
area_choice = 'wijken'

# Select area(s) for pilot
my_areas = ['Nieuwmarkt/Lastage', 'Osdorp-Midden']

# Minimum interior size to remain in BGT data
min_interior_size = 10

# Min area size of a sidewalk polygon in sqm for which width will be computed
min_area_size = 1

# Maximum length of linestring (in meters), otherwise cut
max_ls_length = 2

# Select which layers of BGT data to include
# (https://www.amsterdam.nl/stelselpedia/bgt-index/producten-bgt/prodspec-bgt-dgn-imgeo)
bgt_layers = ['BGT_WGL_voetpad', 'BGT_WGL_voetgangersgebied', 'BGT_WGL_inrit', 'BGT_WGL_woonerf']  # Pedestrian, note: 'BGT_WGL_voetpad_op_trap' not included
bgt_layers_bike = ['BGT_WGL_fietspad']  # Bikes

# Select location for BGT data
bbox = None  # Get all data, entire Amsterdam
#bbox = ((122000, 485550), (122300, 485250))

# Resolution (in m) for min and avg width computation
width_resolution = 1

# Precision (in decimals) for min and avg width computation
width_precision = 1

# Boundary for filtering out (in meters)
min_path_width = 0.4

# Boundaries between the final colors (in meters)
width_1 = 0.9
width_2 = 1.5
width_3 = 2.0
width_4 = 2.2
width_5 = 2.9
width_6 = 3.6

# Maximum distance between intended start point and start node (in meters)
max_dist = 3

# Minimum length for short-ends (in meters), otherwise removed (in full width calculation)
min_se_length_fw = 10