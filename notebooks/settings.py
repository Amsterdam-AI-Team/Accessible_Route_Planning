"""Settings that or not paths or secrets"""

# Select to run local or on Azure
my_run = 'local'

# Select coordinate reference system
CRS = 'EPSG:28992'
CRS_map = 'EPSG:4326'

# Select area granularity (buurten/wijken/ggwgebieden/stadsdelen)
area_choice = 'wijken'

# Select area(s) for pilot
# my_areas = ['Nieuwmarkt/Lastage', 'Osdorp-Midden']
my_areas = []

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
bgt_road_layers = ['BGT_WGL_rijbaan_lokale_weg', 'BGT_WGL_rijbaan_regionale_weg',
                    'BGT_WGL_rijbaan_autoweg', 'BGT_WGL_rijbaan_autosnelweg',
                    'BGT_WGL_ov-baan', 'BGT_WGL_fietspad'] # Roads

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
width_1 = 0.6
width_2 = 0.8
width_3 = 1.0
width_4 = 1.2
width_5 = 1.4
width_6 = 1.6

# Maximum distance between intended start point and start node (in meters)
max_dist = 3

# Minimum length for short-ends (in meters), otherwise removed (in full width calculation)
min_se_length_fw = 10

# Weight for crossing edges in the network
crossing_weight_factor = 1.4

# Weight for walk and bike edges in network
walk_bike_preference_weight_factor = 0.6

# Coordinates for pilot area in main GitHub
coordinates =   [(114698.30483798476, 484920.6323956598), (114698.29606542762, 484920.6304669031), (114698.28715519028, 484920.6293330904),
                (114698.27817915859, 484920.62900336896), (114602.40417915859, 484921.41600336897), (114602.39453137369, 484921.4165494703),
                (114602.38498134272, 484921.41802422056), (114602.37561824192, 484921.4204138488), (114602.36652950205, 484921.42369604134),
                (114602.3577999919, 484921.42784014955), (114602.3495112259, 484921.4328074766), (114602.34174060287, 484921.4385516387),
                (114602.3345606833, 484921.4450189979), (114602.32803851186, 484921.45214916335), (114602.32223499124, 484921.459875555),
                (114602.31720431356, 484921.46812602546), (114602.31299345425, 484921.47682353336), (114602.30964173349, 484921.4858868632),
                (114602.21364173348, 484921.7898868632), (114602.21229535202, 484921.7945400106), (114602.09739765202, 484922.23095581064),
                (114602.0964713246, 484922.2347780403), (114593.30036902461, 484961.9233622403), (114593.29869830214, 484961.9332028478),
                (114593.29801691124, 484961.9431609889), (114593.29833164054, 484961.9531374519), (114593.29963935443, 484961.9630328424),
                (114593.30192702431, 484961.9727485737), (114593.30517185837, 484961.9821878491), (114593.3093415287, 484961.9912566262),
                (114593.31439449335, 484961.99986455374), (114593.3202804102, 484962.007925872), (114593.32694063852, 484962.01536026684),
                (114662.46994063852, 485031.84536026686), (114662.47940477947, 485031.85377835244), (114674.53240477947, 485041.27777835244),
                (114674.5414038738, 485041.2840508525), (114674.55103584655, 485041.2892999531), (114674.56118479819, 485041.29346249276),
                (114774.2621847982, 485075.9284624927), (114780.60827155599, 485078.12649258674), (114780.61063862359, 485078.12727951945),
                (114782.33663862359, 485078.67727951944), (114782.33730404134, 485078.6774890048), (114783.78430404134, 485079.1274890048),
                (114783.79410573425, 485079.1300011132), (114783.80411111237, 485079.1315098483), (114783.81421773674, 485079.13199976296),
                (114783.82432213186, 485079.1314658414), (114783.83432084497, 485079.1299135499), (114783.8441115054, 485079.1273587817),
                (114783.85359387258, 485079.1238276933), (114783.86267086238, 485079.1193564374), (114783.87124954101, 485079.1139907925),
                (114783.8792420767, 485079.10778569407), (114783.88656663873, 485079.1008046724), (114783.8931482354, 485079.09311920183),
                (114783.8989194818, 485079.0848079692), (114789.3439194818, 485070.3288079692), (114789.34972290548, 485070.3180636948),
                (114789.35417347684, 485070.30669217015), (114798.31317347682, 485042.52569217014), (114798.31330490865, 485042.52528158494),
                (114813.88130490865, 484993.52828158496), (114813.8813491098, 484993.5281421177), (114815.4243491098, 484988.6471421177),
                (114824.42235046776, 484960.1791378217), (114824.42483846114, 484960.1696793501), (114824.4263906023, 484960.1600230747),
                (114824.42699204454, 484960.15026136057), (114824.4266370349, 484960.14048758114), (114824.42532896918, 484960.1307952253),
                (114824.42308035938, 484960.1212770033), (114824.41991271406, 484960.1120239595), (114824.41585633266, 484960.10312460194),
                (114824.41095001559, 484960.0946640553), (114824.40524069314, 484960.0867232472), (114824.39878297658, 484960.07937813364),
                (114824.39163863579, 484960.0726989727), (114824.38387600836, 484960.06674965244), (114824.37556934601, 484960.0615870797),
                (114824.36679810428, 484960.057260636), (114824.35764618256, 484960.05381170503), (114817.21064618255, 484957.75281170505),
                (114817.210519508, 484957.75277101476), (114723.861519508, 484927.83577101474), (114716.83546133994, 484925.58875239233),
                (114716.83083798476, 484925.5873956598), (114698.30483798476, 484920.6323956598)]
