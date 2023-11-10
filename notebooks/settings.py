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
bgt_layers = ['BGT_WGL_voetpad', 'BGT_WGL_voetgangersgebied', 'BGT_WGL_inrit', 'BGT_WGL_woonerf']  # note: 'BGT_WGL_voetpad_op_trap' not included

# Select location for BGT data
bbox = None  # Get all data, entire Amsterdam
#bbox = ((122000, 485550), (122300, 485250))