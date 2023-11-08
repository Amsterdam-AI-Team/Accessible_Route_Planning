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