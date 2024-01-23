import numpy as np

import shapely.geometry as sg
import geopandas as gpd
import networkx as nx

from scipy.spatial.distance import cdist
from tqdm import tqdm


# Function to find closest target nodes from source nodes and subsequently create edge between tese nodes.
# Edge is a connection between a source and a target node.
# max_dist: maximmum distance between source and target node is max_dist.
# max_connections: maximum number of new edges from source node.
# include_cc_rule: Restricts nodes to be connected to the same walking network component multiple times
def get_crossing_edges(gdf_source_nodes, gdf_target_nodes, max_dist=20, max_connections=3, crs='EPSG:28992', include_cc_rule=False):

    # Get distance matrices
    dist_matrix = cdist(gdf_source_nodes[['x', 'y']].values, gdf_target_nodes[['x', 'y']].values, metric='euclidean')
    np.fill_diagonal(dist_matrix, 10**6)
    dist_sort = np.sort(dist_matrix, axis=1)
    dist_argsort = np.argsort(dist_matrix, axis=1)

    # Calculate new edges
    idxs = np.where(dist_sort < max_dist, True, False)
    nodes_to_connect = [list(row[row_idxs]) for row, row_idxs in zip(dist_argsort, idxs)]

    if include_cc_rule:
        edges_geometries = []
        for source_node in tqdm(range(len(dist_sort))):
            restricted_cc, connections_count = [], 0

            for target_node in nodes_to_connect[source_node]:
                target_cc = gdf_target_nodes.iloc[target_node]['cc']
                if target_cc not in restricted_cc and connections_count < max_connections:
                    edge = sg.LineString([gdf_source_nodes.iloc[source_node]['geometry'], gdf_target_nodes.iloc[target_node]['geometry']])
                    edges_geometries.append(edge)
                    restricted_cc.append(target_cc)
                    connections_count += 1

    else:
        edges = [[i, nodes_to_connect[i][j]] for i in range(len(dist_sort)) for j in range(len(nodes_to_connect[i])) if j < max_connections]
        edges_geometries = [sg.LineString([gdf_source_nodes.iloc[edge[0]]['geometry'], gdf_target_nodes.iloc[edge[1]]['geometry']]) for edge in edges]
    
    gdf_edges = gpd.GeoDataFrame(geometry=edges_geometries, crs=crs)
    return gdf_edges



# Function to find closest target nodes from source nodes and subsequently create edge between tese nodes.
# Edge is a connection between a source and a target node.
# max_dist: maximmum distance between source and target node is max_dist.
# max_connections: maximum number of new edges from source node.
def get_crossing_edges_from_curb_heights(gdf_source_nodes, gdf_target_nodes, gdf_roads, min_dist=10, max_dist=20, max_connections=3, cc_column='cc_from_sidewalk_edges', crs='EPSG:28992'):

    # Get distance matrices
    print('Determining target nodes within distance {}m-{}m from source node...'.format(min_dist, max_dist))
    dist_matrix = cdist(gdf_source_nodes[['x', 'y']].values, gdf_target_nodes[['x', 'y']].values, metric='euclidean')
    np.fill_diagonal(dist_matrix, 10**6)
    dist_sort = np.sort(dist_matrix, axis=1)
    dist_argsort = np.argsort(dist_matrix, axis=1)
    idxs = np.where((dist_sort > min_dist) & (dist_sort < max_dist), True, False)
    nodes_to_connect = [list(row[row_idxs]) for row, row_idxs in zip(dist_argsort, idxs)]
    print('Possible target nodes determined.')

    # Calculate possible crossing edges
    print('Determining possible edges from source nodes to target nodes...')
    edges_dict = {}
    for source_node in tqdm(range(len(dist_sort))):
        source_cc = gdf_source_nodes.loc[source_node, cc_column]
        restricted_cc, connections_count = [source_cc], 0
        if source_cc not in edges_dict.keys():
            edges_dict[source_cc] = {}

        # Loop over possible target nodes for source node
        for target_node in nodes_to_connect[source_node]:
            target_cc = gdf_target_nodes.loc[target_node, cc_column]

            # Check if target node is not part of restricted connected component
            if target_cc not in restricted_cc and connections_count < max_connections:
                
                pos_edge = sg.LineString([gdf_source_nodes.iloc[source_node]['centroid'], gdf_target_nodes.iloc[target_node]['centroid']])
                pos_length = pos_edge.length

                # Add crossing edge if distance between source connected component and target node is the shortest known route
                if target_node in edges_dict[source_cc].keys():
                    if edges_dict[source_cc][target_node]['length'] > pos_length:
                        edges_dict[source_cc][target_node]['edge'] = pos_edge
                        edges_dict[source_cc][target_node]['length'] = pos_length
                        connections_count += 1
                        restricted_cc.append(target_cc)
                else:
                    edges_dict[source_cc][target_node] = {}
                    edges_dict[source_cc][target_node]['edge'] = pos_edge
                    edges_dict[source_cc][target_node]['length'] = pos_length

                    connections_count += 1
                    restricted_cc.append(target_cc)

    print('Determined possible edges from source nodes to target nodes.')

    print('Removing edges that do not cross the street or bikepath...')
    edges_geometries = [edges_dict[source_cc][target_node].get('edge') for source_cc in edges_dict.keys() for target_node in edges_dict[source_cc].keys()]
    edges_geometries_final = [edge for edge in edges_geometries if gdf_roads.intersects(edge).nunique() > 1]
    print('Removed edges that do not cross the street or bikepath.')

    gdf_edges = gpd.GeoDataFrame(geometry=edges_geometries_final, crs=crs)
    return gdf_edges


def connect_curb_crossing_edge(gdf_source_nodes, gdf_target_nodes, walking_graph, max_dist=20, max_connections=3, crs='EPSG:28992', network_to_network=False):

    # Get distance matrices
    dist_matrix = cdist(gdf_source_nodes[['x', 'y']].values, gdf_target_nodes[['x', 'y']].values, metric='euclidean')
    np.fill_diagonal(dist_matrix, 10**6)
    dist_sort = np.sort(dist_matrix, axis=1)
    dist_argsort = np.argsort(dist_matrix, axis=1)

    # Calculate new edges
    idxs = np.where(dist_sort < max_dist, True, False)
    nodes_to_connect = [list(row[row_idxs]) for row, row_idxs in zip(dist_argsort, idxs)]
    edges = [[i, nodes_to_connect[i][j]] for i in range(len(dist_sort)) for j in range(len(nodes_to_connect[i])) if j < max_connections]

    # Only connect the ends of a curb crossing if they are connected to different network nodes
    if len(edges) == 2:

        # check length between network target nodes
        try:
            point_1_network = gdf_target_nodes.iloc[edges[0][1]]['geometry']
            point_2_network = gdf_target_nodes.iloc[edges[1][1]]['geometry']
            node_1_network = (point_1_network.x, point_1_network.y)
            node_2_network = (point_2_network.x, point_2_network.y)
            sp_length = nx.shortest_path_length(walking_graph, node_1_network, node_2_network)
        except:
            sp_length = 1000

        # Only connect the ends of a curb crossing if the network nodes they are connected to are at least 20 meter from eachother
        if sp_length > 20:
            if network_to_network:
                edges_geometries = [sg.LineString([gdf_target_nodes.iloc[edges[0][1]]['geometry'], gdf_target_nodes.iloc[edges[1][1]]['geometry']])]
            else:
                edges_geometries = [sg.LineString([gdf_source_nodes.iloc[edge[0]]['geometry'], gdf_target_nodes.iloc[edge[1]]['geometry']]) for edge in edges]
                edges_geometries.append(sg.LineString([gdf_source_nodes.iloc[0]['geometry'], gdf_source_nodes.iloc[1]['geometry']]))
            gdf_edges = gpd.GeoDataFrame(geometry=edges_geometries, crs=crs)
            return gdf_edges
        else:
            return gpd.GeoDataFrame()


# # Function to find closest target nodes from source nodes and subsequently create edge between tese nodes.
# # Edge is a connection between a source and a target node.
# # max_dist: maximmum distance between source and target node is max_dist.
# # max_connections: maximum number of new edges from source node.
# # include_cc_rule: Restricts nodes to be connected to the same walking network component multiple times
def get_connections(gdf_source_nodes, gdf_target_nodes, max_dist=20, max_connections=3, cc_column=None, include_cc_rule=False):

    # Get distance matrices
    dist_matrix = cdist(gdf_source_nodes[['x', 'y']].values, gdf_target_nodes[['x', 'y']].values, metric='euclidean')
    np.fill_diagonal(dist_matrix, 10**6)
    dist_sort = np.sort(dist_matrix, axis=1)
    dist_argsort = np.argsort(dist_matrix, axis=1)

    # Calculate new edges
    idxs = np.where(dist_sort < max_dist, True, False)
    nodes_to_connect = [list(row[row_idxs]) for row, row_idxs in zip(dist_argsort, idxs)]

    if include_cc_rule:
        edges, edges_geometries = [], []
        for source_node in tqdm(range(len(dist_sort))):
            restricted_cc, connections_count = [], 0

            for target_node in nodes_to_connect[source_node]:
                target_cc = gdf_target_nodes.iloc[target_node][cc_column]
                if target_cc not in restricted_cc and connections_count < max_connections:
                    edges.append([source_node, target_node])
                    edge = sg.LineString([gdf_source_nodes.iloc[source_node]['geometry'], gdf_target_nodes.iloc[target_node]['geometry']])
                    edges_geometries.append(edge)
                    restricted_cc.append(target_cc)
                    connections_count += 1

    else:
        edges = [[i, nodes_to_connect[i][j]] for i in range(len(dist_sort)) for j in range(len(nodes_to_connect[i])) if j < max_connections]
        edges_geometries = [sg.LineString([gdf_source_nodes.iloc[edge[0]]['geometry'], gdf_target_nodes.iloc[edge[1]]['geometry']]) for edge in edges]
    
    return edges, edges_geometries