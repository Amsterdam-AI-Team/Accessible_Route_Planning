import numpy as np
import shapely.geometry as sg
import geopandas as gpd
import networkx as nx
from scipy.spatial.distance import cdist
from tqdm.notebook import tqdm
tqdm.pandas()


def get_distance_matrices(source_nodes, target_nodes):
    """
    Compute distance matrices between source and target nodes.

    Parameters:
    - source_nodes (GeoDataFrame): GeoDataFrame of source nodes.
    - target_nodes (GeoDataFrame): GeoDataFrame of target nodes.

    Returns:
    Tuple of NumPy arrays (dist_sort, dist_argsort) representing
    sorted distances and corresponding indices.
    """
    source_x_y = source_nodes[['x', 'y']].values
    target_x_y = target_nodes[['x', 'y']].values
    dist_matrix = cdist(source_x_y, target_x_y, metric='euclidean')
    np.fill_diagonal(dist_matrix, 10**6)
    dist_sort = np.sort(dist_matrix, axis=1)
    dist_argsort = np.argsort(dist_matrix, axis=1)
    return dist_sort, dist_argsort


def get_nodes_to_connect(dist_sort, dist_argsort, min_dist=0, max_dist=10):
    """
    Get nodes to connect based on distance matrices.

    Parameters:
    - dist_sort (numpy.ndarray): Sorted distance matrix.
    - dist_argsort (numpy.ndarray): Indices of sorted distances.
    - min_dist (float): Minimum distance threshold.
    - max_dist (float): Maximum distance threshold.

    Returns:
    List of lists containing indices of nodes to connect for each source node.
    """
    idxs = np.where((dist_sort > min_dist) & (dist_sort < max_dist), True, False)
    nodes_to_connect = [list(row[row_idxs]) for row, row_idxs in zip(dist_argsort, idxs)]
    return nodes_to_connect


def create_edges_geometries(gdf_source_nodes, gdf_target_nodes, nodes_to_connect,
                            dist_sort, max_connections):
    """
    Create edges and corresponding geometries.

    Parameters:
    - gdf_source_nodes (GeoDataFrame): GeoDataFrame of source nodes.
    - gdf_target_nodes (GeoDataFrame): GeoDataFrame of target nodes.
    - nodes_to_connect (list): List of lists containing indices of nodes to
      connect for each source node.
    - dist_sort (numpy.ndarray): Sorted distance matrix.
    - max_connections (int): Maximum number of connections per source node.

    Returns:
    Tuple of lists (edges, edges_geometries) representing edge indices and
    corresponding geometries.
    """
    edges, edges_geometries = [], []
    for i in range(len(dist_sort)):
        for j in range(len(nodes_to_connect[i])):
            if j < max_connections:
                edges.append([i, nodes_to_connect[i][j]])
    for edge in edges:
        source_node = gdf_source_nodes.iloc[edge[0]]['geometry']
        target_node = gdf_target_nodes.iloc[edge[1]]['geometry']
        edges_geometries.append(sg.LineString([source_node, target_node]))
    return edges, edges_geometries


def get_connections(gdf_source_nodes, gdf_target_nodes, max_dist=20, max_connections=3,
                    crs='EPSG:28992', include_cc_rule=False, cc_column=None, return_gdf=True):
    """
    Get connections between source and target nodes.

    Parameters:
    - gdf_source_nodes (GeoDataFrame): GeoDataFrame of source nodes.
    - gdf_target_nodes (GeoDataFrame): GeoDataFrame of target nodes.
    - max_dist (float): Maximum distance for connections.
    - max_connections (int): Maximum number of connections per source node.
    - crs (str): Coordinate Reference System.
    - include_cc_rule (bool): Whether to include connected components rule.
    - cc_column (str): Column representing connected components.
    - return_gdf (bool): Whether to return a GeoDataFrame.

    Returns:
    GeoDataFrame or Tuple of lists representing connections between nodes.
    """
    dist_sort, dist_argsort = get_distance_matrices(gdf_source_nodes, gdf_target_nodes)
    nodes_to_connect = get_nodes_to_connect(dist_sort, dist_argsort, max_dist=max_dist)

    if include_cc_rule:
        edges, edges_geometries = [], []
        for source_node in tqdm(range(len(dist_sort))):
            restricted_cc, connections_count = [], 0

            # Only connect multiple target nodes to source node if
            # target nodes have different connected component.
            for target_node in nodes_to_connect[source_node]:
                target_cc = gdf_target_nodes.iloc[target_node][cc_column]
                if target_cc not in restricted_cc and connections_count < max_connections:
                    edges.append([source_node, target_node])
                    source_node_geom = gdf_source_nodes.iloc[source_node]['geometry']
                    target_node_geom = gdf_target_nodes.iloc[target_node]['geometry']
                    edge = sg.LineString([source_node_geom, target_node_geom])
                    edges_geometries.append(edge)
                    restricted_cc.append(target_cc)
                    connections_count += 1
    else:
        edges, edges_geometries = create_edges_geometries(gdf_source_nodes, gdf_target_nodes,
                                                          nodes_to_connect, dist_sort,
                                                          max_connections=max_connections)

    if return_gdf:
        gdf_edges = gpd.GeoDataFrame(geometry=edges_geometries, crs=crs)
        return gdf_edges
    else:
        return edges, edges_geometries


def get_crossing_edges_from_curb_heights(gdf_source_nodes, gdf_target_nodes,
                                         min_dist=0, max_dist=20, max_connections=3,
                                         crs='EPSG:28992', cc_column='cc_from_sidewalk_edges'):
    """
    Get crossing edges based on curb heights.

    Parameters:
    - gdf_source_nodes (GeoDataFrame): GeoDataFrame of source nodes.
    - gdf_target_nodes (GeoDataFrame): GeoDataFrame of target nodes.
    - min_dist (float): Minimum distance for connections.
    - max_dist (float): Maximum distance for connections.
    - max_connections (int): Maximum number of connections per source node.
    - crs (str): Coordinate Reference System.
    - cc_column (str): Column representing connected components.

    Returns:
    GeoDataFrame representing crossing edges.
    """
    dist_sort, dist_argsort = get_distance_matrices(gdf_source_nodes, gdf_target_nodes)
    nodes_to_connect = get_nodes_to_connect(dist_sort, dist_argsort,
                                            min_dist=min_dist, max_dist=max_dist)

    edges_geometries, edges_dict = [], {}
    for source_node in tqdm(range(len(dist_sort))):
        source_cc = gdf_source_nodes.loc[source_node, cc_column]
        restricted_cc, connections_count = [source_cc], 0

        if source_cc not in edges_dict.keys():
            edges_dict[source_cc] = {}

        for target_node in nodes_to_connect[source_node]:
            target_cc = gdf_target_nodes.loc[target_node, cc_column]

            # Only connect multiple target nodes to source node if
            # target nodes have different connected component.
            if target_cc not in restricted_cc and connections_count < max_connections:
                source_node_geom = gdf_source_nodes.iloc[source_node]['centroid']
                target_node_geom = gdf_target_nodes.iloc[target_node]['centroid']
                pos_edge = sg.LineString([source_node_geom, target_node_geom])
                pos_length = pos_edge.length

                # Only keep shortest possible edge between source node and target cc.
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

    # Create edge geometries.
    for source_cc in edges_dict.keys():
        for target_node in edges_dict[source_cc].keys():
            edges_geometries.append(edges_dict[source_cc][target_node].get('edge'))

    gdf_edges = gpd.GeoDataFrame(geometry=edges_geometries, crs=crs)
    return gdf_edges


def connect_curb_crossing_edge(gdf_source_nodes, gdf_target_nodes, walking_graph, max_dist=20,
                               max_connections=3, crs='EPSG:28992', network_to_network=False):
    """
    Connect curb crossing edges.

    Parameters:
    - gdf_source_nodes (GeoDataFrame): GeoDataFrame of source nodes.
    - gdf_target_nodes (GeoDataFrame): GeoDataFrame of target nodes.
    - walking_graph (networkx.Graph): Walking graph.
    - max_dist (float): Maximum distance for connections.
    - max_connections (int): Maximum number of connections per source node.
    - crs (str): Coordinate Reference System.
    - network_to_network (bool): Whether to connect network to network.

    Returns:
    GeoDataFrame representing connected edges.
    """
    dist_sort, dist_argsort = get_distance_matrices(gdf_source_nodes, gdf_target_nodes)
    nodes_to_connect = get_nodes_to_connect(dist_sort, dist_argsort, max_dist=max_dist)
    edges, _ = create_edges_geometries(gdf_source_nodes, gdf_target_nodes, nodes_to_connect,
                                       dist_sort, max_connections=max_connections)

    if len(edges) == 2:
        try:
            target_node_1 = gdf_target_nodes.iloc[edges[0][1]]['geometry']
            target_node_2 = gdf_target_nodes.iloc[edges[1][1]]['geometry']
            node_1_network = (target_node_1.x, target_node_1.y)
            node_2_network = (target_node_2.x, target_node_2.y)
            sp_length = nx.shortest_path_length(walking_graph, node_1_network, node_2_network)
        except Exception:
            sp_length = 1000

        # Only connect crossing edge if target nodes are in different connected components
        # or the target nodes are at least 20 meters apart from eachother.
        if sp_length > 20:
            edges_geometries = []
            if network_to_network:
                target_node_1 = gdf_target_nodes.iloc[edges[0][1]]['geometry']
                target_node_2 = gdf_target_nodes.iloc[edges[1][1]]['geometry']
                edges_geometries.append(sg.LineString([target_node_1, target_node_2]))
            else:
                for edge in edges:
                    source_node = gdf_source_nodes.iloc[edge[0]]['geometry']
                    target_node = gdf_target_nodes.iloc[edge[1]]['geometry']
                    edges_geometries.append(sg.LineString([source_node, target_node]))
                source_node_1 = gdf_source_nodes.iloc[0]['geometry']
                source_node_2 = gdf_source_nodes.iloc[1]['geometry']
                edges_geometries.append(sg.LineString([source_node_1, source_node_2]))
            gdf_edges = gpd.GeoDataFrame(geometry=edges_geometries, crs=crs)
            return gdf_edges
        else:
            return gpd.GeoDataFrame()
    else:
        return gpd.GeoDataFrame()


def count_line_gdf_intersections(line, gdf, geom_column='geometry'):
    """
    Count intersections between a line and a GeoDataFrame of lines.

    Parameters:
    - line (shapely.geometry.LineString): Line to count intersections.
    - gdf (GeoDataFrame): GeoDataFrame of lines.
    - geom_column (str): Column name containing geometries.

    Returns:
    Count of intersections.
    """
    count = 0

    for other_line in gdf[geom_column]:
        intersections = line.intersection(other_line)

        if intersections.is_empty:
            continue

        if intersections.geom_type == 'Point':
            count += 1
        elif intersections.geom_type == 'MultiPoint':
            count += len(intersections)

    return count
